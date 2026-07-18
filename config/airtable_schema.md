# Airtable Schema Reference

Create a base called **"Event Ops"** with these four tables. Field types noted in parentheses.

## Table: Events
| Field | Type |
|---|---|
| Event Name | Single line text (primary field) |
| URL | URL |
| Dates | Single line text (or Date range if using a date-range friendly view) |
| Location | Single line text |
| Cost | Currency |
| Audience Size | Single line text |
| Competitor Presence | Long text |
| Fit Score | Number (1-5) |
| Fit Rationale | Long text |
| Status | Single select: Researching / Confirmed / Live / Completed |
| Leads Captured | Number |
| Notes | Long text |

## Table: Vendors
| Field | Type |
|---|---|
| Vendor Name | Single line text (primary field) |
| Linked Event | Link to Events |
| Contract Status | Single select: Unsigned / Signed |
| Contract Deadline | Date |
| Payment Status | Single select: Unpaid / Paid |
| Payment Due Date | Date |
| Contact Email | Email |
| Risk Flag | Single select: Green / Yellow / Red (colored) |

## Table: Contacts
| Field | Type |
|---|---|
| Contact Name | Single line text (primary field) |
| Company | Single line text |
| Persona | Single line text |
| Linked Event | Link to Events |
| Sequence Stage | Single select: teaser / invite / reminder / follow_up |
| Draft Email Subject | Single line text |
| Draft Email Body | Long text |
| Status | Single select: Draft / Approved / Sent |

## Table: Reports
| Field | Type |
|---|---|
| Linked Event | Link to Events (primary field via lookup, or add a Name field) |
| AI-Generated Summary | Long text |
| Cost per Lead | Single line text |
| Notable Wins | Long text |
| Notable Issues | Long text |
| Report File Link | URL or single line text |

## Import Tip
You can bulk-import `data/sample_events.csv`, `data/sample_vendors.csv`, and `data/sample_contacts.csv` directly via Airtable's **"Add or import → CSV file"** option when first creating each table, then adjust field types afterward to match the types above (Airtable will default everything to text on import).
