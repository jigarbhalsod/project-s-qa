"""DRAFT ONLY. Gate nested-CV outputs; dev-only, optimistic; no test inputs."""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, precision_recall_fscore_support

SEEDS, FOLDS = (42, 123, 2026), range(5)
PARTIAL = 1

def safe_path(s):
    if "test" in str(s).lower(): raise SystemExit(f"Refusing test-named path: {s}")
    return Path(s)

def scores(y, p):
    q = np.asarray(p); pr, rc, f1, _ = precision_recall_fscore_support(y, q, labels=[PARTIAL], average=None, zero_division=0)
    return {"accuracy": accuracy_score(y, q), "macro_f1": f1_score(y, q, labels=[0, 1, 2], average="macro", zero_division=0), "qwk": cohen_kappa_score(y, q, labels=[0, 1, 2], weights="quadratic"), "partial_precision": pr[0], "partial_recall": rc[0], "partial_f1": f1[0]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-text", required=True); ap.add_argument("--baseline", required=True); ap.add_argument("--prediction-dir", required=True)
    ap.add_argument("--negation-diagnostic"); a = ap.parse_args()
    paths = [a.dev_text, a.baseline, a.prediction_dir] + ([a.negation_diagnostic] if a.negation_diagnostic else [])
    dev_path, base_path, pred_dir = map(safe_path, paths[:3]); dev, base = pd.read_parquet(dev_path), pd.read_parquet(base_path)
    if a.negation_diagnostic: safe_path(a.negation_diagnostic)
    if len(dev) != 2049 or dev.uid.nunique() != 2049 or dev.split.astype(str).str.contains("test", case=False).any(): raise SystemExit("Dev-only UID/split assertion failed")
    label_map = {"correct": 2, "partially_correct_incomplete": 1, "contradictory": 0, "irrelevant": 0, "non_domain": 0}
    dev["gold3"] = dev.label5.astype(str).str.lower().map(label_map)
    if dev.gold3.isna().any(): raise SystemExit("Unmapped gold label")
    if base.uid.duplicated().any() or set(base.uid) != set(dev.uid): raise SystemExit("Baseline UID set does not equal dev UID set")
    base = dev[["uid", "dataset", "split", "question_id", "gold3"]].merge(base, on=["uid", "dataset", "split", "question_id"], validate="one_to_one")
    if len(base) != 2049: raise SystemExit("Baseline UID alignment failed")
    bp = np.c_[base.d_p1 + base.d_p3 + base.d_p4, base.d_p2, base.d_p0].argmax(1); y = base.gold3.to_numpy(); bscore = scores(y, bp)
    pred_by_seed, run_records = {}, {}
    for seed in SEEDS:
        frames, records = [], []
        for fold in FOLDS:
            folder = pred_dir / f"seed_{seed}" / f"outer_{fold}"
            csvp, jsonp = folder / f"A_x1_seed{seed}_fold{fold}.csv", folder / f"A_x1_seed{seed}_fold{fold}.json"
            if not csvp.exists() or not jsonp.exists(): raise SystemExit(f"Missing prediction or run record: {folder}")
            q = pd.read_csv(csvp); rec = json.loads(jsonp.read_text(encoding="utf-8"))
            if rec.get("seed") != seed or rec.get("outer_fold") != fold or set(q.outer_fold.unique()) != {fold}: raise SystemExit(f"Seed/fold metadata mismatch: {folder}")
            frames.append(q); records.append(rec)
        c = pd.concat(frames, ignore_index=True)
        if c.uid.duplicated().any() or set(c.uid) != set(dev.uid): raise SystemExit(f"Seed {seed}: OOF UIDs do not equal dev UIDs")
        c = dev[["uid", "dataset", "split", "question_id", "gold3"]].merge(c, on=["uid", "dataset", "split", "question_id", "gold3"], validate="one_to_one")
        pred_by_seed[seed] = c[["p0", "p1", "p2"]].to_numpy().argmax(1); run_records[seed] = records
    metric_by_seed = {s: scores(y, p) for s, p in pred_by_seed.items()}; means = {k: float(np.mean([v[k] for v in metric_by_seed.values()])) for k in metric_by_seed[42]}
    groups = (dev.dataset.astype(str) + "|" + dev.question_id.astype(str)).to_numpy(); uniq = np.unique(groups); gidx = {g: np.flatnonzero(groups == g) for g in uniq}; rng = np.random.default_rng(42); boot = []
    for _ in range(10000):
        ix = np.concatenate([gidx[g] for g in rng.choice(uniq, len(uniq), replace=True)])
        boot.append(np.mean([f1_score(y[ix], pred_by_seed[s][ix], labels=[0, 1, 2], average="macro", zero_division=0) - f1_score(y[ix], bp[ix], labels=[0, 1, 2], average="macro", zero_division=0) for s in SEEDS]))
    macro_delta = means["macro_f1"] - bscore["macro_f1"]; ci = np.quantile(boot, [.025, .975])
    uq = dev.split.eq("dev_uq").to_numpy(); uq_y, uq_bp = y[uq], bp[uq]
    uq_base = cohen_kappa_score(uq_y, uq_bp, labels=[0, 1, 2], weights="quadratic")
    uq_cand = float(np.mean([cohen_kappa_score(y[uq], pred_by_seed[s][uq], labels=[0, 1, 2], weights="quadratic") for s in SEEDS]))
    ug = groups[uq]; uuniq = np.unique(ug); uidx = {g: np.flatnonzero(ug == g) for g in uuniq}; uq_boot = []
    for _ in range(10000):
        ix = np.concatenate([uidx[g] for g in rng.choice(uuniq, len(uuniq), replace=True)])
        uq_boot.append(cohen_kappa_score(uq_y[ix], uq_bp[ix], labels=[0, 1, 2], weights="quadratic"))
    uq_ci = np.nanquantile(uq_boot, [.025, .975]); proposed_margin = min(0.01, float((uq_ci[1] - uq_ci[0]) / 2))
    latency = {b: np.concatenate([np.asarray(r[f"latency_batch{b}_ms_runs"], dtype=float) for s in SEEDS for r in run_records[s]]) for b in (1, 32)}
    print("EXPLORATORY: dev-only, optimistic; outer dev folds are not a locked test")
    print("baseline", bscore, "candidate_three_seed_mean", means)
    print("macro_f1_gain", macro_delta, "paired_question_bootstrap_95_ci", ci.tolist(), "gate", macro_delta >= .01 and ci[0] > 0)
    print("accuracy_gate", means["accuracy"] > bscore["accuracy"], "overall_qwk_gate", means["qwk"] > bscore["qwk"])
    print("baseline_unseen_qwk_bootstrap_95_ci", uq_ci.tolist(), "dev-only")
    print("unseen_qwk", "candidate_mean", uq_cand, "baseline", uq_base, "proposed_margin", proposed_margin, "gate", uq_cand >= uq_base - proposed_margin)
    print("partial_recall_gate", means["partial_recall"] > bscore["partial_recall"], "partial_f1_gate", means["partial_f1"] > bscore["partial_f1"])
    print("negation", "12-case diagnostic only; no gate")
    for b, vals in latency.items(): print(f"batch{b}_latency_ms median={np.median(vals):.3f} p95={np.quantile(vals,.95):.3f} (reported only)")
    if a.negation_diagnostic:
        n = pd.read_csv(safe_path(a.negation_diagnostic))
        if len(n) != 12 or not {"gold3", "p0", "p1", "p2"}.issubset(n.columns): raise SystemExit("Negation diagnostic must contain 12 rows and gold3,p0,p1,p2")
        if "split" in n and n.split.astype(str).str.contains("test", case=False).any(): raise SystemExit("Test split found in negation diagnostic")
        ny = n.gold3.to_numpy(dtype=int); npred = n[["p0", "p1", "p2"]].to_numpy().argmax(1)
        print("negation_diagnostic_only", f"{int((ny == npred).sum())}/12", "no gate")
    else: print("negation_diagnostic_only", "not supplied; no gate")

if __name__ == "__main__": main()
