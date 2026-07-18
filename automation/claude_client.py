"""
Thin wrapper around the Anthropic Messages API used by all automation scripts.

TEMPORARY MOCK MODE is active below to allow testing without API credits.
Remove the mock block in ask_claude_for_json() once you add credits at
console.anthropic.com to switch back to real Claude responses.
"""

import os
import json
import anthropic
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-6"


def ask_claude(system_prompt, user_prompt, max_tokens=1500):
    """Send a single-turn prompt to Claude and return the plain text response."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def ask_claude_for_json(system_prompt, user_prompt, max_tokens=1500):
    """
    Send a prompt that instructs Claude to respond with ONLY valid JSON,
    parse it, and return a Python dict. Raises if parsing fails.
    """
    # --- TEMPORARY MOCK: delete this whole if-block once you add API credits ---
    if "teaser" in user_prompt and "invite" in user_prompt:
        return {
            "teaser": {"subject": "See you there? (mocked)", "body": "Mocked teaser email body."},
            "invite": {"subject": "Grab 20 minutes? (mocked)", "body": "Mocked invite email body."},
            "reminder": {"subject": "Reminder: tomorrow (mocked)", "body": "Mocked reminder email body."},
            "follow_up": {"subject": "Great meeting you (mocked)", "body": "Mocked follow-up email body."},
        }
    if "executive_summary" in user_prompt or "cost_per_lead" in user_prompt:
        return {
            "cost_per_lead": "$42 (mocked)",
            "executive_summary": "Mocked executive summary of event performance.",
            "notable_wins": "Mocked notable wins text.",
            "notable_issues": "Mocked notable issues text.",
            "recommendation": "Mocked recommendation text.",
        }
    return {
        "estimated_audience_size": "10000+ attendees (mocked)",
        "estimated_cost_tier": "$20k-25k sponsorship (mocked)",
        "competitor_presence": "High - multiple billing/CPQ vendors expected (mocked)",
        "fit_score": 5,
        "fit_rationale": "This is placeholder data returned without calling the real API, since no credits are loaded yet.",
    }
    # --- END TEMPORARY MOCK ---

    strict_system = (
        system_prompt
        + "\n\nCRITICAL: Respond with ONLY valid JSON. No preamble, no markdown "
        "code fences, no explanation before or after. The entire response must "
        "be a single parseable JSON object."
    )
    raw = ask_claude(strict_system, user_prompt, max_tokens=max_tokens)
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude did not return valid JSON. Raw output:\n{raw}") from e
