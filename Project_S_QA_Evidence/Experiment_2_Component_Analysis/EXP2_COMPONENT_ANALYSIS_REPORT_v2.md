# Experiment 2 — Component contribution, ablation and complementarity

Scope: dev-only, optimistic; saved development probabilities only. No model inference or training.

## Executive conclusion

Path A reconstruction agrees with saved deployed predictions on 2049/2,049 UIDs; component-export Path A agrees on 2049/2,049. Maximum raw five-way mean difference versus deployed d_p: 0.00114184829; versus the saved three-way export: 4.09421825e-08.
Highest two-component Macro-F1 point estimate: C4; strongest standalone unseen-question accuracy: C3 = 0.481481, n=1296. Component-correct/full-wrong rows: {'ft': 185, 'sb': 148, 'nl': 208}; component-wrong/full-correct rows: {'ft': 205, 'sb': 204, 'nl': 351}.
Overall recommendation: INCONCLUSIVE — RETAIN WITH COMPONENT INVESTIGATION. No production change is proposed.

## Artifact validation

| Artifact | Bytes | SHA-256 | Rows / unique UIDs |
| dev text (Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet) | 107715 | 21e7305557825b392a297fc4558b73e1161fcefb07d82c9f802e33c877836ea2 | 2049 / 2049 |
| component probabilities (Project_S_QA_Evidence/Phase_8_Accuracy_Max/A_component_probs_v7.parquet) | 444822 | 71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88 | 2049 / 2049 |
| deployed dev probabilities (project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet) | 131382 | 2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e | 2049 / 2049 |
| A_predict.py source (read only) | 7626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | n/a |

UID sets, gold labels, dataset, question IDs and split metadata match exactly by UID. Splits: {'dev_uq': 1296, 'dev_ua': 753}. Dataset counts: {'scientsbank': 1129, 'beetle': 920}. Unique question counts by dataset/split: {('beetle', 'dev_ua'): 37, ('beetle', 'dev_uq'): 7, ('scientsbank', 'dev_ua'): 113, ('scientsbank', 'dev_uq'): 20}. Gold label5 counts: {'correct': 866, 'partially_correct_incomplete': 524, 'contradictory': 307, 'irrelevant': 283, 'non_domain': 69}.
All three component vectors have five finite normalized probabilities per row. Class order is verified from A_predict.py and the exporter: ['correct', 'contradictory', 'partially_correct_incomplete', 'irrelevant', 'non_domain'].
Duplicate sensitivity validated: 17 exact-content groups, 36 rows in groups, 19 excess rows; primary n=2,049, approved lexicographic-UID subset n=2030. Raw-source provenance remains Unverified.

## Component probability audit

Static source evidence: A_predict.py LABEL5_ORDER line 13, five-to-three mapping lines 56–57, equal component mean and optional temperature lines 152–157, component outputs ft/sb/nl/features line 136. The saved component parquet has ft_p0-p4, sb_p0-p4 and nl_p0-p4; exporter v7 uses A_predict.LABEL5_ORDER. Model IDs in A_predict.py: fine-tuned local DistilRoBERTa directory, cross-encoder/nli-deberta-v3-base, sentence-transformers/all-MiniLM-L6-v2; pooled logistic-regression artifacts are loaded by the scorer. Exact per-row export runtime provenance and checkpoint hashes are not embedded and remain Unverified.

## Path A reproduction

PASS: equal mean of the three saved five-class vectors, five-to-three collapse and argmax exactly matches deployed d_p predictions: 2049/2,049. Component-export three-class prediction agreement: 2049/2,049. Max probability differences are listed above; prediction agreement is exact.

## Metrics by configuration — dev, optimistic

Configs: C1 FT; C2 SBERT-LR; C3 NLI-LR; C4 FT+SBERT-LR; C5 FT+NLI-LR; C6 SBERT-LR+NLI-LR; C7 full ensemble. C4-C6 are also the three leave-one-out ablations. Metrics include each class precision/recall/F1/support. The CSV includes overall, seen/unseen, SciEntsBank and Beetle scopes.

Overall metrics:
  population   scope config                          name    n  accuracy  macro_f1  weighted_f1      qwk  partial_precision  partial_recall  partial_f1  incorrect_precision  incorrect_recall  incorrect_f1  incorrect_support  partial_support  correct_precision  correct_recall  correct_f1  correct_support  partial_tp  false_partial  missed_partial  incorrect_to_partial  correct_to_partial  contradictory_to_partial
primary_2049 overall     C1                 DistilRoBERTa 2049  0.553929  0.528401     0.550001 0.391777           0.426267        0.353053    0.386221             0.521088          0.581184      0.549498                659              524           0.644318        0.654734    0.649485              866         185            249             339                   144                 105                        62
primary_2049 overall     C2                      SBERT-LR 2049  0.536359  0.518943     0.535653 0.339528           0.450935        0.368321    0.405462             0.468368          0.640364      0.541026                659              524           0.672222        0.558891    0.610340              866         193            235             331                   139                  96                        64
primary_2049 overall     C3                        NLI-LR 2049  0.493899  0.407190     0.438741 0.322199           0.346939        0.064885    0.109325             0.426897          0.939302      0.587008                659              524           0.716567        0.414550    0.525238              866          34             64             490                     4                  60                         0
primary_2049 overall     C4      DistilRoBERTa + SBERT-LR 2049  0.557833  0.532811     0.554006 0.386358           0.458228        0.345420    0.393906             0.494019          0.626707      0.552508                659              524           0.671149        0.633949    0.652019              866         181            214             343                   132                  82                        58
primary_2049 overall     C5        DistilRoBERTa + NLI-LR 2049  0.548560  0.497241     0.522718 0.390998           0.500000        0.192748    0.278237             0.466558          0.867982      0.606897                659              524           0.726248        0.520785    0.606590              866         101            101             423                    41                  60                        11
primary_2049 overall     C6             SBERT-LR + NLI-LR 2049  0.529039  0.487000     0.506976 0.343490           0.508850        0.219466    0.306667             0.442901          0.871017      0.587212                659              524           0.749526        0.456120    0.567121              866         115            111             409                    50                  61                        26
primary_2049 overall     C7 Full three-component ensemble 2049  0.563690  0.527046     0.549617 0.401530           0.514925        0.263359    0.348485             0.479452          0.796662      0.598632                659              524           0.717201        0.568129    0.634021              866         138            130             386                    71                  59                        28
  dedup_2030 overall     C1                 DistilRoBERTa 2030  0.555665  0.530410     0.551658 0.394014           0.430233        0.355769    0.389474             0.522634          0.579909      0.549784                657              520           0.645235        0.658851    0.651972              853         185            245             335                   144                 101                        62
  dedup_2030 overall     C2                      SBERT-LR 2030  0.536453  0.519585     0.535773 0.339259           0.451991        0.371154    0.407603             0.469866          0.640791      0.542176                657              520           0.671853        0.556858    0.608974              853         193            234             327                   139                  95                        64
  dedup_2030 overall     C3                        NLI-LR 2030  0.492611  0.405926     0.436946 0.318320           0.350515        0.065385    0.110211             0.426990          0.939117      0.587060                657              520           0.715164        0.409144    0.520507              853          34             63             486                     4                  59                         0
  dedup_2030 overall     C4      DistilRoBERTa + SBERT-LR 2030  0.559606  0.534970     0.555800 0.389082           0.461735        0.348077    0.396930             0.495788          0.627093      0.553763                657              520           0.672862        0.636577    0.654217              853         181            211             339                   132                  79                        58
  dedup_2030 overall     C5        DistilRoBERTa + NLI-LR 2030  0.550246  0.499211     0.524476 0.391146           0.512690        0.194231    0.281729             0.466830          0.867580      0.607029                657              520           0.728758        0.522860    0.608874              853         101             96             419                    41                  55                        11
  dedup_2030 overall     C6             SBERT-LR + NLI-LR 2030  0.529064  0.487325     0.506914 0.342141           0.511111        0.221154    0.308725             0.443755          0.870624      0.587873                657              520           0.750000        0.453693    0.565376              853         115            110             405                    50                  60                        26
  dedup_2030 overall     C7 Full three-component ensemble 2030  0.563547  0.527431     0.549544 0.400945           0.514925        0.265385    0.350254             0.480699          0.796043      0.599427                657              520           0.716617        0.566237    0.632613              853         138            130             382                    71                  59                        28

Seen/unseen and dataset breakdowns:
  population         scope config                          name    n  accuracy  macro_f1  weighted_f1      qwk  partial_precision  partial_recall  partial_f1  incorrect_precision  incorrect_recall  incorrect_f1  incorrect_support  partial_support  correct_precision  correct_recall  correct_f1  correct_support  partial_tp  false_partial  missed_partial  incorrect_to_partial  correct_to_partial  contradictory_to_partial
primary_2049   seen_dev_ua     C1                 DistilRoBERTa  753  0.681275  0.659850     0.679196 0.594465           0.574074        0.494681    0.531429             0.640138          0.728346      0.681400                254              188           0.778146        0.755627    0.766721              311          93             69              95                    37                  32                        21
primary_2049   seen_dev_ua     C2                      SBERT-LR  753  0.682603  0.668828     0.683267 0.569311           0.602339        0.547872    0.573816             0.617834          0.763780      0.683099                254              188           0.809701        0.697749    0.749568              311         103             68              85                    34                  34                        18
primary_2049   seen_dev_ua     C3                        NLI-LR  753  0.515272  0.427154     0.462967 0.324156           0.583333        0.074468    0.132075             0.437500          0.909449      0.590793                254              188           0.711443        0.459807    0.558594              311          14             10             174                     1                   9                         0
primary_2049   seen_dev_ua     C4      DistilRoBERTa + SBERT-LR  753  0.699867  0.683863     0.699040 0.593305           0.637500        0.542553    0.586207             0.636066          0.763780      0.694097                254              188           0.802083        0.742765    0.771285              311         102             58              86                    27                  31                        15
primary_2049   seen_dev_ua     C5        DistilRoBERTa + NLI-LR  753  0.628154  0.580793     0.608598 0.513026           0.644737        0.260638    0.371212             0.518681          0.929134      0.665726                254              188           0.846847        0.604502    0.705441              311          49             27             139                     8                  19                         4
primary_2049   seen_dev_ua     C6             SBERT-LR + NLI-LR  753  0.625498  0.601361     0.616674 0.456095           0.711340        0.367021    0.484211             0.503212          0.925197      0.651872                254              188           0.883598        0.536977    0.668000              311          69             28             119                    11                  17                         5
primary_2049   seen_dev_ua     C7 Full three-component ensemble  753  0.691899  0.665502     0.685324 0.587950           0.722222        0.414894    0.527027             0.575377          0.901575      0.702454                254              188           0.866397        0.688103    0.767025              311          78             30             110                    11                  19                         4
primary_2049 unseen_dev_uq     C1                 DistilRoBERTa 1296  0.479938  0.451340     0.474850 0.271031           0.338235        0.273810    0.302632             0.443946          0.488889      0.465335                405              336           0.574394        0.598198    0.586055              555          92            180             244                   107                  73                        41
primary_2049 unseen_dev_uq     C2                      SBERT-LR 1296  0.451389  0.431169     0.449436 0.209457           0.350195        0.267857    0.303541             0.388416          0.562963      0.459677                405              336           0.590708        0.481081    0.530288              555          90            167             246                   105                  62                        46
primary_2049 unseen_dev_uq     C3                        NLI-LR 1296  0.481481  0.395867     0.424411 0.321577           0.270270        0.059524    0.097561             0.420824          0.958025      0.584778                405              336           0.720000        0.389189    0.505263              555          20             54             316                     3                  51                         0
primary_2049 unseen_dev_uq     C4      DistilRoBERTa + SBERT-LR 1296  0.475309  0.443610     0.468997 0.267278           0.336170        0.235119    0.276708             0.412429          0.540741      0.467949                405              336           0.600000        0.572973    0.586175              555          79            156             257                   105                  51                        43
primary_2049 unseen_dev_uq     C5        DistilRoBERTa + NLI-LR 1296  0.502315  0.449300     0.473049 0.320431           0.412698        0.154762    0.225108             0.435798          0.829630      0.571429                405              336           0.659148        0.473874    0.551363              555          52             74             284                    33                  41                         7
primary_2049 unseen_dev_uq     C6             SBERT-LR + NLI-LR 1296  0.472994  0.419307     0.441668 0.280122           0.356589        0.136905    0.197849             0.408926          0.837037      0.549433                405              336           0.674556        0.410811    0.510638              555          46             83             290                    39                  44                        21
primary_2049 unseen_dev_uq     C7 Full three-component ensemble 1296  0.489198  0.446166     0.470140 0.294900           0.375000        0.178571    0.241935             0.424677          0.730864      0.537205                405              336           0.633257        0.500901    0.559356              555          60            100             276                    60                  40                        24
primary_2049   SciEntsBank     C1                 DistilRoBERTa 1129  0.508415  0.492699     0.508501 0.329875           0.377622        0.363636    0.370497             0.495074          0.544715      0.518710                369              297           0.606407        0.572354    0.588889              463         108            178             189                    96                  82                        29
primary_2049   SciEntsBank     C2                      SBERT-LR 1129  0.499557  0.490572     0.502860 0.295577           0.397993        0.400673    0.399329             0.445833          0.579946      0.504122                369              297           0.660000        0.498920    0.568266              463         119            180             178                    98                  82                        35
primary_2049   SciEntsBank     C3                        NLI-LR 1129  0.465899  0.381848     0.403439 0.276598           0.314286        0.074074    0.119891             0.420927          0.959350      0.585124                369              297           0.688073        0.323974    0.440529              463          22             48             275                     4                  44                         0
primary_2049   SciEntsBank     C4      DistilRoBERTa + SBERT-LR 1129  0.523472  0.508347     0.523798 0.345056           0.410448        0.370370    0.389381             0.476496          0.604336      0.532855                369              297           0.656489        0.557235    0.602804              463         110            158             187                    88                  70                        27
primary_2049   SciEntsBank     C5        DistilRoBERTa + NLI-LR 1129  0.533215  0.494430     0.509820 0.356117           0.493151        0.242424    0.325056             0.467344          0.872629      0.608696                369              297           0.707483        0.449244    0.549538              463          72             74             225                    27                  47                         3
primary_2049   SciEntsBank     C6             SBERT-LR + NLI-LR 1129  0.514615  0.484478     0.496026 0.319807           0.466292        0.279461    0.349474             0.444759          0.850949      0.584186                369              297           0.751020        0.397408    0.519774              463          83             95             214                    37                  58                        16
primary_2049   SciEntsBank     C7 Full three-component ensemble 1129  0.542958  0.518796     0.533114 0.369712           0.474747        0.316498    0.379798             0.473258          0.791328      0.592292                369              297           0.722930        0.490281    0.584299              463          94            104             203                    50                  54                        14
primary_2049        Beetle     C1                 DistilRoBERTa  920  0.609783  0.570887     0.599430 0.462072           0.520270        0.339207    0.410667             0.553191          0.627586      0.588045                290              227           0.681716        0.749380    0.713948              403          77             71             150                    48                  23                        33
primary_2049        Beetle     C2                      SBERT-LR  920  0.581522  0.551805     0.573748 0.387917           0.573643        0.325991    0.415730             0.494062          0.717241      0.585091                290              227           0.683784        0.627792    0.654592              403          74             55             153                    41                  14                        29
primary_2049        Beetle     C3                        NLI-LR  920  0.528261  0.430997     0.475970 0.373605           0.428571        0.052863    0.094118             0.435140          0.913793      0.589544                290              227           0.738516        0.518610    0.609329              403          12             16             215                     0                  16                         0
primary_2049        Beetle     C4      DistilRoBERTa + SBERT-LR  920  0.600000  0.560512     0.588915 0.432064           0.559055        0.312775    0.401130             0.516304          0.655172      0.577508                290              227           0.684706        0.722084    0.702899              403          71             56             156                    44                  12                        31
primary_2049        Beetle     C5        DistilRoBERTa + NLI-LR  920  0.567391  0.491765     0.532776 0.429934           0.517857        0.127753    0.204947             0.465549          0.862069      0.604595                290              227           0.743119        0.602978    0.665753              403          29             27             198                    14                  13                         8
primary_2049        Beetle     C6             SBERT-LR + NLI-LR  920  0.546739  0.479898     0.513548 0.369157           0.666667        0.140969    0.232727             0.440678          0.896552      0.590909                290              227           0.748227        0.523573    0.616058              403          32             16             195                    13                   3                        10
primary_2049        Beetle     C7 Full three-component ensemble  920  0.589130  0.528979     0.563938 0.435961           0.628571        0.193833    0.296296             0.487448          0.803448      0.606771                290              227           0.712366        0.657568    0.683871              403          44             26             183                    21                   5                        14
  dedup_2030   seen_dev_ua     C1                 DistilRoBERTa  746  0.683646  0.662722     0.681087 0.596861           0.584906        0.494681    0.536023             0.642361          0.728346      0.682657                254              188           0.775920        0.763158    0.769486              304          93             66              95                    37                  29                        21
  dedup_2030   seen_dev_ua     C2                      SBERT-LR  746  0.679625  0.666759     0.680116 0.564075           0.602339        0.547872    0.573816             0.617834          0.763780      0.683099                254              188           0.804598        0.690789    0.743363              304         103             68              85                    34                  34                        18
  dedup_2030   seen_dev_ua     C3                        NLI-LR  746  0.512064  0.424241     0.458458 0.317480           0.583333        0.074468    0.132075             0.438330          0.909449      0.591549                254              188           0.702564        0.450658    0.549098              304          14             10             174                     1                   9                         0
  dedup_2030   seen_dev_ua     C4      DistilRoBERTa + SBERT-LR  746  0.702413  0.686946     0.701255 0.595493           0.649682        0.542553    0.591304             0.638158          0.763780      0.695341                254              188           0.800000        0.750000    0.774194              304         102             55              86                    27                  28                        15
  dedup_2030   seen_dev_ua     C5        DistilRoBERTa + NLI-LR  746  0.630027  0.583201     0.609907 0.512872           0.671233        0.260638    0.375479             0.519824          0.929134      0.666667                254              188           0.844749        0.608553    0.707457              304          49             24             139                     8                  16                         4
  dedup_2030   seen_dev_ua     C6             SBERT-LR + NLI-LR  746  0.623324  0.599393     0.613725 0.451377           0.711340        0.367021    0.484211             0.504292          0.925197      0.652778                254              188           0.879781        0.529605    0.661191              304          69             28             119                    11                  17                         5
  dedup_2030   seen_dev_ua     C7 Full three-component ensemble  746  0.690349  0.664621     0.683408 0.585837           0.722222        0.414894    0.527027             0.576826          0.901575      0.703533                254              188           0.863071        0.684211    0.763303              304          78             30             110                    11                  19                         4
  dedup_2030 unseen_dev_uq     C1                 DistilRoBERTa 1284  0.481308  0.452785     0.476411 0.272947           0.339483        0.277108    0.305141             0.444444          0.486352      0.464455                403              332           0.576923        0.601093    0.588760              549          92            179             240                   107                  72                        41
  dedup_2030 unseen_dev_uq     C2                      SBERT-LR 1284  0.453271  0.433233     0.451568 0.212304           0.351562        0.271084    0.306122             0.390034          0.563275      0.460914                403              332           0.594170        0.482696    0.532663              549          90            166             242                   105                  61                        46
  dedup_2030 unseen_dev_uq     C3                        NLI-LR 1284  0.481308  0.395578     0.424269 0.319345           0.273973        0.060241    0.098765             0.420479          0.957816      0.584406                403              332           0.723549        0.386157    0.503563              549          20             53             312                     3                  50                         0
  dedup_2030 unseen_dev_uq     C4      DistilRoBERTa + SBERT-LR 1284  0.476636  0.445237     0.470708 0.270280           0.336170        0.237952    0.278660             0.413662          0.540943      0.468817                403              332           0.603448        0.573770    0.588235              549          79            156             253                   105                  51                        43
  dedup_2030 unseen_dev_uq     C5        DistilRoBERTa + NLI-LR 1284  0.503894  0.451050     0.475102 0.320908           0.419355        0.156627    0.228070             0.435463          0.828784      0.570940                403              332           0.664122        0.475410    0.554140              549          52             72             280                    33                  39                         7
  dedup_2030 unseen_dev_uq     C6             SBERT-LR + NLI-LR 1284  0.474299  0.420742     0.443379 0.280897           0.359375        0.138554    0.200000             0.409478          0.836228      0.549755                403              332           0.678679        0.411658    0.512472              549          46             82             286                    39                  43                        21
  dedup_2030 unseen_dev_uq     C7 Full three-component ensemble 1284  0.489875  0.447154     0.471233 0.295442           0.375000        0.180723    0.243902             0.425470          0.729529      0.537477                403              332           0.635104        0.500911    0.560081              549          60            100             272                    60                  40                        24
  dedup_2030   SciEntsBank     C1                 DistilRoBERTa 1110  0.510811  0.495604     0.510828 0.332648           0.382979        0.368601    0.375652             0.497500          0.542234      0.518905                367              293           0.607477        0.577778    0.592255              450         108            174             185                    96                  78                        29
  dedup_2030   SciEntsBank     C2                      SBERT-LR 1110  0.499099  0.490938     0.502296 0.293784           0.399329        0.406143    0.402707             0.448421          0.580381      0.505938                367              293           0.658754        0.493333    0.564168              450         119            179             174                    98                  81                        35
  dedup_2030   SciEntsBank     C3                        NLI-LR 1110  0.463063  0.378077     0.398873 0.267555           0.318841        0.075085    0.121547             0.421053          0.959128      0.585204                367              293           0.682927        0.311111    0.427481              450          22             47             271                     4                  43                         0
  dedup_2030   SciEntsBank     C4      DistilRoBERTa + SBERT-LR 1110  0.526126  0.511658     0.526521 0.348909           0.415094        0.375427    0.394265             0.479482          0.604905      0.534940                367              293           0.659686        0.560000    0.605769              450         110            155             183                    88                  67                        27
  dedup_2030   SciEntsBank     C5        DistilRoBERTa + NLI-LR 1110  0.536036  0.497707     0.512856 0.355248           0.510638        0.245734    0.331797             0.467836          0.871935      0.608944                367              293           0.712281        0.451111    0.552381              450          72             69             221                    27                  42                         3
  dedup_2030   SciEntsBank     C6             SBERT-LR + NLI-LR 1110  0.514414  0.484392     0.495399 0.316311           0.468927        0.283276    0.353191             0.446352          0.850136      0.585366                367              293           0.752137        0.391111    0.514620              450          83             94             210                    37                  57                        16
  dedup_2030   SciEntsBank     C7 Full three-component ensemble 1110  0.542342  0.518778     0.532399 0.367346           0.474747        0.320819    0.382892             0.475410          0.790191      0.593654                367              293           0.721854        0.484444    0.579787              450          94            104             199                    50                  54                        14
  dedup_2030        Beetle     C1                 DistilRoBERTa  920  0.609783  0.570887     0.599430 0.462072           0.520270        0.339207    0.410667             0.553191          0.627586      0.588045                290              227           0.681716        0.749380    0.713948              403          77             71             150                    48                  23                        33
  dedup_2030        Beetle     C2                      SBERT-LR  920  0.581522  0.551805     0.573748 0.387917           0.573643        0.325991    0.415730             0.494062          0.717241      0.585091                290              227           0.683784        0.627792    0.654592              403          74             55             153                    41                  14                        29
  dedup_2030        Beetle     C3                        NLI-LR  920  0.528261  0.430997     0.475970 0.373605           0.428571        0.052863    0.094118             0.435140          0.913793      0.589544                290              227           0.738516        0.518610    0.609329              403          12             16             215                     0                  16                         0
  dedup_2030        Beetle     C4      DistilRoBERTa + SBERT-LR  920  0.600000  0.560512     0.588915 0.432064           0.559055        0.312775    0.401130             0.516304          0.655172      0.577508                290              227           0.684706        0.722084    0.702899              403          71             56             156                    44                  12                        31
  dedup_2030        Beetle     C5        DistilRoBERTa + NLI-LR  920  0.567391  0.491765     0.532776 0.429934           0.517857        0.127753    0.204947             0.465549          0.862069      0.604595                290              227           0.743119        0.602978    0.665753              403          29             27             198                    14                  13                         8
  dedup_2030        Beetle     C6             SBERT-LR + NLI-LR  920  0.546739  0.479898     0.513548 0.369157           0.666667        0.140969    0.232727             0.440678          0.896552      0.590909                290              227           0.748227        0.523573    0.616058              403          32             16             195                    13                   3                        10
  dedup_2030        Beetle     C7 Full three-component ensemble  920  0.589130  0.528979     0.563938 0.435961           0.628571        0.193833    0.296296             0.487448          0.803448      0.606771                290              227           0.712366        0.657568    0.683871              403          44             26             183                    21                   5                        14

Partial TP, FP, FN and class-specific measures appear in metrics CSV. Gold-contradictory rows mapped to Incorrect are retained in UID-level analysis for contradiction-to-Partial counts.

## Full ensemble and ablations

  population               comparison candidate                candidate_name reference                reference_name    n  delta_accuracy  delta_macro_f1  delta_weighted_f1  delta_partial_precision  delta_partial_recall  delta_partial_f1  delta_qwk
primary_2049     component_minus_full        C1                 DistilRoBERTa        C7 Full three-component ensemble 2049       -0.009761        0.001356           0.000384                -0.088658              0.089695          0.037736  -0.009752
primary_2049     component_minus_full        C2                      SBERT-LR        C7 Full three-component ensemble 2049       -0.027330       -0.008103          -0.013965                -0.063991              0.104962          0.056977  -0.062002
primary_2049     component_minus_full        C3                        NLI-LR        C7 Full three-component ensemble 2049       -0.069790       -0.119856          -0.110876                -0.167987             -0.198473         -0.239160  -0.079330
primary_2049 full_minus_leave_one_out        C7 Full three-component ensemble        C4      DistilRoBERTa + SBERT-LR 2049        0.005857       -0.005766          -0.004389                 0.056698             -0.082061         -0.045422   0.015172
primary_2049 full_minus_leave_one_out        C7 Full three-component ensemble        C5        DistilRoBERTa + NLI-LR 2049        0.015129        0.029804           0.026900                 0.014925              0.070611          0.070248   0.010532
primary_2049 full_minus_leave_one_out        C7 Full three-component ensemble        C6             SBERT-LR + NLI-LR 2049        0.034651        0.040046           0.042642                 0.006076              0.043893          0.041818   0.058039
  dedup_2030     component_minus_full        C1                 DistilRoBERTa        C7 Full three-component ensemble 2030       -0.007882        0.002979           0.002114                -0.084693              0.090385          0.039220  -0.006931
  dedup_2030     component_minus_full        C2                      SBERT-LR        C7 Full three-component ensemble 2030       -0.027094       -0.007847          -0.013771                -0.062935              0.105769          0.057349  -0.061685
  dedup_2030     component_minus_full        C3                        NLI-LR        C7 Full three-component ensemble 2030       -0.070936       -0.121505          -0.112598                -0.164410             -0.200000         -0.240043  -0.082625
  dedup_2030 full_minus_leave_one_out        C7 Full three-component ensemble        C4      DistilRoBERTa + SBERT-LR 2030        0.003941       -0.007539          -0.006256                 0.053191             -0.082692         -0.046676   0.011862
  dedup_2030 full_minus_leave_one_out        C7 Full three-component ensemble        C5        DistilRoBERTa + NLI-LR 2030        0.013300        0.028221           0.025068                 0.002235              0.071154          0.068524   0.009799
  dedup_2030 full_minus_leave_one_out        C7 Full three-component ensemble        C6             SBERT-LR + NLI-LR 2030        0.034483        0.040107           0.042630                 0.003814              0.044231          0.041529   0.058804
Positive component-minus-full differences favor a component; positive full-minus-pair differences favor the full model. Pairwise comparisons use same UIDs. See bootstrap file for paired intervals.

## Paired bootstrap uncertainty

10,000 paired row resamples and 10,000 paired question-group resamples per population, seed 20261110. Each sampled group is dataset::question_id and all its rows stay together. Row intervals are supplementary; question-group intervals are primary. Intervals crossing zero do not establish a difference.
  population                scheme  comparison         metric  difference  ci95_low  ci95_high  includes_zero  resamples     seed
primary_2049            paired_row C1_minus_C7       accuracy   -0.009761 -0.028795   0.009273           True      10000 20261110
primary_2049            paired_row C1_minus_C7       macro_f1    0.001356 -0.018484   0.020939           True      10000 20261110
primary_2049            paired_row C1_minus_C7    weighted_f1    0.000384 -0.018859   0.019513           True      10000 20261110
primary_2049            paired_row C1_minus_C7 partial_recall    0.089695  0.054716   0.123508          False      10000 20261110
primary_2049            paired_row C1_minus_C7     partial_f1    0.037736  0.001424   0.073577          False      10000 20261110
primary_2049            paired_row C1_minus_C7            qwk   -0.009752 -0.044594   0.024830           True      10000 20261110
primary_2049            paired_row C2_minus_C7       accuracy   -0.027330 -0.045388  -0.009273          False      10000 20261110
primary_2049            paired_row C2_minus_C7       macro_f1   -0.008103 -0.026171   0.011064           True      10000 20261110
primary_2049            paired_row C2_minus_C7    weighted_f1   -0.013965 -0.031954   0.004613           True      10000 20261110
primary_2049            paired_row C2_minus_C7 partial_recall    0.104962  0.072578   0.139707          False      10000 20261110
primary_2049            paired_row C2_minus_C7     partial_f1    0.056977  0.023712   0.092232          False      10000 20261110
primary_2049            paired_row C2_minus_C7            qwk   -0.062002 -0.094909  -0.030329          False      10000 20261110
primary_2049            paired_row C3_minus_C7       accuracy   -0.069790 -0.092240  -0.047340          False      10000 20261110
primary_2049            paired_row C3_minus_C7       macro_f1   -0.119856 -0.145191  -0.094378          False      10000 20261110
primary_2049            paired_row C3_minus_C7    weighted_f1   -0.110876 -0.135507  -0.086174          False      10000 20261110
primary_2049            paired_row C3_minus_C7 partial_recall   -0.198473 -0.240081  -0.156125          False      10000 20261110
primary_2049            paired_row C3_minus_C7     partial_f1   -0.239160 -0.290677  -0.186148          False      10000 20261110
primary_2049            paired_row C3_minus_C7            qwk   -0.079330 -0.116427  -0.042104          False      10000 20261110
primary_2049            paired_row C7_minus_C4       accuracy    0.005857 -0.009273   0.020986           True      10000 20261110
primary_2049            paired_row C7_minus_C4       macro_f1   -0.005766 -0.021186   0.009338           True      10000 20261110
primary_2049            paired_row C7_minus_C4    weighted_f1   -0.004389 -0.019360   0.010517           True      10000 20261110
primary_2049            paired_row C7_minus_C4 partial_recall   -0.082061 -0.107487  -0.057732          False      10000 20261110
primary_2049            paired_row C7_minus_C4     partial_f1   -0.045422 -0.072480  -0.019409          False      10000 20261110
primary_2049            paired_row C7_minus_C4            qwk    0.015172 -0.012747   0.043631           True      10000 20261110
primary_2049            paired_row C7_minus_C5       accuracy    0.015129 -0.001464   0.031723           True      10000 20261110
primary_2049            paired_row C7_minus_C5       macro_f1    0.029804  0.010872   0.048911          False      10000 20261110
primary_2049            paired_row C7_minus_C5    weighted_f1    0.026900  0.009044   0.044731          False      10000 20261110
primary_2049            paired_row C7_minus_C5 partial_recall    0.070611  0.038095   0.102714          False      10000 20261110
primary_2049            paired_row C7_minus_C5     partial_f1    0.070248  0.031465   0.109726          False      10000 20261110
primary_2049            paired_row C7_minus_C5            qwk    0.010532 -0.018409   0.039846           True      10000 20261110
primary_2049            paired_row C7_minus_C6       accuracy    0.034651  0.019034   0.050268          False      10000 20261110
primary_2049            paired_row C7_minus_C6       macro_f1    0.040046  0.023149   0.056706          False      10000 20261110
primary_2049            paired_row C7_minus_C6    weighted_f1    0.042642  0.026222   0.059096          False      10000 20261110
primary_2049            paired_row C7_minus_C6 partial_recall    0.043893  0.017308   0.069904          False      10000 20261110
primary_2049            paired_row C7_minus_C6     partial_f1    0.041818  0.010536   0.072014          False      10000 20261110
primary_2049            paired_row C7_minus_C6            qwk    0.058039  0.029512   0.086174          False      10000 20261110
primary_2049 paired_question_group C1_minus_C7       accuracy   -0.009761 -0.035958   0.015658           True      10000 20261110
primary_2049 paired_question_group C1_minus_C7       macro_f1    0.001356 -0.025481   0.026083           True      10000 20261110
primary_2049 paired_question_group C1_minus_C7    weighted_f1    0.000384 -0.025701   0.024778           True      10000 20261110
primary_2049 paired_question_group C1_minus_C7 partial_recall    0.089695  0.041588   0.132232          False      10000 20261110
primary_2049 paired_question_group C1_minus_C7     partial_f1    0.037736 -0.010225   0.076948           True      10000 20261110
primary_2049 paired_question_group C1_minus_C7            qwk   -0.009752 -0.059616   0.038912           True      10000 20261110
primary_2049 paired_question_group C2_minus_C7       accuracy   -0.027330 -0.049631  -0.004468          False      10000 20261110
primary_2049 paired_question_group C2_minus_C7       macro_f1   -0.008103 -0.031514   0.016009           True      10000 20261110
primary_2049 paired_question_group C2_minus_C7    weighted_f1   -0.013965 -0.037484   0.010017           True      10000 20261110
primary_2049 paired_question_group C2_minus_C7 partial_recall    0.104962  0.057447   0.156323          False      10000 20261110
primary_2049 paired_question_group C2_minus_C7     partial_f1    0.056977  0.011844   0.104591          False      10000 20261110
primary_2049 paired_question_group C2_minus_C7            qwk   -0.062002 -0.101314  -0.019264          False      10000 20261110
primary_2049 paired_question_group C3_minus_C7       accuracy   -0.069790 -0.114334  -0.029970          False      10000 20261110
primary_2049 paired_question_group C3_minus_C7       macro_f1   -0.119856 -0.166543  -0.080417          False      10000 20261110
primary_2049 paired_question_group C3_minus_C7    weighted_f1   -0.110876 -0.157866  -0.069505          False      10000 20261110
primary_2049 paired_question_group C3_minus_C7 partial_recall   -0.198473 -0.293067  -0.118182          False      10000 20261110
primary_2049 paired_question_group C3_minus_C7     partial_f1   -0.239160 -0.336217  -0.150881          False      10000 20261110
primary_2049 paired_question_group C3_minus_C7            qwk   -0.079330 -0.158218  -0.008894          False      10000 20261110
primary_2049 paired_question_group C7_minus_C4       accuracy    0.005857 -0.011793   0.023316           True      10000 20261110
primary_2049 paired_question_group C7_minus_C4       macro_f1   -0.005766 -0.023799   0.011090           True      10000 20261110
primary_2049 paired_question_group C7_minus_C4    weighted_f1   -0.004389 -0.021779   0.012860           True      10000 20261110
primary_2049 paired_question_group C7_minus_C4 partial_recall   -0.082061 -0.122154  -0.047617          False      10000 20261110
primary_2049 paired_question_group C7_minus_C4     partial_f1   -0.045422 -0.077128  -0.015976          False      10000 20261110
primary_2049 paired_question_group C7_minus_C4            qwk    0.015172 -0.017925   0.047900           True      10000 20261110
primary_2049 paired_question_group C7_minus_C5       accuracy    0.015129 -0.009836   0.041098           True      10000 20261110
primary_2049 paired_question_group C7_minus_C5       macro_f1    0.029804  0.006999   0.057580          False      10000 20261110
primary_2049 paired_question_group C7_minus_C5    weighted_f1    0.026900  0.003979   0.053915          False      10000 20261110
primary_2049 paired_question_group C7_minus_C5 partial_recall    0.070611  0.031372   0.115196          False      10000 20261110
primary_2049 paired_question_group C7_minus_C5     partial_f1    0.070248  0.028213   0.120940          False      10000 20261110
primary_2049 paired_question_group C7_minus_C5            qwk    0.010532 -0.030966   0.055832           True      10000 20261110
primary_2049 paired_question_group C7_minus_C6       accuracy    0.034651  0.018064   0.053310          False      10000 20261110
primary_2049 paired_question_group C7_minus_C6       macro_f1    0.040046  0.023350   0.057337          False      10000 20261110
primary_2049 paired_question_group C7_minus_C6    weighted_f1    0.042642  0.025727   0.061122          False      10000 20261110
primary_2049 paired_question_group C7_minus_C6 partial_recall    0.043893  0.005736   0.082893          False      10000 20261110
primary_2049 paired_question_group C7_minus_C6     partial_f1    0.041818  0.006143   0.074107          False      10000 20261110
primary_2049 paired_question_group C7_minus_C6            qwk    0.058039  0.026043   0.093799          False      10000 20261110
  dedup_2030            paired_row C1_minus_C7       accuracy   -0.007882 -0.027094   0.011330           True      10000 20261110
  dedup_2030            paired_row C1_minus_C7       macro_f1    0.002979 -0.016624   0.022635           True      10000 20261110
  dedup_2030            paired_row C1_minus_C7    weighted_f1    0.002114 -0.016911   0.021311           True      10000 20261110
  dedup_2030            paired_row C1_minus_C7 partial_recall    0.090385  0.055453   0.125224          False      10000 20261110
  dedup_2030            paired_row C1_minus_C7     partial_f1    0.039220  0.003425   0.075025          False      10000 20261110
  dedup_2030            paired_row C1_minus_C7            qwk   -0.006931 -0.041891   0.028091           True      10000 20261110
  dedup_2030            paired_row C2_minus_C7       accuracy   -0.027094 -0.045320  -0.009360          False      10000 20261110
  dedup_2030            paired_row C2_minus_C7       macro_f1   -0.007847 -0.026247   0.010800           True      10000 20261110
  dedup_2030            paired_row C2_minus_C7    weighted_f1   -0.013771 -0.031885   0.004423           True      10000 20261110
  dedup_2030            paired_row C2_minus_C7 partial_recall    0.105769  0.073307   0.138402          False      10000 20261110
  dedup_2030            paired_row C2_minus_C7     partial_f1    0.057349  0.023652   0.091263          False      10000 20261110
  dedup_2030            paired_row C2_minus_C7            qwk   -0.061685 -0.094716  -0.029324          False      10000 20261110
  dedup_2030            paired_row C3_minus_C7       accuracy   -0.070936 -0.093596  -0.047783          False      10000 20261110
  dedup_2030            paired_row C3_minus_C7       macro_f1   -0.121505 -0.147196  -0.095118          False      10000 20261110
  dedup_2030            paired_row C3_minus_C7    weighted_f1   -0.112598 -0.137904  -0.086740          False      10000 20261110
  dedup_2030            paired_row C3_minus_C7 partial_recall   -0.200000 -0.243195  -0.158377          False      10000 20261110
  dedup_2030            paired_row C3_minus_C7     partial_f1   -0.240043 -0.292742  -0.187023          False      10000 20261110
  dedup_2030            paired_row C3_minus_C7            qwk   -0.082625 -0.120672  -0.043911          False      10000 20261110
  dedup_2030            paired_row C7_minus_C4       accuracy    0.003941 -0.011330   0.019212           True      10000 20261110
  dedup_2030            paired_row C7_minus_C4       macro_f1   -0.007539 -0.022739   0.007808           True      10000 20261110
  dedup_2030            paired_row C7_minus_C4    weighted_f1   -0.006256 -0.021241   0.008697           True      10000 20261110
  dedup_2030            paired_row C7_minus_C4 partial_recall   -0.082692 -0.108007  -0.057426          False      10000 20261110
  dedup_2030            paired_row C7_minus_C4     partial_f1   -0.046676 -0.073227  -0.019977          False      10000 20261110
  dedup_2030            paired_row C7_minus_C4            qwk    0.011862 -0.016531   0.040322           True      10000 20261110
  dedup_2030            paired_row C7_minus_C5       accuracy    0.013300 -0.003448   0.030049           True      10000 20261110
  dedup_2030            paired_row C7_minus_C5       macro_f1    0.028221  0.009402   0.047131          False      10000 20261110
  dedup_2030            paired_row C7_minus_C5    weighted_f1    0.025068  0.007380   0.043075          False      10000 20261110
  dedup_2030            paired_row C7_minus_C5 partial_recall    0.071154  0.039105   0.104628          False      10000 20261110
  dedup_2030            paired_row C7_minus_C5     partial_f1    0.068524  0.030153   0.107713          False      10000 20261110
  dedup_2030            paired_row C7_minus_C5            qwk    0.009799 -0.019916   0.038736           True      10000 20261110
  dedup_2030            paired_row C7_minus_C6       accuracy    0.034483  0.018227   0.050246          False      10000 20261110
  dedup_2030            paired_row C7_minus_C6       macro_f1    0.040107  0.023379   0.056867          False      10000 20261110
  dedup_2030            paired_row C7_minus_C6    weighted_f1    0.042630  0.026021   0.059232          False      10000 20261110
  dedup_2030            paired_row C7_minus_C6 partial_recall    0.044231  0.017928   0.071429          False      10000 20261110
  dedup_2030            paired_row C7_minus_C6     partial_f1    0.041529  0.010275   0.072868          False      10000 20261110
  dedup_2030            paired_row C7_minus_C6            qwk    0.058804  0.029996   0.087903          False      10000 20261110
  dedup_2030 paired_question_group C1_minus_C7       accuracy   -0.007882 -0.033557   0.016384           True      10000 20261110
  dedup_2030 paired_question_group C1_minus_C7       macro_f1    0.002979 -0.023099   0.027115           True      10000 20261110
  dedup_2030 paired_question_group C1_minus_C7    weighted_f1    0.002114 -0.023304   0.025837           True      10000 20261110
  dedup_2030 paired_question_group C1_minus_C7 partial_recall    0.090385  0.042986   0.134401          False      10000 20261110
  dedup_2030 paired_question_group C1_minus_C7     partial_f1    0.039220 -0.007779   0.079557           True      10000 20261110
  dedup_2030 paired_question_group C1_minus_C7            qwk   -0.006931 -0.057543   0.041726           True      10000 20261110
  dedup_2030 paired_question_group C2_minus_C7       accuracy   -0.027094 -0.050021  -0.003788          False      10000 20261110
  dedup_2030 paired_question_group C2_minus_C7       macro_f1   -0.007847 -0.031604   0.016970           True      10000 20261110
  dedup_2030 paired_question_group C2_minus_C7    weighted_f1   -0.013771 -0.038279   0.010624           True      10000 20261110
  dedup_2030 paired_question_group C2_minus_C7 partial_recall    0.105769  0.058235   0.157898          False      10000 20261110
  dedup_2030 paired_question_group C2_minus_C7     partial_f1    0.057349  0.013201   0.104612          False      10000 20261110
  dedup_2030 paired_question_group C2_minus_C7            qwk   -0.061685 -0.101813  -0.020183          False      10000 20261110
  dedup_2030 paired_question_group C3_minus_C7       accuracy   -0.070936 -0.114510  -0.030331          False      10000 20261110
  dedup_2030 paired_question_group C3_minus_C7       macro_f1   -0.121505 -0.167919  -0.081332          False      10000 20261110
  dedup_2030 paired_question_group C3_minus_C7    weighted_f1   -0.112598 -0.159430  -0.070255          False      10000 20261110
  dedup_2030 paired_question_group C3_minus_C7 partial_recall   -0.200000 -0.295848  -0.116105          False      10000 20261110
  dedup_2030 paired_question_group C3_minus_C7     partial_f1   -0.240043 -0.336549  -0.148155          False      10000 20261110
  dedup_2030 paired_question_group C3_minus_C7            qwk   -0.082625 -0.160553  -0.009511          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C4       accuracy    0.003941 -0.013124   0.020823           True      10000 20261110
  dedup_2030 paired_question_group C7_minus_C4       macro_f1   -0.007539 -0.025419   0.008676           True      10000 20261110
  dedup_2030 paired_question_group C7_minus_C4    weighted_f1   -0.006256 -0.023252   0.010501           True      10000 20261110
  dedup_2030 paired_question_group C7_minus_C4 partial_recall   -0.082692 -0.123030  -0.047703          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C4     partial_f1   -0.046676 -0.078743  -0.017519          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C4            qwk    0.011862 -0.019476   0.042686           True      10000 20261110
  dedup_2030 paired_question_group C7_minus_C5       accuracy    0.013300 -0.011666   0.038686           True      10000 20261110
  dedup_2030 paired_question_group C7_minus_C5       macro_f1    0.028221  0.004897   0.054634          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C5    weighted_f1    0.025068  0.001857   0.050706          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C5 partial_recall    0.071154  0.030060   0.115859          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C5     partial_f1    0.068524  0.024478   0.117373          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C5            qwk    0.009799 -0.032301   0.055966           True      10000 20261110
  dedup_2030 paired_question_group C7_minus_C6       accuracy    0.034483  0.017484   0.052878          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C6       macro_f1    0.040107  0.023070   0.057601          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C6    weighted_f1    0.042630  0.025383   0.061096          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C6 partial_recall    0.044231  0.006048   0.083902          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C6     partial_f1    0.041529  0.005602   0.073801          False      10000 20261110
  dedup_2030 paired_question_group C7_minus_C6            qwk    0.058804  0.026067   0.093523          False      10000 20261110

## Error complementarity

  population first    first_name second second_name    n  both_correct  both_wrong  first_correct_second_wrong  first_wrong_second_correct  same_wrong_class  disagree  disagreement_rate  error_intersection  error_union  error_jaccard  first_error_rate  second_error_rate  second_error_given_first_wrong  first_error_given_second_wrong  first_partial_rescues  second_partial_rescues  first_contradiction_error_second_correct  second_contradiction_error_first_correct
primary_2049    C1 DistilRoBERTa     C2    SBERT-LR 2049           839         654                         296                         260               492       718           0.350415                 654         1210       0.540496          0.446071           0.463641                        0.715536                        0.688421                     67                      75                                        46                                        33
primary_2049    C1 DistilRoBERTa     C3      NLI-LR 2049           659         561                         476                         353               342      1048           0.511469                 561         1390       0.403597          0.446071           0.506101                        0.613786                        0.540984                    168                      17                                       136                                        10
primary_2049    C2      SBERT-LR     C3      NLI-LR 2049           646         584                         453                         366               401      1002           0.489019                 584         1403       0.416251          0.463641           0.506101                        0.614737                        0.563163                    182                      23                                       133                                        20
  dedup_2030    C1 DistilRoBERTa     C2    SBERT-LR 2030           834         647                         294                         255               486       710           0.349754                 647         1196       0.540970          0.444335           0.463547                        0.717295                        0.687566                     67                      75                                        46                                        32
  dedup_2030    C1 DistilRoBERTa     C3      NLI-LR 2030           653         555                         475                         347               337      1040           0.512315                 555         1377       0.403050          0.444335           0.507389                        0.615299                        0.538835                    168                      17                                       136                                        10
  dedup_2030    C2      SBERT-LR     C3      NLI-LR 2030           638         579                         451                         362               396       996           0.490640                 579         1392       0.415948          0.463547           0.507389                        0.615303                        0.562136                    182                      23                                       132                                        20
Counts include both-correct, both-wrong, directional unique corrections, same-wrong-class, disagreement, error intersection/union/Jaccard, conditional error rates, partial rescues, and contradiction-specific directional errors.
UID-level CSV contains UID and metadata, gold labels, every config prediction/correctness, and pairwise disagreement flags; no answer text.

## Calibration and confidence diagnostics — dev, optimistic

  population config                          name    n  mean_max_probability  brier_3class  log_loss_3class
primary_2049     C1                 DistilRoBERTa 2049              0.671025      0.569020         0.966720
primary_2049     C2                      SBERT-LR 2049              0.684790      0.615000         1.067606
primary_2049     C3                        NLI-LR 2049              0.616345      0.672796         1.124571
primary_2049     C4      DistilRoBERTa + SBERT-LR 2049              0.638699      0.550135         0.931514
primary_2049     C5        DistilRoBERTa + NLI-LR 2049              0.569892      0.552293         0.925311
primary_2049     C6             SBERT-LR + NLI-LR 2049              0.583220      0.578469         0.962482
primary_2049     C7 Full three-component ensemble 2049              0.576937      0.540752         0.906331
  dedup_2030     C1                 DistilRoBERTa 2030              0.671089      0.567099         0.963810
  dedup_2030     C2                      SBERT-LR 2030              0.684783      0.613799         1.065669
  dedup_2030     C3                        NLI-LR 2030              0.617295      0.673549         1.125991
  dedup_2030     C4      DistilRoBERTa + SBERT-LR 2030              0.638830      0.548662         0.929289
  dedup_2030     C5        DistilRoBERTa + NLI-LR 2030              0.570006      0.551513         0.924105
  dedup_2030     C6             SBERT-LR + NLI-LR 2030              0.583371      0.578082         0.962177
  dedup_2030     C7 Full three-component ensemble 2030              0.577074      0.539842         0.905012
Mean max probability, collapsed three-class Brier score, and log loss are descriptive only. No calibrator was fitted; threshold 0.64 was not changed.

## Architecture decision

Component classifications from paired question-grouped C7-vs-ablation intervals in both populations: DistilRoBERTa = CORE CONTRIBUTOR (C7 beats C6 on accuracy, Macro-F1, Partial recall/F1 and QWK with intervals above zero); SBERT-LR = COMPLEMENTARY CONTRIBUTOR (C7 beats C5 on Macro-F1 and Partial recall/F1 with intervals above zero; accuracy interval includes zero); NLI-LR = POTENTIALLY HARMFUL for Partial recall/F1 (C7 is lower than C4 with intervals below zero), while overall accuracy/Macro-F1/QWK differences include zero. NLI-LR also has unique correct cases, so this does not justify automatic removal.
Does the full ensemble beat every standalone component? Read C7 against C1-C3 in the metrics and paired intervals; do not infer from a single metric.
Direct answer: C7 accuracy (0.563690) exceeds each standalone component; FT has a slightly higher standalone Macro-F1 (0.528401 vs C7 0.527046) and weighted-F1 (0.550001 vs C7 0.549617).
Marginal value: FT inclusion (C7 vs C6) improves all listed primary grouped metrics with CIs above zero, and repeats in the 2,030 sensitivity set. SBERT-LR inclusion (C7 vs C5) improves Macro-F1 and Partial recall/F1 with grouped CIs above zero in both populations; accuracy CI includes zero. NLI-LR inclusion (C7 vs C4) reduces Partial recall/F1 with grouped CIs below zero; accuracy, Macro-F1 and QWK intervals include zero in both populations.
Additional value: components can contribute distinct correct predictions, but unique rescue and full-rescue counts above are not causal estimates.
Standalone Partial recall: {'ft': 0.3530534351145038, 'sb': 0.3683206106870229, 'nl': 0.0648854961832061}; false Partial predictions: {'ft': 249, 'sb': 235, 'nl': 64}. FT has the most standalone false-Partial predictions (249), versus SBERT-LR 235 and NLI-LR 64. SBERT-LR has the highest standalone Partial recall; its marginal inclusion also has the largest positive Partial-recall change among added components.
Strongest standalone unseen accuracy: C3 (0.481481, n=1296); strongest unseen Macro-F1: C1 (0.451340). Accuracy edge is descriptive and subgroup intervals are not computed.
Best pair by primary Macro-F1 point estimate: C4 (DistilRoBERTa + SBERT-LR, Macro-F1=0.532811); the grouped interval for C7-minus-C4 Macro-F1 crosses zero.
Most standalone unique correct predictions versus C7: NLI-LR (208); most standalone errors corrected by C7: NLI-LR (351). NLI is mixed, not a clear removal candidate.
Final recommendation: RETAIN WITH COMPONENT INVESTIGATION. Proposed Experiment 3: evaluate component contributions on genuine held-out question-grouped predictions or a clean confirmation set, without test tuning.

## Limitations

All scores are dev-only, optimistic; only 27 dev questions are unseen. The 2,030-row result is a duplicate sensitivity analysis. Original-source duplicate provenance is Unverified. Component probabilities are saved exports, not shown to be OOF. No test data, training, inference, model loading, A_predict import, notebook execution, or production modification occurred.

## Reproduction

From the project root run the script named in the manifest. Requires installed pandas, NumPy, scikit-learn and a parquet engine. Reads only the three dev artifacts and A_predict.py source text; never imports A_predict. Versioned outputs are never overwritten.

### Probability identity and preprocessing

For each component, the saved parquet holds a 2,049 x 5 vector under its named p0-p4 columns; the order is A_predict LABEL5_ORDER. Gold label5 maps to Incorrect for indices 1/3/4, Partial for index 2, Correct for index 0. DistilRoBERTa probabilities are softmax; SBERT-LR and NLI-LR are LogisticRegression predict_proba outputs reordered to LABEL5_ORDER. No temperature is applied to individual vectors in component_probs; the optional final temperature is applied after equal averaging and collapse. Export file: Phase_8_Accuracy_Max/A_component_probs_v7.parquet; exporter source is recorded in the manifest. The parquet contains seven NLI features: ['nli_f_ent_mean', 'nli_f_ent_min', 'nli_f_con_max', 'nli_f_neu_mean', 'nli_r_ent', 'nli_r_con', 'nli_r_neu']. The file does not embed checkpoint hashes or a run manifest, so exact model/checkpoint provenance for the saved rows is Unverified.

NLI/feature max, min and other distributions are retained in the saved input; this experiment validates their presence, row alignment, null-free state and seven-column numeric shape but does not use them to create new predictions.
