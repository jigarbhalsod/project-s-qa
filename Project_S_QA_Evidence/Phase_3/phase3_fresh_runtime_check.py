from pathlib import Path; import os, sys, json, hashlib
ROOT=Path(os.environ.get("PROJECT_S_ROOT","/content/drive/MyDrive/project_s_qa")); V2=ROOT/"reports_v2"; API=V2/"A_predict.py"
REF=V2/"A_demo_reference_outputs_v2.json"; POLICY=V2/"A_abstain_policy_v2.json"; LOG=Path(os.environ.get("PHASE3_DIR",Path(__file__).resolve().parent))/"phase3_fresh_runtime_check.log"
paths=[ROOT,API,REF,POLICY,LOG,Path(__file__)]
if any("test" in str(p).lower() for p in paths): raise ValueError("Refusing a path containing 'test'")
missing=[str(p) for p in (API,REF,POLICY) if not p.is_file()]
if missing: raise FileNotFoundError("Missing runtime files: "+", ".join(missing))
digest=hashlib.sha256(API.read_bytes()).hexdigest(); data=json.loads(REF.read_text(encoding="utf-8"))
if digest!="ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053" or data.get("a_predict_sha256")!=digest: raise RuntimeError("A_predict SHA-256 mismatch")
if data.get("scorer_mode")!="pooled": raise RuntimeError("Reference scorer_mode is not pooled")
if not LOG.parent.is_dir(): raise FileNotFoundError("Create/use the Phase_3 log folder before running")
sys.dont_write_bytecode=True; os.environ.update(PROJECT_S_ROOT=str(ROOT),HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1"); sys.path.insert(0,str(V2))
import A_predict
cases=data["cases"][:5]
if len(cases)!=5: raise ValueError("Reference JSON has fewer than five cases")
items=[{k:c[k] for k in ("question","reference_answer","student_answer")} for c in cases]
results=A_predict.predict_batch(items,dataset="pooled")
lines=[f'{c["case_id"]}: {r["pred_label"]}; probs incorrect/partial/correct={r["p_incorrect"]}/{r["p_partial"]}/{r["p_correct"]}; confidence={r["confidence"]}; review={r["needs_teacher_review"]}' for c,r in zip(cases,results)]
for line in lines: print(line)
LOG.open("x",encoding="utf-8").write("\n".join(lines)+"\n")
