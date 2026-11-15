# Data Dictionary — Subscription Churn Prediction & Risk Scoring

## Overview & Provenance
- **Dataset Scale**: 20,000 Customers | 635,628 total relational records across 6 CSV files.
- **Dataset Provenance**: Production-grade synthetic relational dataset modeled after a standard B2B/B2C SaaS business model. Generated using python (`python/generate_dataset.py`) following strict behavioral probability models and temporal cutoff rules.
- **Observation Window**: `2023-01-01` to `2025-06-30` (Feature engineering history).
- **Prediction Cutoff**: `2025-06-30`.
- **Outcome Window**: `2025-07-01` to `2025-09-30` (Observed churn outcome).

---

## 1. Customers (`data/raw/customers.csv`)
**Grain**: 1 record per customer (20,000 rows).

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customer_id` | STRING | **PK** | No | Unique identifier for customer | `CUST-10000` to `CUST-29999` |
| `signup_date` | DATE | — | No | Date customer joined platform | `2023-01-01` to `2025-05-31` |
| `age_group` | STRING | — | No | Customer age cohort | `18-24`, `25-34`, `35-44`, `45-54`, `55+` |
| `gender` | STRING | — | No | Self-reported gender identity | `Female`, `Male`, `Non-Binary`, `Other` |
| `region` | STRING | — | No | Geographic region | `North America`, `Europe`, `Asia-Pacific`, `Latin America`, `MEA` |
| `acquisition_channel` | STRING | — | No | Channel through which customer joined | `Organic Search`, `Paid Ads`, `Referral`, `Social Media`, `Partner`, `Direct` |

---

## 2. Subscriptions (`data/raw/subscriptions.csv`)
**Grain**: 1 record per subscription (20,000 rows).

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `subscription_id` | STRING | **PK** | No | Unique subscription identifier | `SUB-10001` to `SUB-30000` |
| `customer_id` | STRING | **FK** | No | Foreign key referencing `customers.customer_id` | References valid `customer_id` |
| `plan` | STRING | — | No | Tiered subscription level | `Basic` ($15), `Pro` ($49), `Enterprise` ($199) |
| `billing_cycle` | STRING | — | No | Billing frequency | `Monthly`, `Annual` |
| `start_date` | DATE | — | No | Subscription start date | Equal to `signup_date` |
| `end_date` | DATE | — | Yes | Cancellation date (if churned) | Null for active; `2025-07-01` to `2025-09-30` if churned |
| `monthly_fee` | DECIMAL | — | No | Effective monthly recurring charge ($ USD) | $12.00 to $199.00 |
| `discount_pct` | INTEGER | — | No | Discount percentage applied | `0`, `10`, `20` |
| `auto_renew` | INTEGER | — | No | Auto-renewal flag | `1` (Yes), `0` (No) |

---

## 3. Usage (`data/raw/usage.csv`)
**Grain**: 1 record per customer per active month (318,985 rows).

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `usage_id` | STRING | **PK** | No | Unique usage log identifier | `USG-10001` to `USG-328985` |
| `customer_id` | STRING | **FK** | No | Foreign key referencing `customers.customer_id` | References valid `customer_id` |
| `activity_month` | STRING | — | No | Year-Month of activity log | `2023-01` to `2025-06` |
| `sessions_count` | INTEGER | — | No | Number of login sessions in month | 0 to 75 sessions |
| `usage_hours` | DECIMAL | — | No | Total hours logged in application | 0.5 to 65.0 hours |
| `features_used_count` | INTEGER | — | No | Count of distinct features engaged | 1 to 12 features |
| `active_days` | INTEGER | — | No | Distinct active days in month | 1 to 28 days |

---

## 4. Payments (`data/raw/payments.csv`)
**Grain**: 1 record per payment transaction attempt (235,720 rows).

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `payment_id` | STRING | **PK** | No | Unique transaction identifier | `PAY-10001` to `PAY-245720` |
| `customer_id` | STRING | **FK** | No | Foreign key referencing `customers.customer_id` | References valid `customer_id` |
| `payment_date` | DATE | — | No | Date of billing attempt | `2023-01-01` to `2025-06-30` |
| `amount` | DECIMAL | — | No | Billed amount ($ USD) | $0.00 (if failed) or $12.00 to $2,388.00 |
| `payment_status` | STRING | — | No | Transaction status outcome | `Success`, `Failed`, `Refunded` |
| `payment_method` | STRING | — | No | Payment method used | `Credit Card`, `PayPal`, `ACH Bank Transfer`, `Debit Card` |

---

## 5. Support Tickets (`data/raw/support_tickets.csv`)
**Grain**: 1 record per customer support ticket submitted (40,923 rows).

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ticket_id` | STRING | **PK** | No | Unique ticket identifier | `TCK-10001` to `TCK-50923` |
| `customer_id` | STRING | **FK** | No | Foreign key referencing `customers.customer_id` | References valid `customer_id` |
| `ticket_date` | DATE | — | No | Date ticket was created | `2023-01-02` to `2025-06-29` |
| `issue_type` | STRING | — | No | Categorized ticket issue | `Technical Bug`, `Billing`, `Onboarding`, `Feature Request`, `Account Management` |
| `resolution_time_hours` | DECIMAL | — | No | Hours taken to resolve ticket | 0.5 to 145.0 hours |
| `satisfaction_score` | FLOAT | — | Yes | Customer CSAT rating post-resolution | `1.0` (Poor) to `5.0` (Excellent), Null if unrated (~2%) |

---

## 6. Churn Outcome (`data/raw/churn.csv`)
**Grain**: 1 record per customer (20,000 rows).

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customer_id` | STRING | **PK/FK** | No | References `customers.customer_id` | `CUST-10000` to `CUST-29999` |
| `churn_flag` | INTEGER | — | No | Binary target label (1 = Churned, 0 = Active) | `1` (33.02%), `0` (66.98%) |
| `churn_date` | DATE | — | Yes | Cancellation date in outcome window | Null if active (`0`), `2025-07-01` to `2025-09-30` if `1` |
| `churn_reason` | STRING | — | Yes | Primary stated/inferred reason for cancellation | `Payment Failure`, `Poor Customer Support`, `Product Unused`, `High Price`, `Competitor Switch`, `Missing Features`, `Business Closure` |
