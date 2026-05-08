import os
import json
<<<<<<< HEAD
from groq import Groq


def _get_llm_client():
    """Initialize and return the Groq client."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    return Groq(api_key=api_key)


def _get_gemini_model():
    """
    Mock function to maintain compatibility with existing imports.
    Returns the model name string for Groq.
    """
    return os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def _strip_code_fences(raw_text: str) -> str:
    """Removes markdown code blocks to extract raw JSON."""
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
=======
import google.generativeai as genai


def _get_gemini_model():
    """Initialize and return the Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-3.1-flash-lite")
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376


def call_gemini(prompt: str) -> dict:
    """
<<<<<<< HEAD
    Redirects calls to Groq API while preserving the interface.
    Returns parsed dict or raises an exception.
    """
    client = _get_llm_client()
    model_name = _get_gemini_model()

    # Groq uses the ChatCompletion interface
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a professional assistant that only returns valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,  # Low temperature for consistent JSON output
        response_format={"type": "json_object"}  # Groq specific JSON mode
    )

    raw_text = (response.choices[0].message.content or "").strip()
    if not raw_text:
        raise ValueError("Groq returned an empty response.")

    raw_text = _strip_code_fences(raw_text)
=======
    Send a prompt to Gemini and parse the JSON response.
    Returns parsed dict or raises an exception.
    """
    model = _get_gemini_model()
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
<<<<<<< HEAD
        raise ValueError(f"Groq returned invalid JSON: {e}\nRaw response:\n{raw_text}")
=======
        raise ValueError(f"Gemini returned invalid JSON: {e}\nRaw response:\n{raw_text}")
>>>>>>> 041a279946a7f606a0bfa9973faa39aa3fac3376
