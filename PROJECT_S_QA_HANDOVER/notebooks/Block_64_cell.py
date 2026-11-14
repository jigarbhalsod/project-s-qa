"""Exact draft cell to paste only into a separate notebook run copy."""
import os
import sys
from pathlib import Path

# Set these environment variables in Colab after confirming their Drive paths.
PROJECT_S_ROOT = Path(os.environ["PROJECT_S_ROOT"]).resolve()
HANDOVER_ROOT = Path(os.environ["PROJECT_S_HANDOVER_ROOT"]).resolve()
if not (PROJECT_S_ROOT / "reports_v2" / "A_predict.py").is_file():
    raise FileNotFoundError("PROJECT_S_ROOT must contain reports_v2/A_predict.py")
if not (HANDOVER_ROOT / "question_bank" / "questions.json").is_file():
    raise FileNotFoundError("PROJECT_S_HANDOVER_ROOT must contain question_bank/questions.json")
sys.path.insert(0, str(PROJECT_S_ROOT / "reports_v2"))
sys.path.insert(0, str(HANDOVER_ROOT / "src"))
import A_predict
from block64_demo_bank import build_demo
from question_bank import load_bank

bank, rubrics = load_bank(HANDOVER_ROOT / "question_bank")
demo = build_demo(bank, rubrics, A_predict.predict)
demo.launch(share=False)
