from utils.gemini_analysis import call_gemini
from prompts.applicant_prompts import get_applicant_analysis_prompt
from utils.gemini_analysis import call_gemini


def generate_suggested_skills(role: str, experience: str) -> list:
    """Generate relevant skills using Gemini."""

    from prompts.applicant_prompts import get_skill_generation_prompt

    prompt = get_skill_generation_prompt(role, experience)

    json_prompt = (
        f"{prompt}\n\n"
        'Respond ONLY with a JSON object like: '
        '{"skills": ["skill1", "skill2", "skill3"]}'
    )

    response_dict = call_gemini(json_prompt)

    return response_dict.get("skills", [])

def analyze_applicant_resume(
    resume_text: str,
    role: str,
    experience: str,
    required_skills: list | None = None,
) -> dict:
    """
    Analyze a single applicant resume using Gemini.
    Returns structured analysis dict.
    """
    prompt = get_applicant_analysis_prompt(resume_text, role, experience, required_skills)
    result = call_gemini(prompt)
    return result


def get_score_color(score: int) -> str:
    """Return a color string based on score value."""
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"


def get_score_label(score: int) -> str:
    """Return a label based on score value."""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Needs Improvement"
    else:
        return "Poor"
