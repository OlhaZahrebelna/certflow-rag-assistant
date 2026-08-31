---
document_id: ACD-KB-001
title: Account Data Certification Overview
document_type: policy
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Master Data Governance Team
status: active
confidentiality: internal
tags: account_certification, master_data, data_quality
---

# Account Data Certification Overview

## 1. Purpose

Account Data Certification is the controlled process used by Atlas Data Services (ADS) to confirm that a company account record is complete, accurate, consistent, traceable, and suitable for operational and analytical use. The certified object is the **account record**, not a person or organization receiving a professional credential.

Certification supports account onboarding, duplicate prevention, entity matching, reporting, segmentation, customer communication, and synchronization between HorizonCRM, MeridianMDM, and BeaconLake.

## 2. Systems and ownership

MeridianMDM is the system of record for core master fields. HorizonCRM consumes certified account data for commercial workflows and may own operational fields where an active field rule explicitly assigns ownership to it. BeaconLake receives approved data for analytics and reporting.

When the same core master field differs between systems, the MeridianMDM value takes precedence unless an active field-specific rule explicitly assigns ownership elsewhere. Master Fields are governed and updated in MeridianMDM and synchronized downstream where applicable. Operational Fields are updated in their owning operational system. Derived Fields are recalculated from certified source fields and must not be manually overwritten except to correct a defective calculation.

## 3. Certification scope

The standard certification scope includes:

- Account ID and source-system identifier;
- Legal Name and Display Name;
- Website and Primary Domain;
- Headquarters Address;
- Country and State or Province;
- Account Status;
- Parent Account relationship;
- Ownership Type;
- Trading Symbol and Exchange Code, where applicable;
- Industry classification;
- source links, verification date, processor, and change reason.

Certification may be full or targeted. A full certification assesses all mandatory fields. A targeted certification assesses the fields named in an approved request plus the mandatory identity and duplicate controls defined in `ACD-KB-003`. It does not require every mandatory field outside the approved scope to be recertified.

## 4. Account certification outcomes

Account-level certification status is separate from field-level outcomes. A proposed field change may be rejected while the overall account can still be Verified if the existing certified value remains supported and all controls in scope are satisfied.

| Account outcome | Meaning | Certification flag |
|---|---|---|
| Verified | All fields and controls in the certification scope meet the active rules | Yes |
| Pending Evidence | Required evidence for one or more in-scope decisions is insufficient, unavailable, or contradictory | No |
| Pending QA | Analyst review is complete and mandatory QA is still required | No |
| Rejected | The account itself cannot be certified under the active rules; this is not used merely because one proposed field change was rejected | No |
| Escalated | Governance, legal, privacy, or material entity-resolution issue requires higher-authority review | No |

Field-level outcomes are defined in `ACD-KB-003` and must not be confused with account-level status.

The certification flag may be set to **Yes** only after all mandatory controls within the certification scope are verified, required change reasons are recorded, evidence links are saved, duplicate screening is complete, and any required QA review has passed.

## 5. Business principles

- Every changed value must have a standardized change reason.
- A reviewer must be able to reproduce the decision from the saved evidence and comments.
- Source quality takes precedence over source quantity.
- Field-specific validation rules take precedence over generic fallback rules.
- Search results, snippets, and AI-generated summaries cannot be used as certification evidence.
- Conflicting evidence must be resolved or escalated; analysts must not select the most convenient value.
- The assistant may retrieve policy and suggest steps, but a trained analyst remains responsible for certification.

## 6. Certification validity

Certification confirms the record as of the recorded verification date. It does not guarantee that the real-world organization will remain unchanged. A record must be recertified when a material change is reported, a scheduled review becomes due, a trusted source contradicts the certified value, or a downstream matching failure indicates possible inaccuracy.

## 7. Service targets

| Activity | Target |
|---|---:|
| Standard single-account certification | 3 business days |
| Simple correction request | 2 business days |
| Bulk project review | Agreed in project plan |
| QA review | 2 business days |
| Critical duplicate or legal-entity escalation routing | Within 4 business hours |

Targets measure processing time while the case is assigned to ADS. Time waiting for requester clarification or external evidence is excluded. Escalation acknowledgement targets are defined separately in `ACD-KB-008`.