from pathlib import Path
import os, sys, json, hashlib, time
ROOT=Path(os.environ.get("PROJECT_S_ROOT","/content/drive/MyDrive/project_s_qa")); V2=ROOT/"reports_v2"
API=V2/"A_predict.py"; CONTRACT=V2/"A_predict_contract_v2.json"; REF=V2/"A_demo_reference_outputs_v2.json"; POLICY=V2/"A_abstain_policy_v2.json"
P3=Path(__file__).resolve().parent; LOG=P3/"phase3_fresh_runtime_check_v2.log"
paths=[ROOT,API,CONTRACT,REF,POLICY,LOG,Path(__file__).resolve()]
if P3.name!="Phase_3": raise RuntimeError("Place this script in Project_S_QA_Evidence/Phase_3")
if any("test" in str(p).lower() for p in paths): raise ValueError("Refusing a path containing 'test'")
missing=[str(p) for p in (API,CONTRACT,REF,POLICY) if not p.is_file()]
if missing: raise FileNotFoundError("Missing packaged runtime files: "+", ".join(missing))
contract=json.loads(CONTRACT.read_text(encoding="utf-8")); data=json.loads(REF.read_text(encoding="utf-8"))
if not isinstance(contract,dict) or data.get("scorer_mode")!="pooled": raise ValueError("Invalid contract or scorer_mode is not pooled")
api_hash=hashlib.sha256(API.read_bytes()).hexdigest(); policy_hash=hashlib.sha256(POLICY.read_bytes()).hexdigest()
if api_hash!="ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053" or data.get("a_predict_sha256")!=api_hash: raise ValueError("A_predict SHA-256 mismatch")
if data.get("policy_sha256")!=policy_hash: raise ValueError("A_abstain_policy_v2.json hash mismatch")
if LOG.exists(): raise FileExistsError(f"Refusing to overwrite log: {LOG}")
sys.dont_write_bytecode=True; os.environ.update(PROJECT_S_ROOT=str(ROOT),HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1"); sys.path.insert(0,str(V2))
import A_predict
if Path(A_predict.__file__).resolve()!=API.resolve(): raise RuntimeError("Imported A_predict is not the packaged file")
if hashlib.sha256(Path(A_predict.__file__).read_bytes()).hexdigest()!=api_hash: raise RuntimeError("Imported A_predict hash changed")
cases=data.get("cases",[])[:5]
if len(cases)!=5: raise ValueError("Reference JSON has fewer than five demo cases")
lines=[]
for c in cases:
 t0=time.perf_counter(); r=A_predict.predict(c["question"],c["reference_answer"],c["student_answer"],dataset="pooled"); ms=(time.perf_counter()-t0)*1000
 lines.append(f'{c["case_id"]}: label={r["pred_label"]}; probs incorrect/partial/correct={r["p_incorrect"]}/{r["p_partial"]}/{r["p_correct"]}; confidence={r["confidence"]}; review={r["needs_teacher_review"]}; single-run timing, not Block 62={ms:.1f} ms')
for line in lines: print(line)
with LOG.open("x",encoding="utf-8") as f: f.write("\n".join(lines)+"\n")
