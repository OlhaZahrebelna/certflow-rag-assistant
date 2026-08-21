---
document_id: ACD-KB-010
title: Account Certification Policy Change Log
document_type: change_log
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Master Data Governance Team
status: active_reference
confidentiality: internal
tags: change_log, release_notes, history
---

# Account Certification Policy Change Log

## 1. Purpose

This document records historical rule changes. Active policies and standards already contain current instructions. Historical rules must not be applied to current records unless a time-based audit question specifically requires them.

## 2. Release ACD-2026.04

**Effective date:** 2026-04-01  
**Release owner:** Master Data Governance Team

### Change 1: trading data split into two fields

**Previous rule:** A legacy `Market Listing` field stored the trading symbol and exchange together using the format `SYMBOL@EXCHANGE`.

**Current rule:** Store the official symbol in **Trading Symbol** and the approved exchange code in **Exchange Code**. Do not store the combined legacy format in either field.

**Reason:** Separate attributes improve matching, filtering, validation, and downstream reporting.

**Implemented in:** `ACD-KB-004`, version 1.0.

### Change 2: stronger fallback evidence for headquarters address

**Previous rule:** One approved commercial database could be used when the official website did not provide a headquarters address.

**Current rule:** Use the official corporate website first, then the official professional-network profile. If neither contains the address, the same value must appear in at least two independent approved business databases.

**Reason:** QA identified inconsistent address updates caused by stale values in individual data providers.

**Implemented in:** `ACD-KB-005`, version 1.0, and `ACD-KB-006`, version 1.1.

### Change 3: standardized field-level change reasons

**Previous rule:** Analysts could enter free-text reasons such as “updated” or “business request.”

**Current rule:** Every changed field must use one standardized change reason and a separate detailed comment.

**Reason:** Standardized reasons support audit reporting, error analysis, training, and measurement of certification workload.

**Implemented in:** `ACD-KB-003`, version 1.0, and `ACD-KB-007`, version 1.0.

### Change 4: explicit RAG Assistant boundary

**Previous rule:** No AI-assistant role was defined.

**Current rule:** The RAG Assistant may retrieve and explain policy but cannot certify records, approve exceptions, or update production data.

**Reason:** The boundary preserves human accountability and prevents policy retrieval from being mistaken for a data decision.

**Implemented in:** `ACD-KB-001`, version 1.0, and `ACD-KB-002`, version 1.0.

## 3. Migration guidance

Open records created before 2026-04-01 must be processed under the active rules when certification is completed on or after the effective date. Legacy combined listing values must be split during the next material update or scheduled certification. Historical audit entries must not be rewritten.

## 4. RAG retrieval guidance

For a current-process question, retrieve the active owning document instead of using the “Previous rule” text in this change log. Use this file when the user asks what changed, why a value was migrated, or which rule applied before 2026-04-01.
