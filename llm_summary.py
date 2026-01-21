import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def generate_incident_summary(logs):
    """
    Generate an incident summary using an LLM if available.
    Falls back to deterministic summary if LLM is unavailable.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    # -----------------------------
    # Fallback summary (SAFE DEFAULT)
    # -----------------------------
    def fallback_summary():
        total = len(logs)
        high = sum(1 for l in logs if l["severity"] == "HIGH")
        medium = sum(1 for l in logs if l["severity"] == "MEDIUM")
        low = sum(1 for l in logs if l["severity"] == "LOW")

        return f"""
LLM unavailable. Generated fallback incident summary.

Incident Overview:
- Total events: {total}
- High severity events: {high}
- Medium severity events: {medium}
- Low severity events: {low}

Recommended Next Actions:
- Investigate high severity errors first
- Review recurring database, memory, or timeout issues
- Monitor system stability after remediation
""".strip()

    # -----------------------------
    # If OpenAI is not usable → fallback
    # -----------------------------
    if OpenAI is None or not api_key:
        return fallback_summary()

    # -----------------------------
    # LLM-based summary
    # -----------------------------
    try:
        client = OpenAI(api_key=api_key)

        context = "\n".join(
            f"[{l['level']}] {l['message']}" for l in logs[:50]
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an SRE assistant summarizing incidents from logs.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following logs:\n{context}",
                },
            ],
        )

        return response.choices[0].message.content

    except Exception:
        return fallback_summary()
