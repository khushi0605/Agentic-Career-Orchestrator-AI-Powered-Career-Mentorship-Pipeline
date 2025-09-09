# actual_final_mentor_bot

Professional AI-driven career mentorship pipeline: parse resumes, map skills to career trees, generate personalized career plans, score fit for roles, map interview questions, tailor resumes/cover letters, and produce job-application PDFs.

## What this repo solves

Job seekers and early-career engineers need an automated, reproducible way to:

- Identify where they fit in career ladders,
- Discover skill gaps and prioritized steps to progress,
- Generate role-specific resumes, cover letters and application PDFs,
- Map common interview questions to gaps and strengths.

This project combines resume parsing, career-tree matching, trend aggregation, and language-model generation into a runnable pipeline and a Streamlit UI.

## Key features

- Resume parsing from PDF (parse_resume_from_pdf)
- Career-tree matching and fit scoring
- Personalized career-plan generation (LM integration)
- Skill-gap analysis and interview-question mapping
- Tailored resume and cover-letter generation
- Job-application autofill and PDF export

## Repository layout (key files)

- app.py — Streamlit application and session orchestration
- agent_testing.py — StateGraph / node implementations and pipeline entry points
- this_one_works.py — working pipeline helpers and PDF generation utilities
- Software_Questions.csv — interview-question dataset
- interview_results.txt — example output

Notable functions / entry points:

- parse_resume_from_pdf (resume extraction)
- generate_career_plan_node (career-plan node)
- fit_score_from_tree_node (fit scoring)
- tailor_resume_node (resume tailoring)
- save_application_pdf / job_application_agent (PDF export & application autofill)

## Quickstart (macOS)

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

- If a requirements file is available:

```bash
pip install -r requirements.txt
```

- Otherwise install common dependencies:

```bash
pip install streamlit pandas spacy reportlab PyMuPDF requests python-dotenv langgraph
python -m spacy download en_core_web_sm
```

3. Configure environment variables (recommended via `.env`):

- GOOGLE_API_KEY
- SERP_API_KEY
- RAPIDAPI_KEY
- Any provider keys required by your LM integration

Example `.env`:

```
GOOGLE_API_KEY=your_key
SERP_API_KEY=your_key
RAPIDAPI_KEY=your_key
```

4. Run the Streamlit UI:

```bash
streamlit run app.py
```

Upload a resume PDF and use the "Run Career Mentorship Pipeline" control in the UI.

5. Run backend scripts / tests:

```bash
python this_one_works.py
python agent_testing.py
```

## Notes & troubleshooting

- Ensure spaCy model `en_core_web_sm` is installed before running parsing workflows.
- When testing without API keys, review `this_one_works.py` for mocks and commented examples.
- Never commit secret keys; use environment variables or a secrets manager.

## Contributing

- Open issues or PRs for bug fixes and improvements.
- Add tests for new nodes or pipeline changes.
- Maintain API-key safety and update README when adding external dependencies.

## License

Add a LICENSE file (e.g., MIT) if you plan to open-source.
