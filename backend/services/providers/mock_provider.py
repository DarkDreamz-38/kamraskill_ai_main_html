"""
services/providers/mock_provider.py

DEVELOPMENT-ONLY mock text-generation provider.

This provider is NEVER used unless MOCK_GEMINI=true is explicitly set in the
environment.  It produces deterministic, structured JSON responses that
satisfy the exact same JSON contract expected by mcq_engine.py — one MCQ
per section, with section_number, question, options A-D, correct_answer,
explanation, and difficulty.

Mock questions are derived from the section heading and body content so that
every question is distinct and maps unambiguously to its source section.

This file must NOT contact the Gemini API under any circumstances.
"""
import json
import re

# Rotating correct-answer positions so demos don't show every answer as "A".
_POSITIONS = ["A", "B", "C", "D"]

# Plausible-sounding but incorrect distractor templates, keyed by rotation.
_DISTRACTORS = [
    "It applies only to data collected before 2020 and has since been withdrawn from official practice.",
    "It recommends ignoring documentation requirements in favour of faster ad-hoc processing.",
    "It states that the concept is relevant solely to private-sector analytics, not official statistics.",
    "It reverses the standard practice by prioritising speed of release over accuracy and rigor.",
]


def _first_sentence(body: str, fallback: str) -> str:
    """Extract the first complete sentence from a section body."""
    text = " ".join(body.split())
    if not text:
        return fallback
    parts = re.split(r"(?<=[.!?])\s+", text)
    sentence = parts[0].strip() if parts else text
    if len(sentence) > 160:
        sentence = sentence[:157].rstrip() + "..."
    if sentence and sentence[-1] not in ".!?":
        sentence += "."
    return sentence or fallback


def generate_text(prompt: str) -> str:
    """
    Parse the incoming batch prompt to extract section numbers and headings,
    then return a deterministic JSON array of MCQs — one per section.

    The prompt format emitted by _build_batch_prompt() is:
        SECTION <n>: <heading>
        <body>
    """
    section_pattern = re.compile(
        r"SECTION\s+(\d+):\s+(.+?)(?=\n---|\nSECTION|\Z)", re.DOTALL
    )
    matches = section_pattern.findall(prompt)

    questions = []
    for raw_num, raw_block in matches:
        number = int(raw_num)
        lines = raw_block.strip().splitlines()
        heading = re.sub(r"^\d+\.\s*", "", lines[0].strip())
        body_lines = lines[1:] if len(lines) > 1 else []
        body_preview = " ".join(body_lines).strip()
        correct_text = _first_sentence(body_preview, heading)

        # Rotate the correct answer position deterministically per section.
        correct_letter = _POSITIONS[number % len(_POSITIONS)]

        distractor_pool = [
            _DISTRACTORS[number % len(_DISTRACTORS)],
            _DISTRACTORS[(number + 1) % len(_DISTRACTORS)],
            _DISTRACTORS[(number + 2) % len(_DISTRACTORS)],
        ]

        options = {}
        d_idx = 0
        for letter in _POSITIONS:
            if letter == correct_letter:
                options[letter] = correct_text
            else:
                options[letter] = distractor_pool[d_idx]
                d_idx += 1

        questions.append({
            "section_number": number,
            "question": (
                f"Which of the following statements best reflects the guidance on "
                f"'{heading}' given in the learning material?"
            ),
            "options": options,
            "correct_answer": correct_letter,
            "explanation": (
                f"The correct option restates the key point of section {number} "
                f"({heading}). The remaining options contradict or misapply the "
                f"guidance described in the material."
            ),
            "difficulty": "Easy",
        })

    return json.dumps(questions)
