import gradio as gr
import pdfplumber
import json

with open("jobs.json", "r") as f:
    JOBS = json.load(f)

def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file.name) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text.lower()

def analyze_resume(pdf_file, role):

    resume_text = extract_text(pdf_file)

    required_skills = JOBS[role]

    found_skills = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            found_skills.append(skill)

    missing_skills = list(set(required_skills) - set(found_skills))

    score = int((len(found_skills) / len(required_skills)) * 100)

    if score >= 80:
        status = "✅ Highly Recommended"

    elif score >= 60:
        status = "🟡 Recommended"

    else:
        status = "❌ Not Eligible"

    recommendation = ""

    if score < 60:
        recommendation = (
            "Your resume lacks important skills required "
            "for this role. Learn the missing skills and update your resume."
        )

    report = f"""
Role Applied: {role}

ATS Score: {score}%

Status: {status}

Skills Found:
{', '.join(found_skills) if found_skills else 'None'}

Missing Skills:
{', '.join(missing_skills) if missing_skills else 'None'}

Recommendation:
{recommendation}
"""

    return report

demo = gr.Interface(
    fn=analyze_resume,
    inputs=[
        gr.File(label="Upload Resume PDF"),
        gr.Dropdown(
            choices=list(JOBS.keys()),
            label="Select Job Role"
        )
    ],
    outputs=gr.Textbox(
        lines=15,
        label="Resume Analysis Report"
    ),
    title="Resume Analyzer MLOps",
    description="Upload Resume and Check ATS Score"
)

demo.launch(server_name="0.0.0.0", server_port=7860)