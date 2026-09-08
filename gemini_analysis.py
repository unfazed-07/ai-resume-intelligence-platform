import os
import json
from google import genai
from google.genai import types


def _get_llm_client():
    """Initialize and return the Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    return genai.Client(api_key=api_key)


def _get_gemini_model():
    """Return the Gemini model name."""
    return os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def _strip_code_fences(raw_text: str) -> str:
    """Remove markdown code blocks to extract raw JSON."""
    text = raw_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    if text.startswith("json"):
        text = text[4:].lstrip()

    return text


def call_gemini(prompt: str) -> dict:
    """
    Call Gemini API and return the response as a Python dictionary.
    """

    client = _get_llm_client()
    model_name = _get_gemini_model()

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a professional assistant that only returns valid JSON."
            ),
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )

    raw_text = (response.text or "").strip()

    if not raw_text:
        raise ValueError("Gemini returned an empty response.")

    raw_text = _strip_code_fences(raw_text)

    try:
        return json.loads(raw_text)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned invalid JSON: {e}\n"
            f"Raw response:\n{raw_text}"
        )
