"""Drafted: dev, optimistic; not a clean test. Read-only metric report."""
import argparse
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support, cohen_kappa_score, confusion_matrix
SCOPE="dev, optimistic; not a clean test"; ORDER=["correct","contradictory","partially_correct_incomplete","irrelevant","non_domain"]; NAMES=["Incorrect","Partial","Correct"]
p=argparse.ArgumentParser(); p.add_argument("--dev-probs",required=True); p.add_argument("--train-question-ids",required=True); a=p.parse_args(); dp=Path(a.dev_probs).expanduser().resolve(); tp=Path(a.train_question_ids).expanduser().resolve()
if any("test" in str(x).casefold() for x in (dp,tp)) or tp.name.casefold()=="sra_unified_splits_v1.parquet": raise ValueError("Refusing a test path or prohibited unified split file")
if dp.name!="A_deployed_dev_probs_v2.parquet": raise ValueError("--dev-probs must be A_deployed_dev_probs_v2.parquet")
d=pd.read_parquet(dp); need={"uid","split","question_id","dataset","label5",*[f"d_p{i}" for i in range(5)]}; assert need<=set(d.columns),f"Missing columns: {sorted(need-set(d.columns))}"
assert len(d)==2049 and d.uid.notna().all() and d.uid.nunique()==2049,"Expected 2,049 unique non-null dev UIDs"; assert not d.split.astype(str).str.contains("test",case=False,regex=False).any() and d.split.astype(str).str.lower().str.startswith("dev").all(),"Non-dev/test split refused"
def label5(v):
    s=str(v).strip().casefold(); i=int(s) if s.isdigit() else ORDER.index(s) if s in ORDER else -1
    if i not in range(5): raise ValueError(f"Unmapped label5 value: {v!r}")
    return 2 if i==0 else 1 if i==2 else 0
y=np.array([label5(v) for v in d.label5]); P=d[[f"d_p{i}" for i in range(5)]].to_numpy(float); assert np.isfinite(P).all(),"Non-finite probabilities"
p3=np.column_stack((P[:,[1,3,4]].sum(1),P[:,2],P[:,0])); pred=p3.argmax(1); assert np.allclose(P.sum(1),1,atol=1e-5),"Five-class probability rows do not sum to 1"
# Verified mapping mirrors A_predict.py:56-57; unseen rule mirrors x0_make_dev_text_v3.py:26-29 using train-only IDs, not the prohibited unified split file.
assert "train" in tp.name.casefold() and tp.is_file(),"--train-question-ids must be an existing train-only question_id projection"; tq=pd.read_csv(tp,usecols=["question_id"]).question_id.dropna(); unseen=~d.question_id.isin(set(tq)); seen=~unseen
def metrics(ix):
    yy,pp=y[ix],pred[ix]; pr,re,f,_=precision_recall_fscore_support(yy,pp,labels=[0,1,2],zero_division=0); return {"n":len(ix),"accuracy":accuracy_score(yy,pp),"macro_f1":f1_score(yy,pp,labels=[0,1,2],average="macro",zero_division=0),"weighted_f1":f1_score(yy,pp,labels=[0,1,2],average="weighted",zero_division=0),"precision":pr.tolist(),"recall":re.tolist(),"f1":f.tolist(),"qwk":cohen_kappa_score(yy,pp,labels=[0,1,2],weights="quadratic"),"partial_recall":re[1]}
emit=lambda k,v: print(f"[{SCOPE}] {k}: {v}"); full=metrics(np.arange(len(d))); emit("overall metrics; class order Incorrect/Partial/Correct",full); emit("3x3 confusion; rows=gold, columns=predicted",confusion_matrix(y,pred,labels=[0,1,2]).tolist()); emit("predicted class counts",dict(zip(NAMES,np.bincount(pred,minlength=3).tolist())))
def grouped_ci():
    rng=np.random.default_rng(42); q=d.question_id.to_numpy(); groups=[np.flatnonzero(q==z) for z in pd.unique(q)]; vals=[]
    for _ in range(10000):
        ix=np.concatenate([groups[j] for j in rng.integers(0,len(groups),len(groups))]); m=metrics(ix); vals.append([m["accuracy"],m["macro_f1"],m["qwk"]])
    return np.nanquantile(np.asarray(vals,float),[.025,.975],axis=0).T
ci=grouped_ci(); emit("question-group bootstrap 95% CIs; 10,000 resamples; seed=42; accuracy/Macro-F1/QWK",ci.tolist())
for title,mask in [("dataset=beetle",d.dataset.astype(str).str.casefold().eq("beetle")),("dataset=scientsbank",d.dataset.astype(str).str.casefold().eq("scientsbank")),("seen question",seen),("unseen question",unseen)]: emit(title,metrics(np.flatnonzero(mask.to_numpy())))
reported={"accuracy":(56.37,2),"macro_f1":(52.70,2),"qwk":(.4015,4),"partial_recall":(26.34,2),"seen_accuracy":(69.19,2),"unseen_accuracy":(48.92,2)}; observed={"accuracy":100*full["accuracy"],"macro_f1":100*full["macro_f1"],"qwk":full["qwk"],"partial_recall":100*full["partial_recall"],"seen_accuracy":100*metrics(np.flatnonzero(seen))["accuracy"],"unseen_accuracy":100*metrics(np.flatnonzero(unseen))["accuracy"]}
for k,(ref,digits) in reported.items(): emit(f"{k}: observed={observed[k]:.{digits}f}{'%' if k!='qwk' else ''}; Reported={ref:.{digits}f}{'%' if k!='qwk' else ''}; comparison at displayed precision", "MATCH" if round(observed[k],digits)==round(ref,digits) else "MISMATCH")
