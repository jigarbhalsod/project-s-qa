"""Dev-only reproducible Path A/B comparison; reads saved outputs only."""
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score, confusion_matrix, f1_score, precision_recall_fscore_support

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
API = ROOT / "project_s_qa/reports_v2/A_predict.py"
GOLD = ROOT / "project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet"
COMP = ROOT / "Project_S_QA_Evidence/Phase_8_Accuracy_Max/A_component_probs_v7.parquet"
TEXT = ROOT / "Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet"
OUTS = ["EXP1_AGGREGATION_COMPARISON_REPORT_v2.md", "EXP1_METRICS_COMPARISON_v2.csv", "EXP1_CONFUSION_MATRICES_v2.csv", "EXP1_DISAGREEMENT_ANALYSIS_v2.csv", "EXP1_ARTIFACT_MANIFEST_v2.md"]
if any("test" in str(p).casefold() for p in (API, GOLD, COMP, TEXT, OUT)) or any((OUT / n).exists() for n in OUTS):
    raise RuntimeError("Unsafe test path or existing output; refusing to proceed")
api_text = API.read_text(encoding="utf-8")
api_hash = hashlib.sha256(API.read_bytes()).hexdigest()
assert api_hash == "ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053"
assert 'LABEL5_ORDER = ["correct", "contradictory", "partially_correct_incomplete", "irrelevant", "non_domain"]' in api_text
assert "return np.c_[P[:, [1, 3, 4]].sum(1), P[:, 2], P[:, 0]]" in api_text
a, c, d = (pd.read_parquet(p) for p in (GOLD, COMP, TEXT))
req_a = {"uid", "dataset", "split", "question_id", "label5", "score_ours", *[f"d_p{i}" for i in range(5)]}
req_c = {"uid", "dataset", "split", "question_id", "label5", *[f"{p}_p{i}" for p in ("ft", "sb", "nl") for i in range(5)], "p_incorrect", "p_partial", "p_correct"}
req_d = {"uid", "dataset", "split", "question_id", "label5", "question", "reference_answer", "student_answer"}
assert req_a <= set(a) and req_c <= set(c) and req_d <= set(d), "Required schema missing"
assert all(len(x) == 2049 and x.uid.notna().all() and x.uid.is_unique for x in (a, c, d)), "Expected 2,049 unique UIDs per file"
assert set(a.uid) == set(c.uid) == set(d.uid), "UID sets differ"
assert set(a.split.astype(str)) == {"dev_ua", "dev_uq"} and not a.split.astype(str).str.contains("test", case=False, regex=False).any(), "Non-dev/test split found"
am, cm = a.set_index("uid"), c.set_index("uid")
for col in ("dataset", "split", "question_id", "label5"):
    assert am.loc[d.uid, col].astype(str).reset_index(drop=True).equals(d[col].astype(str)), f"UID metadata mismatch: {col}"
order = ["correct", "contradictory", "partially_correct_incomplete", "irrelevant", "non_domain"]
gold_map = {s: (2 if i == 0 else 1 if i == 2 else 0) for i, s in enumerate(order)}
y = am.loc[c.uid, "label5"].astype(str).str.casefold().map(gold_map).to_numpy()
assert np.isfinite(y).all() and np.array_equal(y, am.loc[c.uid, "score_ours"].astype(int).to_numpy()), "Gold-label mapping mismatch"
dp = am.loc[c.uid, [f"d_p{i}" for i in range(5)]].to_numpy(float)
parts = np.stack([cm.loc[c.uid, [f"{p}_p{i}" for i in range(5)]].to_numpy(float) for p in ("ft", "sb", "nl")])
p3 = cm.loc[c.uid, ["p_incorrect", "p_partial", "p_correct"]].to_numpy(float)
assert np.isfinite(dp).all() and np.isfinite(parts).all() and np.isfinite(p3).all(), "Non-finite probability"
assert np.max(np.abs(dp.sum(1)-1)) < 1e-5 and np.max(np.abs(parts.sum(2)-1)) < 1e-5 and np.max(np.abs(p3.sum(1)-1)) < 1e-5, "Probability row sums invalid"
path_a = np.column_stack((dp[:, [1, 3, 4]].sum(1), dp[:, 2], dp[:, 0])).argmax(1)
assert np.array_equal(path_a, p3.argmax(1)), "Path A disagrees with saved component-export Path A"
raw5 = parts.mean(0)
k5 = raw5.argmax(1)
path_b = np.where(np.isin(k5, [1, 3, 4]), 0, np.where(k5 == 2, 1, 2))
key = ["dataset", "question_id", "question", "reference_answer", "student_answer", "label5"]
dupmask = d.duplicated(key, keep=False)
retained = d.sort_values("uid").drop_duplicates(key, keep="first")
assert int(dupmask.sum()) == 36 and int(d.duplicated(key).sum()) == 19 and len(retained) == 2030, "Approved duplicate policy counts changed"
uidsets = {"primary_2049": set(d.uid.astype(str)), "dedup_2030": set(retained.uid.astype(str))}
positions = {name: np.flatnonzero(c.uid.astype(str).isin(uids).to_numpy()) for name, uids in uidsets.items()}
labels = ["Incorrect", "Partial", "Correct"]
def metrics(yy, pp):
    pr, rc, f, _ = precision_recall_fscore_support(yy, pp, labels=[0, 1, 2], zero_division=0)
    return {"accuracy": accuracy_score(yy, pp), "macro_f1": f1_score(yy, pp, labels=[0, 1, 2], average="macro", zero_division=0), "weighted_f1": f1_score(yy, pp, labels=[0, 1, 2], average="weighted", zero_division=0), "partial_precision": pr[1], "partial_recall": rc[1], "partial_f1": f[1], "qwk": cohen_kappa_score(yy, pp, labels=[0, 1, 2], weights="quadratic")}
def cm_metrics(mx):
    support, predicted, diag = mx.sum(1), mx.sum(0), np.diag(mx)
    pr = np.divide(diag, predicted, out=np.zeros(3), where=predicted != 0)
    rc = np.divide(diag, support, out=np.zeros(3), where=support != 0)
    f = np.divide(2*pr*rc, pr+rc, out=np.zeros(3), where=(pr+rc) != 0)
    w = ((np.arange(3)[:, None] - np.arange(3)[None, :]) ** 2) / 4
    exp = np.outer(support, predicted) / max(mx.sum(), 1) ** 2
    qwk = 1 - (w*mx).sum()/mx.sum() / (w*exp).sum() if mx.sum() and (w*exp).sum() else np.nan
    return {"accuracy": diag.sum()/mx.sum(), "macro_f1": f.mean(), "weighted_f1": np.average(f, weights=support) if mx.sum() else np.nan, "partial_precision": pr[1], "partial_recall": rc[1], "partial_f1": f[1], "qwk": qwk}
metric_rows, confusion_rows, disagreements, summaries, cis = [], [], [], {}, {}
for pop, ix in positions.items():
    yy, aa, bb = y[ix], path_a[ix], path_b[ix]
    meta = am.loc[c.uid[ix]]
    slices = {"overall": np.ones(len(ix), dtype=bool), "SciEntsBank": meta.dataset.astype(str).str.casefold().eq("scientsbank").to_numpy(), "Beetle": meta.dataset.astype(str).str.casefold().eq("beetle").to_numpy(), "seen_dev_ua": meta.split.astype(str).eq("dev_ua").to_numpy(), "unseen_dev_uq": meta.split.astype(str).eq("dev_uq").to_numpy()}
    for scope, mask in slices.items():
        for path, pred in (("Path A", aa[mask]), ("Path B", bb[mask])):
            metric_rows.append({"population": pop, "scope": scope, "path": path, "n": int(mask.sum()), **metrics(yy[mask], pred)})
            mx = confusion_matrix(yy[mask], pred, labels=[0, 1, 2])
            confusion_rows.extend({"population": pop, "scope": scope, "path": path, "gold": labels[g], "predicted": labels[p], "count": int(mx[g, p])} for g in range(3) for p in range(3))
    local = pd.DataFrame({"uid": c.uid.astype(str).to_numpy()[ix], "dataset": meta.dataset.to_numpy(), "question_id": meta.question_id.to_numpy(), "split": meta.split.to_numpy(), "gold": [labels[v] for v in yy], "PathA_pred": [labels[v] for v in aa], "PathB_pred": [labels[v] for v in bb], "PathA_correct": aa == yy, "PathB_correct": bb == yy})
    disagreements.extend(local.loc[aa != bb].assign(population=pop).to_dict("records"))
    summaries[pop] = {"n": len(ix), "different": int((aa != bb).sum()), "A_correct_B_wrong": int(((aa == yy) & (bb != yy)).sum()), "A_wrong_B_correct": int(((aa != yy) & (bb == yy)).sum()), "both_correct": int(((aa == yy) & (bb == yy)).sum()), "both_wrong": int(((aa != yy) & (bb != yy)).sum()), "questions": int(meta.question_id.nunique())}
    qids = meta.question_id.to_numpy()
    groups = [np.flatnonzero(qids == q) for q in pd.unique(qids)]
    group_a = np.array([np.bincount(yy[g]*3+aa[g], minlength=9).reshape(3, 3) for g in groups])
    group_b = np.array([np.bincount(yy[g]*3+bb[g], minlength=9).reshape(3, 3) for g in groups])
    rng = np.random.default_rng(20261106)
    for scheme in ("paired_row", "paired_question_group"):
        draws = []
        for _ in range(10000):
            if scheme == "paired_row":
                z = rng.integers(0, len(ix), len(ix))
                ca = np.bincount(yy[z]*3+aa[z], minlength=9).reshape(3, 3)
                cb = np.bincount(yy[z]*3+bb[z], minlength=9).reshape(3, 3)
            else:
                pick = rng.integers(0, len(groups), len(groups))
                ca, cb = group_a[pick].sum(0), group_b[pick].sum(0)
            ma, mb = cm_metrics(ca), cm_metrics(cb)
            draws.append({k: mb[k] - ma[k] for k in ma})
        cis[(pop, scheme)] = {k: np.nanquantile([r[k] for r in draws], [0.025, 0.975]).tolist() for k in draws[0]}
metric_df, cm_df = pd.DataFrame(metric_rows), pd.DataFrame(confusion_rows)
(OUT / "EXP1_METRICS_COMPARISON_v2.csv").write_text(metric_df.to_csv(index=False), encoding="utf-8")
(OUT / "EXP1_CONFUSION_MATRICES_v2.csv").write_text(cm_df.to_csv(index=False), encoding="utf-8")
pd.DataFrame(disagreements).sort_values(["population", "uid"]).to_csv(OUT / "EXP1_DISAGREEMENT_ANALYSIS_v2.csv", index=False)
overall = metric_df[metric_df.scope.eq("overall")]
lines = ["# Experiment 1 — Path A vs Path B", "", "**Scope:** dev-only, optimistic; saved predictions/probabilities only. No model inference, training, notebook execution, or test data access.", "", "## Inputs and validation", "", f"- Path A and gold: `{GOLD.relative_to(ROOT).as_posix()}` SHA-256 `{hashlib.sha256(GOLD.read_bytes()).hexdigest()}`.", f"- Component probabilities: `{COMP.relative_to(ROOT).as_posix()}` SHA-256 `{hashlib.sha256(COMP.read_bytes()).hexdigest()}`.", f"- Dev text metadata: `{TEXT.relative_to(ROOT).as_posix()}` SHA-256 `{hashlib.sha256(TEXT.read_bytes()).hexdigest()}`.", f"- A_predict source checked without import: SHA-256 `{api_hash}`; class order and collapse source verified.", "- PASS: 2,049 unique UIDs per artifact; identical UID sets; dataset/split/question_id/label5 match by UID; only dev_ua/dev_uq splits; required columns, finite probabilities, row sums, mapped gold labels, and Path A export parity verified.", "- Path A uses stored deployed d_p0–d_p4, collapse `[p1+p3+p4, p2, p0]`, argmax. Path B averages saved ft/sb/nl five-class probabilities, five-way argmax, then maps 1/3/4→Incorrect, 2→Partial, 0→Correct.", "- Dedup sensitivity retains the lexicographically smallest UID per exact content group; all original rows remain unchanged. Raw-source provenance remains unverified.", "", "## Overall metrics", "", overall.to_string(index=False), "", "## Dataset and seen/unseen metrics", "", metric_df[~metric_df.scope.eq("overall")].to_string(index=False), "", "## Paired bootstrap differences (Path B minus Path A)", "", "10,000 resamples per population and scheme; seed 20261106. Row bootstrap samples rows; grouped bootstrap samples question IDs. Percentile 95% CIs:", "", "| Population | Scheme | Metric | Difference | 95% CI | Includes zero |", "|---|---|---|---:|---|---|"]
for pop, ix in positions.items():
    ma, mb = metrics(y[ix], path_a[ix]), metrics(y[ix], path_b[ix])
    for scheme in ("paired_row", "paired_question_group"):
        for k, ci in cis[(pop, scheme)].items():
            lines.append(f"| {pop} | {scheme} | {k} | {mb[k]-ma[k]:.6f} | [{ci[0]:.6f}, {ci[1]:.6f}] | {'yes' if ci[0] <= 0 <= ci[1] else 'no'} |")
lines += ["", "## Disagreements and decision gates", "", pd.DataFrame([{"population": k, **v} for k, v in summaries.items()]).to_string(index=False), "", "McNemar was not used: repeated answers are clustered by question, so independent-pair assumptions are not established; question-grouped bootstrap is reported instead.", ""]
delta = metrics(y[positions["primary_2049"]], path_b[positions["primary_2049"]])["accuracy"] - metrics(y[positions["primary_2049"]], path_a[positions["primary_2049"]])["accuracy"]
group_ci = cis[("primary_2049", "paired_question_group")]
lo, hi = group_ci["accuracy"]
important = ("accuracy", "macro_f1", "partial_recall", "partial_f1")
primary_supported = all(group_ci[k][0] > 0 and metrics(y[positions["primary_2049"]], path_b[positions["primary_2049"]])[k] > metrics(y[positions["primary_2049"]], path_a[positions["primary_2049"]])[k] for k in important)
dedup_delta = {k: metrics(y[positions["dedup_2030"]], path_b[positions["dedup_2030"]])[k] - metrics(y[positions["dedup_2030"]], path_a[positions["dedup_2030"]])[k] for k in important}
unseen = metric_df[(metric_df.population == "primary_2049") & (metric_df.scope == "unseen_dev_uq")].set_index("path")
generalization_ok = unseen.loc["Path B", "accuracy"] >= unseen.loc["Path A", "accuracy"]
decision = "PROMISING" if primary_supported and all(v > 0 for v in dedup_delta.values()) and generalization_ok else "INCONCLUSIVE" if delta >= 0 or any(v >= 0 for v in dedup_delta.values()) else "REJECTED"
lines += [f"Primary accuracy difference: {delta:.6f}; question-grouped CI [{lo:.6f}, {hi:.6f}]. Sensitivity differences: {dedup_delta}.", f"Deduplicated unseen/seen safety check: unseen accuracy non-regression={generalization_ok}.", f"**Classification: {decision}.** Path B is not promoted to production.", "", "## Reproduction", "", "From the Project 4 root: `python Project_S_QA_Evidence/Experiment_1_Path_Comparison/EXP1_REPRODUCE_v2.py`. Requires pandas, NumPy, scikit-learn and an installed parquet engine. Refuses test-named paths, source hash/schema/alignment failures, or existing v2 outputs.", ""]
(OUT / "EXP1_AGGREGATION_COMPARISON_REPORT_v2.md").write_text("\n".join(lines), encoding="utf-8")
files = [OUT / n for n in ["EXP1_REPRODUCE_v2.py", "EXP1_AGGREGATION_COMPARISON_REPORT_v2.md", "EXP1_METRICS_COMPARISON_v2.csv", "EXP1_CONFUSION_MATRICES_v2.csv", "EXP1_DISAGREEMENT_ANALYSIS_v2.csv"]]
manifest = ["# Experiment 1 artifact manifest", "", "This manifest excludes itself. Inputs are dev-only; source artifacts were not modified.", "", "| File | Bytes | SHA-256 |", "|---|---:|---|"]
manifest += [f"| `{p.name}` | {p.stat().st_size} | `{hashlib.sha256(p.read_bytes()).hexdigest()}` |" for p in files]
(OUT / "EXP1_ARTIFACT_MANIFEST_v2.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
print("VALIDATION PASS", "primary=2049", "deduplicated=2030", "seed=20261106", "bootstrap=10000")
print("SUMMARY", summaries)
print("OVERALL", overall.to_dict("records"))
print("BOOTSTRAP", cis)
