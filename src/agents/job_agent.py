
from typing import Dict
from src.services.llm import gemini
from src.services.pdf import save_application_pdf
from src.data.loaders import load_job_descriptions

def job_application_agent(resume: dict, target_role: str) -> Dict:
    job = next((job for job in load_job_descriptions() if job["title"] == target_role), None)
    
    app_form = {}
    if job:
        name = resume.get("name", "")
        parts = name.split()
        first_name = parts[0] if parts else ""
        last_name = parts[-1] if len(parts) > 1 else ""
        
        # Safe defaults
        email = f"{first_name.lower()}.{last_name.lower()}@gmail.com" if first_name else "email@example.com"
        
        prompt = f"""
            Write a personalized cover letter for a {target_role} position based on the following resume:
            Name: {name}
            Skills: {', '.join(resume.get('skills', []))}
            Experience: {', '.join(resume.get('experience', []))}
            Job Description: {job['description']}
            """
        
        cover_letter = gemini.invoke(prompt).content.strip()

        app_form = {
            "Full Name": name,
            "Email": email,
            "Phone": "9876543210",
            "LinkedIn": f"https://www.linkedin.com/in/{first_name.lower()}{last_name.lower()}",
            "GitHub": f"https://github.com/{first_name.lower()}{last_name.lower()}",
            "Resume URL": "https://example.com/resume.pdf",
            "Target Role": target_role,
            "Cover Letter": cover_letter
        }
        
    if app_form:
        save_application_pdf(app_form)
        
    return app_form
