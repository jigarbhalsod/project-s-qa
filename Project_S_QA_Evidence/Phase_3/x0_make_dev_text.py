from pathlib import Path
import os
import pandas as pd
ROOT=Path(os.environ.get("PROJECT_S_ROOT","/content/drive/MyDrive/project_s_qa"))
SPLITS=ROOT/"sra_unified_splits_v1.parquet"; PROBS=ROOT/"reports_v2/A_deployed_dev_probs_v2.parquet"
OUT=Path(__file__).resolve().parent/"A_dev_text_v2.parquet"; paths=[SPLITS,PROBS,OUT,Path(__file__)]
if any("test" in str(p).lower() for p in paths): raise ValueError("Refusing a path containing 'test'")
if OUT.exists(): raise FileExistsError(f"Refusing to overwrite {OUT}")
p=pd.read_parquet(PROBS); raw=pd.read_parquet(SPLITS)
assert {"uid","label5"}<=set(p.columns) and p.uid.is_unique
cols=["uid","dataset","split","question_id","label5","question","reference_answer","student_answer"]
assert set(cols)<=set(raw.columns)
d=raw[raw.uid.isin(set(p.uid))].copy(); assert d.split.eq("dev").all()
m=d.merge(p[["uid","label5"]].rename(columns={"label5":"label5_probs"}),on="uid",validate="one_to_one")
assert len(m)==2049 and m.uid.nunique()==2049 and m.label5.equals(m.label5_probs)
m[cols].to_parquet(OUT,index=False)
print(f"rows={len(m)} unique_uids={m.uid.nunique()} splits={m.split.value_counts().to_dict()}")
