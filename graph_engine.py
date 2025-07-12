# from langgraph.graph import StateGraph
# from state_schema import State
# from agents.mentor_agent import (
#     locate_in_career_tree_node,
#     generate_career_plan_node,
#     fit_score_from_tree_node,
#     tailor_resume_node
# )
# from agents.search_agent import combined_job_trend_node

# def build_career_graph():
#     graph = StateGraph(State)

#     # Add nodes (from mentor and search agents)
#     graph.add_node("LocateInTree", locate_in_career_tree_node)
#     graph.add_node("CareerPlan", generate_career_plan_node)
#     graph.add_node("JobTrends", combined_job_trend_node)
#     graph.add_node("FitScore", fit_score_from_tree_node)
#     graph.add_node("TailorResume", tailor_resume_node)

#     # Define flow
#     graph.set_entry_point("LocateInTree")
#     graph.add_edge("LocateInTree", "CareerPlan")
#     graph.add_edge("CareerPlan", "JobTrends")
#     graph.add_edge("JobTrends", "FitScore")
#     graph.add_edge("FitScore", "TailorResume")

#     return graph.compile()
