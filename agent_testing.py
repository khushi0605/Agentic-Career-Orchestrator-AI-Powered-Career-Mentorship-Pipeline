# # new code:
import os
import requests
import json
import fitz  # PyMuPDF
import spacy
import re
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from scraper_agent import fetch_scraped_data

# Load Gemini + API keys
os.environ["GOOGLE_API_KEY"] = "AIzaSyAgf_aF8rXS8PuwKHlt3fKZaiX0VhfmTPc"
os.environ["SERP_API_KEY"] = "3ee5d2063d49c83e1501762e639777de6e6c87d6d5d4a14948147a37c8618a95"
os.environ["RAPIDAPI_KEY"] = "932d130a66mshea167e71c2f82cdp13e7dbjsnb26e597ef597"

# gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", temperature=0.3)
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
nlp = spacy.load("en_core_web_sm")


class State(TypedDict, total=False):
    resume: dict
    user_id: str
    career_tree: dict
    matched_role: str
    match_score: int
    current_level: int
    next_role: str
    career_plan: str
    job_trends: str
    tailored_resume: str
    location: str
    target_role: str
    user_profile: dict
    onboarding_answers: dict
    jd_skills: List[str]

    matched_skills: List[str]
    missing_skills: List[str]
    skill_match_score: int
    skill_gap_summary: str

    interview_questions: List[str]
    interview_feedback: str

# Function to save user profile data in a json file 
def save_user_profile(user_id, data, folder="user_data"):
    os.makedirs(folder, exist_ok=True)  # ensure folder exists
    filepath = os.path.join(folder, f"{user_id}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# for pdf conversion 
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
    for line in data["Cover Letter"].split("\n"):
        for wrapped_line in [line[i:i+90] for i in range(0, len(line), 90)]:
            c.drawString(50, y, wrapped_line)
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 11)

    c.save()


def parse_resume_from_pdf(path: str) -> dict:
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


def analyze_onboarding_node(state: State) -> State:
    onboarding_answers = state.get("onboarding_answers", {})
    if not onboarding_answers:
        return state

    prompt = f"""
    Analyze the following onboarding answers and extract:
    1. Career goals
    2. Interests
    3. Strengths
    4. Weaknesses

    Answers:
    - Why are you interested in this field? {onboarding_answers.get('interest')}
    - What are your strengths? {onboarding_answers.get('strengths')}
    - What are your weaknesses? {onboarding_answers.get('weaknesses')}
    - What are your short- and long-term goals? {onboarding_answers.get('goals')}
    """

    gemini_response = gemini.invoke(prompt).content

    # Optionally, you can parse key insights using regex or just store the raw response
    updated_profile = {**state.get("user_profile", {}), "onboarding_summary": gemini_response}
    return {**state, "user_profile": updated_profile}

def skill_gap_analyzer_node(state: State) -> State:
    user_profile = state.get("user_profile", {})
    resume_skills = set(state["resume"].get("skills", []))
    quiz_skills = set(user_profile.get("quiz_skills", []))  # optional quiz result
    jd_skills = set(state.get("jd_skills", []))              # from job description or scraped JD
    combined_skills = resume_skills.union(quiz_skills).union(jd_skills)

    target_role = state.get("target_role") or state.get("next_role")
    career_tree_data = state["career_tree"]
    matched_branch = None

    # Find correct branch and level in career tree
    for branch in career_tree_data["branches"].values():
        for level in branch:
            if level["title"].lower() == target_role.lower():
                matched_branch = level
                break
        if matched_branch:
            break

    if not matched_branch:
        return {**state, "skill_gap_analysis": "❌ Role not found in career tree."}

    required_skills = set(skill.lower() for skill in matched_branch["skills"])
    user_skillset = set(skill.lower() for skill in combined_skills)

    matched = list(user_skillset.intersection(required_skills))
    missing = list(required_skills - user_skillset)
    score = round((len(matched) / len(required_skills or [1])) * 100)

    summary = f"""🔎 Skill Gap Analysis for **{target_role}**:
✅ Matched: {', '.join(matched) or 'None'}
❌ Missing: {', '.join(missing) or 'None'}
📊 Match Score: {score}%
"""

    return {
        **state,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_match_score": score,
        "skill_gap_summary": summary
   }

### ^all onboarding nodes 
career_tree = {
    "track": "Choose from Software Engineering, Machine Learning, DevOps, Cybersecurity, Frontend, Backend",
    "branches": {
        "Software Engineering": [
            {
                "title": "Junior Software Engineer",
                "level": 1,
                "skills": ["Python", "Git", "OOP"],
                "description": "Assists in writing and testing basic code, debugging issues."
            },
            {
                "title": "Software Engineer",
                "level": 2,
                "skills": ["Data Structures", "Algorithms", "SQL", "APIs"],
                "description": "Builds scalable systems and APIs with production-ready code."
            },
            {
                "title": "Senior Software Engineer",
                "level": 3,
                "skills": ["System Design", "Cloud", "CI/CD", "Code Review"],
                "description": "Designs systems, mentors juniors, manages architecture."
            }
        ],
        "Machine Learning": [
            {
                "title": "Data Scientist",
                "level": 1,
                "skills": ["Python", "EDA", "Machine Learning", "SQL"],
                "description": "Analyzes data and builds predictive models."
            },
            {
                "title": "ML Engineer",
                "level": 2,
                "skills": ["Deep Learning", "Model Deployment", "MLOps"],
                "description": "Deploys, monitors, and scales ML systems."
            },
            {
                "title": "Senior ML Engineer",
                "level": 3,
                "skills": ["Distributed Training", "Feature Stores", "Kubernetes"],
                "description": "Leads ML infra and handles complex pipeline automation."
            }
        ],
        "DevOps / Cloud": [
            {
                "title": "Cloud Engineer",
                "level": 1,
                "skills": ["Linux", "AWS", "Terraform", "Shell Scripting"],
                "description": "Manages cloud infrastructure and automation scripts."
            },
            {
                "title": "DevOps Engineer",
                "level": 2,
                "skills": ["CI/CD", "Docker", "Monitoring", "IaC"],
                "description": "Builds pipelines and manages cloud-native deployments."
            },
            {
                "title": "Site Reliability Engineer",
                "level": 3,
                "skills": ["Kubernetes", "SLOs/SLIs", "Chaos Engineering"],
                "description": "Ensures system reliability at scale using advanced tooling."
            }
        ],
        "Cybersecurity": [
            {
                "title": "Security Analyst",
                "level": 1,
                "skills": ["Networking", "Linux", "SIEM", "Threat Analysis"],
                "description": "Monitors security alerts and investigates threats."
            },
            {
                "title": "Security Engineer",
                "level": 2,
                "skills": ["Penetration Testing", "Firewalls", "Encryption", "Scripting"],
                "description": "Builds secure systems and fixes vulnerabilities."
            },
            {
                "title": "Security Architect",
                "level": 3,
                "skills": ["Zero Trust", "Cloud Security", "Risk Management"],
                "description": "Designs and audits end-to-end secure systems."
            }
        ],
        "Frontend Engineering": [
            {
                "title": "Junior Frontend Developer",
                "level": 1,
                "skills": ["HTML", "CSS", "JavaScript", "Git"],
                "description": "Implements UI components and fixes minor issues."
            },
            {
                "title": "Frontend Developer",
                "level": 2,
                "skills": ["React", "TypeScript", "Redux", "API Integration"],
                "description": "Builds interactive interfaces and connects to backend APIs."
            },
            {
                "title": "Senior Frontend Engineer",
                "level": 3,
                "skills": ["System Design", "Performance Optimization", "Web Accessibility"],
                "description": "Architects frontend systems and mentors teams."
            }
        ],
        "Backend Engineering": [
            {
                "title": "Backend Developer",
                "level": 1,
                "skills": ["Python", "Node.js", "SQL", "REST APIs"],
                "description": "Implements and maintains backend logic and services."
            },
            {
                "title": "Backend Engineer",
                "level": 2,
                "skills": ["Microservices", "Authentication", "Caching", "Message Queues"],
                "description": "Builds scalable backend systems with authentication and queues."
            },
            {
                "title": "Senior Backend Engineer",
                "level": 3,
                "skills": ["Distributed Systems", "Database Scaling", "System Design"],
                "description": "Designs backend architecture for large-scale applications."
            }
        ]
    }
}

def locate_in_career_tree_node(state: State) -> State:
    resume_skills = set(state["resume"]["skills"])
    track = state["career_tree"].get("track", "Software Engineering")
    levels = state["career_tree"]["branches"][track]

    best_level, best_match, max_overlap = 0, None, 0
    for level in levels:
        overlap = len(resume_skills.intersection(level["skills"]))
        if overlap > max_overlap:
            max_overlap = overlap
            best_level = level["level"]
            best_match = level["title"]

    next_role = state.get("target_role") or next((lvl["title"] for lvl in levels if lvl["level"] == best_level + 1), None)

    # ✅ add "levels" back into the state for later nodes to use
    return {
        **state,
        "matched_role": best_match,
        "current_level": best_level,
        "next_role": next_role,
        "career_tree": {**state["career_tree"], "levels": levels}
    }

def generate_career_plan_node(state: State) -> State:
    resume = state.get("resume", {})
    onboarding = state.get("onboarding_answers", {})
    user_profile = state.get("user_profile", {})
    gpa = user_profile.get("GPA", "N/A")
    weak_subjects = user_profile.get("weak_subjects", [])
    target_role = state.get("next_role", "Data Scientist")
    prompt = f"""
        The user is being onboarded into an AI career mentorship system.

        They currently have:
        - Resume Skills: {', '.join(resume['skills'])}
        - GPA: {gpa}
        - Weak Subjects: {', '.join(weak_subjects)}
        - Onboarding Info:
            - Interests: {onboarding.get('interest')}
            - Strengths: {onboarding.get('strengths')}
            - Weaknesses: {onboarding.get('weaknesses')}
            - Goals: {onboarding.get('goals')}
        - Target Role: {target_role}

        Using this information, generate a mentorship-style career plan that includes:
        1. Where They Are Now (summary)
        2. Where They Want to Go (goals)
        3. Key Growth Areas (technical, academic, soft skills)
        4. Actionable Milestones (what to build, practice, or review)
        5. How a Mentor Can Help
        6. A Recommended 3-Month Roadmap

        Be specific, clear, and motivational.
        """

    plan = gemini.invoke(prompt).content
    return {**state, "career_plan": plan}

def career_tree_level_comparison(user_skills: List[str], career_tree: Dict, target_role: str) -> Dict:
    matched_level, total_levels, missing_skills = 0, len(career_tree.get("levels", [])), []
    user_skillset = set(skill.lower() for skill in user_skills)
    for level in career_tree["levels"]:
        required_skills = set(skill.lower() for skill in level.get("skills", []))
        if len(user_skillset.intersection(required_skills)) / len(required_skills or [1]) >= 0.6:
            matched_level = level["level"]
        if level.get("title", "").lower() == target_role.lower():
            missing_skills = list(required_skills - user_skillset)
            break
    return {"matched_level": matched_level, "total_levels": total_levels, "missing_skills": missing_skills}

def combined_job_trend_node(state: State) -> State:
    role, location = state.get("target_role") or state.get("matched_role"), state.get("location", "India")
    serp_api_key, rapidapi_key = os.getenv("SERP_API_KEY"), os.getenv("RAPIDAPI_KEY")
    jobs = []
    try:
        serp_resp = requests.get(f"https://serpapi.com/search.json?q={role} jobs in {location}&engine=google_jobs&hl=en&gl=in&api_key={serp_api_key}")
        if serp_resp.status_code == 200:
            jobs.extend(serp_resp.json().get("jobs_results", []))
    except Exception: pass
    try:
        headers = {"X-RapidAPI-Key": rapidapi_key, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
        jsearch_resp = requests.get("https://jsearch.p.rapidapi.com/search", headers=headers, params={"query": f"{role} in {location}", "page": "1"})
        if jsearch_resp.status_code == 200:
            for job in jsearch_resp.json().get("data", []):
                jobs.append({"title": job.get("job_title"), "company_name": job.get("employer_name"), "description": job.get("job_description", "")})
    except Exception: pass
    summary = f"Top job listings for '{role}' in {location}:\n- " + "\n- ".join([f"{j.get('title')} @ {j.get('company_name')}" for j in jobs[:5]])
    return {**state, "job_trends": summary, "live_jobs": jobs}

def fit_score_from_tree_node(state: State) -> State:
    user_skills, career_tree_data, target_role = state["resume"]["skills"], state["career_tree"], state["next_role"]
    fit = career_tree_level_comparison(user_skills, career_tree_data, target_role)
    score = round((fit["matched_level"] / fit["total_levels"]) * 100) if fit["total_levels"] else 0
    summary = f"✅ Your fit score for **{target_role}** is **{score}%**.\nYou match level {fit['matched_level']} out of {fit['total_levels']}.\n"
    if fit["missing_skills"]:
        summary += "🔧 Skills to learn:\n" + "\n".join(f"- {s}" for s in fit["missing_skills"])
    else:
        summary += "🎉 You have all the skills required for this role!"
    return {**state, "fit_score": score, "fit_score_summary": summary}


# def fetch_interview_questions(role: str) -> List[str]:
#     serp_api_key = os.getenv("SERP_API_KEY")
#     query = f"{role} interview questions site:geeksforgeeks.org"

#     url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={serp_api_key}"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             results = response.json().get("organic_results", [])
#             article_texts = [r.get("snippet", "") for r in results if "question" in r.get("snippet", "").lower()]

#             if not article_texts:
#                 return ["⚠️ No direct questions found. Try again later."]

#             # Ask Gemini to extract actual questions from the text
#             raw_text = "\n".join(article_texts[:3])
#             prompt = f"""From the following text snippets, extract 5 clear interview questions only.
# Snippets:
# {raw_text}
# Output: List them clearly."""
#             return gemini.invoke(prompt).content.strip().split("\n")
#     except Exception as e:
#         return [f"❌ Error fetching questions: {str(e)}"]

#testing the api results:
def fetch_interview_questions(role: str) -> List[str]:
    serp_api_key = os.getenv("SERP_API_KEY")
    query = f"{role} interview questions site:geeksforgeeks.org"
    url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={serp_api_key}"

    try:
        response = requests.get(url)

        # ⬇️ DEBUG: Print status and raw response
        print("Status code:", response.status_code)
        print("Raw JSON:", response.json())

        if response.status_code == 200:
            results = response.json().get("organic_results", [])

            # ⬇️ DEBUG: Print full result list
            print("Organic Results:", results)

            article_texts = [r.get("snippet", "") for r in results if r.get("snippet", "")]

            if not article_texts:
                return ["⚠️ No snippet content found."]

            # Ask Gemini to extract actual questions from the text
            raw_text = "\n".join(article_texts[:3])

            # ⬇️ DEBUG: What Gemini will receive
            print("Snippets sent to Gemini:\n", raw_text)

            prompt = f"""From the following text snippets, extract 5 clear interview questions only.
Snippets:
{raw_text}
Output: List them clearly."""

            return gemini.invoke(prompt).content.strip().split("\n")

    except Exception as e:
        return [f"❌ Error fetching questions: {str(e)}"]


def interview_agent_node(state: State) -> State:
    role = state.get("target_role") or state.get("matched_role") or "Software Engineer"
    questions = fetch_interview_questions(role)
    question_1 = questions[0] if questions else "Tell me about a recent project."

    # Save in session for next step
    return {
        **state,
        "interview_questions": questions,
        "current_interview_question": question_1,
        "interview_feedback": "💬 Waiting for your answer..."
    }

# new interview node with scraping agent 

# def web_scraping_node(state: State) -> State:
#     role = state.get("target_role", "software engineer")
#     location = state.get("location", "India")
#     interest = state.get("onboarding_answers", {}).get("interest", "AI")

#     scraped_data = fetch_scraped_data(role, location, interest)

#     return {**state, **scraped_data}
def web_scraping_node(state: State) -> State:
    try:
        scraped = fetch_scraped_data(role=state.get("target_role", "Software Engineer"))
        return {
            **state,
            "jobs": scraped.get("jobs", []),
            "courses": scraped.get("courses", []),
            "interview_questions": scraped.get("interview_questions", [])
        }
    except Exception as e:
        print("Scraper error:", e)
        return state


def tailor_resume_node(state: State) -> State:
    resume, role = state["resume"], state["matched_role"]
    prompt = f"""Tailor the following resume to match the job role: {role}.
    Name: {resume['name']}
    Skills: {', '.join(resume['skills'])}
    Experience: {', '.join(resume['experience'])}"""
    tailored = gemini.invoke(prompt).content
    return {**state, "tailored_resume": tailored}

def job_application_agent(resume: dict, target_role: str) -> Dict:
    name = resume.get("name", "")
    first_name, last_name = name.split()[0], name.split()[-1] if len(name.split()) > 1 else ""
    app_form = {
        "Full Name": name,
        "Email": f"{first_name.lower()}.{last_name.lower()}@gmail.com",
        "Phone": "9876543210",
        "LinkedIn": f"https://www.linkedin.com/in/{first_name.lower()}{last_name.lower()}",
        "GitHub": f"https://github.com/{first_name.lower()}{last_name.lower()}",
        "Resume URL": "https://example.com/resume.pdf",
        "Target Role": target_role,
        "Cover Letter": gemini.invoke(f"""
        Write a personalized cover letter for a {target_role} position based on the following resume:
        Name: {name}
        Skills: {', '.join(resume.get('skills', []))}
        Experience: {', '.join(resume.get('experience', []))}
        """).content.strip()
    }
    save_application_pdf(app_form)
    return app_form

def save_profile_node(state):
    user_id = state["user_id"]
    save_user_profile(user_id, {
        "resume": state.get("resume"),
        "user_profile": state.get("user_profile"),
        "onboarding_answers": state.get("onboarding_answers", {}),
        "location": state.get("location"),
        "target_role": state.get("target_role"),
        "track": state.get("career_tree", {}).get("track"),
        "career_plan": state.get("career_plan", ""),
        "job_trends": state.get("job_trends", ""),
        "matched_role": state.get("matched_role", ""),
        "next_role": state.get("next_role", ""),
        "match_score": state.get("match_score", "")
    })
    return state



# Build LangGraph flow
graph = StateGraph(State)

graph.add_node("AnalyzeOnboarding", analyze_onboarding_node)
graph.add_node("LocateInTree", locate_in_career_tree_node)
graph.add_node("CareerPlan", generate_career_plan_node)
graph.add_node("JobTrends", combined_job_trend_node)
graph.add_node("FitScore", fit_score_from_tree_node)
graph.add_node("TailorResume", tailor_resume_node)
graph.add_node("SkillGapAnalyzer", skill_gap_analyzer_node)
graph.add_node("InterviewAgent", interview_agent_node)
graph.add_node("SaveUserProfile", save_profile_node)
graph.add_node("ScrapeWebInfo", web_scraping_node)
# Entry point
graph.set_entry_point("LocateInTree")
# Edges
graph.add_edge("LocateInTree", "AnalyzeOnboarding")
graph.add_edge("AnalyzeOnboarding", "CareerPlan")
graph.add_edge("CareerPlan", "JobTrends")       
graph.add_edge("JobTrends", "FitScore")
graph.add_edge("FitScore", "SkillGapAnalyzer")
graph.add_edge("SkillGapAnalyzer", "TailorResume")
graph.add_edge("TailorResume", "InterviewAgent")
graph.add_edge("InterviewAgent", "ScrapeWebInfo")
graph.add_edge("InterviewAgent", "ScrapeWebInfo")
graph.add_edge("ScrapeWebInfo", "SaveUserProfile")
graph.set_finish_point("SaveUserProfile")
simple_graph = graph.compile()
