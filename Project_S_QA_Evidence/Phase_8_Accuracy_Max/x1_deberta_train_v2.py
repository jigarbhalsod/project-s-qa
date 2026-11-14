"""DRAFT ONLY. Dev-only nested CV; run only after Phase 3 and Stage 1 approval."""
import argparse, json, math, statistics, time
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer, TrainingArguments, set_seed

CKPTS = ("MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli", "cross-encoder/nli-deberta-v3-base")
MAXLEN, LR, EPOCHS, WARMUP, TRAIN_BS, EVAL_BS, ACCUM = 256, 2e-5, 3, 0.10, 4, 8, 4
LABELS = {"correct": 2, "partially_correct_incomplete": 1, "contradictory": 0, "irrelevant": 0, "non_domain": 0}

def safe_path(s):
    if "test" in str(s).lower(): raise SystemExit(f"Refusing test-named path: {s}")
    return Path(s)

def load_pair():
    errors = []
    for ckpt in CKPTS:
        try: return ckpt, AutoTokenizer.from_pretrained(ckpt), AutoModelForSequenceClassification.from_pretrained(ckpt, num_labels=3, ignore_mismatched_sizes=True)
        except Exception as exc: errors.append(f"{ckpt}: {type(exc).__name__}: {exc}")
    raise RuntimeError("Both approved checkpoints unavailable: " + "; ".join(errors))

class Rows(torch.utils.data.Dataset):
    def __init__(self, frame, tok): self.frame, self.tok = frame.reset_index(drop=True), tok
    def __len__(self): return len(self.frame)
    def __getitem__(self, i):
        r = self.frame.iloc[i]
        z = self.tok(f"[QUESTION] {r.question} [REFERENCE] {r.reference_answer}", str(r.student_answer), truncation=True, max_length=MAXLEN)
        return {**z, "labels": int(r.label3)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-text", required=True); ap.add_argument("--folds", required=True)
    ap.add_argument("--output-dir", default="/content/phase8_tmp"); ap.add_argument("--seed", type=int, choices=(42, 123, 2026), required=True)
    ap.add_argument("--fold", type=int, choices=range(5), required=True)
    a = ap.parse_args(); dev_path, fold_path, out_root = map(safe_path, (a.dev_text, a.folds, a.output_dir))
    if not torch.cuda.is_available(): raise SystemExit("CUDA GPU required; Colab T4 is the planned runtime")
    gpu_name = torch.cuda.get_device_name(0)
    df, folds = pd.read_parquet(dev_path), pd.read_csv(fold_path)
    if df.split.astype(str).str.contains("test", case=False).any(): raise SystemExit("Test split found; refusing to continue")
    df["label3"] = df.label5.astype(str).str.lower().map(LABELS)
    if df.label3.isna().any() or df.uid.duplicated().any() or len(df) != 2049: raise SystemExit("Dev rows/UID/label validation failed")
    z = df.merge(folds, on=["uid", "dataset", "question_id", "label3"], validate="one_to_one")
    if len(z) != len(df) or z.uid.nunique() != 2049: raise SystemExit("Fold UID alignment failed")
    z["group"] = z.dataset.astype(str) + "|" + z.question_id.astype(str)
    if z.groupby("group").outer_fold.nunique().max() != 1 or z.groupby("group").inner_fold.nunique().max() != 1: raise SystemExit("Question group split across folds")
    outer_train, outer_eval = z[z.outer_fold != a.fold].copy(), z[z.outer_fold == a.fold].copy()
    if outer_eval.empty or outer_train.empty: raise SystemExit("Selected outer fold is empty")
    run_dir = out_root / f"seed_{a.seed}" / f"outer_{a.fold}"
    pred_path, run_path = run_dir / f"A_x1_seed{a.seed}_fold{a.fold}.csv", run_dir / f"A_x1_seed{a.seed}_fold{a.fold}.json"
    if pred_path.exists() or run_path.exists(): raise SystemExit(f"Refusing to overwrite: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=False)
    all_scores = {e: [] for e in range(1, EPOCHS + 1)}; selected_ids = []
    ckpt_id = None; tokenizer = None
    for inner in range(4):
        tr, va = outer_train[outer_train.inner_fold != inner], outer_train[outer_train.inner_fold == inner]
        if tr.empty or va.empty: raise SystemExit(f"Empty inner fold {inner} within outer training")
        set_seed(a.seed); ckpt_id, tokenizer, model = load_pair(); model.classifier.apply(model._init_weights)
        args = TrainingArguments(output_dir=str(run_dir / f"inner_{inner}"), seed=a.seed, data_seed=a.seed, learning_rate=LR, num_train_epochs=EPOCHS, warmup_ratio=WARMUP, fp16=True, per_device_train_batch_size=TRAIN_BS, per_device_eval_batch_size=EVAL_BS, gradient_accumulation_steps=ACCUM, eval_strategy="epoch", save_strategy="no", report_to="none")
        trainer = Trainer(model=model, args=args, train_dataset=Rows(tr, tokenizer), eval_dataset=Rows(va, tokenizer), data_collator=DataCollatorWithPadding(tokenizer), compute_metrics=lambda p: {"macro_f1": f1_score(p.label_ids, p.predictions.argmax(-1), labels=[0, 1, 2], average="macro", zero_division=0)})
        trainer.train()
        for log in trainer.state.log_history:
            if "eval_macro_f1" in log and "epoch" in log: all_scores[int(round(log["epoch"]))].append(float(log["eval_macro_f1"]))
        selected_ids.append((inner, len(tr), len(va)))
    mean_scores = {e: float(np.mean(v)) for e, v in all_scores.items() if v}
    if any(len(v) != 4 for v in all_scores.values()) or not mean_scores: raise SystemExit("Inner validation Macro-F1 is missing from one or more inner folds")
    best_epoch = max(mean_scores, key=mean_scores.get)
    set_seed(a.seed); ckpt_id, tokenizer, model = load_pair(); model.classifier.apply(model._init_weights)
    args = TrainingArguments(output_dir=str(run_dir / "outer_fit"), seed=a.seed, data_seed=a.seed, learning_rate=LR, num_train_epochs=best_epoch, warmup_ratio=WARMUP, fp16=True, per_device_train_batch_size=TRAIN_BS, per_device_eval_batch_size=EVAL_BS, gradient_accumulation_steps=ACCUM, eval_strategy="no", save_strategy="no", report_to="none")
    trainer = Trainer(model=model, args=args, train_dataset=Rows(outer_train, tokenizer), data_collator=DataCollatorWithPadding(tokenizer))
    trainer.train(); eval_rows = Rows(outer_eval, tokenizer)
    trunc = [len(tokenizer(f"[QUESTION] {r.question} [REFERENCE] {r.reference_answer}", str(r.student_answer), truncation=False)["input_ids"]) > MAXLEN for r in pd.concat([outer_train, outer_eval]).itertuples()]
    def timed(frame):
        ds = Rows(frame, tokenizer); samples = []
        trainer.predict(ds); torch.cuda.synchronize()
        for _ in range(20):
            torch.cuda.synchronize(); t0 = time.perf_counter(); trainer.predict(ds); torch.cuda.synchronize(); samples.append((time.perf_counter() - t0) * 1000)
        return samples
    lat1 = timed(outer_eval.iloc[:1]); lat32 = timed(outer_eval.iloc[:32]); logits = trainer.predict(eval_rows).predictions
    probs = torch.softmax(torch.tensor(logits), dim=1).cpu().numpy()
    pd.DataFrame({"uid": outer_eval.uid, "dataset": outer_eval.dataset, "split": outer_eval.split, "question_id": outer_eval.question_id, "outer_fold": a.fold, "gold3": outer_eval.label3, **{f"p{i}": probs[:, i] for i in range(3)}}).to_csv(pred_path, index=False)
    payload = {"seed": a.seed, "outer_fold": a.fold, "gpu": gpu_name, "checkpoint_id": ckpt_id, "selected_epoch": best_epoch, "inner_mean_macro_f1_by_epoch": mean_scores, "inner_fold_sizes": selected_ids, "rows": len(outer_eval), "max_length": MAXLEN, "truncation_count": int(sum(trunc)), "truncation_pct": float(100 * np.mean(trunc)), "latency_batch1_ms_runs": lat1, "latency_batch32_ms_runs": lat32, "latency_timer": "predict call plus CUDA synchronization; no file writes in timed interval", "scope": "dev-only, optimistic"}
    run_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"DRAFT protocol output: {len(outer_eval)} held-out dev rows; selected epoch={best_epoch}; truncation_pct={payload['truncation_pct']:.3f}")

if __name__ == "__main__": main()
