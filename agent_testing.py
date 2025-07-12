# import os
# import requests
# import json
# import fitz  # PyMuPDF
# import spacy
# import re
# from langgraph.graph import StateGraph
# from typing import TypedDict
# from typing import List, Dict
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from pprint import pprint

# # defining state and typedict for the graph
# class State(TypedDict, total=False):
#     resume: dict
#     career_tree: dict
#     matched_role: str
#     match_score: int
#     current_level: int
#     next_role: str
#     career_plan: str
#     job_trends: str
#     tailored_resume: str
#     location: str
#     target_role: str  # optional (user can choose); overrides auto-next-role 
# # Load Gemini API key
# os.environ["GOOGLE_API_KEY"] = "AIzaSyAgf_aF8rXS8PuwKHlt3fKZaiX0VhfmTPc"
# os.environ["SERP_API_KEY"] = "3ee5d2063d49c83e1501762e639777de6e6c87d6d5d4a14948147a37c8618a95"
# os.environ["RAPIDAPI_KEY"] = "932d130a66mshea167e71c2f82cdp13e7dbjsnb26e597ef597"


# # Initialize Gemini model
# gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", temperature=0.3)

# # for testing (predefined): 

# # Mock resume data
# # mock_resume = {
# #     "name": "Khushi Mahesh",
# #     "skills": ["Python", "Machine Learning", "Data Analysis", "Flask", "SQL"],
# #     "experience": ["Data Science Intern at ABC Corp", "Research Assistant at PES"]
# # }

# # real resume data
# nlp = spacy.load("en_core_web_sm")
# def parse_resume_from_pdf(path: str) -> dict:
#     doc = fitz.open(path)
#     full_text = "\n".join(page.get_text() for page in doc)

#     name = full_text.splitlines()[0].strip()  # naive approach, assume name at top

#     # Extract skills (you can make this smarter)
#     skill_keywords = [
#         "Python", "Java", "C++", "SQL", "Flask", "React", "Django",
#         "Machine Learning", "Deep Learning", "MLOps", "AWS", "Docker", "Git"
#     ]
#     skills = [kw for kw in skill_keywords if kw.lower() in full_text.lower()]

#     # Extract experience lines (very basic)
#     experience_lines = [line.strip() for line in full_text.splitlines() if "intern" in line.lower() or "engineer" in line.lower() or "developer" in line.lower()]

#     return {
#         "name": name,
#         "skills": skills,
#         "experience": experience_lines
#     }
# use_pdf = input("📄 Do you want to upload a resume PDF? (y/n): ").lower().startswith("y")

# if use_pdf:
#     path = input("🔍 Enter path to your resume PDF: ").strip()
#     resume = parse_resume_from_pdf(path)
#     print("✅ Resume parsed!")
#     print("\n📝 Here's what we extracted from your resume:")
#     print("👤 Name:", resume.get("name"))
#     print("🛠  Skills:", ", ".join(resume.get("skills", [])))
#     print("💼 Experience:")
#     for exp in resume.get("experience", []):
#         print("   -", exp)

#     print("\n⚠️  Please review the above information.")
#     input("👉 Press Enter to continue if it looks correct...")

# else:
#     resume = {
#         "name": "Khushi Mahesh",
#         "skills": ["Python", "Machine Learning", "Data Analysis", "Flask", "SQL"],
#         "experience": ["Data Science Intern at ABC Corp", "Research Assistant at PES"]
#     }

# # Mock career tree
# career_tree = {
#     "track": "Choose from Software Engineering, Machine Learning, DevOps, Cybersecurity, Frontend, Backend",
#     "branches": {
#         "Software Engineering": [
#             {
#                 "title": "Junior Software Engineer",
#                 "level": 1,
#                 "skills": ["Python", "Git", "OOP"],
#                 "description": "Assists in writing and testing basic code, debugging issues."
#             },
#             {
#                 "title": "Software Engineer",
#                 "level": 2,
#                 "skills": ["Data Structures", "Algorithms", "SQL", "APIs"],
#                 "description": "Builds scalable systems and APIs with production-ready code."
#             },
#             {
#                 "title": "Senior Software Engineer",
#                 "level": 3,
#                 "skills": ["System Design", "Cloud", "CI/CD", "Code Review"],
#                 "description": "Designs systems, mentors juniors, manages architecture."
#             }
#         ],
#         "Machine Learning": [
#             {
#                 "title": "Data Scientist",
#                 "level": 1,
#                 "skills": ["Python", "EDA", "Machine Learning", "SQL"],
#                 "description": "Analyzes data and builds predictive models."
#             },
#             {
#                 "title": "ML Engineer",
#                 "level": 2,
#                 "skills": ["Deep Learning", "Model Deployment", "MLOps"],
#                 "description": "Deploys, monitors, and scales ML systems."
#             },
#             {
#                 "title": "Senior ML Engineer",
#                 "level": 3,
#                 "skills": ["Distributed Training", "Feature Stores", "Kubernetes"],
#                 "description": "Leads ML infra and handles complex pipeline automation."
#             }
#         ],
#         "DevOps / Cloud": [
#             {
#                 "title": "Cloud Engineer",
#                 "level": 1,
#                 "skills": ["Linux", "AWS", "Terraform", "Shell Scripting"],
#                 "description": "Manages cloud infrastructure and automation scripts."
#             },
#             {
#                 "title": "DevOps Engineer",
#                 "level": 2,
#                 "skills": ["CI/CD", "Docker", "Monitoring", "IaC"],
#                 "description": "Builds pipelines and manages cloud-native deployments."
#             },
#             {
#                 "title": "Site Reliability Engineer",
#                 "level": 3,
#                 "skills": ["Kubernetes", "SLOs/SLIs", "Chaos Engineering"],
#                 "description": "Ensures system reliability at scale using advanced tooling."
#             }
#         ],
#         "Cybersecurity": [
#             {
#                 "title": "Security Analyst",
#                 "level": 1,
#                 "skills": ["Networking", "Linux", "SIEM", "Threat Analysis"],
#                 "description": "Monitors security alerts and investigates threats."
#             },
#             {
#                 "title": "Security Engineer",
#                 "level": 2,
#                 "skills": ["Penetration Testing", "Firewalls", "Encryption", "Scripting"],
#                 "description": "Builds secure systems and fixes vulnerabilities."
#             },
#             {
#                 "title": "Security Architect",
#                 "level": 3,
#                 "skills": ["Zero Trust", "Cloud Security", "Risk Management"],
#                 "description": "Designs and audits end-to-end secure systems."
#             }
#         ],
#         "Frontend Engineering": [
#             {
#                 "title": "Junior Frontend Developer",
#                 "level": 1,
#                 "skills": ["HTML", "CSS", "JavaScript", "Git"],
#                 "description": "Implements UI components and fixes minor issues."
#             },
#             {
#                 "title": "Frontend Developer",
#                 "level": 2,
#                 "skills": ["React", "TypeScript", "Redux", "API Integration"],
#                 "description": "Builds interactive interfaces and connects to backend APIs."
#             },
#             {
#                 "title": "Senior Frontend Engineer",
#                 "level": 3,
#                 "skills": ["System Design", "Performance Optimization", "Web Accessibility"],
#                 "description": "Architects frontend systems and mentors teams."
#             }
#         ],
#         "Backend Engineering": [
#             {
#                 "title": "Backend Developer",
#                 "level": 1,
#                 "skills": ["Python", "Node.js", "SQL", "REST APIs"],
#                 "description": "Implements and maintains backend logic and services."
#             },
#             {
#                 "title": "Backend Engineer",
#                 "level": 2,
#                 "skills": ["Microservices", "Authentication", "Caching", "Message Queues"],
#                 "description": "Builds scalable backend systems with authentication and queues."
#             },
#             {
#                 "title": "Senior Backend Engineer",
#                 "level": 3,
#                 "skills": ["Distributed Systems", "Database Scaling", "System Design"],
#                 "description": "Designs backend architecture for large-scale applications."
#             }
#         ]
#     }
# }

# # nodes: (executing some function or task)

# # Node 1: Match to Career Tree (hierarchical structure)
# def locate_in_career_tree_node(state: State) -> State:
#     resume_skills = set(state["resume"]["skills"])
#     best_level = 0
#     best_match = None
#     max_overlap = 0
    
#     for level in state["career_tree"]["levels"]:
#         overlap = len(resume_skills.intersection(level["skills"]))
#         if overlap > max_overlap:
#             max_overlap = overlap
#             best_level = level["level"]
#             best_match = level["title"]
    
#     # Use manually provided target_role if present
#     next_role = state.get("target_role")
#     if not next_role:
#         next_level = best_level + 1
#         next_role = next((lvl["title"] for lvl in state["career_tree"]["levels"] if lvl["level"] == next_level), None)

#     return {**state, "matched_role": best_match, "current_level": best_level, "next_role": next_role}

# # Node 2: generate career plan using Gemini
# def generate_career_plan_node(state: State) -> State:
#     resume = state["resume"]
#     next_role = state.get("next_role", "Data Scientist")
#     prompt = f"""
#     The user currently has the following skills: {', '.join(resume['skills'])}.
#     They are best matched to the role '{state['matched_role']}' and want to progress to '{next_role}'.

#     Give them a personalized 3-step plan to grow into that next role, mentioning key skills to learn, projects to try, or certifications to get.
#     """
#     plan = gemini.invoke(prompt).content
#     return {**state, "career_plan": plan}

# # this is for career tree comparisons an extra addition for the fitscore 
# def career_tree_level_comparison(user_skills: List[str], career_tree: Dict, target_role: str) -> Dict:
#     levels = career_tree.get("levels", [])
#     matched_level = 0
#     total_levels = len(levels)
#     missing_skills = []
#     user_skillset = set(skill.lower() for skill in user_skills)

#     for level in levels:
#         required_skills = set(skill.lower() for skill in level.get("skills", []))
#         level_number = level.get("level", 0)
#         role_title = level.get("title")

#         overlap = user_skillset.intersection(required_skills)
#         match_ratio = len(overlap) / len(required_skills) if required_skills else 0

#         if match_ratio >= 0.6:  # Consider 60%+ as enough to match that level
#             matched_level = level_number

#         if role_title.lower() == target_role.lower():
#             missing_skills = list(required_skills - user_skillset)
#             break

#     return {
#         "matched_level": matched_level,
#         "total_levels": total_levels,
#         "missing_skills": missing_skills
#     }

# # Node 3: this will be new and better for combined job trend search 
# def combined_job_trend_node(state: State) -> State:
#     role = state.get("target_role") or state.get("matched_role")
#     location = state.get("location", "India")

#     serp_api_key = os.getenv("SERP_API_KEY")
#     rapidapi_key = os.getenv("RAPIDAPI_KEY")

#     jobs = []

#     ## --- Fetch from SerpAPI ---
#     serp_url = f"https://serpapi.com/search.json?q={role} jobs in {location}&engine=google_jobs&hl=en&gl=in&api_key={serp_api_key}"
#     try:
#         serp_resp = requests.get(serp_url)
#         if serp_resp.status_code == 200:
#             serp_data = serp_resp.json()
#             serp_jobs = serp_data.get("jobs_results", [])
#             print(">>> SerpAPI job titles:")
#             for job in serp_jobs[:3]:
#                 print("-", job.get("title"), "@", job.get("company_name"))
#             jobs.extend(serp_jobs)
#     except Exception as e:
#         print("SerpAPI error:", e)

#     ## --- Fetch from JSearch API ---
#     try:
#         headers = {
#             "X-RapidAPI-Key": rapidapi_key,
#             "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
#         }
#         jsearch_url = "https://jsearch.p.rapidapi.com/search"
#         querystring = {"query": f"{role} in {location}", "page": "1", "num_pages": "1"}

#         response = requests.get(jsearch_url, headers=headers, params=querystring)
#         if response.status_code == 200:
#             jsearch_data = response.json()
#             jsearch_jobs = jsearch_data.get("data", [])
#             print(">>> JSearch job titles:")
#             for job in jsearch_jobs[:3]:
#                 print("-", job.get("job_title"), "@", job.get("employer_name"))
#             # Convert to unified structure
#             for job in jsearch_jobs:
#                 jobs.append({
#                     "title": job.get("job_title"),
#                     "company_name": job.get("employer_name"),
#                     "description": job.get("job_description", "")
#                 })
#     except Exception as e:
#         print("JSearch error:", e)

#     # Create summary
#     job_titles = [f"{job.get('title')} @ {job.get('company_name')}" for job in jobs[:5]]
#     summary = f"Top job listings for '{role}' in {location}:\n- " + "\n- ".join(job_titles)

#     return {**state, "job_trends": summary, "live_jobs": jobs}

# # adding a function for the fit score 
# # def calculate_fit_score(resume_skills, job_snippet) -> int:
# #     score = 0
# #     for skill in resume_skills:
# #         if skill.lower() in job_snippet.lower():
# #             score += 1
# #     return score
# # # Node 4 : Now creating the fitscore node 
# # def fit_score_node(state: State) -> State:
# #     resume_skills = state["resume"]["skills"]
# #     jobs = state.get("live_jobs", [])
# #     print(">>> Number of live jobs received:", len(jobs))
# #     scored_jobs = []

# #     for job in jobs:
# #         snippet = job.get("description") or job.get("snippet") or ""
# #         score = calculate_fit_score(resume_skills, snippet)
# #         scored_jobs.append({
# #             "title": job.get("title"),
# #             "company": job.get("company_name"),
# #             "fit_score": score
# #         })

# #     # Sort jobs by fit score (desc)
# #     top_matches = sorted(scored_jobs, key=lambda x: x["fit_score"], reverse=True)[:3]
# #     summary = "\n".join([f"{j['title']} @ {j['company']} → Fit Score: {j['fit_score']}" for j in top_matches])
# #     print(">>> Fit Score Summary:\n", summary)
# #     return {**state, "fit_score_summary": summary}

# # this is the other fitscore version that uses the career tree
# def fit_score_from_tree_node(state: State) -> State:
#     print(">>> fit_score_from_tree_node is running...")
#     user_skills = state["resume"]["skills"]
#     career_tree = state["career_tree"]
#     target_role = state["next_role"]

#     fit = career_tree_level_comparison(user_skills, career_tree, target_role)
#     matched_level = fit["matched_level"]
#     total_levels = fit["total_levels"]
#     missing_skills = fit["missing_skills"]

#     score = round((matched_level / total_levels) * 100) if total_levels else 0

#     summary = f"✅ Your fit score for **{target_role}** is **{score}%**.\n"
#     summary += f"You match level {matched_level} out of {total_levels} in the career path.\n"

#     if missing_skills:
#         summary += "🔧 Skills to learn for the next level:\n"
#         summary += "\n".join(f"- {s}" for s in missing_skills)
#     else:
#         summary += "🎉 You have all the skills required for this role!"
    
#     print(">>> SUMMARY GENERATED:\n", summary)

#     return {**state, "fit_score": score, "fit_score_summary": summary}
# # Node 5 : Tailor Resume using Gemini
# def tailor_resume_node(state: State) -> State:
#     resume = state["resume"]
#     role = state["matched_role"]
    
#     prompt = f"""Tailor the following resume to match the job role: {role}.
    
#     Resume:
#     Name: {resume['name']}
#     Skills: {', '.join(resume['skills'])}
#     Experience: {', '.join(resume['experience'])}
#     """
#     tailored = gemini.invoke(prompt).content
#     return {**state, "tailored_resume": tailored}
# # making an agent to autofill job applications and generate cover letters
# def job_application_agent(resume: dict, target_role: str):

#     print("\n🧠 Job Application Agent is filling your application form...")

#     # Autofill fields from resume
#     name = resume.get("name", "")
#     first_name = name.split()[0]
#     last_name = name.split()[-1] if len(name.split()) > 1 else ""
#     email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
#     phone = "9876543210"
#     linkedin = f"https://www.linkedin.com/in/{first_name.lower()}{last_name.lower()}"
#     github = f"https://github.com/{first_name.lower()}{last_name.lower()}"
#     resume_url = "https://example.com/resume.pdf"

#     # Generate a cover letter using Gemini
#     cover_prompt = f"""
#     Write a personalized cover letter for a {target_role} position based on the following resume:

#     Name: {name}
#     Skills: {', '.join(resume.get('skills', []))}
#     Experience: {', '.join(resume.get('experience', []))}

#     The tone should be professional, enthusiastic, and highlight relevant qualifications.
#     """
#     print("\n📝 Generating cover letter...")
#     cover_letter = gemini.invoke(cover_prompt).content.strip()

#     # Application form dictionary
#     app_form = {
#         "Full Name": name,
#         "Email": email,
#         "Phone": phone,
#         "LinkedIn": linkedin,
#         "GitHub": github,
#         "Resume URL": resume_url,
#         "Target Role": target_role,
#         "Cover Letter": cover_letter
#     }

#     # Allow user to review and optionally edit fields
#     print("\n🔍 Review and edit your application form:")
#     for key in app_form:
#         print(f"\n{key}:")
#         print(app_form[key])
#         user_input = input(f"✏️  Enter new value to edit, or press Enter to keep as is: ").strip()
#         if user_input:
#             app_form[key] = user_input

#     # Save the final form
#     filename_safe = re.sub(r"\W+", "_", name.lower())  # safe file name
#     filepath = f"job_application_{filename_safe}.json"
#     with open(filepath, "w") as f:
#         json.dump(app_form, f, indent=2)

#     print(f"\n✅ Final application saved as '{filepath}'")




# # Build graph (with edges to connect the functionalities of the nodes)

# graph = StateGraph(State)

# graph.add_node("LocateInTree", locate_in_career_tree_node)
# graph.add_node("CareerPlan", generate_career_plan_node)
# graph.add_node("JobTrends", combined_job_trend_node)
# graph.add_node("FitScore", fit_score_from_tree_node)
# graph.add_node("TailorResume", tailor_resume_node)

# graph.set_entry_point("LocateInTree")
# graph.add_edge("LocateInTree", "CareerPlan")
# graph.add_edge("CareerPlan", "JobTrends")
# graph.add_edge("JobTrends", "FitScore")
# graph.add_edge("FitScore", "TailorResume")

# simple_graph = graph.compile()
# # for branching career tree
# print("Available career tracks:")
# for track in career_tree["branches"]:
#     print("-", track)

# chosen_track = input("\n👉 Enter your career track: ").strip()

# if chosen_track not in career_tree["branches"]:
#     raise ValueError("Invalid track selected.")

# track_levels = career_tree["branches"][chosen_track]

# print(f"\nAvailable roles in {chosen_track}:")
# for level in track_levels:
#     print(f"- {level['title']}")

# chosen_role = input("\n🎯 Enter your target role from the list above: ").strip()
# valid_titles = [level["title"] for level in track_levels]
# if chosen_role not in valid_titles:
#     raise ValueError("Invalid role selected.")


# # Run with test data
# initial_state = {
#     "resume": resume,
#     "career_tree": {
#         "track": chosen_track,
#         "levels": track_levels
#     },
#     "location": "India",
#     "target_role": chosen_role
# }

# output = simple_graph.invoke(initial_state)

# # Print the output
# # print(">>> FINAL OUTPUT KEYS:", output.keys())
# pprint({
#     "Matched Role": output.get("matched_role"),
#     "Current Level": output.get("current_level"),
#     "Next Role": output.get("next_role"),
#     "Career Plan": output.get("career_plan"),
#     "Job Trends": output.get("job_trends"),
#     # "Top Job Fit Scores": output.get("fit_score_summary", "[Missing]"),
#     # "Top Job Fit Scores": output.get("fit_score_summary"),
#     "Tailored Resume": output.get("tailored_resume")
# })

# # calling the job application agent after graph execution
# job_application_agent(resume, target_role=output["next_role"])

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

# Load Gemini + API keys
os.environ["GOOGLE_API_KEY"] = "AIzaSyAgf_aF8rXS8PuwKHlt3fKZaiX0VhfmTPc"
os.environ["SERP_API_KEY"] = "3ee5d2063d49c83e1501762e639777de6e6c87d6d5d4a14948147a37c8618a95"
os.environ["RAPIDAPI_KEY"] = "932d130a66mshea167e71c2f82cdp13e7dbjsnb26e597ef597"

gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", temperature=0.3)
nlp = spacy.load("en_core_web_sm")


class State(TypedDict, total=False):
    resume: dict
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
    best_level, best_match, max_overlap = 0, None, 0
    for level in state["career_tree"]["levels"]:
        overlap = len(resume_skills.intersection(level["skills"]))
        if overlap > max_overlap:
            max_overlap = overlap
            best_level = level["level"]
            best_match = level["title"]
    next_role = state.get("target_role") or next((lvl["title"] for lvl in state["career_tree"]["levels"] if lvl["level"] == best_level + 1), None)
    return {**state, "matched_role": best_match, "current_level": best_level, "next_role": next_role}

def generate_career_plan_node(state: State) -> State:
    resume, next_role = state["resume"], state.get("next_role", "Data Scientist")
    prompt = f"""
    The user currently has the following skills: {', '.join(resume['skills'])}.
    They are best matched to the role '{state['matched_role']}' and want to progress to '{next_role}'.
    Give them a personalized 3-step plan to grow into that next role.
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


# Build LangGraph flow
graph = StateGraph(State)
graph.add_node("LocateInTree", locate_in_career_tree_node)
graph.add_node("CareerPlan", generate_career_plan_node)
graph.add_node("JobTrends", combined_job_trend_node)
graph.add_node("FitScore", fit_score_from_tree_node)
graph.add_node("TailorResume", tailor_resume_node)
graph.set_entry_point("LocateInTree")
graph.add_edge("LocateInTree", "CareerPlan")
graph.add_edge("CareerPlan", "JobTrends")
graph.add_edge("JobTrends", "FitScore")
graph.add_edge("FitScore", "TailorResume")
simple_graph = graph.compile()
