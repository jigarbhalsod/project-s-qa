# Phase 0 Verification Report

## Scope and stop point

| Task | Status | Finding |
|---|---|---|
| 1. Backup | Verified | Complete local copy created at `C:\Users\Jigar\OneDrive\Desktop\Project 4\project_s_qa_backup_20261106_1957`. Source 67 files; backup 67 files; 0 missing, extra, size, or SHA-256 mismatches. Directory paths: 7 source and 7 backup; 0 missing/extra. |
| 2. Staged v2 pair | Verified | Local staged files and pooled/hash checks are listed below. |
| 3. Staged vs current copies | BLOCKED | A_predict.py matches; the JSON differs. `policy_sha256` differs. Stopped as instructed for Jigar's decision. |
| 4. Notebook candidate | BLOCKED | Not inspected after Task 3 conflict. |
| 5. T3, backup chain, README | BLOCKED | Not inspected after Task 3 conflict. No output fields were examined. |
| 6. Block safety classification | BLOCKED | Notebook source was not inspected after Task 3 conflict. |

## Task 2: staged pair

| File | Local path | Size | LastWriteTime | SHA-256 | Result |
|---|---|---:|---|---|---|
| A_predict.py | `C:\Users\Jigar\OneDrive\Desktop\Project 4\project_s_qa\reports_v2\A_predict.py` | 7626 | 2026-11-06 00:02:08.3777872 +05:30 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | Verified |
| A_demo_reference_outputs_v2.json | `C:\Users\Jigar\OneDrive\Desktop\Project 4\project_s_qa\reports_v2\A_demo_reference_outputs_v2.json` | 16474 | 2026-11-06 00:02:08.3959188 +05:30 | c99b7d84d000046c9629708d5ee440d5a20ab28fd298f63708e2e8c13f89dc92 | Verified |

| Check | Status | Evidence |
|---|---|---|
| scorer_mode | Verified | `pooled` |
| JSON stored A_predict hash | Verified | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053; equals staged scorer hash |

## Task 3: local staged vs packaged current pair

| File | Staged SHA-256 | Current local SHA-256 | Result |
|---|---|---|---|
| A_predict.py | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | Match |
| A_demo_reference_outputs_v2.json | c99b7d84d000046c9629708d5ee440d5a20ab28fd298f63708e2e8c13f89dc92 | ea5288e9f12b25d28a66f36ec38d48b08c65e19452bf3b5efa17eed2be20aeb9 | DIFFER |

| JSON field | Staged value | Current packaged value |
|---|---|---|
| a_predict_sha256 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 |
| policy_sha256 | babf76f460d2a6516d9ef11d317f69ceddb0958dd67a2ce06d3b67496163ad25 | b6548edeb682eabd2ba6b74d9b9b67bff293c1fea9c3cb6345e0a7ebf7e9ef9b |

**BLOCKED:** The local current JSON conflicts with the staged JSON. No file was overwritten or reconciled. Await Jigar's decision before continuing Tasks 4-6.

## Drive status

**Unverified:** No local Google Drive mount was found (`G:\My Drive` and checked user-profile paths absent; visible filesystem drives C, D, E). Live Drive status and cloud synchronization are UNVERIFIED. The inspection compared local copies only.

## Done-when check

| Check | Status |
|---|---|
| Backup exists and verified | PASS |
| Notebook candidate identified | BLOCKED; stopped at JSON conflict |
| Staged scorer/reference pair identified | PASS locally; current JSON conflict remains |
| Hash and pooled configuration checks recorded | PASS for staged pair |
| T3 and safety classification | BLOCKED; not inspected |

## Remaining blockers / open decision

- **BLOCKED:** Decide which local reference JSON is authoritative, given the different `policy_sha256` values.
- **Unverified:** Live Google Drive state and synchronization.
- **BLOCKED:** Notebook candidate comparison, T3, backup-chain/README audit, and block-safety classification are pending the JSON decision.

## Per-file backup SHA-256 manifest

| Relative path | Source bytes | Source SHA-256 | Backup bytes | Backup SHA-256 |
|---|---:|---|---:|---|
| A_submission_v2.zip | 369541 | 0abb38aaba65194cc4fbd495a441861afce7d2ab2ee3659e83cd51703d93f09f | 369541 | 0abb38aaba65194cc4fbd495a441861afce7d2ab2ee3659e83cd51703d93f09f |
| A_submission_v2\demo\A_predict.py | 7626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | 7626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 |
| A_submission_v2\demo\demo_outputs_PREVIOUS.json | 1671 | e0b0ccdee58e5f8d2e3b0c056496cfdc37a726aa3168a5cc5ea932481fde881e | 1671 | e0b0ccdee58e5f8d2e3b0c056496cfdc37a726aa3168a5cc5ea932481fde881e |
| A_submission_v2\demo\demo_outputs.json | 1672 | cb8aed9894aec3ef435e0538e30d2a4a9bf3e029a07a4364c260239bd85cf81b | 1672 | cb8aed9894aec3ef435e0538e30d2a4a9bf3e029a07a4364c260239bd85cf81b |
| A_submission_v2\demo\example_inputs.json | 3940 | 4adcfd39eb78e7cb667b9a850b80ebc5da58029d099deb8b213b7dfe2d37b3d5 | 3940 | 4adcfd39eb78e7cb667b9a850b80ebc5da58029d099deb8b213b7dfe2d37b3d5 |
| A_submission_v2\reports_v2\A_abstain_policy_v2.json | 784 | b6548edeb682eabd2ba6b74d9b9b67bff293c1fea9c3cb6345e0a7ebf7e9ef9b | 784 | b6548edeb682eabd2ba6b74d9b9b67bff293c1fea9c3cb6345e0a7ebf7e9ef9b |
| A_submission_v2\reports_v2\A_block56_withdrawn_v2.json | 402 | fc05cb978e591acdadf0ba7e91f1d7e788dc3acf8a5edf55b0f97a70abc9265a | 402 | fc05cb978e591acdadf0ba7e91f1d7e788dc3acf8a5edf55b0f97a70abc9265a |
| A_submission_v2\reports_v2\A_bootstrap_ci_v2.csv | 4987 | 0cc527649a78fe7f471485aa2982bc88343c70a97b3591b65ab8eceef4a14e96 | 4987 | 0cc527649a78fe7f471485aa2982bc88343c70a97b3591b65ab8eceef4a14e96 |
| A_submission_v2\reports_v2\A_calibration_dev_v2.csv | 924 | 090883b4acabf1d2bb1238864e6ef4a5426d56b100737760d8c5895d0c6aa3d2 | 924 | 090883b4acabf1d2bb1238864e6ef4a5426d56b100737760d8c5895d0c6aa3d2 |
| A_submission_v2\reports_v2\A_calibration_params_v2.json | 892 | 9cd65066da32d2954b2b0a3c91338b771b6badf6d1cd9dca2e363dec17934f7f | 892 | 9cd65066da32d2954b2b0a3c91338b771b6badf6d1cd9dca2e363dec17934f7f |
| A_submission_v2\reports_v2\A_cluster_breakdown_v2.csv | 1397 | 46da77b76a71c02ecddc30d2fa57451a6297e209ac6f93c30d7cfa2f50646fb1 | 1397 | 46da77b76a71c02ecddc30d2fa57451a6297e209ac6f93c30d7cfa2f50646fb1 |
| A_submission_v2\reports_v2\A_component_check_v2.json | 1423 | 0f91c8644349df4e93f10904b3c0c7bc87e25a70f819ee9a09061341a6d5dc51 | 1423 | 0f91c8644349df4e93f10904b3c0c7bc87e25a70f819ee9a09061341a6d5dc51 |
| A_submission_v2\reports_v2\A_concept_evidence_demo_v2.csv | 2006 | 78e609afb8e795005d4e44f0ab0ae87517ea37216dd538030c87a3149b46697f | 2006 | 78e609afb8e795005d4e44f0ab0ae87517ea37216dd538030c87a3149b46697f |
| A_submission_v2\reports_v2\A_concepts_review_sheet_v2.csv | 13050 | e1e4dcb91e86ef802ea9661bf48399ed4ba6464adf1b74efb4f05295746fc60f | 13050 | e1e4dcb91e86ef802ea9661bf48399ed4ba6464adf1b74efb4f05295746fc60f |
| A_submission_v2\reports_v2\A_dataset_default_v2.json | 1006 | 57f172d6c9d9cb2318c060a9cdc614a622c1e8d464e638763a1dd36312e48e3f | 1006 | 57f172d6c9d9cb2318c060a9cdc614a622c1e8d464e638763a1dd36312e48e3f |
| A_submission_v2\reports_v2\A_dataset_option_dev_v2.csv | 959 | 8faa3c081c862354a51e1b69481f2309c6ec8c98f6e7491777d7c24eb3f4679b | 959 | 8faa3c081c862354a51e1b69481f2309c6ec8c98f6e7491777d7c24eb3f4679b |
| A_submission_v2\reports_v2\A_demo_cases_summary_v2.csv | 1820 | 4c3df2ccf6162804ae1722d8f990f00d93e6e50e4933dfb0182f4ea33429fa32 | 1820 | 4c3df2ccf6162804ae1722d8f990f00d93e6e50e4933dfb0182f4ea33429fa32 |
| A_submission_v2\reports_v2\A_demo_five_cases_v2.csv | 437 | d1ee304787b047007bab0466edb5da4cfdadf84fadeffbccf0f69b7dae63798b | 437 | d1ee304787b047007bab0466edb5da4cfdadf84fadeffbccf0f69b7dae63798b |
| A_submission_v2\reports_v2\A_demo_parity_v2.csv | 1006 | c8c57587d97026cf3c6d2f0c531e26c08a3d364a689a364c78a5a456e2d75e3d | 1006 | c8c57587d97026cf3c6d2f0c531e26c08a3d364a689a364c78a5a456e2d75e3d |
| A_submission_v2\reports_v2\A_demo_parity_v2.json | 113 | 99bf38b28e9692c8e1e1f1a6b7f81818fbef5063cd9acd58574b8c6c5e4ce828 | 113 | 99bf38b28e9692c8e1e1f1a6b7f81818fbef5063cd9acd58574b8c6c5e4ce828 |
| A_submission_v2\reports_v2\A_demo_reference_outputs_v2.json | 16474 | ea5288e9f12b25d28a66f36ec38d48b08c65e19452bf3b5efa17eed2be20aeb9 | 16474 | ea5288e9f12b25d28a66f36ec38d48b08c65e19452bf3b5efa17eed2be20aeb9 |
| A_submission_v2\reports_v2\A_deployed_dev_probs_v2.parquet | 131382 | 2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e | 131382 | 2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e |
| A_submission_v2\reports_v2\A_deployed_metrics_ci_v2.csv | 627 | 31e49c3c02136543294972302db3fc453ba39f35ac346bb8a987223ad8a45126 | 627 | 31e49c3c02136543294972302db3fc453ba39f35ac346bb8a987223ad8a45126 |
| A_submission_v2\reports_v2\A_deployed_scorer_v2.json | 222 | 5bdfe4bba65ea6b81d1442dc71a1843fcf6367fe80af1d5ae7ec49d8808f53bc | 222 | 5bdfe4bba65ea6b81d1442dc71a1843fcf6367fe80af1d5ae7ec49d8808f53bc |
| A_submission_v2\reports_v2\A_error_analysis_dev_v2.csv | 219 | b5c91e9e03ecc37f1db46863f18a3d704707a2d55efe6f6643cabadf653aa8b6 | 219 | b5c91e9e03ecc37f1db46863f18a3d704707a2d55efe6f6643cabadf653aa8b6 |
| A_submission_v2\reports_v2\A_error_hard_questions_dev_v2.csv | 1507 | 40c1f56fc38dacaa97bed3b5233591db726f27d45fbff9cd567beb22d7c2eb35 | 1507 | 40c1f56fc38dacaa97bed3b5233591db726f27d45fbff9cd567beb22d7c2eb35 |
| A_submission_v2\reports_v2\A_errors_sample_dev_v2.csv | 6925 | 2a19431b983d131a92dfe1b0708c44bb433db6bf04ae3b8cb265a0478cc21496 | 6925 | 2a19431b983d131a92dfe1b0708c44bb433db6bf04ae3b8cb265a0478cc21496 |
| A_submission_v2\reports_v2\A_final_tables_v2.md | 4675 | b5949f7aaec5ef4dc9924d1dc72a10c464b4a44f2d3e15aab3ad3c3632c2a304 | 4675 | b5949f7aaec5ef4dc9924d1dc72a10c464b4a44f2d3e15aab3ad3c3632c2a304 |
| A_submission_v2\reports_v2\A_freeze_resolution_v2.json | 462 | 724f54cfea5f47bd9ec56baea335b4301a3fcd74420b26e1adf4b9753db3956c | 462 | 724f54cfea5f47bd9ec56baea335b4301a3fcd74420b26e1adf4b9753db3956c |
| A_submission_v2\reports_v2\A_handtests_v2.csv | 548 | f4bb8c364221392448cc4ed4c0be9e271a1526403c4419d37bc024f713db0500 | 548 | f4bb8c364221392448cc4ed4c0be9e271a1526403c4419d37bc024f713db0500 |
| A_submission_v2\reports_v2\A_learned_deferral_cv_v2.csv | 159 | fd2754df25bf49f7443542d864a5677d748b4089bb1c726b347638fe56248c5d | 159 | fd2754df25bf49f7443542d864a5677d748b4089bb1c726b347638fe56248c5d |
| A_submission_v2\reports_v2\A_learned_deferral_verdict_v2.json | 593 | 816ba06cb8ca3b537553bdccf880ea6ed98ddcbaf13c9514157ea2e56e200e19 | 593 | 816ba06cb8ca3b537553bdccf880ea6ed98ddcbaf13c9514157ea2e56e200e19 |
| A_submission_v2\reports_v2\A_ml_only_audit_v2.json | 2273 | 367f6992d7b7cd016e29c7ccacfdf252eda3af3401d244d7a745b54d2f24a94c | 2273 | 367f6992d7b7cd016e29c7ccacfdf252eda3af3401d244d7a745b54d2f24a94c |
| A_submission_v2\reports_v2\A_model_comparison_dev_v2.csv | 9136 | ea236f31c082ef2ad35578216f69f7cc84952601a1a6f4e856c6c26235c582f4 | 9136 | ea236f31c082ef2ad35578216f69f7cc84952601a1a6f4e856c6c26235c582f4 |
| A_submission_v2\reports_v2\A_negation_paraphrase_v2.csv | 3657 | a4b7f45a12f1a4de8c256ee2634de2fc10f06c2b664ff74eb500b2d730e5a5ab | 3657 | a4b7f45a12f1a4de8c256ee2634de2fc10f06c2b664ff74eb500b2d730e5a5ab |
| A_submission_v2\reports_v2\A_parity_v2.csv | 2282 | 6697d6cdbee9234fa23c888e9557e2d9a678db9278aacc57ab62ea413130d3fd | 2282 | 6697d6cdbee9234fa23c888e9557e2d9a678db9278aacc57ab62ea413130d3fd |
| A_submission_v2\reports_v2\A_predict_contract_v2.json | 1217 | 1a2b21a94eba50f70f390995a038a8329c4d6d81ab58775e26083329a97d837c | 1217 | 1a2b21a94eba50f70f390995a038a8329c4d6d81ab58775e26083329a97d837c |
| A_submission_v2\reports_v2\A_predict.py | 7626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | 7626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 |
| A_submission_v2\reports_v2\A_question_clusters_v2.csv | 2675 | 6c059f26d74012e72abda1534bdd5e9ecfed3d81dc7a83a90ad1056e85794bb0 | 2675 | 6c059f26d74012e72abda1534bdd5e9ecfed3d81dc7a83a90ad1056e85794bb0 |
| A_submission_v2\reports_v2\A_question_descriptors_v2.csv | 64634 | cedbb8001e512ff6341c157def59bb9f2157b429fa769f2ec0260c324ff3eb30 | 64634 | cedbb8001e512ff6341c157def59bb9f2157b429fa769f2ec0260c324ff3eb30 |
| A_submission_v2\reports_v2\A_risk_coverage_v2.csv | 532 | 69e6956e1938c9900a55dfa278f41d5bba11519e430ed02bf902e46a28c6f1e6 | 532 | 69e6956e1938c9900a55dfa278f41d5bba11519e430ed02bf902e46a28c6f1e6 |
| A_submission_v2\reports_v2\A_rubrics_v2.json | 428317 | aa3549f46f2e9385829f3d870df05c5439eb589c3649166802b89ce45ecc6e70 | 428317 | aa3549f46f2e9385829f3d870df05c5439eb589c3649166802b89ce45ecc6e70 |
| A_submission_v2\reports_v2\A_run_manifest_v2.json | 3170 | 28656c16d68773d0fdd8f1c3f67b264b43667ad26a36f99c62cb839da2a605b3 | 3170 | 28656c16d68773d0fdd8f1c3f67b264b43667ad26a36f99c62cb839da2a605b3 |
| A_submission_v2\reports_v2\A_seed_summary_v2.json | 154 | d21dd1bd5a933b65aa1517ea565bacb3cd2230cf7cc4723ee66b36c858813487 | 154 | d21dd1bd5a933b65aa1517ea565bacb3cd2230cf7cc4723ee66b36c858813487 |
| A_submission_v2\reports_v2\A_stats.py | 1215 | 0e5bbe090ae3707f7884bb9cf4276cd1dfa1a784602e139fd9586e724e99157b | 1215 | 0e5bbe090ae3707f7884bb9cf4276cd1dfa1a784602e139fd9586e724e99157b |
| A_submission_v2\reports_v2\A_submission_manifest_v2.json | 6080 | a52b7902da980546bd70c0f524e97ca11f958ff40feeb773933fac8f509911cf | 6080 | a52b7902da980546bd70c0f524e97ca11f958ff40feeb773933fac8f509911cf |
| A_submission_v2\reports_v2\A_table_dev_ci_v2.csv | 268 | e9cb178fb8a20055a9dba34c57805e9c5441e1ba95f6b7c94556115724b2ef2c | 268 | e9cb178fb8a20055a9dba34c57805e9c5441e1ba95f6b7c94556115724b2ef2c |
| A_submission_v2\reports_v2\A_table_paired_v2.csv | 1916 | 58d3380e222f38f526c55526eff9aa374c1b9c1d78599f65a5c18820948590e3 | 1916 | 58d3380e222f38f526c55526eff9aa374c1b9c1d78599f65a5c18820948590e3 |
| A_submission_v2\reports_v2\A_table_risk_coverage_v2.csv | 311 | e48f3d47968ada089f850d303c903cbc26355d052875bd27e90638499d6a4d4f | 311 | e48f3d47968ada089f850d303c903cbc26355d052875bd27e90638499d6a4d4f |
| A_submission_v2\reports_v2\A_table_test_v2.csv | 667 | b38a3fa692a1e23fa88f1da361d373da51bbbdfd6225ae83e90f00de0380381f | 667 | b38a3fa692a1e23fa88f1da361d373da51bbbdfd6225ae83e90f00de0380381f |
| A_submission_v2\reports_v2\A_table_v1_vs_deployed_v2.csv | 360 | 88c66fc03ecad22bef7472dba1d8562f9390cb1a6222c2530772f6c7bb2b9db0 | 360 | 88c66fc03ecad22bef7472dba1d8562f9390cb1a6222c2530772f6c7bb2b9db0 |
| A_submission_v2\reports_v2\A_test_access_log_v2.json | 393 | ab999796eb6e6626d27d4874b266d918bad3a8ce256d11df515a0e3295f6cbb2 | 393 | ab999796eb6e6626d27d4874b266d918bad3a8ce256d11df515a0e3295f6cbb2 |
| A_submission_v2\reports_v2\A_test_results_v2.csv | 2287 | 458839b4f42fbeb26116ff6810035b45936e71adbc911d3b3543afcc1e68f43f | 2287 | 458839b4f42fbeb26116ff6810035b45936e71adbc911d3b3543afcc1e68f43f |
| A_submission_v2\reports_v2\A_test_scored_v2.parquet | 195541 | 8ec79019686135868b2ae739bac6b9fd7b8cc9fd636477936a39fc9969956faa | 195541 | 8ec79019686135868b2ae739bac6b9fd7b8cc9fd636477936a39fc9969956faa |
| A_submission_v2\reports_v2\A_v1_rule_supersession_v2.json | 348 | 588af06edafaa5fef3947cdb807ab64c79122900dc01101006371ab0ad0d7584 | 348 | 588af06edafaa5fef3947cdb807ab64c79122900dc01101006371ab0ad0d7584 |
| A_submission_v2\reports_v2\A_v2_manifest.json | 5063 | b201e6693a908a557456cad01b3224ac3c7aa6389cce9216e9165c631f8f9fd5 | 5063 | b201e6693a908a557456cad01b3224ac3c7aa6389cce9216e9165c631f8f9fd5 |
| interim\combiner_v1.joblib | 129270 | 057e3decd03aca99c804d4408caa6a5832b44f0dc18de67cfd6061e5c966e875 | 129270 | 057e3decd03aca99c804d4408caa6a5832b44f0dc18de67cfd6061e5c966e875 |
| interim\pooled_lr_v2.joblib | 63625 | 216493152a1b7ae2143f0fc60ce2eed6ffc735f40676e308455225b1b55aa96f | 63625 | 216493152a1b7ae2143f0fc60ce2eed6ffc735f40676e308455225b1b55aa96f |
| interim\ft_distilroberta_v1\config.json | 919 | 8c906f8eb778d92ec953d68975285af55c12092bed2c7151f6b42034e3919416 | 919 | 8c906f8eb778d92ec953d68975285af55c12092bed2c7151f6b42034e3919416 |
| interim\ft_distilroberta_v1\model.safetensors | 328501508 | 671e70acf931c6dedd28ebff73baccfa3acf3b07dba13cb3eb15fc39f04761fd | 328501508 | 671e70acf931c6dedd28ebff73baccfa3acf3b07dba13cb3eb15fc39f04761fd |
| interim\ft_distilroberta_v1\tokenizer_config.json | 388 | aa6a8a3f069d2d98c09444ee3f9671d64c29ce647473dccd78169b10c490d359 | 388 | aa6a8a3f069d2d98c09444ee3f9671d64c29ce647473dccd78169b10c490d359 |
| interim\ft_distilroberta_v1\tokenizer.json | 3558895 | ef73668535466d56fd3571306556bcbf3c3d16fd93cdf5e4d38970290c89165b | 3558895 | ef73668535466d56fd3571306556bcbf3c3d16fd93cdf5e4d38970290c89165b |
| processed\cbse_demo_questions_v1.csv | 2888 | 78852eb405819de017fa99a3839cc47912ed1bd40acd0bd0a3966be4b6987e3b | 2888 | 78852eb405819de017fa99a3839cc47912ed1bd40acd0bd0a3966be4b6987e3b |
| reports_v2\A_demo_reference_outputs_v2.json | 16474 | c99b7d84d000046c9629708d5ee440d5a20ab28fd298f63708e2e8c13f89dc92 | 16474 | c99b7d84d000046c9629708d5ee440d5a20ab28fd298f63708e2e8c13f89dc92 |
| reports_v2\A_negation_paraphrase_v2.csv | 3657 | a4b7f45a12f1a4de8c256ee2634de2fc10f06c2b664ff74eb500b2d730e5a5ab | 3657 | a4b7f45a12f1a4de8c256ee2634de2fc10f06c2b664ff74eb500b2d730e5a5ab |
| reports_v2\A_predict.py | 7626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | 7626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 |
| reports_v2\A_runtime_stage_manifest_v2.json | 3911 | c9e93b8a23ebe568215f0f24dac0baf7be6115c52231e5425683b3c7119332d4 | 3911 | c9e93b8a23ebe568215f0f24dac0baf7be6115c52231e5425683b3c7119332d4 |
