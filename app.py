import streamlit as st
import json
from pprint import pprint
from agent_testing import (
    parse_resume_from_pdf,
    simple_graph,
    job_application_agent,
    career_tree,
    gemini,
    save_application_pdf,
    map_keywords_to_interview_questions,
    interview_question_mapping_node,
    extract_keywords_from_job_description,
    load_interview_questions
)

# ✅ Initialize chat memory BEFORE anything else
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "resume_data" not in st.session_state:
    st.session_state.resume_data = None

if "graph_output" not in st.session_state:
    st.session_state.graph_output = None
#initialize relevant interview questions
if "relevant_interview_questions" not in st.session_state:
    st.session_state.relevant_interview_questions = []


# Load job descriptions from a JSON file
def load_job_descriptions():
    try:
        with open('job_descriptions.json', 'r') as f:
            job_descriptions = json.load(f)
        return job_descriptions
    except Exception as e:
        st.error(f"Error loading job descriptions: {e}")
        return []



# Initialize Streamlit interface
st.set_page_config(page_title="AI Career Mentor", page_icon="🎓")
st.title("🎯 AI Career Mentorship System")

# User Info Section
st.subheader("🧑‍💼 User Info")
user_id = st.text_input("Enter your user ID or email")

# Tabs for functionality
tab1, tab2, tab3 = st.tabs(["🧠 Mentor Guidance", "📄 Application Agent", "💬 Chat with Mentor"])

# Upload Resume
with tab1:
    st.header("📄 Upload Resume")

    uploaded_file = st.file_uploader("Upload your resume PDF", type=["pdf"])
    if uploaded_file:
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())
        resume = parse_resume_from_pdf("temp_resume.pdf")
        st.session_state.resume_data = resume

        st.success("Resume parsed successfully!")
        st.write("👤 **Name:**", resume["name"])
        st.write("🛠 **Skills:**", ", ".join(resume["skills"]))
        st.write("💼 **Experience:**")
        for exp in resume["experience"]:
            st.write(f"- {exp}")

    # Job Search Location and GPA Input
    location = st.text_input("📍 Job Search Location", placeholder="India")
    gpa = st.text_input("Enter your GPA (e.g., 8.5)")
    weak_subjects_input = st.text_area("List a few weak subjects (comma-separated)", placeholder="DBMS, OS, Networks")

    # Onboarding Questions for User Profile
    if "onboarding_step" not in st.session_state:
        st.session_state.onboarding_step = 0
    if "onboarding_answers" not in st.session_state:
        st.session_state.onboarding_answers = {
            "interest": "",
            "strengths": "",
            "weaknesses": "",
            "goals": ""
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

    with col2:
        if step < len(questions) - 1 and st.button("➡️ Next"):
            st.session_state.onboarding_answers[key] = st.session_state[f"input_{key}"]
            st.session_state.onboarding_step += 1

    # Career Track and Role Selection
    if "career_tree" not in st.session_state:
        st.session_state.career_tree = career_tree  # Load the career tree
###
    # Load job descriptions from file
    job_descriptions = load_job_descriptions()

    if not job_descriptions:
        st.warning("No job descriptions found. Please ensure the JSON file is loaded correctly.")
    else:
        track = st.selectbox("Choose your career track", list(st.session_state.career_tree["branches"].keys()))

        # Filter jobs by selected track
        filtered_jobs = [job for job in job_descriptions if job["career_track"] == track]
        roles = [job["title"] for job in filtered_jobs]

        role = st.selectbox("Choose your target role", roles)

        # Display job details for selected role
        selected_job = next(job for job in filtered_jobs if job["title"] == role)

        # Display detailed job description
        st.write(f"## {selected_job['title']} at {selected_job['company']}")
        st.write(f"**Location:** {selected_job['location']}")
        st.write(f"**Required Skills:** {', '.join(selected_job['skills_required'])}")
        st.write(f"**Job Description:** {selected_job['description']}")
        st.write("### Responsibilities:")
        for responsibility in selected_job["responsibilities"]:
            st.write(f"- {responsibility}")
            #loading from backend job descriptions
        # job_descriptions = load_job_descriptions()
        # st.write("Loaded job descriptions:", job_descriptions)
    # Final Step – Ready to Submit
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
                        "track": track
                    },
                    "location": location,
                    "target_role": role,
                    "user_profile": {
                        "GPA": gpa,
                        "weak_subjects": [s.strip() for s in weak_subjects_input.split(",") if s.strip()]
                    },
                    "onboarding_answers": st.session_state.onboarding_answers,
                    "job_descriptions": job_descriptions,
                    "relevant_interview_questions": st.session_state.relevant_interview_questions  # Add this line
                }
                #debug
                # st.write("State being passed to backend:", state)
                with st.spinner("Running mentorship pipeline..."):
                    #just added state for interview question mapping
                    state = interview_question_mapping_node(state)  # Process the state in the backend
                    st.session_state.relevant_interview_questions = state.get("relevant_interview_questions", [])
                    output = simple_graph.invoke(state)
                    st.session_state.graph_output = output
                    st.success("Pipeline executed successfully!")
            else:   
                st.warning("Please enter your user ID to proceed.")
    
    # # After mapping interview questions based on job description keywords
    # st.session_state.relevant_interview_questions = map_keywords_to_interview_questions
    if "relevant_interview_questions" in st.session_state:
        relevant_questions = st.session_state.relevant_interview_questions
        st.write("Relevant Questions in Session State:", relevant_questions)
        
        if relevant_questions:
            st.subheader("📋 Interview Questions to Prepare For")
            for idx, question in enumerate(relevant_questions, 1):
                st.markdown(f"{idx}. {question}")
        else:
            st.write("No relevant interview questions found based on the selected job.")
    else:
        st.warning("Please enter your user ID to proceed.")
    # Show the results
    if st.session_state.graph_output:
        out = st.session_state.graph_output
        st.subheader("🔍 Results")
        st.markdown(f"**Matched Role:** {out['matched_role']}")
        st.markdown(f"**Current Level:** {out['current_level']}")
        st.markdown(f"**Next Role:** {out['next_role']}")
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

with tab2:
    st.header("📄 Job Application Agent")

    if not st.session_state.resume_data or not st.session_state.graph_output:
        st.warning("Please complete the Mentor tab first!")
    else:
        resume = st.session_state.resume_data
        target_role = st.session_state.graph_output["next_role"]

        st.write("ℹ️ We'll generate a job application for the role:", target_role)
        st.write("Name:", resume.get("name"))
        st.write("Skills:", ", ".join(resume.get("skills")))
        st.write("Experience:")
        for exp in resume.get("experience"):
            st.write("-", exp)

        if st.button("✉️ Generate Application & Cover Letter"):
            with st.spinner("Filling application..."):
                # job_application_agent(resume, target_role)
                app_form = job_application_agent(resume, target_role)

                # ✅ Save and offer download of PDF
                from agent_testing import save_application_pdf
                pdf_path = "job_application.pdf"
                save_application_pdf(app_form, pdf_path)

                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                    st.download_button(
                        label="📄 Download Application PDF",
                        data=pdf_bytes,
                        file_name=pdf_path,
                        mime="application/pdf"
                    )
            st.success("Application form and cover letter generated and saved!")

with tab3:
    st.header("💬 Talk to Your AI Mentor")

    if not st.session_state.resume_data or not st.session_state.graph_output:
        st.warning("⚠️ Please complete the Resume + Mentor tabs first.")
    else:
        user_input = st.chat_input("Ask anything about your career path, resume, or job market...")
        
        if user_input:
            # Build context prompt for Gemini
            resume = st.session_state.resume_data
            graph = st.session_state.graph_output

            context = f"""
            You are an expert career mentor. The user has uploaded this resume:
            Name: {resume['name']}
            Skills: {', '.join(resume['skills'])}
            Experience: {', '.join(resume['experience'])}

            Based on this, we matched them to the role: {graph['matched_role']} and recommended career path: {graph['career_plan']}.
            Top job trends: {graph['job_trends']}
            Tailored Resume: {graph['tailored_resume'][:300]}...

            The user now asked: {user_input}
            Respond in a friendly, practical way, using the above data.
            """

            response = gemini.invoke(context).content
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", response))

        for sender, msg in st.session_state.chat_history:
            if sender == "user":
                st.chat_message("user").write(msg)
            else:
                st.chat_message("assistant").write(msg)
        