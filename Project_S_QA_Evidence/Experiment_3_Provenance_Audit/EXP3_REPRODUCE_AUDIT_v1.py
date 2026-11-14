"""Static Project S artifact checks; no model loading, inference, or writes."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import pandas as pd

HASHES = {
"Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet":"21e7305557825b392a297fc4558b73e1161fcefb07d82c9f802e33c877836ea2",
"Project_S_QA_Evidence/Phase_8_Accuracy_Max/A_component_probs_v7.parquet":"71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88",
"project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet":"2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e",
"project_s_qa/A_submission_v2/reports_v2/A_predict.py":"ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053",
"project_s_qa/interim/pooled_lr_v2.joblib":"216493152a1b7ae2143f0fc60ce2eed6ffc735f40676e308455225b1b55aa96f",
"project_s_qa/interim/ft_distilroberta_v1/model.safetensors":"671e70acf931c6dedd28ebff73baccfa3acf3b07dba13cb3eb15fc39f04761fd",
"Project_S_QA_Evidence/Phase_8_Accuracy_Max/x0_export_component_probs_v7.py":"75b8ae23f41a9a5e92df4186c888c0dcdc23c2205b9882dc23b20cdadad0eb3b"}
OUTS = ["EXP3_PROVENANCE_AUDIT_REPORT_v1.md","EXP3_COMPONENT_PROVENANCE_v1.csv","EXP3_LEAKAGE_AUDIT_v1.csv","EXP3_INFORMATION_FLOW_v1.csv","EXP3_ARTIFACT_INVENTORY_v1.csv","EXP3_RISK_REGISTER_v1.md","EXP3_ARTIFACT_MANIFEST_v1.md","EXP3_REPRODUCE_AUDIT_v1.py"]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(p):
    if "test" in str(p).casefold(): raise RuntimeError("Refusing test-named path: "+str(p))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",type=Path,default=Path(__file__).resolve().parents[2]); root=ap.parse_args().project_root.resolve()
    files={s:root/s for s in HASHES}
    for s,p in files.items():
        safe(p)
        if not p.is_file() or sha(p)!=HASHES[s]: raise RuntimeError("Missing/hash mismatch: "+s)
    text,comp,dep=[pd.read_parquet(files[s]) for s in list(HASHES)[:3]]
    api=files["project_s_qa/A_submission_v2/reports_v2/A_predict.py"].read_text(encoding="utf-8")
    if 'LABEL5_ORDER = ["correct", "contradictory", "partially_correct_incomplete", "irrelevant", "non_domain"]' not in api or "return np.c_[P[:, [1, 3, 4]].sum(1), P[:, 2], P[:, 0]]" not in api: raise RuntimeError("A_predict class order/mapping changed")
    frames=[text,comp,dep]
    if any(len(x)!=2049 or x.uid.isna().any() or not x.uid.is_unique for x in frames): raise RuntimeError("Expected 2,049 unique UIDs")
    if not (set(text.uid)==set(comp.uid)==set(dep.uid)): raise RuntimeError("UID sets differ")
    if any(set(x.split.astype(str))!={"dev_ua","dev_uq"} for x in frames): raise RuntimeError("Non-dev split found")
    for x in (comp,dep):
        cols=([f"{k}_p{i}" for k in ("ft","sb","nl") for i in range(5)] if x is comp else [f"d_p{i}" for i in range(5)])
        a=x[cols].to_numpy(float)
        if not np.isfinite(a).all() or np.max(np.abs(a.reshape(len(x),-1,5).sum(2)-1))>1e-5: raise RuntimeError("Invalid probability rows")
    for col in ("dataset","split","question_id","label5"):
        a=text.set_index("uid")[col].sort_index(); b=comp.set_index("uid")[col].sort_index(); c=dep.set_index("uid")[col].sort_index()
        if not a.equals(b) or not a.equals(c): raise RuntimeError("Metadata mismatch: "+col)
    m={"correct":2,"partially_correct_incomplete":1,"contradictory":0,"irrelevant":0,"non_domain":0}
    if not np.array_equal(text.set_index("uid").loc[dep.uid].label5.astype(str).str.lower().map(m).to_numpy(),dep.score_ours.astype(int).to_numpy()): raise RuntimeError("Gold mapping mismatch")
    key=["dataset","question_id","question","reference_answer","student_answer","label5"]; d=text.sort_values("uid").drop_duplicates(key,keep="first")
    if len(d)!=2030 or text.duplicated(key,keep=False).sum()!=36: raise RuntimeError("Approved duplicate sensitivity population changed")
    audit_dir=root/"Project_S_QA_Evidence/Experiment_3_Provenance_Audit"
    missing=[n for n in OUTS if not (audit_dir/n).is_file() or (audit_dir/n).stat().st_size==0]
    if missing: raise RuntimeError("Missing audit outputs: "+", ".join(missing))
    print("PASS: hashes, dev-only schemas, 2,049 UID alignment, class map, row sums and duplicate policy")
    print("UNVERIFIED: train/dev UID overlap; no verified training UID manifest is configured")
    print("PASS: expected audit output files exist; no files were written")
if __name__=="__main__": main()

