"""
Thin wrapper around the Airtable REST API used by all automation scripts.
Centralizes table/field name constants so a schema change is a one-line edit.
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json",
}

# ---- Table names (edit here if you rename tables in Airtable) ----
TABLE_EVENTS = "Events"
TABLE_VENDORS = "Vendors"
TABLE_CONTACTS = "Contacts"
TABLE_REPORTS = "Reports"


def _check_config():
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        raise EnvironmentError(
            "AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set in your environment (.env)."
        )


def list_records(table_name, params=None):
    _check_config()
    url = f"{AIRTABLE_API_URL}/{table_name}"
    resp = requests.get(url, headers=HEADERS, params=params or {})
    resp.raise_for_status()
    return resp.json().get("records", [])


def get_record(table_name, record_id):
    _check_config()
    url = f"{AIRTABLE_API_URL}/{table_name}/{record_id}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def update_record(table_name, record_id, fields, dry_run=False):
    _check_config()
    if dry_run:
        print(f"[DRY RUN] Would update {table_name}/{record_id} with fields:")
        print(fields)
        return {"id": record_id, "fields": fields}
    url = f"{AIRTABLE_API_URL}/{table_name}/{record_id}"
    resp = requests.patch(url, headers=HEADERS, json={"fields": fields})
    resp.raise_for_status()
    return resp.json()


def create_record(table_name, fields, dry_run=False):
    _check_config()
    if dry_run:
        print(f"[DRY RUN] Would create record in {table_name} with fields:")
        print(fields)
        return {"fields": fields}
    url = f"{AIRTABLE_API_URL}/{table_name}"
    resp = requests.post(url, headers=HEADERS, json={"fields": fields})
    resp.raise_for_status()
    return resp.json()
