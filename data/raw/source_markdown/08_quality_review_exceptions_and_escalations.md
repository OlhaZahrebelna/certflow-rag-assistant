---
document_id: ACD-KB-008
title: Quality Review, Exceptions, and Escalations
document_type: procedure
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Master Data Governance Team
status: active
confidentiality: internal
tags: qa, exceptions, escalation
---

# Quality Review, Exceptions, and Escalations

## 1. Quality review purpose

Quality review confirms that the certification decision is reproducible, evidence-based, and consistent with current policy. QA checks the process and decision; it does not merely verify that all fields are populated.

## 2. Mandatory QA triggers

QA is mandatory for:

- possible or confirmed duplicates;
- merges involving active customer records;
- conflicting primary sources;
- legal-name changes connected to merger or acquisition;
- parent changes affecting more than five accounts;
- bulk updates above 100 records;
- suspected source manipulation;
- requests to use a non-approved source;
- certification performed under an approved exception.

## 3. QA checklist

The QA Reviewer confirms:

1. the correct entity and record were selected;
2. scope is clear;
3. mandatory fields were processed;
4. source hierarchy was followed;
5. source names and links are reproducible;
6. field values follow normalization rules;
7. duplicate screening was completed;
8. change reasons and comments are sufficient;
9. system values match the documented decision;
10. downstream synchronization status is recorded.

## 4. QA outcomes

**Passed** means certification may be completed. **Returned for Correction** means the analyst can correct a defined issue without a Governance decision. **Escalated** means policy interpretation, entity identity, legal risk, or systemic impact requires a higher authority.

## 5. Exceptions

An exception permits an alternative operational control when the standard method is unavailable. It does not permit unsupported data or lower evidence quality.

Governance may approve limited exceptions involving temporary source unavailability, non-standard file transfer, extended processing time, or an alternative approved verification route. Exceptions must identify the affected rule, reason, risk, compensating control, approver, and expiry date.

The following cannot be waived:

- correct entity identification;
- duplicate screening;
- evidence traceability;
- mandatory privacy and access controls;
- required QA for a merge;
- prohibition on invented values;
- human responsibility for the certification decision.

## 6. Escalation levels

| Level | Example | Owner | Acknowledgement target |
|---|---|---|---:|
| Operational | Missing field, sync failure, requester clarification | Data Operations Lead | 1 business day |
| Data Governance | Conflicting sources, field-ownership ambiguity | Governance Lead | 2 business days |
| Entity Resolution | Duplicate, merger, complex hierarchy | QA Lead and Account Steward | 1 business day |
| Legal or Privacy | Sanctions concern, legal demand, personal-data exposure | Legal or Privacy Team | Immediate |

## 7. Pending Evidence

Use Pending Evidence when the correct value may exist but cannot yet be supported. Record sources checked, missing evidence, person responsible for follow-up, and review date. Do not set a placeholder value simply to close the request.

## 8. Suspected manipulation

Do not accuse the requester or modify submitted evidence. Preserve the request and sources, restrict comments to authorized users, place the record in Pending QA, and escalate. Certification remains No until the issue is resolved.

## 9. Repeated defects

QA aggregates recurring errors by field, source, request type, and processor. Repeated issues may indicate unclear documentation, training gaps, defective integration rules, or unreliable vendors. Governance reviews trends quarterly and updates rules or training when necessary.
