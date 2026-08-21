---
document_id: ACD-KB-004
title: Account Fields and Validation Rules
document_type: standard
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Master Data Governance Team
status: active
confidentiality: internal
tags: fields, validation, master_fields
---

# Account Fields and Validation Rules

## 1. Field classes

**Master Fields** define entity identity and are governed in MeridianMDM. **Operational Fields** support internal workflows and may be owned by HorizonCRM. **Derived Fields** are calculated from certified values and must not be manually overwritten unless the calculation is defective.

## 2. Core field catalog

| Field | Class | Required | Primary validation rule |
|---|---|---|---|
| Account ID | Master | Yes | System-generated and unique |
| Legal Name | Master | Yes | Match legal registration or official filing |
| Display Name | Operational | Yes | Recognizable public or trading name |
| Primary Domain | Master | Yes | Normalized domain controlled by the entity |
| Website URL | Master | Yes | Reachable official website using HTTPS when available |
| Address Line 1 | Master | Yes | Street and building information for headquarters |
| Address Line 2 | Master | Conditional | Suite, unit, floor, or local secondary information |
| City | Master | Yes | Official locality name |
| Postal Code | Master | Conditional | Required where the country uses postal codes |
| State or Province | Master | Conditional | Required for countries with governed subdivisions |
| Country | Master | Yes | Approved country name and ISO alpha-2 code |
| Parent Account | Master | Conditional | Verified controlling or direct parent entity |
| Account Status | Operational | Yes | Active, Inactive, Acquired, Closed, or Unknown |
| Ownership Type | Master | Yes | Public, Private, Government, Nonprofit, or Unknown |
| Trading Symbol | Master | Conditional | Symbol only, without exchange name |
| Exchange Code | Master | Conditional | Approved exchange code stored separately |
| Industry | Master | Yes | Approved taxonomy category |

## 3. Legal Name

Legal Name must represent the registered entity, including the legal suffix when supported by the governing source. Do not replace a legal name with a brand or product name. When an organization uses multiple registered entities, certify the entity that matches the account's country, contract, or operational purpose.

A legal-name change requires evidence of registration, official filing, merger, or reorganization. A website rebrand alone does not prove a legal-name change.

## 4. Display Name

Display Name is the recognizable name used in user interfaces. It may omit legal suffixes when that improves usability. It must not imply that a subsidiary is the parent company or combine unrelated organizations.

## 5. Website and Primary Domain

Store the canonical public website without tracking parameters or unnecessary paths. Primary Domain contains only the normalized host, for example `atlas-example.com`, without protocol, `www`, path, or query string.

Redirects are acceptable when they resolve to the same organization. A social profile, marketplace listing, email-provider domain, or reseller page cannot be the primary website.

## 6. Account Status

Use **Active** when the organization is operating and the entity can be verified. Use **Acquired** when the entity has been purchased but remains historically relevant. Use **Closed** only when a reliable source confirms cessation or dissolution. A broken website alone is insufficient to mark an account Closed.

## 7. Parent Account

Parent relationships must reflect verified ownership or control, not partnership, brand similarity, or distribution agreements. The direct parent is preferred over the ultimate parent unless the data model specifies otherwise. Evidence must identify both entities and the relationship.

## 8. Trading Symbol and Exchange Code

For public companies, store the trading symbol and exchange code in separate fields. Use the primary listing unless the certification request explicitly concerns another listed security. Do not include punctuation that belongs to the exchange display format unless it is part of the official symbol.

## 9. Unknown values

Use an approved **Unknown** value only when the field permits it and the analyst has completed the required research. Empty, `N/A`, `-`, `TBD`, and invented placeholder values are not interchangeable.
