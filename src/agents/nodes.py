
import json
import os
import requests
from typing import List, Dict, Any
from src.core.state import State
from src.core.config import SERP_API_KEY, RAPIDAPI_KEY
from src.services.llm import gemini
from src.data.loaders import load_job_descriptions, load_interview_questions, extract_keywords_from_job_description
import pandas as pd

# Helper function to save user profile
def save_user_profile(user_id, data, folder="user_data"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{user_id}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# Helper function to map keywords to interview questions
def map_keywords_to_interview_questions(keywords: List[str], interview_questions_df: pd.DataFrame) -> List[str]:
    relevant_questions = []
    for idx, row in interview_questions_df.iterrows():
        question_keywords = row['Question'].split(" ")
        for keyword in keywords:
            if any(kw.lower() == keyword.lower() for kw in question_keywords):
                relevant_questions.append(row['Question'])
                break
    return relevant_questions

# Helper: Career tree comparison
def career_tree_level_comparison(user_skills: List[str], career_tree: Dict, target_role: str) -> Dict:
    matched_level, total_levels, missing_skills = 0, len(career_tree.get("levels", [])), []
    user_skillset = set(skill.lower() for skill in user_skills)
    for level in career_tree.get("levels", []):
        required_skills = set(skill.lower() for skill in level.get("skills", []))
        if required_skills and len(user_skillset.intersection(required_skills)) / len(required_skills) >= 0.6:
            matched_level = level["level"]
        if level.get("title", "").lower() == target_role.lower():
            missing_skills = list(required_skills - user_skillset)
            break
    return {"matched_level": matched_level, "total_levels": total_levels, "missing_skills": missing_skills}


# --- NODES ---

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
    updated_profile = {**state.get("user_profile", {}), "onboarding_summary": gemini_response}
    return {**state, "user_profile": updated_profile}


def locate_in_career_tree_node(state: State) -> State:
    resume_skills = set(state["resume"]["skills"])
    track = state["career_tree"].get("track", "Software Engineering")
    # Access branches safely
    branches = state["career_tree"].get("branches", {})
    levels = branches.get(track, [])

    best_level, best_match, max_overlap = 0, None, 0
    for level in levels:
        overlap = len(resume_skills.intersection(level["skills"]))
        if overlap > max_overlap:
            max_overlap = overlap
            best_level = level["level"]
            best_match = level["title"]

    next_role = state.get("target_role") or next((lvl["title"] for lvl in levels if lvl["level"] == best_level + 1), None)

    job_descriptions = load_job_descriptions()
    selected_job = next((job for job in job_descriptions if job.get("career_track") == track and job.get("title") == best_match), None)

    if selected_job:
        state["job_descriptions"] = [selected_job] # Store as list as per State definition

    # Add levels to career_tree in state for later nodes
    updated_career_tree = {**state["career_tree"], "levels": levels}
    
    return {
        **state,
        "matched_role": best_match,
        "current_level": best_level,
        "next_role": next_role,
        "career_tree": updated_career_tree
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
        - Resume Skills: {', '.join(resume.get('skills', []))}
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


def combined_job_trend_node(state: State) -> State:
    role = state.get("target_role") or state.get("matched_role")
    location = state.get("location", "India")
    
    jobs = []
    
    # SerpAPI
    try:
        if SERP_API_KEY:
            serp_url = f"https://serpapi.com/search.json?q={role} jobs in {location}&engine=google_jobs&hl=en&gl=in&api_key={SERP_API_KEY}"
            serp_resp = requests.get(serp_url)
            if serp_resp.status_code == 200:
                jobs.extend(serp_resp.json().get("jobs_results", []))
    except Exception as e:
        print(f"SerpAPI Error: {e}")

    # RapidAPI
    try:
        if RAPIDAPI_KEY:
            headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
            jsearch_resp = requests.get("https://jsearch.p.rapidapi.com/search", headers=headers, params={"query": f"{role} in {location}", "page": "1"})
            if jsearch_resp.status_code == 200:
                for job in jsearch_resp.json().get("data", []):
                    jobs.append({"title": job.get("job_title"), "company_name": job.get("employer_name"), "description": job.get("job_description", "")})
    except Exception as e:
        print(f"RapidAPI Error: {e}")

    summary = f"Top job listings for '{role}' in {location}:\n- " + "\n- ".join([f"{j.get('title')} @ {j.get('company_name')}" for j in jobs[:5]])
    return {**state, "job_trends": summary} # live_jobs removed from State type dict above, checking... explicit State def has no live_jobs, but TypedDict allows extras if not strict? The def had total=False.
    # Actually wait, State def in original code had live_jobs? 
    # Checking my src/core/state.py... I did NOT include live_jobs in the explicit fields. 
    # But State(TypedDict, total=False) allows adding keys. So it should be fine.


def fit_score_from_tree_node(state: State) -> State:
    user_skills = state["resume"]["skills"]
    career_tree_data = state["career_tree"]
    target_role = state.get("next_role") or state.get("matched_role")
    
    fit = career_tree_level_comparison(user_skills, career_tree_data, target_role)
    score = round((fit["matched_level"] / fit["total_levels"]) * 100) if fit["total_levels"] else 0
    
    summary = f"✅ Your fit score for **{target_role}** is **{score}%**.\nYou match level {fit['matched_level']} out of {fit['total_levels']}.\n"
    if fit["missing_skills"]:
        summary += "🔧 Skills to learn:\n" + "\n".join(f"- {s}" for s in fit["missing_skills"])
    else:
        summary += "🎉 You have all the skills required for this role!"
        
    return {**state, "match_score": score, "skill_gap_summary": summary} # Mapping fit_score to match_score for consistency with State



def tailor_resume_node(state: State) -> State:
    resume = state["resume"]
    role = state["matched_role"]
    prompt = f"""Tailor the following resume to match the job role: {role}.
    Name: {resume['name']}
    Skills: {', '.join(resume['skills'])}
    Experience: {', '.join(resume['experience'])}"""
    tailored = gemini.invoke(prompt).content
    return {**state, "tailored_resume": tailored}


def skill_gap_analyzer_node(state: State) -> State:
    user_profile = state.get("user_profile", {})
    resume_skills = set(state["resume"].get("skills", []))
    quiz_skills = set(user_profile.get("quiz_skills", []))
    jd_skills = set(state.get("jd_skills", []))
    combined_skills = resume_skills.union(quiz_skills).union(jd_skills)

    target_role = state.get("target_role") or state.get("next_role")
    career_tree_data = state["career_tree"]
    
    # Logic to find matched branch is a bit redundant with locate_node but needed here if state doesn't have it explicitly
    # But we passed 'levels' in career_tree in locate_node.
    levels = career_tree_data.get("levels", [])
    matched_level_data = next((lvl for lvl in levels if lvl["title"].lower() == target_role.lower()), None)

    if not matched_level_data:
        # Fallback search if levels not populated or role changes
        track = career_tree_data.get("track")
        if track:
             levels = career_tree_data.get("branches", {}).get(track,[])
             matched_level_data = next((lvl for lvl in levels if lvl["title"].lower() == target_role.lower()), None)

    if not matched_level_data:
        return {**state, "skill_gap_summary": "❌ Role not found in career tree."}

    required_skills = set(skill.lower() for skill in matched_level_data.get("skills", []))
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


def interview_question_mapping_node(state: State) -> State:
    # Logic to extract keywords from JD and map to questions
    selected_jobs = state.get("job_descriptions", [])
    selected_job = None
    if isinstance(selected_jobs, list) and selected_jobs:
        selected_job = selected_jobs[0]
    elif isinstance(selected_jobs, dict):
        selected_job = selected_jobs

    if selected_job and "description" in selected_job:
        job_description = selected_job["description"]
        job_keywords = extract_keywords_from_job_description(job_description)
        
        # Load questions
        interview_questions_df = load_interview_questions()
        
        relevant_questions = map_keywords_to_interview_questions(job_keywords, interview_questions_df)
        state["relevant_interview_questions"] = relevant_questions
    
    return state


def save_profile_node(state: State) -> State:
    user_id = state.get("user_id", "guest")
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
        "match_score": state.get("match_score", ""),
        "job_descriptions": state.get("job_descriptions", []),
        "relevant_interview_questions": state.get("relevant_interview_questions", [])
    })
    return state
