# NLI contradiction analysis

**Dev-only, optimistic; the rule was chosen on these rows.**

Rows: 2049; seed: 42; question-group bootstrap resamples: 2,000.
Pooled overall accuracy (unchanged by review routing): 1155/2049.
Baseline confidence-only review threshold: 0.64; recomputed coverage 0.306003, selective accuracy 0.751196.

## Component accuracy
ft: 1135/2049
sb: 1099/2049
nl: 1012/2049

NLI-LR correct where pooled is wrong: 208/2049.

## Seen/unseen accuracy
seen: n=753; pooled=0.691899; ft=0.681275; sb=0.682603; nl=0.515272
unseen: n=1296; pooled=0.489198; ft=0.479938; sb=0.451389; nl=0.481481
Rows without a recognized seen/unseen split tag: 0.

## Contradiction routing
Paired bootstrap intervals are for new-minus-baseline coverage and selective accuracy, resampling question IDs.

### Threshold 0.90
- scope: dev-only, optimistic; rule chosen on these rows
- contradiction_rows: 360
- gold_label_distribution: {'contradictory': 129, 'correct': 91, 'partially_correct_incomplete': 82, 'irrelevant': 55, 'non_domain': 3}
- pooled_correct_pred_rows: 73
- wrong_among_pooled_correct: 37
- wrong_caught_conf_lt_0.64: 36
- wrong_missed_conf_ge_0.64: 1
- added_review_rows: 124
- baseline_coverage: 0.30600292825768666
- new_coverage: 0.24548560273304051
- baseline_selective_accuracy: 0.7511961722488039
- new_selective_accuracy: 0.7554671968190855
- overall_accuracy_unchanged: 0.5636896046852123
- delta_coverage_CI95: [-0.08665728109515956, -0.04002020959356735]
- delta_selective_accuracy_CI95: [-0.022386730715678094, 0.03719774093427073]
### Threshold 0.95
- scope: dev-only, optimistic; rule chosen on these rows
- contradiction_rows: 342
- gold_label_distribution: {'contradictory': 125, 'correct': 87, 'partially_correct_incomplete': 74, 'irrelevant': 53, 'non_domain': 3}
- pooled_correct_pred_rows: 70
- wrong_among_pooled_correct: 35
- wrong_caught_conf_lt_0.64: 34
- wrong_missed_conf_ge_0.64: 1
- added_review_rows: 118
- baseline_coverage: 0.30600292825768666
- new_coverage: 0.24841386041971694
- baseline_selective_accuracy: 0.7511961722488039
- new_selective_accuracy: 0.756385068762279
- overall_accuracy_unchanged: 0.5636896046852123
- delta_coverage_CI95: [-0.08309730395475175, -0.03791913708419847]
- delta_selective_accuracy_CI95: [-0.02212340770100008, 0.03922199272379959]
### Threshold 0.99
- scope: dev-only, optimistic; rule chosen on these rows
- contradiction_rows: 252
- gold_label_distribution: {'contradictory': 102, 'correct': 63, 'partially_correct_incomplete': 52, 'irrelevant': 35}
- pooled_correct_pred_rows: 55
- wrong_among_pooled_correct: 32
- wrong_caught_conf_lt_0.64: 31
- wrong_missed_conf_ge_0.64: 1
- added_review_rows: 91
- baseline_coverage: 0.30600292825768666
- new_coverage: 0.26159102000976087
- baseline_selective_accuracy: 0.7511961722488039
- new_selective_accuracy: 0.7574626865671642
- overall_accuracy_unchanged: 0.5636896046852123
- delta_coverage_CI95: [-0.06613471594043022, -0.027669538004903883]
- delta_selective_accuracy_CI95: [-0.017362780410975984, 0.034154478811140206]
