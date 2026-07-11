# CVInsight Pro 🎯

> AI-powered ATS resume scorer — analyse any resume against any job description in under 30 seconds.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Supabase](https://img.shields.io/badge/Supabase-Auth-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

---

## What it does

CVInsight Pro scores a resume against a job description across **5 dimensions**:

| Dimension | What it checks |
|---|---|
| Keyword alignment | Exact and semantic keyword match rate |
| Skills coverage | Required vs. present technical skills |
| Formatting quality | ATS-parseable structure, no tables/graphics |
| Experience match | Seniority level and years of experience |
| ATS compatibility | Overall pass/fail prediction |

It then generates specific, actionable recommendations using **Groq's LLM API** so the user knows exactly what to fix before applying.

---

## Tech stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend API | FastAPI + Uvicorn | REST endpoints, async request handling |
| AI scoring | Groq LLM (LLaMA 3) | Natural language recommendations |
| Semantic matching | Sentence Transformers (all-MiniLM-L6-v2) | Keyword similarity scoring |
| Auth | Supabase (email + Google OAuth) | User authentication and sessions |
| Database | Supabase PostgreSQL | Score history and user data |
| Frontend | Streamlit | Interactive web UI |
| PDF export | ReportLab | Downloadable score reports |

---

## Screenshots

<!-- Add your screenshots after setup -->
<!-- Example: -->
<!-- ![Landing page](docs/screenshots/landing.png) -->
<!-- ![Score result](docs/screenshots/scorer.png) -->
<!-- ![History](docs/screenshots/history.png) -->

---

## Local setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/cvinsight-pro.git
cd cvinsight-pro

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Open .env and fill in your Supabase and Groq API keys

# 5. Start the backend (Terminal 1)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 6. Start the frontend (Terminal 2)
streamlit run frontend/streamlit_app.py
```

Backend API: `http://localhost:8000`  
Frontend app: `http://localhost:8501`

---

## Project structure
