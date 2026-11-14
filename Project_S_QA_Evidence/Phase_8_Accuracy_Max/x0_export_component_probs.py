import os, sys, random, inspect, numpy as np, pandas as pd, torch
from google.colab import drive; drive.mount("/content/drive")
ROOT="/content/drive/MyDrive/project_s_qa"; DATA=f"{ROOT}/processed/sra_unified_splits_v1.parquet"; REF=f"{ROOT}/reports_v2/A_deployed_dev_probs_v2.parquet"; OUT=f"{ROOT}/reports_v2/A_x0_component_probs_dev_v2.parquet"
INPUTS=[DATA,REF]; assert not any("test" in p.lower() for p in INPUTS), "Refusing test-named input path"; assert not os.path.exists(OUT), f"Refusing overwrite: {OUT}"
sys.path.insert(0,f"{ROOT}/reports_v2"); import A_predict
assert list(inspect.signature(A_predict.component_probs).parameters)==["items","dataset"]
random.seed(42); np.random.seed(42); torch.manual_seed(42)
rows=pd.read_parquet(DATA,filters=[("split","in",["dev_ua","dev_uq"])])
need={"uid","dataset","split","question_id","label5","score_ours","question","reference_answer","student_answer"}; assert need<=set(rows.columns), f"Missing columns: {need-set(rows.columns)}"
assert len(rows)==2049 and rows.uid.is_unique and set(rows.split)<={"dev_ua","dev_uq"}, "Expected unique 2,049 dev rows only"
ref=pd.read_parquet(REF); rc=[f"d_p{k}" for k in range(5)]; assert set(["uid",*rc])<=set(ref.columns) and ref.uid.is_unique
T=float(A_predict._load_policy().get("temperature",1.0)); fn=["nli_f_ent_mean","nli_f_ent_min","nli_f_con_max","nli_f_neu_mean","nli_r_ent","nli_r_con","nli_r_neu"]; parts=[]
for start in range(0,len(rows),8):
 b=rows.iloc[start:start+8]; items=b[["question","reference_answer","student_answer"]].to_dict("records"); c=A_predict.component_probs(items,dataset="pooled")
 p5=(c["ft"]+c["sb"]+c["nl"])/3; p3=A_predict._to3(p5)
 if T!=1.0: q=np.clip(p3,1e-9,1.0)**(1.0/T); p3=q/q.sum(1,keepdims=True)
 z=pd.DataFrame({"uid":b.uid.to_numpy(),**{f"{m}_p{k}":c[m][:,k] for m in ("ft","sb","nl") for k in range(5)},**{n:c["feats"][:,k] for k,n in enumerate(fn)},"max_concept_contradiction":c["feats"][:,2],**{f"pooled_p{k}":p5[:,k] for k in range(5)},"p_incorrect":p3[:,0],"p_partial":p3[:,1],"p_correct":p3[:,2],"confidence":p3.max(1)})
 parts.append(z)
out=pd.concat(parts,ignore_index=True); cols=[f"pooled_p{k}" for k in range(5)]; chk=out.merge(ref[["uid",*rc]],on="uid",validate="one_to_one"); assert len(chk)==len(out)==len(ref)==2049 and np.allclose(chk[cols].to_numpy(),chk[rc].to_numpy(),atol=1e-6,rtol=0), "UID or pooled-probability parity failed"
out.to_parquet(OUT,index=False); print("PASS: dev component probabilities exported and pooled parity <= 1e-6")
