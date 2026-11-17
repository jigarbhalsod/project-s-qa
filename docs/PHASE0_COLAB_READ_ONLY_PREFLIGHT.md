# Project S — Colab Read-Only Preflight

**Status: Drafted; live verification blocked until Jigar runs this manually.**
This does not select a notebook or configuration. Do not treat the candidate
hashes below as approved deployment values.

## Before running

1. Jigar must select the notebook, runtime root, and JSON/policy option in the
   decision register. The defaults below describe a candidate snapshot only.
2. Open the selected notebook in the authorized Colab account and select the
   intended runtime. Do not run notebook cells.
3. Run the first line only if you authorize mounting your Drive. Colab's
   mount is not an OS-enforced read-only mount; this diagnostic itself issues
   read operations only and performs no writes.
4. Do not run this if the selected root or approved hashes differ from the
   candidate constants. Update the constants only after approving the exact
   manifest.

## Copy-paste preflight

The diagnostic reads metadata, hashes files, parses JSON, and inspects cached
model revision directory names. It does not read notebook outputs, import
`A_predict`, load model weights, run inference, access test artifacts, change
environment variables, create files, install packages, or download anything.
It prints paths and hashes only; do not paste secrets or credentials.

```python
from google.colab import drive
drive.mount('/content/drive')  # Run only after you authorize the mount.

import hashlib, importlib.metadata as md, json, os, platform, re, sys
from pathlib import Path

# Candidate manifest from the 7 Nov local snapshot. NOT YET APPROVED.
ROOT = Path('/content/drive/MyDrive/project_s_qa')
NOTEBOOK = ROOT / 'notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb'
APPROVED_MANIFEST = False  # Jigar sets True only after approving exact hashes.
EXPECTED = {
    'A_predict.py': 'CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053',
    'A_demo_reference_outputs_v2.json': 'EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9',
    'A_abstain_policy_v2.json': 'B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B',
    'config.json': '8C906F8EB778D92EC953D68975285AF55C12092BED2C7151F6B42034E3919416',
    'model.safetensors': '671E70ACF931C6DEDD28EBFF73BACCFA3ACF3B07DBA13CB3EB15FC39F04761FD',
    'tokenizer_config.json': 'AA6A8A3F069D2D98C09444EE3F9671D64C29CE647473DCCD78169B10C490D359',
    'tokenizer.json': 'EF73668535466D56FD3571306556BCBF3C3D16FD93CDF5E4D38970290C89165B',
    'combiner_v1.joblib': '057E3DECD03ACA99C804D4408CAA6A5832B44F0DC18DE67CFD6061E5C966E875',
    'pooled_lr_v2.joblib': '216493152A1B7AE2143F0FC60CE2EED6FFC735F40676E308455225B1B55AA96F',
    'cbse_demo_questions_v1.csv': '78852EB405819DE017FA99A3839CC47912ED1BD40ACD0BD0A3966BE4B6987E3B',
    'A_negation_paraphrase_v2.csv': 'A4B7F45A12F1A4DE8C256EE2634DE2FC10F06C2B664FF74EB500B2D730E5A5AB',
    'Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb': 'SET_AFTER_NOTEBOOK_APPROVAL',
}
REQUIRED = {
    'notebook': NOTEBOOK,
    'scorer': ROOT / 'reports_v2/A_predict.py',
    'reference_json': ROOT / 'reports_v2/A_demo_reference_outputs_v2.json',
    'policy': ROOT / 'reports_v2/A_abstain_policy_v2.json',
    'demo_csv': ROOT / 'processed/cbse_demo_questions_v1.csv',
    'negation_csv': ROOT / 'reports_v2/A_negation_paraphrase_v2.csv',
    'ft_config': ROOT / 'interim/ft_distilroberta_v1/config.json',
    'ft_weights': ROOT / 'interim/ft_distilroberta_v1/model.safetensors',
    'ft_tokenizer_config': ROOT / 'interim/ft_distilroberta_v1/tokenizer_config.json',
    'ft_tokenizer': ROOT / 'interim/ft_distilroberta_v1/tokenizer.json',
    'combiner': ROOT / 'interim/combiner_v1.joblib',
    'pooled_lr': ROOT / 'interim/pooled_lr_v2.joblib',
}
checks = []
def report(name, ok, detail):
    checks.append(bool(ok))
    print(f'{"PASS" if ok else "FAIL"} | {name} | {detail}')
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest().upper()

report('approved manifest', APPROVED_MANIFEST,
       'candidate hashes are not deployment approval')
report('candidate root exists', ROOT.is_dir(), str(ROOT))
effective_root = Path(os.environ.get('PROJECT_S_ROOT', '/content/drive/MyDrive/project_s_qa'))
report('PROJECT_S_ROOT agrees', effective_root.resolve() == ROOT.resolve(),
       f'env={os.environ.get("PROJECT_S_ROOT", "<unset; scorer default applies>")} root={ROOT}')
report('notebook root declaration agrees', NOTEBOOK_ROOT_IN_SOURCE == str(ROOT),
       f'declared={NOTEBOOK_ROOT_IN_SOURCE} root={ROOT}')
for name, path in REQUIRED.items():
    exists = path.is_file()
    digest = sha(path) if exists else 'MISSING'
    expected = EXPECTED.get(path.name)
    ok = exists and expected is not None and digest == expected
    report(name, ok, f'{path} | sha256={digest} | expected={expected or "UNSET"}')
report('interim directory', (ROOT / 'interim').is_dir(), str(ROOT / 'interim'))
report('processed directory', (ROOT / 'processed').is_dir(), str(ROOT / 'processed'))

# Parse notebook SOURCE fields only; never access the outputs field.
try:
    nb = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
    sources = []
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', '')
            sources.append(''.join(source) if isinstance(source, list) else source)
    relevant = '\n'.join(line for src in sources for line in src.splitlines()
                          if 'sys.path' in line or 'PROJECT_S_ROOT' in line or 'reports_v2' in line)
    paths = re.findall(r'["\'](/content/drive/[^"\']+)', relevant)
    roots = sorted({p[:-len('/reports_v2')] if p.endswith('/reports_v2') else p
                    for p in paths})
    agrees = str(ROOT) in roots and all(p == str(ROOT) for p in roots)
    report('notebook source root agrees', agrees,
           f'notebook={NOTEBOOK.name} sha256={sha(NOTEBOOK) if NOTEBOOK.is_file() else "MISSING"} roots={roots or "NOT FOUND"}')
except Exception as e:
    report('notebook source root agrees', False, type(e).__name__ + ': ' + str(e))

json_path = REQUIRED['reference_json']
policy_path = REQUIRED['policy']
scorer_path = REQUIRED['scorer']
try:
    cfg = json.loads(json_path.read_text(encoding='utf-8'))
    policy = json.loads(policy_path.read_text(encoding='utf-8'))
    report('JSON scorer mode', cfg.get('scorer_mode') == 'pooled', str(cfg.get('scorer_mode')))
    report('JSON scorer hash field', cfg.get('a_predict_sha256', '').upper() == sha(scorer_path),
           f'stored={cfg.get("a_predict_sha256")} actual={sha(scorer_path)}')
    report('JSON policy hash field', cfg.get('policy_sha256', '').upper() == sha(policy_path),
           f'stored={cfg.get("policy_sha256")} actual={sha(policy_path)}')
    report('effective policy', policy.get('scorer_mode') == 'pooled' and
           policy.get('confidence_threshold') == 0.64 and
           policy.get('temperature') == 1.0000000000000004 and
           policy.get('use_contradiction_flag') is False,
           f'mode={policy.get("scorer_mode")} temperature={policy.get("temperature")} threshold={policy.get("confidence_threshold")} contradiction={policy.get("use_contradiction_flag")}')
except Exception as e:
    report('JSON/policy parse', False, type(e).__name__ + ': ' + str(e))

print('ENVIRONMENT | python=' + sys.version.split()[0] + ' | platform=' + platform.platform())
for package in ('torch','transformers','pandas','numpy','joblib','sentence-transformers','gradio','scikit-learn','huggingface-hub'):
    try:
        version = md.version(package)
        report('package ' + package, True, version)
    except md.PackageNotFoundError:
        report('package ' + package, False, 'MISSING')

models = {
    'NLI': 'cross-encoder/nli-deberta-v3-base',
    'SBERT': 'sentence-transformers/all-MiniLM-L6-v2',
    'Whisper': 'openai/whisper-small',
}
cache = Path(os.environ.get('HF_HOME', Path.home() / '.cache/huggingface')) / 'hub'
for label, model_id in models.items():
    model_dir = cache / ('models--' + model_id.replace('/', '--'))
    snaps = sorted(p.name for p in (model_dir / 'snapshots').glob('*') if p.is_dir()) if (model_dir / 'snapshots').is_dir() else []
    report('model cache ' + label, bool(snaps),
           f'id={model_id} cache_dir={model_dir.exists()} snapshots={snaps or "NONE"}')
    print(f'MODEL_CACHE | {label} | id={model_id} | cache_dir={model_dir.exists()} | snapshots={snaps or "NONE"} | revision approval=UNVERIFIED')

print('SUMMARY | ' + ('PASS' if all(checks) else 'FAIL / BLOCKED') +
      f' | passed={sum(checks)} total={len(checks)} | no files written; no model loaded')
```

## Reading the result

Every PASS is local to the mounted runtime at the time of execution. Any
missing file, hash mismatch, `PROJECT_S_ROOT` divergence, absent model cache,
or unapproved manifest is a blocker. `APPROVED_MANIFEST` intentionally starts
false. Change it only after Jigar has approved the exact notebook/configuration
and the notebook hash placeholder has been replaced with that approved
manifest. The cache list
is metadata only; it does not pin or prove that a model can load. Return the
entire printed output and the selected notebook path/hash. Do not run Blocks
59–62 as part of this preflight.
