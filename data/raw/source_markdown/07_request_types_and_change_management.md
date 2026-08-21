---
document_id: ACD-KB-007
title: Request Types and Change Management
document_type: procedure
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Data Operations Team
status: active
confidentiality: internal
tags: requests, change_log, audit
---

# Request Types and Change Management

## 1. Standard request types

| Request type | Trigger | Typical scope |
|---|---|---|
| Scheduled Account Certification | Periodic quality review | Full record |
| Auto-Created Account Certification | New account created by integration | Identity, address, domain, duplicates |
| Stakeholder Change Request | Business user proposes a change | Named fields |
| Data Correction Request | Error identified in a system or report | Incorrect fields and downstream impact |
| Project or Initiative Review | Approved bulk activity | Defined population and fields |
| System Data-Quality Alert | Automated validation rule fails | Triggering fields plus identity check |

The request type describes why work started. It does not determine whether the proposed change will be accepted.

## 2. Intake requirements

Each request must contain:

- Account ID and Account Name;
- source system;
- request type;
- requester and stakeholder team;
- project or initiative, when applicable;
- requested field or scope;
- proposed value, when applicable;
- source type and source link;
- business reason;
- requested completion date.

Missing information may be completed during triage when the entity is still identifiable. Otherwise, the request is returned to the requester.

## 3. Standardized change reasons

Use one primary reason for every changed field:

- Source-Based Validation;
- Account Certification;
- Auto-Created Account Certification;
- Stakeholder Request;
- Data Correction;
- Merger or Acquisition;
- Legal Entity Change;
- Address Relocation;
- Project or Initiative Update;
- System Synchronization Repair.

The change reason must describe the business cause, while comments explain the evidence and decision. Do not use vague reasons such as “updated,” “fixed,” or “requested.”

## 4. Required audit record

For every processed field, capture:

| Audit attribute | Description |
|---|---|
| Account identification | Account ID, Account Name, and source system |
| Value change | Previous value and approved new value |
| Decision | Field outcome and verification status |
| Reason and comments | Standardized reason plus decision explanation |
| Evidence | Source level, exact source name, and reproducible link |
| Request context | Requester, request type, and project or initiative |
| Processing | Processor and processing date |

## 5. Comments standard

A sufficient comment explains the original issue, research performed, source selected, difference found, final decision, and any follow-up. It should allow another trained analyst to understand the change without repeating the entire investigation.

Example:

> Updated Headquarters City from Northfield to Eastport. The official company contact page identifies Eastport as headquarters, and the approved professional-network profile shows the same address. Northfield is a former office location. Change reason: Address Relocation.

## 6. Bulk changes

Bulk changes require an approved field mapping, source definition, exception plan, sample validation, and row-level log. A successful upload does not prove that the data is certified.

Activity above 100 records requires QA sampling and Governance approval. Failed rows must be isolated unless they indicate a systemic mapping issue.

## 7. Rejected requests

When a proposed value is unsupported, retain the certified value, set the field outcome to Rejected, and explain the reason to the requester. Rejection of a proposed change does not mean the complete account record is rejected.
