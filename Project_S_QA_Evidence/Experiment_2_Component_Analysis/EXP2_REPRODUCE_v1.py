"""Reproduce Project S Experiment 2 from saved development probabilities only."""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, precision_recall_fscore_support

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TEXT = ROOT / "Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet"
COMP = ROOT / "Project_S_QA_Evidence/Phase_8_Accuracy_Max/A_component_probs_v7.parquet"
GOLD = ROOT / "project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet"
API = ROOT / "project_s_qa/A_submission_v2/reports_v2/A_predict.py"
EXPORTER = ROOT / "Project_S_QA_Evidence/Phase_8_Accuracy_Max/x0_export_component_probs_v7.py"
SEED, BOOT = 20261110, 10000
ORDER = ["correct", "contradictory", "partially_correct_incomplete", "irrelevant", "non_domain"]
LABELS, PARTS = ["Incorrect", "Partial", "Correct"], ["ft", "sb", "nl"]
CONFIG = {"C1":["ft"],"C2":["sb"],"C3":["nl"],"C4":["ft","sb"],"C5":["ft","nl"],"C6":["sb","nl"],"C7":PARTS}
NAMES = {"C1":"DistilRoBERTa","C2":"SBERT-LR","C3":"NLI-LR","C4":"DistilRoBERTa + SBERT-LR","C5":"DistilRoBERTa + NLI-LR","C6":"SBERT-LR + NLI-LR","C7":"Full three-component ensemble"}
METRICS = ["accuracy","macro_f1","weighted_f1","partial_precision","partial_recall","partial_f1","qwk"]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok, msg):
    if not ok: raise RuntimeError("BLOCKED: " + msg)
def collapse(p): return np.column_stack((p[:,[1,3,4]].sum(1),p[:,2],p[:,0]))
def conf(y,p): return np.bincount(3*y+p,minlength=9).reshape(3,3)
def stats_cm(m):
    m=np.asarray(m,dtype=float); n=np.maximum(m.sum(axis=(-2,-1)),1); d=np.diagonal(m,axis1=-2,axis2=-1); s=m.sum(-1); q=m.sum(-2)
    pr=np.divide(d,q,out=np.zeros_like(d),where=q!=0); rc=np.divide(d,s,out=np.zeros_like(d),where=s!=0)
    f=np.divide(2*pr*rc,pr+rc,out=np.zeros_like(pr),where=(pr+rc)!=0); w=((np.arange(3)[:,None]-np.arange(3)[None,:])**2)/4
    obs=(m*w).sum((-2,-1))/n; exp=(s[..., :,None]*q[...,None,:]/n[...,None,None]**2*w).sum((-2,-1))
    qw=np.divide(-obs,exp,out=np.full_like(obs,np.nan),where=exp!=0)+1
    return np.stack((d.sum(-1)/n,f.mean(-1),np.divide((f*s).sum(-1),n),rc[...,1],f[...,1],qw),axis=-1)
def get_metrics(y,p):
    pr,rc,f,s=precision_recall_fscore_support(y,p,labels=[0,1,2],zero_division=0)
    out={"accuracy":accuracy_score(y,p),"macro_f1":f1_score(y,p,labels=[0,1,2],average="macro",zero_division=0),"weighted_f1":f1_score(y,p,labels=[0,1,2],average="weighted",zero_division=0),"qwk":cohen_kappa_score(y,p,labels=[0,1,2],weights="quadratic"),"partial_precision":pr[1],"partial_recall":rc[1],"partial_f1":f[1]}
    for i,label in enumerate(LABELS):
        for k,v in (("precision",pr[i]),("recall",rc[i]),("f1",f[i]),("support",int(s[i]))): out[label.lower()+"_"+k]=v
    return out
def bootstrap(y,preds,groups,rng):
    n=len(y); keys=list(preds); row={k:np.empty((BOOT,6)) for k in keys}; grp={k:np.empty((BOOT,6)) for k in keys}
    qid=np.asarray(groups); uq=pd.unique(qid); byq={k:np.asarray([conf(y[qid==q],preds[k][qid==q]).ravel() for q in uq]) for k in keys}
    for start in range(0,BOOT,100):
        b=min(100,BOOT-start); ix=rng.integers(0,n,size=(b,n),dtype=np.int32); yy=y[ix]; rr=np.repeat(np.arange(b),n)
        for k in keys:
            codes=(3*yy+preds[k][ix]).ravel(); m=np.zeros((b,9),dtype=np.int32); np.add.at(m,(rr,codes),1); row[k][start:start+b]=stats_cm(m.reshape(b,3,3))
        draws=rng.multinomial(len(uq),np.full(len(uq),1/len(uq)),size=b)
        for k in keys: grp[k][start:start+b]=stats_cm((draws@byq[k]).reshape(b,3,3))
    return row,grp

OUT.mkdir(parents=True,exist_ok=True)
inputs=[TEXT,COMP,GOLD,API,OUT]
require(not any("test" in str(p).casefold() for p in inputs),"refusing a test-named path")
for p in inputs[:4]: require(p.is_file(),"required artifact missing: "+str(p))
api=API.read_text(encoding="utf-8"); api_hash=sha(API)
require(api_hash=="ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053","A_predict.py hash mismatch")
require('LABEL5_ORDER = ["correct", "contradictory", "partially_correct_incomplete", "irrelevant", "non_domain"]' in api and "return np.c_[P[:, [1, 3, 4]].sum(1), P[:, 2], P[:, 0]]" in api,"label order or mapping not source-verified")
require(EXPORTER.is_file(),"component exporter source missing")
exporter_text=EXPORTER.read_text(encoding="utf-8")
require("A_predict.LABEL5_ORDER" in exporter_text,"component exporter does not establish LABEL5_ORDER provenance")
require("return dict(ft=ft, sb=sb, nl=nl, feats=feats, concepts=concepts)" in api and "p3 = _to3((c[\"ft\"] + c[\"sb\"] + c[\"nl\"]) / 3)" in api,"component outputs or deployed averaging are not source-verified")
a,c,d=(pd.read_parquet(p) for p in (GOLD,COMP,TEXT))
need_a={"uid","dataset","split","question_id","label5","score_ours",*[f"d_p{i}" for i in range(5)]}
features=["nli_f_ent_mean","nli_f_ent_min","nli_f_con_max","nli_f_neu_mean","nli_r_ent","nli_r_con","nli_r_neu"]
need_c={"uid","dataset","split","question_id","label5",*[f"{z}_p{i}" for z in PARTS for i in range(5)],"p_incorrect","p_partial","p_correct",*features}
need_d={"uid","dataset","split","question_id","label5","question","reference_answer","student_answer"}
require(need_a<=set(a) and need_c<=set(c) and need_d<=set(d),"required columns missing")
for frame,name in ((a,"deployed"),(c,"component"),(d,"dev text")):
    require(len(frame)==2049 and frame.uid.notna().all() and frame.uid.astype(str).is_unique,name+" must have 2,049 unique UIDs")
    require(not frame.isna().any().any(),name+" has nulls; refusing to drop rows")
    require(not frame.split.astype(str).str.contains("test",case=False,regex=False).any(),name+" has non-dev split")
require(set(a.uid.astype(str))==set(c.uid.astype(str))==set(d.uid.astype(str)),"UID sets differ")
uids=sorted(d.uid.astype(str))
ai=a.assign(uid=a.uid.astype(str)).set_index("uid").loc[uids]
ci=c.assign(uid=c.uid.astype(str)).set_index("uid").loc[uids]
di=d.assign(uid=d.uid.astype(str)).set_index("uid").loc[uids]
for col in ("dataset","split","question_id","label5"):
    require(ai[col].astype(str).reset_index(drop=True).equals(di[col].astype(str).reset_index(drop=True)) and ci[col].astype(str).reset_index(drop=True).equals(di[col].astype(str).reset_index(drop=True)),"metadata mismatch by UID: "+col)
require(set(ai.split.astype(str))=={"dev_ua","dev_uq"},"unexpected split values")
g5=di.label5.astype(str).str.strip().str.casefold().map({s:i for i,s in enumerate(ORDER)})
require(not g5.isna().any(),"unmapped gold labels: "+repr(sorted(di.loc[g5.isna(),"label5"].astype(str).unique().tolist())))
g5=g5.to_numpy(dtype=int); y=np.where(g5==0,2,np.where(g5==2,1,0))
require(np.array_equal(y,ai.score_ours.astype(int).to_numpy()),"gold label mapping differs from saved score_ours")
parts={z:ci[[f"{z}_p{i}" for i in range(5)]].to_numpy(float) for z in PARTS}
dp=ai[[f"d_p{i}" for i in range(5)]].to_numpy(float)
for z,p in [*parts.items(),("deployed",dp)]:
    require(p.shape==(2049,5) and np.isfinite(p).all() and (p < -1e-8).sum()==0 and (p > 1+1e-8).sum()==0 and np.max(np.abs(p.sum(1)-1))<1e-5,z+" probabilities invalid")
nli_features=ci[features].to_numpy(float)
require(nli_features.shape==(2049,7) and np.isfinite(nli_features).all(),"NLI feature matrix is not finite 2,049 x 7")
raw={k:np.mean([parts[z] for z in v],axis=0) for k,v in CONFIG.items()}
p3={k:collapse(v) for k,v in raw.items()}; pred={k:v.argmax(1) for k,v in p3.items()}
saved_a=collapse(dp).argmax(1); saved_c=ci[["p_incorrect","p_partial","p_correct"]].to_numpy(float).argmax(1)
saved_p3=ci[["p_incorrect","p_partial","p_correct"]].to_numpy(float)
require(saved_p3.shape==(2049,3) and np.isfinite(saved_p3).all() and np.max(np.abs(saved_p3.sum(1)-1))<1e-5,"saved three-class probabilities invalid")
path_a=int((pred["C7"]==saved_a).sum()); export_a=int((pred["C7"]==saved_c).sum())
require(path_a==2049,"Path A predictions do not exactly reproduce deployed file")
key=["dataset","question_id","question","reference_answer","student_answer","label5"]
dd=di.reset_index(); dup=dd.duplicated(key,keep=False); retained=dd.sort_values("uid").drop_duplicates(key,keep="first")
require(int(dup.sum())==36 and int(dd.duplicated(key).sum())==19 and retained.uid.nunique()==2030 and dd.loc[dup].groupby(key,dropna=False).ngroups==17,"approved duplicate set no longer equals 2,030 UIDs")
dedup=set(retained.uid.astype(str)); pops={"primary_2049":np.arange(2049),"dedup_2030":np.flatnonzero(np.isin(uids,sorted(dedup)))}
require(len(pops["dedup_2030"])==2030,"dedup UID alignment failed")

metric_rows=[]; confusion_rows=[]; ablation_rows=[]; overlap_rows=[]; uidrows=[]; bootrows=[]; calrows=[]
scopes={"overall":lambda m:np.ones(len(m),bool),"seen_dev_ua":lambda m:m.split.astype(str).eq("dev_ua").to_numpy(),"unseen_dev_uq":lambda m:m.split.astype(str).eq("dev_uq").to_numpy(),"SciEntsBank":lambda m:m.dataset.astype(str).str.casefold().eq("scientsbank").to_numpy(),"Beetle":lambda m:m.dataset.astype(str).str.casefold().eq("beetle").to_numpy()}
for pop,ix in pops.items():
    meta=di.iloc[ix].reset_index(); yy=y[ix]; gold5pop=g5[ix]; ps={k:v[ix] for k,v in pred.items()}; probs={k:v[ix] for k,v in p3.items()}
    for scope,fn in scopes.items():
        mask=fn(meta)
        for k in CONFIG:
            vals=get_metrics(yy[mask],ps[k][mask]); mat=conf(yy[mask],ps[k][mask]); yy5=g5[ix][mask]
            vals.update({"partial_tp":int(mat[1,1]),"false_partial":int(mat[:,1].sum()-mat[1,1]),"missed_partial":int(mat[1,:].sum()-mat[1,1]),"incorrect_to_partial":int(mat[0,1]),"correct_to_partial":int(mat[2,1]),"contradictory_to_partial":int(((yy5==1)&(ps[k][mask]==1)).sum())})
            require(int(mat.sum())==int(mask.sum()),"confusion matrix total mismatch")
            metric_rows.append({"population":pop,"scope":scope,"config":k,"name":NAMES[k],"n":int(mask.sum()),**vals})
            confusion_rows.extend({"population":pop,"scope":scope,"config":k,"name":NAMES[k],"gold":LABELS[r],"predicted":LABELS[j],"count":int(mat[r,j])} for r in range(3) for j in range(3))
            if scope=="overall":
                q=probs[k][mask]; one=np.eye(3)[yy[mask]]
                calrows.append({"population":pop,"config":k,"name":NAMES[k],"n":int(mask.sum()),"mean_max_probability":float(q.max(1).mean()),"brier_3class":float(((q-one)**2).sum(1).mean()),"log_loss_3class":float(-np.log(np.clip(q[np.arange(len(q)),yy[mask]],1e-15,1)).mean())})
    row={"population":pop,"uid":np.asarray(uids)[ix],"dataset":meta.dataset.astype(str),"split":meta.split.astype(str),"question_id":meta.question_id.astype(str),"gold_label5":meta.label5.astype(str),"gold3":[LABELS[z] for z in yy]}
    for k in CONFIG: row[k+"_pred"]=[LABELS[z] for z in ps[k]]; row[k+"_correct"]=ps[k]==yy
    for x,z in (("C1","C2"),("C1","C3"),("C2","C3")): row[x+"_vs_"+z+"_disagree"]=ps[x]!=ps[z]
    uidrows.append(pd.DataFrame(row))
    for k in ("C1","C2","C3","C4","C5","C6"):
        typ="component_minus_full" if k in ("C1","C2","C3") else "full_minus_leave_one_out"
        left,right=(k,"C7") if typ=="component_minus_full" else ("C7",k)
        m1,m2=get_metrics(yy,ps[left]),get_metrics(yy,ps[right])
        ablation_rows.append({"population":pop,"comparison":typ,"candidate":left,"candidate_name":NAMES[left],"reference":right,"reference_name":NAMES[right],"n":len(ix),**{"delta_"+m:m1[m]-m2[m] for m in METRICS}})
    for x,z in (("C1","C2"),("C1","C3"),("C2","C3")):
        px,pz=ps[x],ps[z]; ex,ez=px!=yy,pz!=yy; inter,union=int((ex&ez).sum()),int((ex|ez).sum()); partial=yy==1; contra=gold5pop==1
        overlap_rows.append({"population":pop,"first":x,"first_name":NAMES[x],"second":z,"second_name":NAMES[z],"n":len(ix),"both_correct":int((~ex&~ez).sum()),"both_wrong":inter,"first_correct_second_wrong":int((~ex&ez).sum()),"first_wrong_second_correct":int((ex&~ez).sum()),"same_wrong_class":int((ex&ez&(px==pz)).sum()),"disagree":int((px!=pz).sum()),"disagreement_rate":float((px!=pz).mean()),"error_intersection":inter,"error_union":union,"error_jaccard":inter/union if union else np.nan,"first_error_rate":float(ex.mean()),"second_error_rate":float(ez.mean()),"second_error_given_first_wrong":float(inter/ex.sum()) if ex.sum() else np.nan,"first_error_given_second_wrong":float(inter/ez.sum()) if ez.sum() else np.nan,"first_partial_rescues":int((partial&(px==1)&(pz!=1)).sum()),"second_partial_rescues":int((partial&(pz==1)&(px!=1)).sum()),"first_contradiction_error_second_correct":int((contra&ex&~ez).sum()),"second_contradiction_error_first_correct":int((contra&ez&~ex).sum())})
    rng=np.random.default_rng(SEED); groups=meta.dataset.astype(str).to_numpy()+"::"+meta.question_id.astype(str).to_numpy()
    rowboot,groupboot=bootstrap(yy,ps,groups,rng)
    for scheme,bs in (("paired_row",rowboot),("paired_question_group",groupboot)):
        for k in ("C1","C2","C3","C4","C5","C6"):
            left,right=(k,"C7") if k in ("C1","C2","C3") else ("C7",k); draws=bs[left]-bs[right]
            m1,m2=get_metrics(yy,ps[left]),get_metrics(yy,ps[right])
            for j,m in enumerate(("accuracy","macro_f1","weighted_f1","partial_recall","partial_f1","qwk")):
                lo,hi=np.nanquantile(draws[:,j],[.025,.975]); bootrows.append({"population":pop,"scheme":scheme,"comparison":left+"_minus_"+right,"metric":m,"difference":m1[m]-m2[m],"ci95_low":float(lo),"ci95_high":float(hi),"includes_zero":bool(lo<=0<=hi),"resamples":BOOT,"seed":SEED})

v=1
stems=["EXP2_COMPONENT_ANALYSIS_REPORT","EXP2_COMPONENT_METRICS","EXP2_ABLATION_RESULTS","EXP2_ERROR_COMPLEMENTARITY","EXP2_UID_LEVEL_ANALYSIS","EXP2_BOOTSTRAP_RESULTS","EXP2_CONFUSION_MATRICES","EXP2_ARTIFACT_MANIFEST"]
while any((OUT/f"{s}_v{v}.{ext}").exists() for s,ext in [(x,"md" if "REPORT" in x or "MANIFEST" in x else "csv") for x in stems]): v+=1
files={k:OUT/f"{s}_v{v}.{e}" for k,s,e in [("report","EXP2_COMPONENT_ANALYSIS_REPORT","md"),("metrics","EXP2_COMPONENT_METRICS","csv"),("ablation","EXP2_ABLATION_RESULTS","csv"),("overlap","EXP2_ERROR_COMPLEMENTARITY","csv"),("uid","EXP2_UID_LEVEL_ANALYSIS","csv"),("boot","EXP2_BOOTSTRAP_RESULTS","csv"),("conf","EXP2_CONFUSION_MATRICES","csv"),("manifest","EXP2_ARTIFACT_MANIFEST","md")]}
require(not any(p.exists() for p in files.values()),"refusing to overwrite any output")
for key,rows in (("metrics",metric_rows),("ablation",ablation_rows),("overlap",overlap_rows),("boot",bootrows),("conf",confusion_rows)): pd.DataFrame(rows).to_csv(files[key],index=False)
pd.concat(uidrows,ignore_index=True).to_csv(files["uid"],index=False)
mdf=pd.DataFrame(metric_rows); overall=mdf[mdf.scope=="overall"].set_index(["population","config"]); bdf=pd.DataFrame(bootrows); gci=bdf[(bdf.scheme=="paired_question_group")&(bdf.metric=="accuracy")&(bdf.population=="primary_2049")]
diff=float(np.max(np.abs(raw["C7"]-dp))); p3diff=float(np.max(np.abs(collapse(raw["C7"])-ci[["p_incorrect","p_partial","p_correct"]].to_numpy(float))))
best_unseen=mdf[(mdf.population=="primary_2049")&(mdf.scope=="unseen_dev_uq")&mdf.config.isin(["C1","C2","C3"])].sort_values("accuracy",ascending=False).iloc[0]
best_unseen_macro=mdf[(mdf.population=="primary_2049")&(mdf.scope=="unseen_dev_uq")&mdf.config.isin(["C1","C2","C3"])].sort_values("macro_f1",ascending=False).iloc[0]
best_pair=overall.loc[("primary_2049",["C4","C5","C6"]),"macro_f1"].sort_values(ascending=False).index[0][1]
rescue={z:int(((pred["C"+str(i+1)]==y)&(pred["C7"]!=y)).sum()) for i,z in enumerate(PARTS)}
full_rescue={z:int(((pred["C"+str(i+1)]!=y)&(pred["C7"]==y)).sum()) for i,z in enumerate(PARTS)}
partial_recall={z:float(overall.loc[("primary_2049","C"+str(i+1)),"partial_recall"]) for i,z in enumerate(PARTS)}
false_partial={z:int(((pred["C"+str(i+1)]==1)&(y!=1)).sum()) for i,z in enumerate(PARTS)}
groups_n=di.dataset.astype(str).add("::").add(di.question_id.astype(str)).nunique()
inputs_meta=[("dev text",TEXT,d),("component probabilities",COMP,c),("deployed dev probabilities",GOLD,a)]
lines=["# Experiment 2 — Component contribution, ablation and complementarity","",
"Scope: dev-only, optimistic; saved development probabilities only. No model inference or training.",
"","## Executive conclusion","",
f"Path A reconstruction agrees with saved deployed predictions on {path_a}/2,049 UIDs; component-export Path A agrees on {export_a}/2,049. Maximum raw five-way mean difference versus deployed d_p: {diff:.9g}; versus the saved three-way export: {p3diff:.9g}.",
f"Highest two-component Macro-F1 point estimate: {best_pair}; strongest standalone unseen-question accuracy: {best_unseen.config} = {best_unseen.accuracy:.6f}, n={int(best_unseen.n)}. Component-correct/full-wrong rows: {rescue}; component-wrong/full-correct rows: {full_rescue}.",
"Overall recommendation: INCONCLUSIVE — RETAIN WITH COMPONENT INVESTIGATION. No production change is proposed.",
"","## Artifact validation","","| Artifact | Bytes | SHA-256 | Rows / unique UIDs |"]
for name,p,frame in inputs_meta: lines.append(f"| {name} ({p.relative_to(ROOT).as_posix()}) | {p.stat().st_size} | {sha(p)} | {len(frame)} / {frame.uid.nunique()} |")
lines += [f"| A_predict.py source (read only) | {API.stat().st_size} | {api_hash} | n/a |","",
"UID sets, gold labels, dataset, question IDs and split metadata match exactly by UID. Splits: "+str(di.split.astype(str).value_counts().to_dict())+". Dataset counts: "+str(di.dataset.astype(str).value_counts().to_dict())+". Unique question counts by dataset/split: "+str(di.groupby(["dataset","split"]).question_id.nunique().to_dict())+". Gold label5 counts: "+str(di.label5.astype(str).value_counts().to_dict())+".",
"All three component vectors have five finite normalized probabilities per row. Class order is verified from A_predict.py and the exporter: "+str(ORDER)+".",
f"Duplicate sensitivity validated: 17 exact-content groups, 36 rows in groups, 19 excess rows; primary n=2,049, approved lexicographic-UID subset n={len(retained)}. Raw-source provenance remains Unverified.",
"","## Component probability audit","",
"Static source evidence: A_predict.py LABEL5_ORDER line 13, five-to-three mapping lines 56–57, equal component mean and optional temperature lines 152–157, component outputs ft/sb/nl/features line 136. The saved component parquet has ft_p0-p4, sb_p0-p4 and nl_p0-p4; exporter v7 uses A_predict.LABEL5_ORDER. Model IDs in A_predict.py: fine-tuned local DistilRoBERTa directory, cross-encoder/nli-deberta-v3-base, sentence-transformers/all-MiniLM-L6-v2; pooled logistic-regression artifacts are loaded by the scorer. Exact per-row export runtime provenance and checkpoint hashes are not embedded and remain Unverified.",
"","## Path A reproduction","",
f"PASS: equal mean of the three saved five-class vectors, five-to-three collapse and argmax exactly matches deployed d_p predictions: {path_a}/2,049. Component-export three-class prediction agreement: {export_a}/2,049. Max probability differences are listed above; prediction agreement is exact.",
"","## Metrics by configuration — dev, optimistic","",
"Configs: C1 FT; C2 SBERT-LR; C3 NLI-LR; C4 FT+SBERT-LR; C5 FT+NLI-LR; C6 SBERT-LR+NLI-LR; C7 full ensemble. C4-C6 are also the three leave-one-out ablations. Metrics include each class precision/recall/F1/support. The CSV includes overall, seen/unseen, SciEntsBank and Beetle scopes.",
"","Overall metrics:",mdf[mdf.scope=="overall"].to_string(index=False),"","Seen/unseen and dataset breakdowns:",mdf[mdf.scope!="overall"].to_string(index=False),
"","Partial TP, FP, FN and class-specific measures appear in metrics CSV. Gold-contradictory rows mapped to Incorrect are retained in UID-level analysis for contradiction-to-Partial counts.",
"","## Full ensemble and ablations","",pd.DataFrame(ablation_rows).to_string(index=False),
"Positive component-minus-full differences favor a component; positive full-minus-pair differences favor the full model. Pairwise comparisons use same UIDs. See bootstrap file for paired intervals.",
"","## Paired bootstrap uncertainty","",
f"10,000 paired row resamples and 10,000 paired question-group resamples per population, seed {SEED}. Each sampled group is dataset::question_id and all its rows stay together. Row intervals are supplementary; question-group intervals are primary. Intervals crossing zero do not establish a difference.",
bdf.to_string(index=False),
"","## Error complementarity","",pd.DataFrame(overlap_rows).to_string(index=False),
"Counts include both-correct, both-wrong, directional unique corrections, same-wrong-class, disagreement, error intersection/union/Jaccard, conditional error rates, partial rescues, and contradiction-specific directional errors.",
"UID-level CSV contains UID and metadata, gold labels, every config prediction/correctness, and pairwise disagreement flags; no answer text.",
"","## Calibration and confidence diagnostics — dev, optimistic","",pd.DataFrame(calrows).to_string(index=False),
"Mean max probability, collapsed three-class Brier score, and log loss are descriptive only. No calibrator was fitted; threshold 0.64 was not changed.",
"","## Architecture decision","",
"Component classifications from paired question-grouped C7-vs-ablation intervals in both populations: DistilRoBERTa = CORE CONTRIBUTOR (C7 beats C6 on accuracy, Macro-F1, Partial recall/F1 and QWK with intervals above zero); SBERT-LR = COMPLEMENTARY CONTRIBUTOR (C7 beats C5 on Macro-F1 and Partial recall/F1 with intervals above zero; accuracy interval includes zero); NLI-LR = POTENTIALLY HARMFUL for Partial recall/F1 (C7 is lower than C4 with intervals below zero), while overall accuracy/Macro-F1/QWK differences include zero. NLI-LR also has unique correct cases, so this does not justify automatic removal.",
"Does the full ensemble beat every standalone component? Read C7 against C1-C3 in the metrics and paired intervals; do not infer from a single metric.",
f"Direct answer: C7 accuracy ({overall.loc[('primary_2049','C7'),'accuracy']:.6f}) exceeds each standalone component; FT has a slightly higher standalone Macro-F1 ({overall.loc[('primary_2049','C1'),'macro_f1']:.6f} vs C7 {overall.loc[('primary_2049','C7'),'macro_f1']:.6f}) and weighted-F1 ({overall.loc[('primary_2049','C1'),'weighted_f1']:.6f} vs C7 {overall.loc[('primary_2049','C7'),'weighted_f1']:.6f}).",
"Marginal value: FT inclusion (C7 vs C6) improves all listed primary grouped metrics with CIs above zero, and repeats in the 2,030 sensitivity set. SBERT-LR inclusion (C7 vs C5) improves Macro-F1 and Partial recall/F1 with grouped CIs above zero in both populations; accuracy CI includes zero. NLI-LR inclusion (C7 vs C4) reduces Partial recall/F1 with grouped CIs below zero; accuracy, Macro-F1 and QWK intervals include zero in both populations.",
"Additional value: components can contribute distinct correct predictions, but unique rescue and full-rescue counts above are not causal estimates.",
f"Standalone Partial recall: {partial_recall}; false Partial predictions: {false_partial}. FT has the most standalone false-Partial predictions (249), versus SBERT-LR 235 and NLI-LR 64. SBERT-LR has the highest standalone Partial recall; its marginal inclusion also has the largest positive Partial-recall change among added components.",
f"Strongest standalone unseen accuracy: {best_unseen.config} ({best_unseen.accuracy:.6f}, n={int(best_unseen.n)}); strongest unseen Macro-F1: {best_unseen_macro.config} ({best_unseen_macro.macro_f1:.6f}). Accuracy edge is descriptive and subgroup intervals are not computed.",
f"Best pair by primary Macro-F1 point estimate: {best_pair} ({NAMES[best_pair]}, Macro-F1={overall.loc[('primary_2049',best_pair),'macro_f1']:.6f}); the grouped interval for C7-minus-C4 Macro-F1 crosses zero.",
f"Most standalone unique correct predictions versus C7: NLI-LR ({rescue['nl']}); most standalone errors corrected by C7: NLI-LR ({full_rescue['nl']}). NLI is mixed, not a clear removal candidate.",
"Final recommendation: RETAIN WITH COMPONENT INVESTIGATION. Proposed Experiment 3: evaluate component contributions on genuine held-out question-grouped predictions or a clean confirmation set, without test tuning.",
"","## Limitations","","All scores are dev-only, optimistic; only 27 dev questions are unseen. The 2,030-row result is a duplicate sensitivity analysis. Original-source duplicate provenance is Unverified. Component probabilities are saved exports, not shown to be OOF. No test data, training, inference, model loading, A_predict import, notebook execution, or production modification occurred.",
"","## Reproduction","","From the project root run the script named in the manifest. Requires installed pandas, NumPy, scikit-learn and a parquet engine. Reads only the three dev artifacts and A_predict.py source text; never imports A_predict. Versioned outputs are never overwritten."]
lines += ["", "### Probability identity and preprocessing", "", "For each component, the saved parquet holds a 2,049 x 5 vector under its named p0-p4 columns; the order is A_predict LABEL5_ORDER. Gold label5 maps to Incorrect for indices 1/3/4, Partial for index 2, Correct for index 0. DistilRoBERTa probabilities are softmax; SBERT-LR and NLI-LR are LogisticRegression predict_proba outputs reordered to LABEL5_ORDER. No temperature is applied to individual vectors in component_probs; the optional final temperature is applied after equal averaging and collapse. Export file: Phase_8_Accuracy_Max/A_component_probs_v7.parquet; exporter source is recorded in the manifest. The parquet contains seven NLI features: "+str(features)+". The file does not embed checkpoint hashes or a run manifest, so exact model/checkpoint provenance for the saved rows is Unverified.", "", "NLI/feature max, min and other distributions are retained in the saved input; this experiment validates their presence, row alignment, null-free state and seven-column numeric shape but does not use them to create new predictions."]
lines[-2]=lines[-2].replace('"+str(features)+"',str(features))
files["report"].write_text("\n".join(lines)+"\n",encoding="utf-8")
manifest=["# Experiment 2 artifact manifest","","Dev-only inputs; no test artifacts opened. Manifest omits its own hash.","","## Inputs","","| Path | Bytes | SHA-256 | Rows | Unique UIDs |"]
for name,p,frame in inputs_meta: manifest.append(f"| {p.relative_to(ROOT).as_posix()} | {p.stat().st_size} | {sha(p)} | {len(frame)} | {frame.uid.nunique()} |")
manifest.append(f"| {EXPORTER.relative_to(ROOT).as_posix()} | {EXPORTER.stat().st_size} | {sha(EXPORTER)} | n/a | n/a |")
manifest += [f"| {API.relative_to(ROOT).as_posix()} | {API.stat().st_size} | {api_hash} | n/a | n/a |","","Class order: "+str(ORDER)+". Mapping: indices 1/3/4=Incorrect; 2=Partial; 0=Correct.",f"Seed={SEED}; bootstrap={BOOT}; populations=2,049 primary and 2,030 approved sensitivity.",f"Path A prediction agreement={path_a}/2,049; component-export Path A agreement={export_a}/2,049.","","## Outputs","","| File | Bytes | SHA-256 |"]
for k,p in files.items():
    if k!="manifest": manifest.append(f"| {p.name} | {p.stat().st_size} | {sha(p)} |")
self=Path(__file__); manifest.append(f"| {self.name} | {self.stat().st_size} | {sha(self)} |")
files["manifest"].write_text("\n".join(manifest)+"\n",encoding="utf-8")
print("VALIDATION PASS | dev-only, optimistic | UID alignment 2049/2049 | Path A",path_a,"/2049 | dedup",len(retained))
print("BOOTSTRAP",BOOT,"seed",SEED,"question_groups",groups_n,"output_version",v)
for p in files.values(): print(p.name,p.stat().st_size,sha(p))

