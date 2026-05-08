from utils.gemini_analysis import call_gemini
from prompts.applicant_prompts import get_applicant_analysis_prompt
<<<<<<< HEAD
from utils.gemini_analysis import call_gemini


def generate_suggested_skills(role: str, experience: str) -> list:
    """Uses LLM to generate a list of relevant skills for a given role/level."""
    from prompts.applicant_prompts import get_skill_generation_prompt

    prompt = get_skill_generation_prompt(role, experience)

    # We wrap the prompt in a way that call_gemini can return a list
    # Since call_gemini expects JSON, update the prompt or handle the return
    try:
        # If your prompt asks for a comma-separated list, call_gemini might fail
        # because it tries to json.loads() the response.
        # Let's use a specialized prompt to ensure we get JSON back.
        json_prompt = f"{prompt} Respond ONLY with a JSON object like: {{\"skills\": [\"skill1\", \"skill2\"]}}"
        response_dict = call_gemini(json_prompt)
        return response_dict.get("skills", [])
    except Exception as e:
        print(f"Skill generation failed: {e}")
        return []

def analyze_applicant_resume(
    resume_text: str,
    role: str,
    experience: str,
    required_skills: list | None = None,
) -> dict:
=======


def analyze_applicant_resume(resume_text: str, role: str, experience: str) -> dict:
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376
    """
    Analyze a single applicant resume using Gemini.
    Returns structured analysis dict.
    """
<<<<<<< HEAD
    prompt = get_applicant_analysis_prompt(resume_text, role, experience, required_skills)
=======
    prompt = get_applicant_analysis_prompt(resume_text, role, experience)
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376
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
