
from langgraph.graph import StateGraph
from src.core.state import State
from src.agents.nodes import (
    analyze_onboarding_node,
    locate_in_career_tree_node,
    generate_career_plan_node,
    combined_job_trend_node,
    fit_score_from_tree_node,
    tailor_resume_node,
    skill_gap_analyzer_node,
    save_profile_node,
    interview_question_mapping_node
)

# Build LangGraph flow
graph = StateGraph(State)

graph.add_node("AnalyzeOnboarding", analyze_onboarding_node)
graph.add_node("LocateInTree", locate_in_career_tree_node)
graph.add_node("CareerPlan", generate_career_plan_node)
graph.add_node("JobTrends", combined_job_trend_node)
graph.add_node("FitScore", fit_score_from_tree_node)
graph.add_node("TailorResume", tailor_resume_node)
graph.add_node("SkillGapAnalyzer", skill_gap_analyzer_node)
graph.add_node("SaveUserProfile", save_profile_node)
graph.add_node("InterviewQuestionMapping", interview_question_mapping_node)

# Entry point
graph.set_entry_point("LocateInTree")

# Edges
graph.add_edge("LocateInTree", "AnalyzeOnboarding")
graph.add_edge("AnalyzeOnboarding", "CareerPlan")
graph.add_edge("CareerPlan", "JobTrends")       
graph.add_edge("JobTrends", "FitScore")
graph.add_edge("FitScore", "SkillGapAnalyzer")
graph.add_edge("SkillGapAnalyzer", "InterviewQuestionMapping")
graph.add_edge("InterviewQuestionMapping", "TailorResume")
graph.add_edge("TailorResume", "SaveUserProfile")

graph.set_finish_point("SaveUserProfile")

simple_graph = graph.compile()
