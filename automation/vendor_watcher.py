"""
vendor_watcher.py

Scans the Vendors table daily for contracts/payments approaching or past
deadline, flags them in Airtable, and optionally pushes a Slack alert via
a Zapier webhook.

Usage:
    python vendor_watcher.py --dry-run
    python vendor_watcher.py            # live run (writes to Airtable + Slack)

Intended to be run daily via the GitHub Actions workflow in
.github/workflows/vendor_watcher.yml
"""

import argparse
import os
import requests
from datetime import datetime, timedelta

from airtable_client import list_records, update_record, TABLE_VENDORS

CONTRACT_WARNING_DAYS = 5
PAYMENT_OVERDUE_GRACE_DAYS = 3

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")


def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def evaluate_vendor(fields):
    """Returns (risk_flag, reason) or (None, None) if no risk."""
    today = datetime.today()

    contract_status = fields.get("Contract Status", "")
    contract_deadline = parse_date(fields.get("Contract Deadline"))
    payment_status = fields.get("Payment Status", "")
    payment_due = parse_date(fields.get("Payment Due Date"))

    if contract_status != "Signed" and contract_deadline:
        days_left = (contract_deadline - today).days
        if days_left <= CONTRACT_WARNING_DAYS:
            status = "OVERDUE" if days_left < 0 else f"{days_left} day(s) left"
            return "Red", f"Contract unsigned, deadline {status}"

    if payment_status != "Paid" and payment_due:
        days_overdue = (today - payment_due).days
        if days_overdue >= PAYMENT_OVERDUE_GRACE_DAYS:
            return "Red", f"Payment overdue by {days_overdue} day(s)"

    if contract_status != "Signed" and contract_deadline:
        days_left = (contract_deadline - today).days
        if CONTRACT_WARNING_DAYS < days_left <= CONTRACT_WARNING_DAYS * 2:
            return "Yellow", f"Contract deadline approaching ({days_left} days left)"

    return None, None


def send_slack_alert(message):
    if not SLACK_WEBHOOK_URL:
        print("[INFO] SLACK_WEBHOOK_URL not set, skipping Slack alert.")
        return
    requests.post(SLACK_WEBHOOK_URL, json={"message": message})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    vendors = list_records(TABLE_VENDORS)
    alerts = []

    for vendor in vendors:
        fields = vendor["fields"]
        risk_flag, reason = evaluate_vendor(fields)

        current_flag = fields.get("Risk Flag")
        if risk_flag and risk_flag != current_flag:
            vendor_name = fields.get("Vendor Name", "Unknown vendor")
            alerts.append(f":warning: *{vendor_name}* — {reason}")
            update_record(TABLE_VENDORS, vendor["id"], {"Risk Flag": risk_flag}, dry_run=args.dry_run)
        elif not risk_flag and current_flag in ("Red", "Yellow"):
            # Risk has cleared (e.g. contract got signed) — reset flag
            update_record(TABLE_VENDORS, vendor["id"], {"Risk Flag": "Green"}, dry_run=args.dry_run)

    if alerts:
        message = "*Vendor risk alerts:*\n" + "\n".join(alerts)
        print(message)
        if not args.dry_run:
            send_slack_alert(message)
    else:
        print("No vendor risks detected today.")


if __name__ == "__main__":
    main()
