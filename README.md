
# Agentic Career Orchestrator: AI-Powered Career Mentorship Pipeline

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
- **Multimodal Feedback Module:** Integration of text, voice, and webcam emotion analysis for holistic interview practice.
- **Automated Document Synthesis:** Dynamic PDF export of tailored applications.
- **Market-Aware Analytics:** Integration with live APIs (SERP/RapidAPI) for real-time trend aggregation.

## 📂 Repository Architecture
The project has been refactored into a modular service architecture:

```
.
├── app.py                # Main Entry Point (Streamlit UI)
├── requirements.txt      # Python Dependencies
├── .env                  # Environment Variables (Create this)
└── src/
    ├── agents/           # LangGraph Agents & Nodes
    │   ├── graph.py      # Main graph definition
    │   └── nodes.py      # Logical nodes (Career Tree, Job Trends, etc.)
    ├── core/             # Core Configuration & State
    ├── data/             # Data Loaders & Static Assets
    ├── services/         # External Services (LLM, PDF, Analysis)
    └── ui/               # UI Components (Multimedia Input)
```

## 🛠️ Quickstart

### 1. Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory with your API keys:

```ini
GOOGLE_API_KEY=your_gemini_key
SERP_API_KEY=your_serp_key
RAPIDAPI_KEY=your_rapidapi_key
```

### 3. Run the Application

```bash
streamlit run app.py
```

## 💡 How it Works
1.  **Upload Resume:** The system parses your PDF resume to extract skills and experience.
2.  **Onboarding:** You answer a few questions about your goals and interests.
3.  **Pipeline Execution:** The **LangGraph** agent:
    *   Locates you in the **Career Tree**.
    *   Generates a **Career Plan**.
    *   Fetches live **Job Trends**.
    *   Calculates a **Fit Score** and **Skill Gaps**.
    *   Maps **Interview Questions** to your target role.
4.  **Practice:** Use the Interview tab to answer questions via Text, Voice, or Webcam.
5.  **Apply:** Use the Application Agent to generate a tailored cover letter and PDF application.

## 🤝 Contributing
- Open issues or PRs for bug fixes and improvements.
- Add tests for new nodes or pipeline changes.

## 📄 License
[MIT License](LICENSE)
