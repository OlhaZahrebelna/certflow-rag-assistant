---
document_id: ACD-KB-006
title: Address Certification and Duplicate Prevention
document_type: standard
version: "1.1"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Data Operations Team
status: active
confidentiality: internal
tags: address, duplicates, entity_matching
---

# Address Certification and Duplicate Prevention

## 1. Business purpose

Headquarters Address is a Master Field used for entity matching, duplicate search, geographic reporting, territory logic, enrichment, and account onboarding. An incomplete or incorrectly normalized address can create duplicate records or cause data from different legal entities to be combined.

## 2. Address components

The certified address contains:

- Address Line 1;
- Address Line 2, when applicable;
- City;
- Postal Code, where used;
- State or Province, where required;
- Country and ISO alpha-2 code.

Address Line 1 and Address Line 2 participate in duplicate-search criteria. Do not move essential street information into comments or omit unit information that distinguishes entities at the same location.

## 3. Address type

Certify the headquarters or principal operating address defined by the active account model. Do not substitute a registered-agent, mailing, billing, branch, warehouse, or virtual-office address unless that address type is explicitly requested and stored in the correct field.

When the official website and government registry show different addresses, determine whether one is headquarters and the other is registered office. Record the headquarters value in the Headquarters Address fields and preserve the registered address only where the model provides separate fields.

## 4. Address source order

Use sources in this order:

1. headquarters or contact page on the official corporate website;
2. official company profile on an approved professional network;
3. matching value from at least two independent approved business databases.

Government registries and regulatory filings may establish a registered address but do not automatically prove the current headquarters address. They should be used according to the address type being certified.

## 5. Normalization

Normalization improves consistency without changing the real-world meaning.

- Use approved country and subdivision names.
- Preserve meaningful building, suite, and unit identifiers.
- Remove duplicate punctuation and unnecessary line breaks.
- Do not translate street or city names unless the country standard requires an approved English form.
- Do not invent a postal code or state from nearby locations.
- Store country code separately from the address text.

## 6. Duplicate screening

Before creating or certifying an account, search by:

- normalized legal and display names;
- primary domain and website;
- Address Line 1 and City;
- postal code and country;
- external identifiers, where available;
- parent account and known aliases.

A match on one weak attribute is not enough. For example, organizations in the same office building may share an address, and unrelated subsidiaries may share a parent domain.

## 7. Duplicate outcomes

| Outcome | Action |
|---|---|
| No likely duplicate | Continue certification |
| Possible duplicate | Set Pending QA and compare identity fields |
| Confirmed duplicate with no activity conflict | Submit merge request |
| Confirmed duplicate with active records or conflicting relationships | Escalate to Account Steward and QA |
| Branch or subsidiary, not duplicate | Retain separate record and document relationship |

## 8. Missing address information

If a required address component is missing, continue research using the source hierarchy. If it cannot be verified, leave the certification flag as No and set the field outcome to Pending Evidence. Do not copy a nearby branch address or use a search-engine map pin as proof.

## 9. Address change

An address change is material when it affects country, state, territory assignment, duplicate matching, or entity identity. Record the previous and new values, change reason, effective date if known, and supporting sources. A major change may require downstream matching or enrichment to be rerun.
