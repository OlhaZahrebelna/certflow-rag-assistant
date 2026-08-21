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

MeridianMDM is the system of record for core master fields. HorizonCRM consumes certified account data for commercial workflows. BeaconLake receives approved data for analytics and reporting. When the same core field differs between systems, the MeridianMDM value takes precedence unless an active field rule explicitly assigns ownership elsewhere.

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

Certification may be full or targeted. A full certification assesses all mandatory fields. A targeted certification assesses only the fields named in an approved request, but it must still include duplicate screening and identity confirmation.

## 4. Certification outcomes

| Outcome | Meaning | Certification flag |
|---|---|---|
| Verified | All fields in scope meet the active rules | Yes |
| Pending Evidence | Available evidence is insufficient or contradictory | No |
| Pending QA | Analyst review is complete and mandatory QA is required | No |
| Rejected | The requested change is unsupported or the record is not certifiable | No |
| Escalated | Governance, legal, privacy, or material entity-resolution issue exists | No |

The certification flag may be set to **Yes** only after mandatory fields are verified, required change reasons are recorded, evidence links are saved, and any required QA review is complete.

## 5. Business principles

- Every changed value must have a standardized change reason.
- A reviewer must be able to reproduce the decision from the saved evidence and comments.
- Source quality takes precedence over source quantity.
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
| Critical duplicate or legal-entity escalation | 4 business hours |

Targets measure processing time while the case is assigned to ADS. Time waiting for requester clarification or external evidence is excluded.
