# 📊 Subscription Churn Prediction & Risk Scoring

> End-to-end data analytics project that predicts customer churn, scores risk on a 0–100 scale, and delivers actionable retention strategies — from raw data to Power BI dashboard.

---

## 🎯 Problem Statement

A SaaS company with **20,000 customers** and **$10.5M ARR** had no systematic way to predict which customers would cancel, understand *why* they were leaving, or quantify the revenue at risk. This project builds a complete churn prediction and risk scoring pipeline to enable **proactive retention** instead of reactive firefighting.

## 🔑 Key Results

| Metric | Value |
|--------|-------|
| Customer Base Analyzed | 20,000 |
| Overall Churn Rate | 33.0% |
| ML Model Accuracy (ROC-AUC) | 0.75 |
| ARR at Risk (High + Critical) | $1.07M |
| At-Risk Accounts Identified | 2,484 (12.4%) |
| Projected Annual Savings | $1.22M |
| #1 Churn Driver | Payment Failure (54.2%) |

## 🏗️ Project Architecture

```
Raw Data (615K records) → SQL Analytics → EDA & Statistics → Feature Engineering (27 features)
    → ML Model (Gradient Boosting) → Risk Scoring (0-100) → Power BI Dashboard
```

## 📁 Repository Structure

```
├── data/
│   ├── raw/                          # 4 source CSVs (customers, usage, payments, support)
│   └── processed/                    # Engineered features & final risk scores
├── notebooks/
│   ├── 01_data_validation.ipynb      # Schema, nulls, duplicates, referential integrity
│   ├── 02_eda.ipynb                  # Univariate & bivariate exploratory analysis
│   ├── 03_statistical_analysis.ipynb # Z-tests, T-tests, Chi-squared, ANOVA
│   ├── 04_feature_engineering.ipynb  # 27 predictive features with temporal cutoff
│   ├── 05_model_training.ipynb       # Logistic Regression, Random Forest, Gradient Boosting
│   └── 06_risk_scoring.ipynb         # 0-100 risk score, 4 tiers, root cause, revenue at risk
├── sql/                              # 10 SQL analysis scripts
├── outputs/
│   └── high_risk_retention_list.csv  # 2,484 priority accounts for Customer Success
├── reports/
│   └── Churn_Project_Executive_Report.html  # Interactive executive report
├── powerbi/
│   ├── SaaS_Executive_Theme.json     # Custom Power BI theme
│   └── templates/                    # SVG layout templates
├── churn.pbix                        # Power BI Dashboard (3 pages)
└── README.md
```

## 📊 Data Sources

| Dataset | Records | Description |
|---------|---------|-------------|
| `customers.csv` | 20,000 | Demographics, signup date, region, acquisition channel |
| `usage.csv` | 318,985 | Monthly sessions, usage hours, features used, active days |
| `payments.csv` | 235,720 | Transaction amounts, success/failure status, payment method |
| `support_tickets.csv` | 40,923 | Issue types, resolution times, CSAT satisfaction scores |

## 🔍 Key Findings

1. **Payment Failure = #1 Churn Driver**: Accounts with ≥1 failed payment churn at 29.6% vs 5.2% for clean accounts (5.7× difference). Responsible for $204K/mo in expected losses.

2. **Monthly Contracts Churn 1.6× More**: Monthly billing (37.5% churn) vs Annual (22.9%). Converting 15% of monthly users to annual could save $45K+ MRR.

3. **Low CSAT Predicts Risk**: High/Critical risk accounts average only 2.06 CSAT (out of 5) vs 3.40 for healthy accounts.

4. **270 Critical Accounts Need Immediate Action**: These have 83.6% churn probability and represent $6,788/mo in expected losses.

5. **Model Lift**: Targeting the top 20% of predicted at-risk accounts captures 42.1% of all actual churners (2.1× lift over random).

## 🚀 Business Recommendations

| Priority | Intervention | Projected Annual Savings |
|----------|-------------|------------------------|
| 🔴 Week 1-2 | Call 270 Critical accounts immediately | — |
| 🟠 Week 2-4 | Automated payment dunning (retry Days 3, 5, 7) | $734,448 |
| 🟡 Month 2 | Monthly → Annual conversion campaign | $366,000 |
| 🟢 Month 3 | CSAT escalation rules + usage re-engagement | $118,920 |
| **Total** | | **$1,219,368/yr** |

## 🛠️ Tech Stack

- **Python 3.13** — Pandas, Scikit-Learn, Matplotlib, Seaborn, Statsmodels
- **SQL Server** — 10 analytical query scripts
- **Jupyter Notebooks** — 6 end-to-end analysis notebooks
- **Power BI** — 3-page interactive executive dashboard
- **Git / GitHub** — Version control and documentation

## 📈 Power BI Dashboard

The dashboard has 3 pages following the Strategic → Tactical → Operational framework:

1. **Executive Risk & Churn Overview** — KPI cards, risk tier distribution, revenue at risk
2. **Churn Drivers & Behavioral Diagnostics** — Root cause treemap, payment failure impact, CSAT analysis
3. **Customer Success Retention Action Center** — Priority outreach table, dynamic retention playbooks

## 👤 Author

**Pratmesh Dalvi**

- GitHub: [@pratmeshdalvi](https://github.com/pratmeshdalvi)

---

*This project demonstrates end-to-end data analytics capabilities: SQL querying, exploratory analysis, statistical hypothesis testing, feature engineering, machine learning, risk scoring, business intelligence dashboarding, and strategic business recommendations.*
