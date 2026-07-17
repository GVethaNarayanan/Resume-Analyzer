import gradio as gr
import pdfplumber
import json
import os

# Load job roles
with open("jobs.json", "r") as f:
    JOBS = json.load(f)


# Extract text from PDF
def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file.name) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.lower()


# Analyze Resume
def analyze_resume(pdf_file, role):

    resume_text = extract_text(pdf_file)

    required_skills = JOBS[role]

    found_skills = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            found_skills.append(skill)

    missing_skills = [
        skill for skill in required_skills
        if skill not in found_skills
    ]

    score = int((len(found_skills) / len(required_skills)) * 100)

    if score >= 80:
        status = "✅ Highly Recommended"
        recommendation = (
            "Excellent! Your resume is a strong match for this role. "
            "Keep updating it with your latest projects, certifications, and achievements."
        )

    elif score >= 60:
        status = "🟡 Recommended"
        recommendation = (
            "Good match! Improving the missing skills listed below can significantly increase your ATS score."
        )

    else:
        status = "❌ Not Eligible"
        recommendation = (
            "Your resume lacks several important skills for this role. "
            "Learn the missing skills, build projects, and update your resume before applying."
        )

    report = f"""
📌 Role Applied: {role}

🎯 ATS Score: {score}%

📈 Status:
{status}

✅ Skills Found:
{', '.join(found_skills) if found_skills else 'None'}

❌ Missing Skills:
{', '.join(missing_skills) if missing_skills else 'None'}

💡 Recommendation:
{recommendation}

⭐ Thank you for using AI Resume Analyzer.
"""

    return report


# Gradio Interface
demo = gr.Interface(
    fn=analyze_resume,

    inputs=[
        gr.File(label="📄 Upload Resume (PDF)"),

        gr.Dropdown(
            choices=list(JOBS.keys()),
            label="💼 Select Job Role"
        )
    ],

    outputs=gr.Textbox(
        lines=18,
        label="📋 Resume Analysis Report"
    ),

    title="🤖 AI Resume Analyzer",

    description="""
Upload your resume, select a job role, and receive an ATS score with personalized feedback.

Developed by **Vetha Narayanan**
""",

    theme=gr.themes.Soft()
)


# Launch App
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
