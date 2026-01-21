import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client using API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_incident_summary(log_entries):
    """
    Generate a human-readable incident summary from structured log entries.

    log_entries: list of dicts with keys:
        - timestamp
        - level
        - category
        - severity
        - message
    """

    # Build context from structured logs
    context = "\n".join([
        f"- [{entry['level']}] {entry['category']} | "
        f"Severity: {entry['severity']} | "
        f"{entry['message']}"
        for entry in log_entries
    ])

    prompt = f"""
You are a technical support assistant.

Summarize the following incident logs into:
1. Incident Overview
2. Impact
3. Recommended Next Action

Keep the summary concise, factual, and suitable for sharing with engineers
and stakeholders.

Logs:
{context}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception:
        # -----------------------------
        # FALLBACK SUMMARY (NO LLM)
        # -----------------------------
        high = sum(1 for e in log_entries if e["severity"] == "HIGH")
        medium = sum(1 for e in log_entries if e["severity"] == "MEDIUM")
        low = sum(1 for e in log_entries if e["severity"] == "LOW")

        return (
            "LLM unavailable. Generated fallback incident summary.\n\n"
            "Incident Overview:\n"
            f"- Total events: {len(log_entries)}\n"
            f"- High severity events: {high}\n"
            f"- Medium severity events: {medium}\n"
            f"- Low severity events: {low}\n\n"
            "Recommended Next Action:\n"
            "- Investigate high severity errors first\n"
            "- Review database, memory, and timeout related issues\n"
            "- Monitor system stability after remediation\n"
        )
