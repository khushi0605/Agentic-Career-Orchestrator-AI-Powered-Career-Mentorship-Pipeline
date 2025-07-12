import streamlit as st
from pprint import pprint
from agent_testing import (
    parse_resume_from_pdf,
    simple_graph,
    job_application_agent,
    career_tree,
    gemini,
    save_application_pdf
)

st.set_page_config(page_title="AI Career Mentor", page_icon="🎓")
st.title("🎯 AI Career Mentorship System")

# ✅ Initialize chat memory BEFORE anything else
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "resume_data" not in st.session_state:
    st.session_state.resume_data = None

if "graph_output" not in st.session_state:
    st.session_state.graph_output = None


# Tabs for functionality
tab1, tab2, tab3 = st.tabs(["🧠 Mentor Guidance", "📄 Application Agent", "💬 Chat with Mentor"])

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

    if st.session_state.resume_data:
        st.subheader("🎯 Choose Career Track & Role")

        track = st.selectbox("Choose your career track", list(career_tree["branches"].keys()))
        roles = [r["title"] for r in career_tree["branches"][track]]
        role = st.selectbox("Choose your target role", roles)
        location = st.text_input("📍 Job Search Location", value="India")

        if st.button("🚀 Run Career Mentorship Pipeline"):
            state = {
                "resume": st.session_state.resume_data,
                "career_tree": {
                    "track": track,
                    "levels": career_tree["branches"][track]
                },
                "location": location,
                "target_role": role
            }
            output = simple_graph.invoke(state)
            st.session_state.graph_output = output

            st.success("Pipeline executed successfully!")

    if st.session_state.graph_output:
        out = st.session_state.graph_output
        st.subheader("🔍 Results")
        st.markdown(f"**Matched Role:** {out['matched_role']}")
        st.markdown(f"**Current Level:** {out['current_level']}")
        st.markdown(f"**Next Role:** {out['next_role']}")
        st.markdown("**Career Plan:**")
        st.info(out["career_plan"])
        st.markdown("**Top Job Trends:**")
        st.success(out["job_trends"])
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
