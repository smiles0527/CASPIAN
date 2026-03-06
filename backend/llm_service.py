import os
import re
from typing import Optional

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def _get_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is not set in environment")
    return OpenAI(api_key=key)

SYSTEM_PROMPT = """You are an AI assistant for CASPIAN Follow-Up Care, a platform that supports people using prosthetic devices (S.O.C.K.S - Sensor-Optimized Comfort & Kinetics System). Your role is to analyze sensor data and how the user is feeling, then provide clear, helpful insights and a short care plan.

Context:
- S.O.C.K.S uses two sensor types in prosthetic sockets (arm prosthetics):
  - Sensors 1–6: Pressure sensors at high-load areas. Monitor force distribution, identify pressure hotspots. Higher values (e.g. 70–100) may indicate areas of concern.
  - Sensors 7–20: Sensory stimulation sensors near nerve-rich regions. Used for phantom limb pain management. Values reflect stimulation intensity or comfort.
- Users enter sensor values (0–100 scale) and describe how they feel.
- You help identify patterns, pressure hotspots, comfort issues, and suggest next steps.
- Use a clear, friendly tone. Don't be overly formal or clinical.
- Always remind users to see their clinician for medical decisions—you're here to support, not replace professional care.

When you receive current sensor data and feelings, plus optional past entries, respond with exactly two sections:

1. **Summary** (2-3 sentences): What do the current readings and feelings suggest? Any patterns or concerns?
2. **Care Plan** (3-5 bullet points): Actionable suggestions—e.g., socket adjustments, monitoring tips, when to reach out to a clinician, comfort strategies.

Keep it practical and easy to follow. If there's no history, focus on the current submission. If there is history, reference trends when relevant."""


def build_user_message(
    sensors: list[Optional[float]],
    feelings: Optional[str],
    history_entries: list[dict],
) -> str:
    parts = []

    # Current submission
    sensor_strs = []
    for i, v in enumerate(sensors, 1):
        if v is not None:
            sensor_strs.append(f"Sensor {i}: {v}")
    if sensor_strs:
        parts.append("Current sensor values:\n" + "\n".join(sensor_strs))
    else:
        parts.append("Current sensor values: (none provided)")

    if feelings:
        parts.append(f"How they're feeling today: {feelings}")
    else:
        parts.append("How they're feeling today: (not provided)")

    # History
    if history_entries:
        parts.append("\n--- Past entries (most recent first) ---")
        for e in history_entries:
            h_sensors = [e.get(f"sensor_{i}") for i in range(1, 21)]
            h_sensor_strs = [f"S{i}: {v}" for i, v in enumerate(h_sensors, 1) if v is not None]
            lines = [f"Date: {e.get('created_at', '')}"]
            if h_sensor_strs:
                lines.append("Sensors: " + ", ".join(h_sensor_strs[:10]) + ("..." if len(h_sensor_strs) > 10 else ""))
            if e.get("feelings"):
                lines.append(f"Feelings: {e['feelings']}")
            parts.append("\n".join(lines))

    return "\n\n".join(parts)


def parse_response(text: str) -> tuple[str, str]:
    """Extract Summary and Care Plan from LLM response."""
    summary = ""
    care_plan = ""

    # Try to split by **Summary** and **Care Plan**
    summary_match = re.search(
        r"\*\*Summary\*\*[:\s]*(.*?)(?=\*\*Care Plan\*\*|\Z)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    care_match = re.search(
        r"\*\*Care Plan\*\*[:\s]*(.*?)\Z",
        text,
        re.DOTALL | re.IGNORECASE,
    )

    if summary_match:
        summary = summary_match.group(1).strip()
    else:
        summary = text.strip()  # fallback to full text

    if care_match:
        care_plan = care_match.group(1).strip()
    else:
        care_plan = ""

    return summary, care_plan


def generate_insights(
    sensors: list[Optional[float]],
    feelings: Optional[str],
    history_entries: list[dict],
) -> tuple[str, str]:
    """Call OpenAI and return (insights/summary, care_plan)."""
    client = _get_client()
    user_msg = build_user_message(sensors, feelings, history_entries)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.4,
    )

    content = response.choices[0].message.content or ""
    summary, care_plan = parse_response(content)
    return summary, care_plan
