from pathlib import Path
import argparse
import pandas as pd
ap=argparse.ArgumentParser(description="Export dev answer text aligned to dev probabilities")
ap.add_argument("--splits",required=True); ap.add_argument("--dev-probs",required=True); ap.add_argument("--output",required=True)
a=ap.parse_args(); splits=Path(a.splits).expanduser().resolve(); probs_path=Path(a.dev_probs).expanduser().resolve(); out_path=Path(a.output).expanduser().resolve()
paths=[splits,probs_path,out_path,Path(__file__).resolve()]
if any("test" in str(p).lower() for p in paths): raise ValueError("Refusing an input/output/script path containing 'test'")
if out_path.exists(): raise FileExistsError(f"Refusing to overwrite output: {out_path}")
probs=pd.read_parquet(probs_path); raw=pd.read_parquet(splits)
if not {"uid","label5","split"}.issubset(probs.columns): raise ValueError("Dev probabilities need uid, label5, and split columns")
if probs.uid.isna().any() or probs.uid.duplicated().any(): raise ValueError("Dev probabilities contain null or duplicate UIDs")
if len(probs)!=2049 or probs.uid.nunique()!=2049: raise ValueError("Expected 2,049 unique dev-probability UIDs")
cols=["uid","dataset","split","question_id","label5","question","reference_answer","student_answer"]
if not set(cols).issubset(raw.columns): raise ValueError("Unified splits is missing required export columns")
kept=raw.loc[raw.uid.isin(probs.uid)].copy()
if kept.uid.isna().any() or kept.uid.duplicated().any(): raise ValueError("Matched rows contain null or duplicate UIDs")
if set(kept.uid)!=set(probs.uid): raise ValueError("Matched rows do not cover the dev-probability UID set")
join_cols=["split","label5"]+[c for c in ("dataset","question_id") if c in probs.columns]
right=probs[["uid"]+join_cols].rename(columns={c:c+"_prob" for c in join_cols})
m=kept.merge(right,on="uid",validate="one_to_one")
for c in join_cols:
 if c=="split" and (m[c].astype(str).str.contains("test",case=False,regex=False).any() or m[c+"_prob"].astype(str).str.contains("test",case=False,regex=False).any()): raise ValueError("A test split value matched the dev UID set")
 if not m[c].astype(str).equals(m[c+"_prob"].astype(str)): raise ValueError(f"{c} mismatch by UID")
out=m[cols]
if list(out.columns)!=cols or len(out)!=2049 or out.uid.nunique()!=2049: raise ValueError("Output schema or UID count is invalid")
if out.question_id.isna().any(): raise ValueError("Matched rows contain null question_id values")
train_splits=raw.split.astype(str).str.lower(); train_ids=set(raw.loc[train_splits.str.startswith("train"),"question_id"].dropna())
unseen_ids=set(out.question_id)-train_ids; unseen_rows=int(out.question_id.isin(unseen_ids).sum()); seen_rows=len(out)-unseen_rows
out.to_parquet(out_path,index=False)
print(f"rows={len(out)} unique_uids={out.uid.nunique()} dataset_counts={out.dataset.value_counts(dropna=False).to_dict()} unseen_questions={len(unseen_ids)} unseen_rows={unseen_rows} seen_rows={seen_rows}")
