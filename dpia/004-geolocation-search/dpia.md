---
title: "DPIA 004 — Geolocation Search"
version: "1.0.0"
status: "reviewed"
owner: "Compliance Team"
dpo: "DPO — journeyoflife.org"
reviewers: ["Legal Counsel", "CISO"]
created: "2026-09-02"
review_date: "2027-01-15"
linked_ropa: ["ROPA-006"]
gate: "G2"
---

# DPIA 004 — Geolocation Search

## 1. Processing Description

### Purpose
Location-based search for parcel lockers, seller proximity, and
delivery options. PostGIS geospatial queries on product/seller locations.

### Data Subjects
- **Buyers**: delivery address, locker preference, IP-based location.
- **Sellers**: business address (for proximity calculations).

### Personal Data Categories

| Data Category | Subjects | Special Category (Art. 9)? |
|---------------|----------|---------------------------|
| Delivery address (lat/lon) | Buyers | No |
| IP address (geo-IP) | Buyers | No |
| Locker preference | Buyers | No |
| Seller business address | Sellers | No |

### Data Flows
```
Buyer browser → Django backend → search_app
  ├── Geo-IP lookup (IP → approximate country/city)
  ├── PostGIS distance query (buyer location → nearest lockers)
  └── Results returned (no location stored beyond session)
```

### Legal Basis

| Processing | Lawful Basis | Reference |
|-----------|-------------|-----------|
| Delivery address | Art. 6(1)(b) — contract performance | ToS §4 |
| Geo-IP (approximate) | Art. 6(1)(f) — legitimate interest | Privacy Policy §8 |
| Locker proximity | Art. 6(1)(b) — contract performance | ToS §4 |

### Retention

| Data | Retention | Deletion |
|------|-----------|----------|
| Delivery address | Duration of order + 10 years (financial) | Anonymize |
| Geo-IP result | Session only | Not stored |
| Locker preference | Session only | Not stored |

## 2. Necessity & Proportionality

- **Delivery address**: Required for shipping. Proportional.
- **Geo-IP**: Used only for country detection (not precise location).
  Proportional — no coordinates stored.
- **PostGIS queries**: Computed on-the-fly from seller/locker data.
  No buyer location stored beyond the session.

## 3. Risk Assessment

| Risk Scenario | Likelihood | Impact | Mitigation | Residual |
|---------------|-----------|--------|------------|----------|
| Location data leak | Low | Medium | Not stored beyond session; PostGIS in-memory | Low |
| Geo-IP profiling | Low | Medium | Country-level only; no precise coordinates | Low |
| Seller address exposure | Low | Medium | Address shown only to buyers in same order | Low |

## 4. Technical & Organizational Measures

- **No location storage**: Buyer location computed on-the-fly, never persisted.
- **PostGIS**: Geospatial queries run in PostgreSQL; results not cached.
- **Geo-IP**: Country-level only (no lat/lon stored).
- **Access control**: Seller addresses visible only to buyers who ordered.

## 5. Processor Check

No new processors. DPD/Omniva receive delivery addresses as part of
shipping (already covered in ROPA-003).

## 6. Legal-Text Impact

| Text | Impact | Version Bump |
|------|--------|-------------|
| Privacy Policy | §8 (location data) | MINOR |

## 7. Conclusion & Sign-off

**Residual risk acceptable: YES.** Location data is not stored beyond the
session. Geo-IP is country-level only. PostGIS queries are computed on-the-fly.

- DPO consulted: [PENDING]
- Approved by: [PENDING]
- Date: [PENDING]
- SHA-256: [COMPUTE AFTER SIGNATURE]
