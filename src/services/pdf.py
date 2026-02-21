
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def parse_resume_from_pdf(path: str) -> dict:
    try:
        doc = fitz.open(path)
        full_text = "\n".join(page.get_text() for page in doc)

        name = full_text.splitlines()[0].strip()

        skill_keywords = [
            "Python", "Java", "C++", "SQL", "Flask", "React", "Django",
            "Machine Learning", "Deep Learning", "MLOps", "AWS", "Docker", "Git"
        ]
        skills = [kw for kw in skill_keywords if kw.lower() in full_text.lower()]
        experience_lines = [line.strip() for line in full_text.splitlines() if any(word in line.lower() for word in ["intern", "engineer", "developer"])]

        return {"name": name, "skills": skills, "experience": experience_lines}
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return {"name": "Unknown", "skills": [], "experience": []}

def save_application_pdf(data: dict, filename: str = "job_application.pdf"):
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Job Application")
    y -= 30

    c.setFont("Helvetica", 12)
    for key in ["Full Name", "Email", "Phone", "LinkedIn", "GitHub", "Target Role"]:
        c.drawString(50, y, f"{key}: {data.get(key, '')}")
        y -= 20

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Cover Letter:")
    y -= 20

    c.setFont("Helvetica", 11)
    if "Cover Letter" in data:
        for line in data["Cover Letter"].split("\n"):
            for wrapped_line in [line[i:i+90] for i in range(0, len(line), 90)]:
                c.drawString(50, y, wrapped_line)
                y -= 15
                if y < 50:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 11)

    c.save()
