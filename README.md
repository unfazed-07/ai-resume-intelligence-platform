# 🧠 AI Resume Intelligence Platform
[VieW Live App](https://fwvw4ibdfpxeeazrt3a7ft.streamlit.app/)
> Azure + Gemini Powered Resume Analysis System

---

## Overview

An AI-powered cloud application for **Job Applicants** and **Recruiters** that intelligently analyzes resumes using **Azure AI Document Intelligence** and **Google Gemini API**.

---

## Features

### 👤 Applicant Mode
- Upload your resume (PDF)
- Select target role and experience level
- Get AI-powered feedback including:
  - Overall, ATS, Technical, and Experience scores
  - Strengths and weaknesses
  - Missing skills detection
  - ATS keyword suggestions
  - Project, formatting, and achievement feedback
  - Top action items to improve your resume

### 🏢 Recruiter Mode
- Upload multiple candidate resumes (batch processing)
- Select hiring role, experience level, and required tech stack
- Get AI-powered candidate evaluation including:
  - Candidate ranking by match score
  - Skill match / missing skill analysis
  - Per-candidate hiring recommendation (Shortlist / Consider / Reject)
  - Interview focus areas
  - Overall hiring summary and insights

---

## Supported Roles

- Software Engineer
- Data Analyst
- Data Scientist
- Data Engineer
- Machine Learning Engineer
- AI Engineer

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python |
| Frontend + Backend | Streamlit |
| PDF Extraction | Azure AI Document Intelligence |
| AI Analysis | Google Gemini API (`gemini-1.5-flash`) |
| PDF Fallback | PyPDF2 |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-resume-intelligence-platform.git
cd ai-resume-intelligence-platform
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env` and fill in your API keys:

```bash
cp .env .env.local
```

Edit `.env`:

```env
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_azure_key_here
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/

GEMINI_API_KEY=your_gemini_key_here
```

> **Note:** If Azure credentials are not set, the app automatically falls back to PyPDF2 for PDF parsing.

### 5. Run the App

```bash
streamlit run app.py
```

---

## Project Structure

```
ai-resume-intelligence-platform/
│
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (API keys)
│
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py             # Azure Doc Intelligence + PyPDF2 fallback
│   ├── gemini_analysis.py        # Gemini API client
│   ├── applicant_analysis.py     # Applicant analysis logic
│   └── recruiter_analysis.py     # Recruiter analysis + ranking logic
│
├── prompts/
│   ├── __init__.py
│   ├── applicant_prompts.py      # Applicant prompts + role-skill expectations
│   └── recruiter_prompts.py      # Recruiter prompts + default tech stacks
│
├── sample_resumes/               # Place sample PDFs here for testing
└── README.md
```

---

## Getting API Keys

### Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Paste into `.env` as `GEMINI_API_KEY`

### Azure Document Intelligence
1. Go to [Azure Portal](https://portal.azure.com)
2. Create a **Document Intelligence** resource
3. Copy the **Key** and **Endpoint**
4. Paste into `.env`

---

## Future Roadmap

- AI-generated cover letters
- LinkedIn profile analysis
- AI interview preparation
- Skill learning roadmap generator
- Candidate comparison dashboard
- Export reports as PDF
- AI-generated interview questions
- SaaS deployment on Azure

---

## License

MIT License — free to use, modify, and distribute.
