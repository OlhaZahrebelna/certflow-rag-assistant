---
document_id: ACD-KB-002
title: Roles and Responsibilities
document_type: procedure
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Master Data Governance Team
status: active
confidentiality: internal
tags: roles, ownership, governance
---

# Roles and Responsibilities

## 1. Requester

The Requester identifies a business need and submits an account certification or data-change request. Requesters may come from Sales Operations, Marketing Operations, Consulting, Finance, Analytics, or another approved business team.

The Requester must provide the Account ID when available, requested field changes, business reason, source link or supporting evidence, deadline, and project or initiative name. A requester proposal is not automatically treated as verified evidence.

## 2. Data Operations Analyst

The Data Operations Analyst performs the certification. The analyst:

- confirms that the correct account has been selected;
- screens for possible duplicates;
- identifies the fields in scope;
- searches sources according to `ACD-KB-005`;
- compares source evidence with current system values;
- updates or retains values according to field rules;
- records source type, source name, link, change reason, verification status, and comments;
- routes qualifying cases to QA or Governance;
- sets the certification flag only when all controls are satisfied.

The analyst must not certify a record when identity is uncertain or when mandatory evidence is missing.

## 3. Account Steward

The Account Steward represents the business ownership of account relationships and hierarchies. The Steward may clarify intended account usage, parent-child relationships, customer status, and commercial context. The Steward cannot override source requirements or directly approve unsupported master-data values.

Account Steward approval is required for material hierarchy changes, merges involving active customer records, and changes that may affect account ownership or reporting responsibility.

## 4. Quality Assurance Reviewer

The QA Reviewer independently checks selected or risk-triggered certifications. QA verifies source hierarchy, field-level evidence, normalization, duplicate screening, change reasons, and alignment between comments and system values.

QA must not replace the original analyst's evidence or rewrite the analyst's decision history. If a correction is needed, the case is returned with a documented QA finding.

## 5. Master Data Governance Lead

The Governance Lead owns policy interpretation, exceptions, field definitions, source approval, and escalations. Governance decides cases involving unresolved entity identity, conflicting primary sources, non-standard field ownership, mass updates, or requests to depart from an active rule.

Governance cannot approve fabricated evidence, bypass legal restrictions, or remove the requirement for decision traceability.

## 6. System Administrator

The System Administrator manages permissions, integrations, and technical configuration. Administrators may restore failed synchronization or correct system defects but cannot make field-certification decisions.

## 7. RAG Assistant

The RAG Assistant retrieves relevant documentation, explains validation rules, identifies required sources, and suggests an escalation path. It must:

- cite the document used;
- distinguish current rules from historical changes;
- state when evidence is insufficient;
- avoid creating facts not present in the source documentation;
- never set a certification status or update a production record.

## 8. Segregation of duties

The same analyst may research, update, and certify a standard low-risk record. Independent QA is mandatory for merges, legal-name changes with conflicting evidence, parent-account changes affecting more than five records, bulk updates above 100 records, and suspected source manipulation.
