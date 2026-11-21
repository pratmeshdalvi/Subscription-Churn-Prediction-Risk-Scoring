# %% [markdown]
# # 04 — Feature Engineering
# ### Project: Subscription Churn Prediction & Risk Scoring
# 
# ---
# 
# ### Objective of this Notebook:
# In raw data, a single customer has **multiple rows** scattered across 6 different tables (monthly usage logs, individual payment attempts, support tickets).
# 
# Machine learning models require **one single row per customer**, with all their behavioral patterns summarized into numeric columns (**features**).
# 
# In this notebook, we transform the raw relational tables into a single model-ready table:
# 1. **Tenure & Demographics**: How long has the customer been subscribed as of the cutoff date?
# 2. **Subscription Terms**: Plan tier, billing frequency, auto-renewal status, and monthly fee.
# 3. **Usage & Engagement**: Monthly sessions, usage intensity, active days, and recent usage trends.
# 4. **Billing Health**: Total payment attempts, failed payment count, and failure rate.
# 5. **Support Friction**: Ticket frequency, resolution delays, and low CSAT indicators.
# 6. **Data Leakage Prevention**: Ensuring all features are calculated strictly on or before **2025-06-30** (Prediction Cutoff).
# 7. **Export**: Save the final feature dataset to `data/processed/customer_features.csv`.

# %% [markdown]
# ## Step 1: Import Libraries

# %%
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)

print("Libraries imported successfully!")

# %% [markdown]
# ## Step 2: Load the Raw Datasets
# We load all 6 relational tables from `data/raw/`.

# %%
customers        = pd.read_csv('data/raw/customers.csv')
subscriptions    = pd.read_csv('data/raw/subscriptions.csv')
usage            = pd.read_csv('data/raw/usage.csv')
payments         = pd.read_csv('data/raw/payments.csv')
support_tickets  = pd.read_csv('data/raw/support_tickets.csv')
churn            = pd.read_csv('data/raw/churn.csv')

print("All 6 raw files loaded successfully.")

# %% [markdown]
# ## Step 3: Feature Set 1 — Customer Tenure & Demographics
# 
# ### What is Tenure?
# Tenure measures **how long a customer has been with the company**.
# In subscription businesses, brand new customers often churn at higher rates than long-standing loyal users.
# 
# - **Prediction Cutoff Date**: `2025-06-30`
# - $\text{tenure\_months} = \frac{\text{Cutoff Date} - \text{signup\_date}}{30 \text{ days}}$

# %%
# Convert signup_date to datetime
customers['signup_date'] = pd.to_datetime(customers['signup_date'])

# Calculate tenure in months as of the prediction cutoff date (2025-06-30)
cutoff_date = pd.to_datetime('2025-06-30')
customers['tenure_months'] = ((cutoff_date - customers['signup_date']).dt.days // 30).astype(int)

# Select demographic and tenure features
customer_features = customers[['customer_id', 'tenure_months', 'age_group', 'gender', 'region', 'acquisition_channel']]

print("Sample Customer & Tenure Features:")
display(customer_features.head(3))

# %% [markdown]
# ## Step 4: Feature Set 2 — Subscription & Contract Attributes
# 
# From `subscriptions.csv`, we extract:
# - `plan`: Basic ($15), Pro ($49), Enterprise ($199)
# - `billing_cycle`: Monthly vs Annual
# - `monthly_fee`: Effective monthly charge in USD
# - `discount_pct`: Discount applied (0%, 10%, 20%)
# - `auto_renew`: Auto-renewal flag (1 = ON, 0 = OFF)

# %%
subscription_features = subscriptions[[
    'customer_id', 'plan', 'billing_cycle', 'monthly_fee', 'discount_pct', 'auto_renew'
]]

print("Sample Subscription Features:")
display(subscription_features.head(3))

# %% [markdown]
# ## Step 5: Feature Set 3 — Product Engagement & Usage Trends
# 
# In EDA, we saw that customers who drop in usage hours and active days are significantly more likely to churn.
# 
# We engineer 7 customer-level usage metrics:
# 1. `total_active_months`: How many months did the customer log in?
# 2. `avg_monthly_sessions`: Average login sessions per month.
# 3. `avg_monthly_hours`: Average hours spent in software per month.
# 4. `avg_monthly_active_days`: Average days logged in per month.
# 5. `avg_features_used`: Depth of feature engagement.
# 6. `hours_per_session`: Usage intensity (hours divided by sessions).
# 7. `usage_trend_ratio`: Recent 3-month hours divided by lifetime average hours.
#    - If ratio $< 1.0$, customer engagement is declining!

# %%
# 1. Lifetime average usage per customer
usage_agg = usage.groupby('customer_id').agg(
    total_active_months = ('activity_month', 'count'),
    avg_monthly_sessions = ('sessions_count', 'mean'),
    avg_monthly_hours    = ('usage_hours', 'mean'),
    avg_active_days      = ('active_days', 'mean'),
    avg_features_used    = ('features_used_count', 'mean')
).reset_index()

# 2. Behavioral Ratios
usage_agg['hours_per_session'] = (usage_agg['avg_monthly_hours'] / usage_agg['avg_monthly_sessions']).round(2)
usage_agg['sessions_per_active_day'] = (usage_agg['avg_monthly_sessions'] / usage_agg['avg_active_days']).round(2)

# 3. Recent Engagement Trend (Last 3 months before cutoff: 2025-04, 2025-05, 2025-06)
recent_months = ['2025-04', '2025-05', '2025-06']
recent_usage = usage[usage['activity_month'].isin(recent_months)].groupby('customer_id').agg(
    recent_avg_hours = ('usage_hours', 'mean')
).reset_index()

# Merge recent usage and calculate the trend ratio
usage_features = usage_agg.merge(recent_usage, on='customer_id', how='left')
usage_features['recent_avg_hours'] = usage_features['recent_avg_hours'].fillna(usage_features['avg_monthly_hours'])
usage_features['usage_trend_ratio'] = (usage_features['recent_avg_hours'] / (usage_features['avg_monthly_hours'] + 1e-5)).round(2)

# Drop intermediate helper column
usage_features.drop(columns=['recent_avg_hours'], inplace=True)

print("Sample Usage Features:")
display(usage_features.head(3))

# %% [markdown]
# ## Step 6: Feature Set 4 — Billing Health & Failed Payments
# 
# Payment failure was the **#1 churn reason** in our EDA and statistical tests ($\chi^2 = 996.4$).
# 
# We engineer 4 payment health metrics:
# 1. `total_payments`: Total billing attempts.
# 2. `failed_payments`: Number of failed charge attempts.
# 3. `payment_failure_rate`: Failed attempts divided by total attempts.
# 4. `had_failed_payment`: Binary indicator (1 if customer ever had a failed payment, else 0).

# %%
payment_features = payments.groupby('customer_id').agg(
    total_payments   = ('payment_id', 'count'),
    failed_payments  = ('payment_status', lambda x: (x == 'Failed').sum())
).reset_index()

payment_features['payment_failure_rate'] = (payment_features['failed_payments'] / payment_features['total_payments']).round(3)
payment_features['had_failed_payment'] = (payment_features['failed_payments'] > 0).astype(int)

print("Sample Payment Features:")
display(payment_features.head(3))

# %% [markdown]
# ## Step 7: Feature Set 5 — Customer Support Friction & CSAT
# 
# Dissatisfied customers leave quickly.
# We engineer:
# 1. `total_tickets`: Total support requests filed (0 if none).
# 2. `tickets_per_tenure_month`: Support ticket submission frequency.
# 3. `avg_resolution_hours`: How long the customer waited on average for issue resolution.
# 4. `avg_csat`: Average customer satisfaction rating (1 to 5).
# 5. `had_low_csat`: Flag indicating if customer gave a rating of 1 or 2 stars.

# %%
support_agg = support_tickets.groupby('customer_id').agg(
    total_tickets         = ('ticket_id', 'count'),
    avg_resolution_hours  = ('resolution_time_hours', 'mean'),
    avg_csat              = ('satisfaction_score', 'mean'),
    had_low_csat          = ('satisfaction_score', lambda x: int((x <= 2).any()))
).reset_index()

print("Sample Support Summary (for customers who submitted tickets):")
display(support_agg.head(3))

# %% [markdown]
# ## Step 8: Assemble the Master Customer-Level Feature Dataset
# 
# We join all 5 feature sets together on `customer_id` and attach our target variable: `churn_flag`.
# 
# ⚠️ **Crucial Rule on Target Leakage**:
# We **do NOT** include `churn_date` or `churn_reason` in our feature dataset!
# Those columns are recorded *after* a customer cancels, so including them would cause 100% artificial data leakage.

# %%
# Combine all engineered feature sets
master = customer_features.merge(
    subscription_features, on='customer_id'
).merge(
    usage_features, on='customer_id'
).merge(
    payment_features, on='customer_id'
).merge(
    support_agg, on='customer_id', how='left'
)

# For customers who never submitted a support ticket, fill ticket counts with 0
master['total_tickets'] = master['total_tickets'].fillna(0).astype(int)
master['had_low_csat']  = master['had_low_csat'].fillna(0).astype(int)
master['tickets_per_tenure_month'] = (master['total_tickets'] / (master['tenure_months'] + 1)).round(3)

# For resolution time and CSAT, fill missing values with the median of rated tickets
median_resolution = master['avg_resolution_hours'].median()
median_csat       = master['avg_csat'].median()

master['avg_resolution_hours'] = master['avg_resolution_hours'].fillna(median_resolution).round(2)
master['avg_csat']             = master['avg_csat'].fillna(median_csat).round(2)

# Attach the target label (churn_flag)
master = master.merge(churn[['customer_id', 'churn_flag']], on='customer_id')

print(f"Master feature table assembled successfully: {master.shape[0]:,} rows, {master.shape[1]} columns")
display(master.head(3))

# %% [markdown]
# ## Step 9: Final Quality & Missingness Audit
# Let's confirm that the engineered dataset is completely clean before exporting.

# %%
# Check for any remaining null values
nulls = master.isnull().sum()
null_cols = nulls[nulls > 0]

print("=== FINAL DATASET QUALITY CHECK ===")
if len(null_cols) == 0:
    print("✅ Zero missing values across all 20,000 customer records!")
else:
    print("⚠️ Missing values detected:")
    print(null_cols)

print(f"✅ Total customers    : {len(master):,}")
print(f"✅ Active customers   : {(master['churn_flag'] == 0).sum():,} ({(master['churn_flag'] == 0).mean()*100:.1f}%)")
print(f"✅ Churned customers  : {(master['churn_flag'] == 1).sum():,} ({(master['churn_flag'] == 1).mean()*100:.1f}%)")
print(f"✅ Total features     : {master.shape[1] - 2} predictor features (excluding customer_id & churn_flag)")

# %% [markdown]
# ## Step 10: Export Processed Dataset for Machine Learning
# 
# We save the final engineered table to `data/processed/customer_features.csv`.
# This file will be loaded directly into **`05_model_training.ipynb`**!

# %%
from pathlib import Path

# Ensure data/processed folder exists
Path('data/processed').mkdir(parents=True, exist_ok=True)

# Export to CSV
output_path = 'data/processed/customer_features.csv'
master.to_csv(output_path, index=False)

print(f"✅ Processed feature dataset saved successfully to: {output_path}")
print(f"File size: {Path(output_path).stat().st_size / (1024*1024):.2f} MB")

# %% [markdown]
# ## Summary of Engineered Features
# 
# | Category | Engineered Feature | Business Meaning |
# | :--- | :--- | :--- |
# | **Tenure** | `tenure_months` | Months subscribed up to cutoff date (2025-06-30). |
# | **Demographics** | `age_group`, `gender`, `region`, `acquisition_channel` | Customer cohort profile and marketing channel. |
# | **Contract** | `plan`, `billing_cycle`, `monthly_fee`, `discount_pct`, `auto_renew` | Plan tier, monthly commitment, and auto-renewal flag. |
# | **Activity** | `total_active_months`, `avg_monthly_sessions`, `avg_monthly_hours` | General customer software usage volume. |
# | **Engagement** | `avg_active_days`, `avg_features_used`, `hours_per_session` | Depth of product adoption and session density. |
# | **Trend** | `usage_trend_ratio` | Ratio of last 3 months hours to lifetime hours ($< 1.0$ signals drop-off). |
# | **Billing Health** | `total_payments`, `failed_payments`, `payment_failure_rate`, `had_failed_payment` | Historical payment success and failure frequency. |
# | **Support Friction** | `total_tickets`, `tickets_per_tenure_month`, `avg_resolution_hours`, `avg_csat`, `had_low_csat` | Support volume, resolution wait times, and poor CSAT warnings. |
# | **Target** | `churn_flag` | The ground-truth outcome label (1 = Churned, 0 = Active). |
# 
# ---
# 
# ### 🚀 Next Step:
# Now that our feature table is saved in `data/processed/customer_features.csv`, we are ready for **`05_model_training.ipynb`** to train and compare Logistic Regression, Random Forest, and XGBoost!
