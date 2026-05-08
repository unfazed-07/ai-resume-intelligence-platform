from typing import Optional


ROLE_SKILL_EXPECTATIONS = {
    "Software Engineer": {
        "Fresher": ["Python/Java/C++", "Data Structures", "Algorithms", "OOP", "Git", "Basic SQL"],
        "Mid-Level": ["System Design", "REST APIs", "Microservices", "CI/CD", "Docker", "Cloud Basics"],
        "Senior-Level": ["Architecture Design", "Distributed Systems", "Team Leadership", "Performance Optimization",
                         "Cloud Infrastructure"],
    },
    "Data Analyst": {
        "Fresher": ["SQL", "Excel", "Python/R basics", "Data Visualization", "Statistics"],
        "Mid-Level": ["Advanced SQL", "Power BI/Tableau", "Python (Pandas)", "A/B Testing", "Dashboard Design"],
        "Senior-Level": ["Data Strategy", "Business Intelligence", "Advanced Analytics", "Stakeholder Management",
                         "Predictive Modeling"],
    },
    "Data Scientist": {
        "Fresher": ["Python", "Statistics", "Machine Learning basics", "Pandas", "Scikit-learn"],
        "Mid-Level": ["Deep Learning", "Feature Engineering", "Model Deployment", "MLflow", "Cloud ML Services"],
        "Senior-Level": ["Research Leadership", "ML Architecture", "Business Strategy", "Advanced Deep Learning",
                         "Team Mentorship"],
    },
    "Data Engineer": {
        "Fresher": ["Python", "SQL", "Pandas", "Basic Cloud Knowledge", "Data Processing"],
        "Mid-Level": ["Apache Spark", "Airflow", "ETL Pipelines", "Azure/AWS", "Database Optimization"],
        "Senior-Level": ["Distributed Systems", "Data Architecture", "Team Leadership", "Cloud Infrastructure",
                         "Performance Optimization"],
    },
    "Machine Learning Engineer": {
        "Fresher": ["Python", "ML Frameworks", "Statistics", "Model Training basics", "Git"],
        "Mid-Level": ["TensorFlow/PyTorch", "Model Deployment", "MLOps", "Docker", "API Development"],
        "Senior-Level": ["ML Platform Design", "Large Scale Training", "Research Leadership", "Infrastructure",
                         "Business Impact"],
    },
    "AI Engineer": {
        "Fresher": ["Python", "Prompt Engineering", "LLM APIs", "Basic ML", "REST APIs"],
        "Mid-Level": ["LangChain", "Vector Databases", "LLMs", "FastAPI", "Cloud Platforms", "RAG Systems"],
        "Senior-Level": ["AI Architecture", "Fine-tuning LLMs", "Scalable AI Systems", "Team Leadership",
                         "Product Strategy"],
    },
}


def get_applicant_analysis_prompt(
    resume_text: str,
    role: str,
    experience: str,
    expected_skills: Optional[list[str]] = None,
) -> str:
    skills = expected_skills if expected_skills else ROLE_SKILL_EXPECTATIONS.get(role, {}).get(experience, [])

    skills_str = "\n".join(f"- {s}" for s in skills)

    return f"""
You are a professional resume analyst and ATS optimization expert.

Analyze the following resume for a **{experience} {role}** position.

Expected skills for this role and level:
{skills_str}

Resume Content:
\"\"\"
{resume_text}
\"\"\"

Provide a comprehensive analysis in the following JSON format:
{{
  "overall_score": <integer 0-100>,
  "ats_score": <integer 0-100>,
  "technical_score": <integer 0-100>,
  "experience_score": <integer 0-100>,
  "strengths": [<list of 3-5 specific strengths>],
  "weaknesses": [<list of 3-5 specific weaknesses>],
  "missing_skills": [<list of skills from expected list that are absent>],
  "keyword_suggestions": [<list of ATS keywords to add>],
  "project_feedback": "<2-3 sentence evaluation of projects>",
  "formatting_feedback": "<2-3 sentence evaluation of resume formatting>",
  "achievement_feedback": "<2-3 sentence evaluation of impact/achievements>",
  "top_suggestions": [<list of 5 most impactful improvements to make>],
  "summary": "<3-4 sentence overall summary of the resume>"
}}

Return ONLY valid JSON. No extra text or markdown.
"""


def get_skill_generation_prompt(role: str, experience: str) -> str:
    """Prompt used to dynamically generate relevant skills for any typed role."""
    return f"""
Act as a technical recruiter. List the top 10-15 essential technical skills and keywords 
required for a {experience} {role}. 
Return ONLY a comma-separated list of skills. 
No conversational text, no numbering.
"""
