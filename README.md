# Agentic-Career-Orchestrator: Multi-Agent Pipeline for Semantic Resume Parsing & Career Mentorship

An enterprise-grade **Agentic AI** pipeline leveraging **LangGraph** and **Large Language Models (LLMs)** to automate end-to-end career development workflows. This system performs granular skill extraction, explainable role-fit scoring, and multimodal feedback generation to bridge the gap between candidate profiles and real-time market requirements.

## 🎯 Problem Statement
Job seekers and early-career engineers lack an automated, reproducible methodology to:
- **Map Competencies:** Identify exact placement within multi-level career ladders.
- **Quantify Skill Gaps:** Discover prioritized, actionable steps for professional progression.
- **Synthesize Documents:** Generate context-aware, ATS-optimized resumes and cover letters.
- **Simulate Interviews:** Map industry-standard question banks to individual candidate weaknesses.

## 🚀 Key Features
- **Semantic Resume Parsing:** High-fidelity data extraction from PDFs utilizing specialized NLP parsing stacks.
- **Stateful Agent Orchestration:** A multi-agent pipeline built on **LangGraph StateGraphs** for resilient decision-making.
- **Predictive Role-Fit Engine:** Explainable scoring algorithms that map extracted skills to complex career trees.
- **Multimodal Feedback Module:** Integration of text and interview-vector mapping to provide rubric-aligned mentorship.
- **Automated Document Synthesis:** Dynamic PDF export of tailored applications using **PyLaTeX**.
- **Market-Aware Analytics:** Integration with live APIs (SERP/RapidAPI) for real-time trend aggregation.

## 📂 Repository Architecture
- `app.py`: Streamlit-based UI for session orchestration and multimodal interaction.
- `agent_testing.py`: Core **StateGraph** implementations and multi-agent node entry points.
- `this_one_works.py`: Production-ready pipeline helpers and PDF synthesis utilities.
- `Software_Questions.csv`: Curated dataset for interview-vector mapping.


## 🛠️ Quickstart (macOS/Linux)

### 1. Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

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
