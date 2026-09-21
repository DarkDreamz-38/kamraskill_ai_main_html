"""
services/gemini_service.py

Text-generation entry point used by material_engine.py.

Honours the MOCK_GEMINI environment flag (same contract as
services/providers/selector.py):
  - MOCK_GEMINI=true  -> deterministic offline mock (no API key needed)
  - otherwise         -> real Gemini API (requires GEMINI_API_KEY in .env)
"""
import json
import os
import re

from dotenv import load_dotenv

load_dotenv()

MOCK_GEMINI = os.getenv("MOCK_GEMINI", "false").strip().lower() == "true"


# ---------------------------------------------------------------------------
# Mock provider (development / prototype demo only)
# ---------------------------------------------------------------------------

_COMPETENCY_KEYWORDS = {
    "Data Analysis": ["analysis", "analytic", "data", "dataset", "insight"],
    "Statistical Reasoning": ["statistic", "sampling", "probability", "variance", "distribution", "inference"],
    "Data Visualization": ["visualiz", "chart", "graph", "dashboard", "plot"],
    "Communication": ["communication", "report", "presentation", "stakeholder", "writing"],
    "Policy Understanding": ["policy", "regulation", "compliance", "governance", "legislat"],
}


def _mock_competency_response(prompt: str) -> str:
    """Extract the learning material from the prompt and map competencies deterministically."""
    marker = "LEARNING MATERIAL:"
    material = prompt.split(marker, 1)[1] if marker in prompt else prompt
    material_lower = material.lower()

    competencies = []
    for name, keywords in _COMPETENCY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in material_lower)
        if hits > 0:
            relevance = min(50 + hits * 10, 95)
            competencies.append({"name": name, "relevance": relevance})

    if not competencies:
        competencies.append({"name": "Data Analysis", "relevance": 55})

    return json.dumps({"competencies": competencies})


def _mock_generate_text(prompt: str) -> str:
    return _mock_competency_response(prompt)


# ---------------------------------------------------------------------------
# Real Gemini provider
# ---------------------------------------------------------------------------

def _real_generate_text(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set in the .env file "
            "(or set MOCK_GEMINI=true to run without it)"
        )

    from google import genai

    client = genai.Client(api_key=api_key)
    interaction = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return interaction.text


generate_text = _mock_generate_text if MOCK_GEMINI else _real_generate_text
