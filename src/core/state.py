
from typing import TypedDict, List, Dict

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
    relevant_interview_questions: List[str]
    job_descriptions: List[dict]
