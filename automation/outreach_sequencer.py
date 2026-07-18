"""
outreach_sequencer.py

Generates a 4-touch outreach email sequence (teaser, invite, reminder,
follow-up) for a given event + target persona, and writes draft records
into the Airtable "Contacts" table for human review.

Usage:
    python outreach_sequencer.py --event-id "recXXXXXXXX" --persona "VP Finance"
"""

import argparse
from claude_client import ask_claude_for_json
from airtable_client import get_record, create_record, TABLE_EVENTS, TABLE_CONTACTS

SYSTEM_PROMPT = """You are a B2B field marketing copywriter for Zenskar, a
usage-based billing and revenue automation platform. You write concise,
specific, non-generic outreach emails to finance and RevOps leaders inviting
them to connect at industry events. Avoid buzzwords, avoid over-selling, and
keep each email under 120 words. Write like a helpful peer, not a salesperson."""


def build_user_prompt(event_name, event_details, persona):
    return f"""Write a 4-email outreach sequence for the following event and persona.

Event: {event_name}
Event details: {event_details}
Target persona: {persona}

The 4 emails are:
1. "teaser" - sent 3 weeks before the event, introduces that Zenskar will be there, no hard ask
2. "invite" - sent 1 week before, direct ask to book a meeting/demo at the event
3. "reminder" - sent 1 day before, short reminder with booth/meeting location details (use placeholder [BOOTH NUMBER] and [MEETING LINK])
4. "follow_up" - sent 2 days after the event, references the event and proposes a concrete next step

Respond with a JSON object with exactly these keys, each containing an object with "subject" and "body":
{{
  "teaser": {{"subject": "...", "body": "..."}},
  "invite": {{"subject": "...", "body": "..."}},
  "reminder": {{"subject": "...", "body": "..."}},
  "follow_up": {{"subject": "...", "body": "..."}}
}}"""


def generate_sequence(event_name, event_details, persona):
    user_prompt = build_user_prompt(event_name, event_details, persona)
    return ask_claude_for_json(SYSTEM_PROMPT, user_prompt, max_tokens=2000)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-id", required=True, help="Airtable record ID of the event")
    parser.add_argument("--persona", required=True, help="Target persona, e.g. 'VP Finance'")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    event_record = get_record(TABLE_EVENTS, args.event_id)
    event_fields = event_record["fields"]
    event_name = event_fields.get("Event Name", "Unknown Event")
    event_details = (
        f"Dates: {event_fields.get('Dates', 'TBD')}, "
        f"Location: {event_fields.get('Location', 'TBD')}, "
        f"Audience: {event_fields.get('Audience Size', 'unknown')}"
    )

    print(f"Generating outreach sequence for '{event_name}' targeting '{args.persona}'...")
    sequence = generate_sequence(event_name, event_details, args.persona)

    for stage, email in sequence.items():
        print(f"\n--- {stage.upper()} ---")
        print(f"Subject: {email['subject']}")
        print(email["body"])

        fields = {
            "Persona": args.persona,
            "Linked Event": [args.event_id],
            "Sequence Stage": stage,
            "Draft Email Subject": email["subject"],
            "Draft Email Body": email["body"],
            "Status": "Draft",
        }
        if args.test:
            print("[TEST MODE] Would create Contacts/Outreach record with above fields.")
        else:
            create_record(TABLE_CONTACTS, fields)

    print("\nDone. Review drafts in the Contacts table before approving/sending.")


if __name__ == "__main__":
    main()
