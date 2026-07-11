# CVInsight Pro 🎯

> AI-powered ATS Resume Scorer — know exactly why your resume gets rejected before a human ever reads it.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA3-F55036?style=flat)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

---

## 🔴 The Problem

Over **75% of resumes are rejected by ATS software** before a recruiter sees them — not because the candidate is unqualified, but because the resume lacks the right keywords and formatting. Job seekers apply blindly with no feedback, no score, and no idea what to fix.

## ✅ The Solution

CVInsight Pro replicates how ATS software reads your resume. Upload your resume, paste a job description — get a detailed compatibility score across 5 dimensions plus AI-generated, line-by-line fix recommendations in under 30 seconds.

---

## 📸 Screenshots

<img width="1908" height="906" alt="Screenshot 2026-07-11 200002" src="https://github.com/user-attachments/assets/3748d60e-5c86-4ade-b169-72d2fdf3c6be" />

---

## ⚙️ How It Works

![CVInsight Pro Pipeline](https://github.com/user-attachments/assets/48a516e1-b1a6-4f83-ba40-171456320fbd)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Uvicorn |
| AI Recommendations | Groq API (LLaMA 3) |
| Semantic Matching | Sentence Transformers (all-MiniLM-L6-v2) |
| Authentication | Supabase (Email + Google OAuth) |
| Database | Supabase PostgreSQL |
| Frontend | Streamlit |
| PDF Export | ReportLab |
---

## ✨ Features

- 🔍 **Semantic keyword matching** — understands meaning, not just exact words
- 📊 **5-dimension ATS score** — keyword alignment, skills, formatting, experience, compatibility
- 🤖 **LLM-powered suggestions** — tells you exactly which lines to rewrite and how
- 🔐 **Google OAuth + email auth** — complete auth via Supabase
- 📈 **Score history** — track improvement across every resume version
- 📄 **PDF report export** — download and share your score report

---

## 🚀 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/Gaurav2025G/cvinsight-pro.git
cd cvinsight-pro

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add environment variables
cp .env.example .env
# Fill in your Supabase and Groq keys in .env

# 5. Start backend  (Terminal 1)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 6. Start frontend  (Terminal 2)
streamlit run frontend/streamlit_app.py
```

| Service | URL |
|---|---|
| App | http://localhost:8501 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🌐 Deployed App

> Coming soon — deployment in progress on Streamlit Cloud + Render

---

## 📁 Project Structure

```
cvinsight-pro/
├── backend/
│   ├── api/                       # Auth + scoring endpoints
│   ├── core/                      # Config + middleware
│   ├── database/                  # Supabase DB client
│   ├── models/                    # Pydantic schemas
│   ├── templates/                 # HTML report templates
│   ├── utils/                     # File + matching utilities
│   └── services/
│       ├── ats_scorer.py          # Core scoring engine
│       ├── groq_parser.py         # Groq LLM integration
│       ├── jd_matcher.py          # JD keyword extractor
│       ├── resume_parser.py       # PDF/DOCX text extraction
│       ├── resume_analyzer.py     # Resume analysis logic
│       ├── recommendation_engine.py  # AI suggestion generator
│       ├── feedback_engine.py     # Feedback builder
│       ├── report_generator.py    # Report builder
│       └── pdf_export.py          # PDF export
├── frontend/
│   ├── views/                     # Streamlit pages
│   │   ├── landing.py             # Dashboard
│   │   ├── scorer.py              # Resume analysis
│   │   ├── history.py             # Score history
│   │   └── resources.py           # ATS tips
│   ├── components/                # Reusable UI components
│   ├── services/                  # API + Supabase client
│   └── assets/                    # CSS styles
├── jupyter notebooks/             # BERT experiments + EDA
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔑 Environment Variables

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
GROQ_API_KEY=your-groq-api-key
```

---

## 💡 Why I Built This

During my own job search I kept getting no responses — no feedback, no reason, nothing. I researched how ATS systems actually work, then built a tool that replicates that process end to end. This project covers the full stack: REST API design, integrating two AI models with different roles (semantic similarity + generative LLM), a complete auth system, and a clean frontend — all connected and production-ready.

---

## 👤 Author

**Gaurav** · [github.com/Gaurav2025G](https://github.com/Gaurav2025G)

*MIT License © 2026*
