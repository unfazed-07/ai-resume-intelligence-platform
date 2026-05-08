import json
from utils.gemini_analysis import call_gemini
from prompts.recruiter_prompts import get_recruiter_analysis_prompt, get_ranking_summary_prompt


def analyze_candidate(resume_text: str, role: str, experience: str, required_skills: list) -> dict:
    """
    Analyze a single candidate resume for a recruiter.
    Returns structured candidate evaluation dict.
    """
    prompt = get_recruiter_analysis_prompt(resume_text, role, experience, required_skills)
    result = call_gemini(prompt)
    return result


def rank_candidates(candidates: list[dict], role: str, experience: str) -> list[dict]:
    """
    Sort candidates by overall_match_score descending.
    candidates: list of analysis dicts from analyze_candidate()
    """
    return sorted(candidates, key=lambda x: x.get("overall_match_score", 0), reverse=True)


def generate_hiring_summary(ranked_candidates: list[dict], role: str, experience: str) -> dict:
    """
    Generate a final hiring summary across all candidates using Gemini.
    """
    summary_parts = []
    for i, c in enumerate(ranked_candidates, 1):
        name = c.get("candidate_name", f"Candidate {i}")
        score = c.get("overall_match_score", 0)
        matched = ", ".join(c.get("matched_skills", []))
        missing = ", ".join(c.get("missing_skills", []))
        rec = c.get("hiring_recommendation", "Unknown")
        summary_parts.append(
            f"{i}. {name} | Score: {score}% | Matched: {matched} | Missing: {missing} | Recommendation: {rec}"
        )

    candidates_summary = "\n".join(summary_parts)
    prompt = get_ranking_summary_prompt(candidates_summary, role, experience)
    return call_gemini(prompt)


def get_recommendation_badge(recommendation: str) -> tuple[str, str]:
    """Return (emoji, color) for a hiring recommendation."""
    rec = recommendation.lower()
    if "shortlist" in rec:
        return "✅", "green"
    elif "consider" in rec:
        return "🟡", "orange"
    else:
        return "❌", "red"
