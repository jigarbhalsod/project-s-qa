"""Final-scorer inference for the Q&A branch (v2): average of DistilRoBERTa, SBERT-LR and NLI-LR."""
import os, re, json
import numpy as np
import joblib
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

ROOT = os.environ.get("PROJECT_S_ROOT", "/content/drive/MyDrive/project_s_qa")
INTERIM, V2 = ROOT + "/interim", ROOT + "/reports_v2"
FT_DIR = INTERIM + "/ft_distilroberta_v1"
NLI_NAME = "cross-encoder/nli-deberta-v3-base"
ST_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LABEL5_ORDER = ["correct", "contradictory", "partially_correct_incomplete", "irrelevant", "non_domain"]
NAMES = ["incorrect", "partial", "correct"]
MODEL_VERSION = "v2-avg3-ft+sbert+nli"
PROVISIONAL_POLICY = {"status": "provisional", "confidence_threshold": 0.60,
                      "contradiction_nli_threshold": 0.5}
_S = {}


def _load():
    if _S:
        return _S
    from sentence_transformers import SentenceTransformer
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    nli = AutoModelForSequenceClassification.from_pretrained(NLI_NAME).to(dev).eval()
    id2 = {int(i): str(l).lower() for i, l in nli.config.id2label.items()}
    _S.update(
        dev=dev,
        ft_tok=AutoTokenizer.from_pretrained(FT_DIR),
        ft=AutoModelForSequenceClassification.from_pretrained(FT_DIR).to(dev).eval(),
        nli_tok=AutoTokenizer.from_pretrained(NLI_NAME), nli=nli,
        nli_idx=[[i for i, l in id2.items() if k in l][0] for k in ("entail", "contra", "neutral")],
        st=SentenceTransformer(ST_NAME, device=dev),
        base=joblib.load(INTERIM + "/combiner_v1.joblib")["base_models"])
    return _S


def _wc(texts):
    return np.array([max(len(t.split()), 1) for t in texts])


def _concepts(ref):
    parts = [p.strip() for p in re.split(r"(?<=[.;!?])\s+|;\s*", ref) if len(p.strip()) > 3]
    return parts or [ref]


def _proba5(clf, X):
    P = clf.predict_proba(X)
    out = np.zeros((X.shape[0], 5))
    for j, c in enumerate(clf.classes_):
        out[:, LABEL5_ORDER.index(c)] = P[:, j]
    return out


def _to3(P):
    return np.c_[P[:, [1, 3, 4]].sum(1), P[:, 2], P[:, 0]]


@torch.no_grad()
def _ft(items, bs=64):
    S = _load()
    a = [it["question"] + " | " + it["reference_answer"] for it in items]
    b = [it["student_answer"] for it in items]
    out = []
    for i in range(0, len(items), bs):
        enc = S["ft_tok"](a[i:i + bs], b[i:i + bs], truncation=True, max_length=160,
                          padding=True, return_tensors="pt").to(S["dev"])
        if S["dev"] == "cuda":
            with torch.autocast("cuda", dtype=torch.float16):
                lg = S["ft"](**enc).logits
        else:
            lg = S["ft"](**enc).logits
        out.append(torch.softmax(lg.float(), -1).cpu().numpy())
    return np.vstack(out)


@torch.no_grad()
def _nli(pairs, bs=64):
    S = _load()
    out = np.zeros((len(pairs), 3), dtype=np.float32)
    order = np.argsort([len(p) + len(h) for p, h in pairs])
    for i in range(0, len(pairs), bs):
        ix = order[i:i + bs]
        enc = S["nli_tok"]([pairs[j][0] for j in ix], [pairs[j][1] for j in ix], truncation=True,
                           max_length=192, padding=True, return_tensors="pt").to(S["dev"])
        pr = torch.softmax(S["nli"](**enc).logits.float(), -1).cpu().numpy()
        out[ix] = pr[:, S["nli_idx"]]
    return out


def _sb_X(items):
    S = _load()
    R = S["st"].encode([it["reference_answer"] for it in items], batch_size=128,
                       normalize_embeddings=True, show_progress_bar=False)
    A = S["st"].encode([it["student_answer"] for it in items], batch_size=128,
                       normalize_embeddings=True, show_progress_bar=False)
    cos = (R * A).sum(1, keepdims=True)
    lenr = np.log(_wc([it["student_answer"] for it in items]) /
                  _wc([it["reference_answer"] for it in items])).reshape(-1, 1)
    return np.hstack([R, A, np.abs(R - A), R * A, cos, lenr])


def _pooled():
    if "pooled" not in _S:
        _S["pooled"] = joblib.load(INTERIM + "/pooled_lr_v2.joblib")
    return _S["pooled"]


def component_probs(items, dataset="pooled"):
    """5-way probabilities of each component (label order = LABEL5_ORDER) plus NLI evidence."""
    S = _load()
    dss = ["beetle", "scientsbank"] if dataset == "both" else [dataset]
    ft, X_sb = _ft(items), _sb_X(items)
    fwd, spans = [], []
    for it in items:
        cs = _concepts(it["reference_answer"])
        spans.append((len(fwd), len(fwd) + len(cs)))
        fwd += [(it["student_answer"], c) for c in cs]
    Pf = _nli(fwd)
    Pr = _nli([(it["reference_answer"], it["student_answer"]) for it in items])
    feats, concepts = np.zeros((len(items), 7)), []
    for k, (a, b) in enumerate(spans):
        P = Pf[a:b]
        feats[k] = [P[:, 0].mean(), P[:, 0].min(), P[:, 1].max(), P[:, 2].mean(), *Pr[k]]
        cs = _concepts(items[k]["reference_answer"])
        concepts.append([{"concept": c, "entail": round(float(p[0]), 4),
                          "contradict": round(float(p[1]), 4), "neutral": round(float(p[2]), 4)}
                         for c, p in zip(cs, P)])
    if dataset == "pooled":
        PL = _pooled()
        sb, nl = _proba5(PL["sbert_lr"], X_sb), _proba5(PL["nli_lr"], feats)
    else:
        sb = np.mean([_proba5(S["base"][d]["sbert_lr"], X_sb) for d in dss], 0)
        nl = np.mean([_proba5(S["base"][d]["nli_lr"], feats) for d in dss], 0)
    return dict(ft=ft, sb=sb, nl=nl, feats=feats, concepts=concepts)


def _load_policy():
    p = V2 + "/A_abstain_policy_v2.json"
    return json.load(open(p)) if os.path.exists(p) else dict(PROVISIONAL_POLICY)


def predict_batch(items, dataset="pooled", policy=None):
    for it in items:
        for k in ("question", "reference_answer", "student_answer"):
            if not isinstance(it.get(k), str) or not it[k].strip():
                raise ValueError("empty or missing field: " + k)
    if dataset not in ("scientsbank", "beetle", "both", "pooled"):
        raise ValueError("dataset must be scientsbank, beetle, both or pooled")
    pol = policy or _load_policy()
    c = component_probs(items, dataset)
    p3 = _to3((c["ft"] + c["sb"] + c["nl"]) / 3)
    T = float(pol.get("temperature", 1.0))
    if T != 1.0:
        q = np.clip(p3, 1e-9, 1.0) ** (1.0 / T)
        p3 = q / q.sum(1, keepdims=True)
    out = []
    for i in range(len(items)):
        k, conf, fcon = int(p3[i].argmax()), float(p3[i].max()), float(c["feats"][i][2])
        reasons = []
        if conf < pol["confidence_threshold"]:
            reasons.append("low_confidence")
        if pol.get("use_contradiction_flag", True) and k == 2 and fcon > pol["contradiction_nli_threshold"]:
            reasons.append("possible_contradiction")
        out.append({"pred_label": NAMES[k], "pred_score": k, "confidence": round(conf, 4),
                    "p_incorrect": round(float(p3[i][0]), 4), "p_partial": round(float(p3[i][1]), 4),
                    "p_correct": round(float(p3[i][2]), 4),
                    "needs_teacher_review": bool(reasons), "review_reasons": reasons,
                    "nli": {"entail": round(float(c["feats"][i][0]), 4), "contradict": round(fcon, 4)},
                    "concepts": c["concepts"][i], "model_version": MODEL_VERSION,
                    "dataset_used": dataset, "policy_status": pol.get("status", "final")})
    return out


def predict(question, reference_answer, student_answer, dataset="pooled"):
    return predict_batch([{"question": question, "reference_answer": reference_answer,
                           "student_answer": student_answer}], dataset)[0]
