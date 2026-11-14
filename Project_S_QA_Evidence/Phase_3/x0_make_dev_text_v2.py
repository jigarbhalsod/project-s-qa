from pathlib import Path
import argparse
import pandas as pd
ap=argparse.ArgumentParser(description="Export aligned dev-only answer text")
ap.add_argument("--splits",required=True); ap.add_argument("--dev-probs",required=True); ap.add_argument("--output",required=True)
a=ap.parse_args(); splits=Path(a.splits).expanduser().resolve(); probs_path=Path(a.dev_probs).expanduser().resolve(); out_path=Path(a.output).expanduser().resolve()
paths=[splits,probs_path,out_path,Path(__file__).resolve()]
if any("test" in str(p).lower() for p in paths): raise ValueError("Refusing an input/output/script path containing 'test'")
if out_path.exists(): raise FileExistsError(f"Refusing to overwrite output: {out_path}")
probs=pd.read_parquet(probs_path); raw=pd.read_parquet(splits)
if not {"uid","label5"}.issubset(probs.columns): raise ValueError("Dev probabilities need uid and label5 columns")
if probs.uid.isna().any() or probs.uid.duplicated().any(): raise ValueError("Dev probabilities contain null or duplicate UIDs")
if len(probs)!=2049 or probs.uid.nunique()!=2049: raise ValueError("Expected 2,049 unique dev-probability UIDs")
cols=["uid","dataset","split","question_id","label5","question","reference_answer","student_answer"]
if not set(cols).issubset(raw.columns): raise ValueError("Unified splits is missing required export columns")
kept=raw.loc[raw.uid.isin(probs.uid)].copy()
if kept.uid.isna().any() or kept.uid.duplicated().any(): raise ValueError("Matched rows contain null or duplicate UIDs")
if set(kept.uid)!=set(probs.uid): raise ValueError("Matched rows do not cover the dev-probability UID set")
s=kept.split.astype(str).str.lower()
if s.str.contains("test",regex=False).any(): raise ValueError("A test-split row matched the dev UID set")
if not s.eq("dev").all(): raise ValueError("Every matched row must have split == 'dev'")
m=kept.merge(probs[["uid","label5"]].rename(columns={"label5":"label5_probs"}),on="uid",validate="one_to_one")
if not m.label5.astype(str).equals(m.label5_probs.astype(str)): raise ValueError("label5 mismatch by UID")
out=m[cols]
if list(out.columns)!=cols or len(out)!=2049 or out.uid.nunique()!=2049: raise ValueError("Output schema or UID count is invalid")
out.to_parquet(out_path,index=False)
print(f"rows={len(out)} unique_uids={out.uid.nunique()} dataset_counts={out.dataset.value_counts(dropna=False).to_dict()}")
meta_cols=[c for c in kept.columns if c not in {"question","reference_answer","student_answer"}]
seen_cols=[c for c in meta_cols if "seen" in c.lower() or "unseen" in c.lower()]
if not seen_cols:
 for c in meta_cols:
  v=kept[c].dropna().astype(str).str.lower()
  if len(v) and v.isin({"seen","unseen","dev_ua","dev_uq","ua","uq"}).all(): seen_cols.append(c)
if seen_cols: print("seen_unseen_counts="+str({c:kept[c].value_counts(dropna=False).to_dict() for c in seen_cols}))
