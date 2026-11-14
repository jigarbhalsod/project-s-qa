# Block 60: question dropdown + voice input demo (adult voices only). Writes no files.
!pip -q install gradio transformers accelerate
import os, sys, importlib
import pandas as pd, torch
from google.colab import drive
drive.mount("/content/drive")
ROOT = "/content/drive/MyDrive/project_s_qa"
sys.path.insert(0, f"{ROOT}/reports_v2")
import A_predict
importlib.reload(A_predict)
import gradio as gr
from transformers import pipeline

# 1. Question bank, read-only. Falls back to one built-in question if the CSV is missing.
QB_PATH = f"{ROOT}/processed/cbse_demo_questions_v1.csv"
if os.path.exists(QB_PATH):
    qb = pd.read_csv(QB_PATH).fillna("")
else:
    print("MISSING:", QB_PATH, "-> using one built-in question")
    qb = pd.DataFrame([{"question_id": "demo", "question_text": "Do plants need sunlight?",
                        "reference_answer": "Plants need sunlight to make food through photosynthesis."}])
LOOKUP = {f"{r['question_id']}: {r['question_text']}": (r["question_text"], r["reference_answer"])
          for _, r in qb.iterrows()}

# 2. Local open-weights speech model (no API, rule L8).
asr = pipeline("automatic-speech-recognition", model="openai/whisper-small",
               device=0 if torch.cuda.is_available() else -1, chunk_length_s=30)

def pick(label):
    return LOOKUP.get(label, ("", ""))          # dropdown fills the question and reference boxes

def transcribe(path):
    if not path:
        return ""
    # UNDERSTAND THIS: the transcript is only a draft. Any error here flows into the score.
    return asr(path, generate_kwargs={"language": "en", "task": "transcribe"})["text"].strip()

def score(question, reference, answer):
    if not (question.strip() and reference.strip() and answer.strip()):
        return "Fill the question, reference and answer boxes.", []
    # UNDERSTAND THIS: same function and default arguments as Block 45c, so demo parity still holds.
    r = A_predict.predict(question, reference, answer)
    why = (" (" + ", ".join(r["review_reasons"]) + ")") if r["review_reasons"] else ""
    text = (f"Predicted: {r['pred_label']} (score {r['pred_score']} / 2)\n"
            f"Confidence: {r['confidence']:.3f}\n"
            f"Teacher review: {'YES' if r['needs_teacher_review'] else 'no'}{why}\n"
            f"P(incorrect / partial / correct): {r['p_incorrect']:.3f} / {r['p_partial']:.3f} / {r['p_correct']:.3f}\n"
            f"NLI: entail {r['nli']['entail']:.3f}, contradict {r['nli']['contradict']:.3f}\n"
            f"Model: {r['model_version']}")
    return text, r["concepts"]

# 3. Page. Check argument names (sources=, stop_recording) against your Gradio version.
with gr.Blocks(title="Project S: Q&A scorer (v2) with voice") as demo:
    gr.Markdown("**Project S Q&A scorer (v2).** Trained on public data (SciEntsBank, Beetle). "
                "The CBSE-style questions and the voice input are untested demo features. "
                "Adult voices only; speech errors flow into the score. "
                "Review flag when confidence is below 0.64. The NLI evidence can mislead on off-topic answers.")
    dd = gr.Dropdown(choices=list(LOOKUP), label="Question bank (optional)")
    q = gr.Textbox(label="Question")
    ref = gr.Textbox(label="Reference answer")
    mic = gr.Audio(sources=["microphone"], type="filepath", label="Speak the answer (adult voice)")
    ans = gr.Textbox(label="Student answer (editable transcript)")
    out = gr.Textbox(label="Result", lines=7)
    ev = gr.JSON(label="Per-idea NLI evidence")
    dd.change(pick, dd, [q, ref])
    mic.stop_recording(transcribe, mic, ans)
    gr.Button("Score").click(score, [q, ref, ans], [out, ev])
demo.launch(debug=False)
