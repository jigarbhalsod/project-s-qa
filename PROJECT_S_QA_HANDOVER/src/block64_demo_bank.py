"""New Block 64 interface wrapper. Rubric is retrieved/displayed, not used to score."""
from question_bank import available_grades, available_subjects, question_choices, retrieve

def build_demo(bank, rubrics, scorer):
    import gradio as gr

    def update_subject(subject):
        grades = available_grades(bank, subject)
        return gr.update(choices=grades, value=grades[0] if grades else None)

    def update_grade(subject, grade):
        return gr.update(choices=question_choices(bank, subject, grade), value=None)

    def show_question(question_id):
        if not question_id:
            return "", "", [], "No question selected"
        q, rubric = retrieve(question_id, bank, rubrics)
        status = f"Question: {q['review_status']}; rubric: {rubric['review_status']}"
        if q.get("needs_review"):
            status += " — REVIEW REQUIRED: " + ", ".join(q["needs_review"])
        return q["question_text"], "\n".join(q["reference_answers"]), q["required_concepts"], status

    def score(question_id, answer):
        if not question_id:
            raise ValueError("Select a question first")
        q, rubric = retrieve(question_id, bank, rubrics)
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Enter a student answer")
        result = scorer(q["question_text"], q["reference_answers"][0], answer, dataset="pooled")
        return {"question_id": question_id, "rubric_status": rubric["review_status"], "rubric_used_for_score": False, "prediction": result}

    subjects = available_subjects(bank)
    with gr.Blocks(title="Project S draft question-bank demo") as demo:
        gr.Markdown("Draft bank demonstration. Questions and rubrics require human review; the frozen scorer does not consume rubric fields.")
        subject = gr.Dropdown(choices=subjects, label="Subject", value=subjects[0] if subjects else None)
        grades = available_grades(bank, subjects[0]) if subjects else []
        grade = gr.Dropdown(choices=grades, label="Grade", value=grades[0] if grades else None)
        question = gr.Dropdown(choices=question_choices(bank, subjects[0], grades[0]) if grades else [], label="Question ID")
        prompt = gr.Textbox(label="Question", interactive=False)
        reference = gr.Textbox(label="Reference answer", interactive=False)
        concepts = gr.JSON(label="Draft required concepts")
        status = gr.Textbox(label="Review status", interactive=False)
        answer = gr.Textbox(label="Student answer")
        button = gr.Button("Score with frozen pooled scorer")
        result = gr.JSON(label="Prediction, confidence and review flag")
        subject.change(update_subject, subject, grade)
        grade.change(update_grade, [subject, grade], question)
        question.change(show_question, question, [prompt, reference, concepts, status])
        button.click(score, [question, answer], result)
    return demo
