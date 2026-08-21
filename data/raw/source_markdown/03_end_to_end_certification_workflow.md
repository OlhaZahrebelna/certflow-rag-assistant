---
document_id: ACD-KB-003
title: End-to-End Account Certification Workflow
document_type: procedure
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Data Operations Team
status: active
confidentiality: internal
tags: workflow, certification, processing
---

# End-to-End Account Certification Workflow

## 1. Intake

Certification starts from a scheduled review, auto-created account review, stakeholder request, data correction request, project initiative, or system-generated data-quality alert. The analyst confirms the request type and records the requester, project, priority, and requested completion date.

Requests without a usable Account ID must include enough information to identify the entity, such as legal name, country, website, and address.

## 2. Identify the correct entity

The analyst searches HorizonCRM and MeridianMDM for existing records using legal name, normalized name, website domain, address, and parent organization. Similar names do not prove that two records are the same entity.

Before creating or updating a record, the analyst must determine whether the request relates to:

- an existing account;
- a possible duplicate;
- a branch or subsidiary;
- a parent organization;
- a renamed legal entity;
- an acquisition or merger;
- an entity that cannot yet be identified.

If identity cannot be established, the status is **Pending Evidence** or **Escalated**, not Verified.

## 3. Define certification scope

For full certification, validate every mandatory master field. For a targeted request, validate the requested fields plus Account ID, Legal Name, Primary Domain, Headquarters Country, and duplicate risk.

The analyst records the current value before making a change. Bulk projects must preserve a row-level before-and-after audit trail.

## 4. Gather evidence

Sources must be selected according to `ACD-KB-005`. The analyst records the exact publisher or vendor name, source type, URL or record reference, publication or access date, and the fields supported.

Evidence must support the field being certified. An official website may support the public brand name but not necessarily the registered legal name. A regulatory filing may support legal identity but contain an outdated operating address.

## 5. Compare and validate

For each field in scope, the analyst compares the current system value, proposed value, and evidence. The analyst applies normalization rules without changing meaning. Examples include standard country codes, approved state names, removal of website tracking parameters, and consistent address formatting.

The analyst selects one field outcome:

- **Confirmed - No Change**;
- **Updated - Source Validated**;
- **Pending - More Evidence Required**;
- **Rejected - Proposed Value Unsupported**;
- **Escalated - Governance Decision Required**.

## 6. Record the change

Every changed field requires a standardized reason and a detailed comment. The comment must explain what changed, why, and which source supports the decision. Vendor and source names must be recorded exactly, not as generic labels such as “internet” or “database.”

Required audit fields are defined in `ACD-KB-007`.

## 7. Duplicate and hierarchy checks

Address lines, domain, legal name, country, and external identifiers are used to identify possible duplicates. The analyst must resolve or route the duplicate before setting certification to Yes. Parent-account changes follow Account Steward review when they alter reporting or commercial relationships.

## 8. Quality review

The analyst sends mandatory-risk cases to QA. Standard cases may be selected through risk-based or random sampling. QA outcomes are **Passed**, **Returned for Correction**, or **Escalated**.

## 9. Certification decision

The analyst sets the account-level status to **Verified** only when all mandatory fields in scope are resolved, evidence is stored, changes have reasons, duplicate screening is complete, and required QA has passed.

The certification record stores certification date, processor, scope, source summary, and next review trigger.

## 10. Synchronization and closure

Approved MeridianMDM values synchronize to HorizonCRM and BeaconLake. The analyst checks the integration status. A successful certification with a failed synchronization is closed as **Verified - Sync Pending**, and a technical incident is created.

The requester receives a summary of approved, rejected, pending, and escalated changes. Internal source assessments and confidential QA notes are not included in routine requester communication.
