# Stage 1 Colab run sheet

**Drafted — NOT RUN. Stage 1 is unapproved.** Wait for Phase 3 completion,
explicit Stage 1 approval, and the output-path/gate decisions in E4. A single
seed is only an exploratory pilot; it cannot satisfy the preregistered
three-seed gates. Expected T4 runtime is **Unverified**.

## Blocker before any training command

The current scripts hard-code `OUT` to
`/content/drive/MyDrive/Project_S_QA_Evidence/Phase_8_Accuracy_Max`
(`x1_deberta_train.py:3`; `x1_gate_check.py:3`). This conflicts with the
required `/content/phase8_tmp` output location. Do not run the uploaded
originals. After approval, use disposable `/content` copies and redirect only
their `OUT` setting to `/content/phase8_tmp`; do not modify the project files.
The trainer also reads filtered train/dev rows from
`project_s_qa/processed/sra_unified_splits_v1.parquet` (`x1_deberta_train.py:3,7`).
That split was not opened in this preparation.

## Ordered Colab steps (future, gated)

1. Select a T4 runtime. Mount Drive in a notebook Python cell:

   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

2. Upload `x1_deberta_train.py` and `x1_gate_check.py` using Colab's Files
   panel. Confirm the source split, baseline dev probabilities, and required
   checkpoint/cache are available. Do not inspect or use test rows.
3. Create `/content/phase8_tmp` and record frozen-input hashes. This `%%bash`
   cell stops at the first error:

   ```bash
   %%bash
   set -euo pipefail
   ROOT=/content/drive/MyDrive/project_s_qa
   mkdir -p /content/phase8_tmp
   cd "$ROOT"
   sha256sum reports_v2/A_predict.py reports_v2/A_demo_reference_outputs_v2.json reports_v2/A_abstain_policy_v2.json interim/combiner_v1.joblib interim/pooled_lr_v2.joblib > /content/phase8_tmp/frozen_before.sha256
   find interim/ft_distilroberta_v1 -type f -print0 | sort -z | xargs -0 sha256sum >> /content/phase8_tmp/frozen_before.sha256
   if [[ -f reports_v2/A_deployed_dev_probs_v2.parquet ]]; then BASE=reports_v2/A_deployed_dev_probs_v2.parquet; elif [[ -f A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet ]]; then BASE=A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet; else echo 'Missing pooled dev probabilities'; exit 1; fi
   sha256sum "$BASE" >> /content/phase8_tmp/frozen_before.sha256
   sha256sum /content/x1_deberta_train.py /content/x1_gate_check.py > /content/phase8_tmp/scripts_before.sha256
   ```

   If any listed file is absent, stop; do not weaken the checks. Confirm the
   baseline parquet at one of the paths in `x1_gate_check.py:3` before run.
   The existing training source filters to `train`, `dev_ua`, and `dev_uq`
   rows (`x1_deberta_train.py:7`); do not change that filter or read test.
4. After Stage 1 approval, create disposable copies in `/content/phase8_tmp`
   by changing only the output directory in each copy. This `%%bash` cell
   stops if a destination exists or the path replacement fails:

   ```bash
   %%bash
   set -euo pipefail
   test ! -e /content/phase8_tmp/x1_deberta_train.py
   test ! -e /content/phase8_tmp/x1_gate_check.py
   sed "s|OUT=Path('/content/drive/MyDrive/Project_S_QA_Evidence/Phase_8_Accuracy_Max')|OUT=Path('/content/phase8_tmp')|" /content/x1_deberta_train.py > /content/phase8_tmp/x1_deberta_train.py
   sed "s|OUT=Path('/content/drive/MyDrive/Project_S_QA_Evidence/Phase_8_Accuracy_Max')|OUT=Path('/content/phase8_tmp')|" /content/x1_gate_check.py > /content/phase8_tmp/x1_gate_check.py
   grep -Fq "OUT=Path('/content/phase8_tmp')" /content/phase8_tmp/x1_deberta_train.py
   grep -Fq "OUT=Path('/content/phase8_tmp')" /content/phase8_tmp/x1_gate_check.py
   test ! -e /content/phase8_tmp/model
   test ! -e /content/phase8_tmp/trainer
   test ! -e /content/phase8_tmp/A_x1_deberta_dev_probs.csv
   test ! -e /content/phase8_tmp/A_x1_deberta_neg_probs.csv
   test ! -e /content/phase8_tmp/A_x1_deberta_run.json
   sha256sum /content/phase8_tmp/x1_deberta_train.py /content/phase8_tmp/x1_gate_check.py > /content/phase8_tmp/run_copies.sha256
   ```

   Then run each command in its own `%%bash` cell, with
   `set -euo pipefail`. **These commands remain blocked until approval:**

   ```bash
   %%bash
   set -euo pipefail
   HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python /content/phase8_tmp/x1_deberta_train.py
   ```

   ```bash
   %%bash
   set -euo pipefail
   HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python /content/phase8_tmp/x1_gate_check.py
   ```

   Stop on the first error. Do not run later cells or tune on test data.
   The train script uses seed 20261106 and `dev_uq` for checkpoint selection;
   one seed is exploratory only.
5. Recheck frozen-input hashes and script copies. This `%%bash` cell stops if
   any protected input changed:

   ```bash
   %%bash
   set -euo pipefail
   ROOT=/content/drive/MyDrive/project_s_qa
   cd "$ROOT"
   sha256sum -c /content/phase8_tmp/frozen_before.sha256
   sha256sum -c /content/phase8_tmp/scripts_before.sha256
   sha256sum -c /content/phase8_tmp/run_copies.sha256
   ```

   If a hash check fails, stop and report it. Save the console output. No
   output belongs in Drive `reports_v2`.
6. Download only the candidate gate inputs from `/content/phase8_tmp`:
   `A_x1_deberta_dev_probs.csv`, `A_x1_deberta_neg_probs.csv`, and
   `A_x1_deberta_run.json`. Keep `model/` and `trainer/` in the Colab temp
   folder pending an approved retention decision. Expected outputs and
   availability are Unverified until a run.
7. After downloading those three files to Windows Downloads, copy them into
   Phase 8 without overwriting existing files:

   ```powershell
   $src = Join-Path $env:USERPROFILE 'Downloads'
   $dst = 'C:\Users\Jigar\OneDrive\Desktop\Project 4\Project_S_QA_Evidence\Phase_8_Accuracy_Max'
   $names = @('A_x1_deberta_dev_probs.csv','A_x1_deberta_neg_probs.csv','A_x1_deberta_run.json')
   foreach ($name in $names) {
       $to = Join-Path $dst $name
       if (Test-Path -LiteralPath $to) { throw "Refusing to overwrite $to" }
       Copy-Item -LiteralPath (Join-Path $src $name) -Destination $to -ErrorAction Stop
   }
   ```

This run sheet is not authorization to train. Phase 3 remains PARTIAL, Stage 1
needs explicit approval, and current gate code does not implement the complete
three-seed preregistration.
