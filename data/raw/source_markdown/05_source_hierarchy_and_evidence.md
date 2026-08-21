---
document_id: ACD-KB-005
title: Source Hierarchy and Evidence Standard
document_type: standard
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Master Data Governance Team
status: active
confidentiality: internal
tags: sources, evidence, hierarchy
---

# Source Hierarchy and Evidence Standard

## 1. Principle

The purpose of the source hierarchy is to make certification decisions consistent and reproducible. Analysts must use the highest-quality reasonably available source that directly supports the field. A lower-level source cannot overrule a current and applicable higher-level source without documented justification.

## 2. Primary sources

Primary sources originate from the organization or an authoritative public body.

| Source | Typical fields supported |
|---|---|
| Official corporate website | Display Name, Website, Primary Domain, Headquarters Address |
| Government company registry | Legal Name, registration status, registered address |
| Regulatory or annual filing | Legal Name, ownership, headquarters, public status |
| Official stock exchange listing | Trading Symbol, Exchange Code, listing status |
| Official parent-company report | Parent relationship, acquisition, subsidiary status |

Primary sources are preferred when they are current, applicable to the correct legal entity, and sufficiently specific. An official website footer may identify a different legal entity from the account under review; the analyst must confirm scope.

## 3. Secondary sources

Secondary sources are reputable sources that compile or publish organization information but do not directly establish every legal fact.

Examples include an official company profile on a major professional network, an approved commercial business-data provider, a recognized industry registry, and a reputable business directory.

Secondary sources may support certification when:

- no usable primary source exists;
- the field is not a legal-identity field; or
- two independent approved sources agree on the same value.

For headquarters address, use the official corporate website first. If unavailable, use the organization's official professional-network profile. If neither provides the value, the same address must appear in at least two independent approved business databases.

## 4. Tertiary indicators

Search snippets, unsourced aggregators, general map results, news summaries, social posts, AI-generated text, and user-edited encyclopedias are indicators only. They may help locate a better source but cannot independently support certification.

## 5. Conflicting sources

When sources conflict, the analyst considers:

1. whether the sources refer to the same legal entity;
2. source authority for the specific field;
3. publication or last-update date;
4. whether one value is registered and another operational;
5. whether a merger, relocation, rebrand, or restructuring occurred;
6. whether the difference is formatting or meaning.

Conflicting primary sources require a documented resolution or Governance escalation. Do not average, combine, or arbitrarily select values.

## 6. Evidence recording

For each certification, record:

- source level: Primary or Secondary;
- exact source or vendor name;
- URL or internal source reference;
- access or publication date;
- fields supported;
- relevant evidence excerpt in paraphrased form;
- analyst conclusion.

Do not record credentials, subscription tokens, personal contact information, or copied copyrighted content beyond what is necessary for traceability.

## 7. Source freshness

There is no single freshness period for every field. Time-sensitive fields such as address, status, parent relationship, and public listing should use the most recent reliable evidence. Stable legal identifiers may rely on older primary evidence when no material change is indicated.

## 8. Unavailable sources

If a source is blocked, inaccessible, or available only through an unapproved personal account, the analyst must not bypass access controls. Use another approved source or set the case to Pending Evidence.
