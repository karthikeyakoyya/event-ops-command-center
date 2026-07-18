"""
Thin wrapper around the Anthropic Messages API used by all automation scripts.
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
