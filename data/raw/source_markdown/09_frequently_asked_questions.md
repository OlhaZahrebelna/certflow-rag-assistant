---
document_id: ACD-KB-009
title: Account Certification Frequently Asked Questions
document_type: faq
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Data Operations Team
status: active
confidentiality: internal
tags: faq, analyst_support
---

# Account Certification Frequently Asked Questions

## General

### Are we certifying the company?

No. We are certifying that the account master-data record meets the current ADS rules based on evidence available on the verification date.

### Can the RAG Assistant certify a record?

No. It can retrieve rules, explain required evidence, and suggest next steps. A trained analyst remains responsible for the decision and system update.

### Does certification mean that every field will remain correct forever?

No. Certification is valid as of the verification date. A material change or new contradictory evidence triggers review.

## Sources

### Can I use the first search result?

No. Search results and snippets are indicators only. Open and assess an approved primary or secondary source.

### What source should I use for headquarters address?

Use the official corporate website first. If it does not provide the address, use the organization's official profile on an approved professional network. If neither is available, the same address must appear in at least two independent approved business databases.

### What if two primary sources disagree?

Check whether they describe different address types, legal entities, or dates. If the conflict cannot be resolved, use Pending Evidence or escalate to Governance.

### Can a requester-provided value be treated as verified?

Only when the attached source independently satisfies the evidence rules. The request itself is not proof.

## Address and duplicates

### Why is address a Master Field?

Address supports duplicate screening, entity matching, onboarding, geographic reporting, enrichment, and territory logic. An incorrect address can create or combine the wrong records.

### Can I use a branch address when headquarters is unavailable?

No. A branch address is a different address type. Use Pending Evidence unless the request specifically concerns a branch and the data model supports it.

### Do two accounts at the same address mean they are duplicates?

No. Different companies may share a building. Compare legal name, domain, identifiers, parent relationship, and other identity evidence.

### Can I merge two records when one has no activity?

Only after identity is confirmed and the merge process is followed. Active records, ownership conflicts, or different relationships require Account Steward and QA review.

## Field decisions

### A company uses a brand name on its website. Should I replace Legal Name?

Not without legal evidence. The brand may be used as Display Name, while Legal Name must follow registration or official filing evidence.

### What should Trading Symbol contain?

Only the official symbol. Store the Exchange Code in its separate field.

### The website is broken. Should Account Status be Closed?

No. A broken website is not sufficient evidence that the organization has closed.

### What if I cannot find a mandatory value?

Record the research, set the field to Pending Evidence, and keep certification No. Do not invent or copy a nearby value.

## Changes and audit

### Do I need a reason when only formatting changes?

Yes. Use the applicable standardized reason and explain that the value was normalized without changing its meaning.

### Can I write “fixed based on internet” in comments?

No. Record the exact source name, source level, link, affected value, and decision explanation.

### Does a successful system upload mean certification succeeded?

No. Technical upload and business certification are separate controls. Certification requires validation, evidence, audit fields, duplicate checks, and any required QA.
