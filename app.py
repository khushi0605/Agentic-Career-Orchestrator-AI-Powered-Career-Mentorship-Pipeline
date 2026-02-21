
import streamlit as st
import json
import os

from src.core.state import State
from src.data.loaders import load_job_descriptions, load_interview_questions
from src.data.career_tree import career_tree
from src.services.pdf import parse_resume_from_pdf
from src.services.llm import gemini
from src.services.analysis import calculate_similarity
from src.ui.multimedia import capture_voice_input, capture_webcam_input
from src.agents.graph import simple_graph
from src.agents.job_agent import job_application_agent

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None
if "graph_output" not in st.session_state:
    st.session_state.graph_output = None
if "relevant_interview_questions" not in st.session_state:
    st.session_state.relevant_interview_questions = []

# Page Config
st.set_page_config(page_title="AI Career Mentor", page_icon="🎓")
st.title("🎯 AI Career Mentorship System")

# User Info
st.subheader("🧑‍💼 User Info")
user_id = st.text_input("Enter your user ID or email")

# Tabs
tab1, tab2, tab3 = st.tabs(["🧠 Mentor Guidance", "📄 Application Agent", "💬 Chat with Mentor"])

# --- TAB 1: Mentor Guidance ---
with tab1:
    st.header("📄 Upload Resume")

    uploaded_file = st.file_uploader("Upload your resume PDF", type=["pdf"])
    if uploaded_file:
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())
        
        try:
            resume = parse_resume_from_pdf("temp_resume.pdf")
            st.session_state.resume_data = resume
            
            st.success("Resume parsed successfully!")
            st.write("👤 **Name:**", resume.get("name", "Unknown"))
            st.write("🛠 **Skills:**", ", ".join(resume.get("skills", [])))
            st.write("💼 **Experience:**")
            for exp in resume.get("experience", []):
                st.write(f"- {exp}")
        except Exception as e:
            st.error(f"Error parsing resume: {e}")

    # Job Search Inputs
    location = st.text_input("📍 Job Search Location", placeholder="India")
    gpa = st.text_input("Enter your GPA (e.g., 8.5)")
    weak_subjects_input = st.text_area("List a few weak subjects (comma-separated)", placeholder="DBMS, OS, Networks")

    # Onboarding Questions
    if "onboarding_step" not in st.session_state:
        st.session_state.onboarding_step = 0
    if "onboarding_answers" not in st.session_state:
        st.session_state.onboarding_answers = {
            "interest": "", "strengths": "", "weaknesses": "", "goals": ""
        }

    questions = [
        ("interest", "What's your area of interest?"),
        ("strengths", "What are your key strengths?"),
        ("weaknesses", "What are some of your weaker areas?"),
        ("goals", "What are your long-term career goals?")
    ]

    step = st.session_state.onboarding_step
    key, prompt = questions[step]
    st.text_input(prompt, key=f"input_{key}", value=st.session_state.onboarding_answers[key])

    col1, col2 = st.columns([1, 1])
    with col1:
        if step > 0 and st.button("⬅️ Back"):
            st.session_state.onboarding_answers[key] = st.session_state[f"input_{key}"]
            st.session_state.onboarding_step -= 1
            st.rerun()

    with col2:
        if step < len(questions) - 1 and st.button("➡️ Next"):
            st.session_state.onboarding_answers[key] = st.session_state[f"input_{key}"]
            st.session_state.onboarding_step += 1
            st.rerun()

    # Track Selection
    job_descriptions = load_job_descriptions()
    
    # Safe fallback if career_tree structure issues or empty
    tracks = list(career_tree.get("branches", {}).keys())
    track = st.selectbox("Choose your career track", tracks) if tracks else None

    if track and job_descriptions:
        filtered_jobs = [job for job in job_descriptions if job.get("career_track") == track]
        roles = [job["title"] for job in filtered_jobs]
        role = st.selectbox("Choose your target role", roles)

        if role:
            selected_job = next((job for job in filtered_jobs if job["title"] == role), None)
            if selected_job:
                st.write(f"## {selected_job['title']} at {selected_job.get('company', 'Unknown')}")
                st.write(f"**Location:** {selected_job.get('location', 'Unknown')}")
                st.write(f"**Required Skills:** {', '.join(selected_job.get('skills_required', []))}")
                st.write(f"**Job Description:** {selected_job.get('description', '')}")

    # Pipeline Execution
    if step == len(questions) - 1:
        st.session_state.onboarding_answers[key] = st.session_state[f"input_{key}"]
        st.markdown("---")
        if st.button("🚀 Run Career Mentorship Pipeline"):
            if user_id:
                state = {
                    "user_id": user_id,
                    "resume": st.session_state.resume_data,
                    "career_tree": {
                        **career_tree, 
                        "track": track # Pass selected track to state
                    },
                    "location": location,
                    "target_role": role,
                    "user_profile": {
                        "GPA": gpa, 
                        "weak_subjects": [s.strip() for s in weak_subjects_input.split(",") if s.strip()]
                    },
                    "onboarding_answers": st.session_state.onboarding_answers,
                    # "job_descriptions": job_descriptions # Don't pass all, let node filter? 
                    # Actually locate_in_career_tree_node loads and selects job description.
                    # We can pass initial empty or let it populate.
                }

                with st.spinner("Running mentorship pipeline..."):
                    # Invoke Graph
                    output = simple_graph.invoke(state)
                    st.session_state.graph_output = output
                    st.session_state.relevant_interview_questions = output.get("relevant_interview_questions", [])
                    st.success("Pipeline executed successfully!")
            else:
                st.warning("Please enter your user ID to proceed.")

    # Interview Interface
    if st.session_state.relevant_interview_questions:
        relevant_questions = st.session_state.relevant_interview_questions
        st.write("### Interview Questions")
        
        # Load dataset for answers
        dataset = load_interview_questions()
        relevant_answers = {}
        
        # Pre-process answers mapping (simplified logic from original)
        if not dataset.empty:
             for idx, question in enumerate(relevant_questions, 1):
                # Simple exact match attempt
                match = dataset[dataset['Question'].str.strip().str.lower() == question.strip().lower()]
                if not match.empty:
                    relevant_answers[idx] = match.iloc[0]['Answer']
                else:
                    relevant_answers[idx] = "No matching answer found in dataset"

        user_answers = {"text": {}, "voice": {}, "webcam": {}, "similarity": {}}

        for idx, question in enumerate(relevant_questions, 1):
            st.subheader(f"Question {idx}: {question}")
            
            # Text Answer
            text_ans = st.text_area(f"Your answer for Q{idx}:", key=f"text_ans_{idx}")
            if text_ans:
                user_answers["text"][idx] = text_ans
                dataset_ans = relevant_answers.get(idx)
                if dataset_ans:
                    sim = calculate_similarity(text_ans, dataset_ans)
                    user_answers["similarity"][idx] = sim
                    st.write(f"**Similarity Score:** {sim*100:.2f}%")

            # Voice Answer
            if st.button(f"🎤 Answer Q{idx} by Voice"):
                voice_ans = capture_voice_input()
                if voice_ans:
                    user_answers["voice"][idx] = voice_ans
                    st.write(f"Voice Response: {voice_ans}")
                    dataset_ans = relevant_answers.get(idx)
                    if dataset_ans:
                         sim = calculate_similarity(voice_ans, dataset_ans)
                         st.write(f"**Similarity Score (Voice):** {sim*100:.2f}%")

            # Webcam Answer
            if st.button(f"📸 Answer Q{idx} using Webcam"):
               # Note: Streamlit execution model might make this tricky with button + camera_input 
               # needing a rerun. For now, we assume user interacts with the camera input if visible.
               st.info("Please use the camera input below if available.")
            
            # Always show camera input if they want to use it
            webcam_res = capture_webcam_input()
            if webcam_res:
                user_answers["webcam"][idx] = webcam_res["emotion"]
                st.write(f"Webcam Emotion: {webcam_res['emotion']}")

    # Results Display
    if st.session_state.graph_output:
        out = st.session_state.graph_output
        st.subheader("🔍 Results")
        st.markdown(f"**Matched Role:** {out.get('matched_role')}")
        st.markdown(f"**Current Level:** {out.get('current_level')}")
        st.markdown(f"**Next Role:** {out.get('next_role')}")
        
        if "career_plan" in out:
            st.markdown("**Career Plan:**")
            st.info(out["career_plan"])
        if "job_trends" in out:
            st.markdown("**Top Job Trends:**")
            st.success(out["job_trends"])
        if "skill_gap_summary" in out:
            st.markdown("**Skill Gap Analysis:**")
            st.warning(out["skill_gap_summary"])
        if "tailored_resume" in out:
             st.markdown("**Tailored Resume:**")
             st.code(out["tailored_resume"])

# --- TAB 2: Job Application ---
with tab2:
    st.header("📄 Job Application Agent")
    if not st.session_state.resume_data or not st.session_state.graph_output:
        st.warning("Please complete the Mentor tab first!")
    else:
        resume = st.session_state.resume_data
        target_role = st.session_state.graph_output.get("next_role")
        
        st.write(f"ℹ️ Generating application for: **{target_role}**")
        
        if st.button("✉️ Generate Application & Cover Letter"):
             with st.spinner("Generating..."):
                 app_form = job_application_agent(resume, target_role)
                 
                 pdf_path = "job_application.pdf"
                 # job_application_agent already saves it, but let's ensure we can read it
                 if os.path.exists(pdf_path):
                     with open(pdf_path, "rb") as f:
                         st.download_button(
                             label="📄 Download Application PDF",
                             data=f.read(),
                             file_name="job_application.pdf",
                             mime="application/pdf"
                         )
                     st.success("Application generated!")
                 else:
                     st.error("Failed to generate PDF.")

# --- TAB 3: Chat ---
with tab3:
    st.header("💬 Talk to Your AI Mentor")
    if not st.session_state.resume_data or not st.session_state.graph_output:
        st.warning("⚠️ Please complete the Resume + Mentor tabs first.")
    else:
        user_input = st.chat_input("Ask anything...")
        if user_input:
            resume = st.session_state.resume_data
            graph = st.session_state.graph_output
            
            context = f"""
            You are an expert career mentor. User Resume: {resume.get('name')}
            Skills: {', '.join(resume.get('skills', []))}
            Matched Role: {graph.get('matched_role')}
            Career Plan: {graph.get('career_plan')}
            
            User: {user_input}
            """
            
            # Simple direct invocation without history context management for now 
            # (Streamlit refreshes history from session state below)
            response = gemini.invoke(context).content
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", response))

        for sender, msg in st.session_state.chat_history:
            st.chat_message("user" if sender == "user" else "assistant").write(msg)