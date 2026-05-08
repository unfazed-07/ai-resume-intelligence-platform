ROLE_DEFAULT_TECH_STACK = {
    "Software Engineer": {
        "Fresher": ["Python", "Java", "Data Structures", "OOP", "Git", "SQL"],
        "Mid-Level": ["System Design", "REST APIs", "Docker", "CI/CD", "Microservices", "Cloud"],
        "Senior-Level": ["Architecture", "Distributed Systems", "Team Leadership", "Cloud Infrastructure", "Performance Engineering"],
    },
    "Data Analyst": {
        "Fresher": ["SQL", "Excel", "Python", "Tableau/Power BI", "Statistics"],
        "Mid-Level": ["Advanced SQL", "Power BI", "Python Pandas", "A/B Testing", "ETL Basics"],
        "Senior-Level": ["BI Strategy", "Advanced Analytics", "Data Governance", "Stakeholder Management", "Predictive Modeling"],
    },
    "Data Scientist": {
        "Fresher": ["Python", "Scikit-learn", "Statistics", "Pandas", "ML Basics"],
        "Mid-Level": ["Deep Learning", "MLflow", "Model Deployment", "Feature Engineering", "Cloud ML"],
        "Senior-Level": ["ML Research", "Advanced Deep Learning", "ML Architecture", "Business Strategy", "Team Mentorship"],
    },
    "Data Engineer": {
        "Fresher": ["Python", "SQL", "Pandas", "ETL Basics", "Cloud Basics"],
        "Mid-Level": ["Apache Spark", "Airflow", "Azure/AWS", "ETL Pipelines", "Database Optimization"],
        "Senior-Level": ["Data Architecture", "Distributed Systems", "Cloud Infrastructure", "Team Leadership", "Performance Optimization"],
    },
    "Machine Learning Engineer": {
        "Fresher": ["Python", "TensorFlow/PyTorch", "Git", "ML Fundamentals", "Statistics"],
        "Mid-Level": ["Model Deployment", "MLOps", "Docker", "FastAPI", "Cloud ML Platforms"],
        "Senior-Level": ["ML Platform Design", "Large Scale ML", "Infrastructure", "Leadership", "Research"],
    },
    "AI Engineer": {
        "Fresher": ["Python", "LLM APIs", "Prompt Engineering", "REST APIs", "Git"],
        "Mid-Level": ["Python", "Machine Learning", "LLMs", "FastAPI", "Vector Databases", "Cloud Platforms", "LangChain"],
        "Senior-Level": ["AI Architecture", "Fine-tuning LLMs", "RAG Systems", "Scalable AI", "Team Leadership", "Product Strategy"],
    },
}


def get_recruiter_analysis_prompt(resume_text: str, role: str, experience: str, required_skills: list) -> str:
<<<<<<< HEAD
    # Use the correct variable name 'required_skills'
=======
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376
    skills_str = "\n".join(f"- {s}" for s in required_skills)

    return f"""
You are a senior technical recruiter and AI hiring specialist.

<<<<<<< HEAD
### TASK:
1. Extract candidate contact information.
2. Look specifically for an email address (e.g., user@example.com). 
   - If no email is found, set "candidate_email" to "No Mail".
3. Evaluate the resume against the required skills for a **{experience} {role}** position.

### REQUIRED SKILLS FOR THIS POSITION:
{skills_str}

### CANDIDATE RESUME:
=======
Evaluate the following resume for a **{experience} {role}** position.

Required Skills for this position:
{skills_str}

Candidate Resume:
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376
\"\"\"
{resume_text}
\"\"\"

<<<<<<< HEAD
### OUTPUT INSTRUCTIONS:
Analyze the candidate and provide a report in the following JSON format ONLY. 
Do not include markdown fences or conversational text.

{{
  "candidate_name": "<extract name from resume or 'Unknown'>",
  "candidate_email": "<extract email address or 'No Mail'>",
=======
Analyze the candidate and provide a report in the following JSON format:
{{
  "candidate_name": "<extract name from resume or 'Unknown'>",
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376
  "overall_match_score": <integer 0-100>,
  "skill_match_score": <integer 0-100>,
  "technical_score": <integer 0-100>,
  "experience_score": <integer 0-100>,
  "ats_score": <integer 0-100>,
  "matched_skills": [<list of required skills found in resume>],
  "missing_skills": [<list of required skills NOT found in resume>],
  "bonus_skills": [<list of extra impressive skills not in required list>],
  "strengths": [<list of 3-4 candidate strengths>],
  "weaknesses": [<list of 2-3 candidate weaknesses>],
  "experience_relevance": "<2 sentence evaluation of work experience relevance>",
  "project_relevance": "<2 sentence evaluation of project quality and relevance>",
  "hiring_recommendation": "<Shortlist / Consider / Reject>",
  "recommendation_reason": "<2-3 sentence explanation for recommendation>",
  "interview_focus_areas": [<list of 3-4 topics to probe in interview>]
}}
<<<<<<< HEAD
=======

Return ONLY valid JSON. No extra text or markdown.
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376
"""


def get_ranking_summary_prompt(candidates_summary: str, role: str, experience: str) -> str:
    return f"""
You are a senior hiring manager reviewing multiple candidates for a {experience} {role} position.

Here is a summary of all evaluated candidates:
{candidates_summary}

Provide a final hiring summary in JSON format:
{{
  "top_candidate": "<name of best overall candidate>",
  "shortlisted": [<list of candidate names to shortlist>],
  "rejected": [<list of candidate names to reject>],
  "hiring_insights": "<3-4 sentence overall insight about the candidate pool>",
  "common_gaps": [<skills missing across most candidates>],
  "recommendation": "<overall hiring recommendation>"
}}

Return ONLY valid JSON. No extra text or markdown.
"""
