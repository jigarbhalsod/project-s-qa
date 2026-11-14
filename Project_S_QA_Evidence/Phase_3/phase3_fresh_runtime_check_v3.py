# Verified source refs: A_predict.py ROOT L8; hub model IDs L11-12 and loaders L26,32,34; predict signature/body L176-178; result keys L166-172.
# Verified JSON keys read: scorer_mode, a_predict_sha256, policy_sha256, cases; case_id/question/reference_answer/student_answer/output; output p_incorrect/p_partial/p_correct.
# Unverified at runtime: uncached hub models may be fetched and cached by A_predict.
from pathlib import Path
import argparse, os, sys, json, hashlib, time
from datetime import datetime, timezone
ap=argparse.ArgumentParser(); ap.add_argument("--phase3-dir",required=True); ap.add_argument("--project-root",default="/content/drive/MyDrive/project_s_qa"); a=ap.parse_args()
ROOT=Path(a.project_root).expanduser().resolve(); V2=ROOT/"reports_v2"; API=V2/"A_predict.py"; CONTRACT=V2/"A_predict_contract_v2.json"; REF=V2/"A_demo_reference_outputs_v2.json"; POLICY=V2/"A_abstain_policy_v2.json"
P3=Path(a.phase3_dir).expanduser().resolve()
if P3.name!="Phase_3" or not P3.is_dir(): raise ValueError("--phase3-dir must be an existing Phase_3 directory")
stamp=datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"); LOG=P3/f"phase3_fresh_runtime_check_{stamp}.log"
paths=[ROOT,V2,API,CONTRACT,REF,POLICY,P3,LOG]
if any("test" in str(p).lower() for p in paths): raise ValueError("Refusing a path containing 'test'")
missing=[str(p) for p in (API,CONTRACT,REF,POLICY) if not p.is_file()]
if missing: raise FileNotFoundError("Missing packaged runtime files: "+", ".join(missing))
contract=json.loads(CONTRACT.read_text(encoding="utf-8")); data=json.loads(REF.read_text(encoding="utf-8"))
if not isinstance(contract,dict) or data.get("scorer_mode")!="pooled": raise ValueError("Invalid contract or scorer_mode is not pooled")
api_hash=hashlib.sha256(API.read_bytes()).hexdigest(); policy_hash=hashlib.sha256(POLICY.read_bytes()).hexdigest()
if api_hash!="ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053" or data.get("a_predict_sha256")!=api_hash: raise ValueError("A_predict SHA-256 mismatch")
if data.get("policy_sha256")!=policy_hash: raise ValueError("A_abstain_policy_v2.json hash mismatch")
if LOG.exists(): raise FileExistsError(f"Refusing to overwrite log: {LOG}")
sys.dont_write_bytecode=True; os.environ["PROJECT_S_ROOT"]=str(ROOT); sys.path.insert(0,str(V2))
if "A_predict" in sys.modules: raise RuntimeError("Use a fresh runtime with A_predict not already imported")
import A_predict
if Path(A_predict.__file__).resolve()!=API.resolve() or hashlib.sha256(Path(A_predict.__file__).read_bytes()).hexdigest()!=api_hash: raise RuntimeError("Imported A_predict path/hash mismatch")
cases=data.get("cases",[])[:5]; pkeys=("p_incorrect","p_partial","p_correct")
if len(cases)!=5: raise ValueError("Reference JSON has fewer than five demo cases")
lines=[]
for i,c in enumerate(cases):
 t0=time.perf_counter(); r=A_predict.predict(c["question"],c["reference_answer"],c["student_answer"],dataset="pooled"); ms=(time.perf_counter()-t0)*1000
 diff=max(abs(float(r[k])-float(c["output"][k])) for k in pkeys) if all(k in c.get("output",{}) for k in pkeys) else None
 timing="cold start, includes model loading; single-run timing, not Block 62" if i==0 else "single-run timing, not Block 62"
 lines.append(f'{c["case_id"]}: label={r["pred_label"]}; probs={r["p_incorrect"]}/{r["p_partial"]}/{r["p_correct"]}; confidence={r["confidence"]}; review={r["needs_teacher_review"]}; {timing}={ms:.1f} ms; max_abs_probability_diff={diff}')
for line in lines: print(line)
with LOG.open("x",encoding="utf-8") as f: f.write("\n".join(lines)+"\n")
