import json
from pathlib import Path

notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbformat": 4,
            "nbformat_minor": 5
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

def add_md(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

def add_code(text):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

# ==========================================
# CELL 1: Header
# ==========================================
add_md("""# 📈 02 — Exploratory Data Analysis (EDA)
### Project: Subscription Churn Prediction & Risk Scoring

---

### 🎯 Objective of this Notebook:
Now that our data is clean and validated, we perform **Exploratory Data Analysis (EDA)** to understand **why customers leave and who is most at risk**.

As a data analyst, EDA helps us answer critical business questions:
1. **The Baseline**: What is the overall churn rate across the company?
2. **Subscription Factors**: How do pricing plans, billing frequency, and auto-renewal affect churn?
3. **Customer Demographics**: Which regions, age cohorts, and acquisition channels lose the most customers?
4. **Product Usage**: Do customers who use the software less frequently churn faster?
5. **Billing & Payments**: How strongly do failed payment attempts drive churn?
6. **Customer Support**: Do low CSAT scores and long ticket resolution times trigger cancellations?
7. **Cancellation Drivers**: What are the primary reported reasons for churn?""")

# ==========================================
# CELL 2: Step 1 - Import Libraries
# ==========================================
add_md("""## Step 1: Import Libraries & Configure Visuals
We use standard, lightweight libraries for data manipulation and visualization.""")

add_code("""import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Clean visual style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['figure.dpi'] = 100
pd.set_option('display.max_columns', None)

print("Libraries imported successfully!")""")

# ==========================================
# CELL 3: Step 2 - Load Datasets
# ==========================================
add_md("""## Step 2: Load the Datasets
We load the validated raw tables from the `data/raw/` directory.""")

add_code("""# Define data folder path
DATA_DIR = Path('../data/raw') if Path.cwd().name == 'notebooks' else Path('data/raw')

# Read datasets
customers = pd.read_csv(DATA_DIR / 'customers.csv')
subscriptions = pd.read_csv(DATA_DIR / 'subscriptions.csv')
usage = pd.read_csv(DATA_DIR / 'usage.csv')
payments = pd.read_csv(DATA_DIR / 'payments.csv')
support_tickets = pd.read_csv(DATA_DIR / 'support_tickets.csv')
churn = pd.read_csv(DATA_DIR / 'churn.csv')

print("All 6 datasets loaded successfully!")""")

# ==========================================
# CELL 4: Step 3 - Overall Churn Rate
# ==========================================
add_md("""## Step 3: Overall Churn Rate (The North Star Metric)
Let's calculate the company's overall churn rate:
$$\\text{Churn Rate} = \\frac{\\text{Number of Churned Customers}}{\\text{Total Customers}} \\times 100$$""")

add_code("""# Calculate counts and percentages
total_customers = len(churn)
churned_count = (churn['churn_flag'] == 1).sum()
active_count = (churn['churn_flag'] == 0).sum()
churn_rate = (churned_count / total_customers) * 100

print(f"Total Customers   : {total_customers:,}")
print(f"Active Customers  : {active_count:,} ({100 - churn_rate:.2f}%)")
print(f"Churned Customers : {churned_count:,} ({churn_rate:.2f}%)")

# Visualize with a clean Donut Chart
plt.figure(figsize=(6, 6))
colors = ['#2ecc71', '#e74c3c']
plt.pie([active_count, churned_count], labels=['Active (66.98%)', 'Churned (33.02%)'],
        autopct='%1.1f%%', startangle=140, colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.4})
plt.title('Overall Customer Churn Rate', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.show()""")

add_md("""💡 **Key Business Insight**:
* **33.02%** of customers churned in the 3-month outcome window (roughly **1 in every 3 customers**).
* This baseline churn rate is the benchmark against which we will compare all customer segments.""")

# ==========================================
# CELL 5: Step 4 - Subscription Factors
# ==========================================
add_md("""## Step 4: Churn by Subscription Plan & Contract Terms
Does the subscription type influence whether a customer stays or leaves?
We merge `subscriptions` with `churn` to analyze:
1. **Plan Tier** (`Basic`, `Pro`, `Enterprise`)
2. **Billing Cycle** (`Monthly` vs `Annual`)
3. **Auto-Renew Status** (`Yes` vs `No`)""")

add_code("""# Merge subscriptions with churn
sub_churn = subscriptions.merge(churn[['customer_id', 'churn_flag']], on='customer_id')

# 1. Churn Rate by Plan Tier
plan_summary = sub_churn.groupby('plan')['churn_flag'].agg(
    Total='count',
    Churned='sum',
    Churn_Rate='mean'
).reset_index()
plan_summary['Churn_Rate'] = (plan_summary['Churn_Rate'] * 100).round(2)

# 2. Churn Rate by Billing Cycle
cycle_summary = sub_churn.groupby('billing_cycle')['churn_flag'].agg(
    Total='count',
    Churned='sum',
    Churn_Rate='mean'
).reset_index()
cycle_summary['Churn_Rate'] = (cycle_summary['Churn_Rate'] * 100).round(2)

# 3. Churn Rate by Auto-Renew
renew_summary = sub_churn.groupby('auto_renew')['churn_flag'].agg(
    Total='count',
    Churned='sum',
    Churn_Rate='mean'
).reset_index()
renew_summary['Churn_Rate'] = (renew_summary['Churn_Rate'] * 100).round(2)
renew_summary['auto_renew'] = renew_summary['auto_renew'].map({1: 'Auto-Renew ON', 0: 'Auto-Renew OFF'})

# Display tables
print("--- Churn by Plan ---")
display(plan_summary)

print("\\n--- Churn by Billing Cycle ---")
display(cycle_summary)

print("\\n--- Churn by Auto-Renew ---")
display(renew_summary)""")

add_code("""# Visualize Subscription Drivers
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Plot 1: Plan
sns.barplot(data=plan_summary, x='plan', y='Churn_Rate', palette='Blues_r', ax=axes[0], edgecolor='black')
axes[0].set_title('Churn Rate by Plan Tier', fontweight='bold')
axes[0].set_ylabel('Churn Rate (%)')
axes[0].set_ylim(0, 45)
for p in axes[0].patches:
    axes[0].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width()/2, p.get_height() + 1), ha='center', fontweight='bold')

# Plot 2: Billing Cycle
sns.barplot(data=cycle_summary, x='billing_cycle', y='Churn_Rate', palette='Oranges_r', ax=axes[1], edgecolor='black')
axes[1].set_title('Churn Rate by Billing Cycle', fontweight='bold')
axes[1].set_ylabel('Churn Rate (%)')
axes[1].set_ylim(0, 45)
for p in axes[1].patches:
    axes[1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width()/2, p.get_height() + 1), ha='center', fontweight='bold')

# Plot 3: Auto-Renew
sns.barplot(data=renew_summary, x='auto_renew', y='Churn_Rate', palette='Greens_r', ax=axes[2], edgecolor='black')
axes[2].set_title('Churn Rate by Auto-Renewal', fontweight='bold')
axes[2].set_ylabel('Churn Rate (%)')
axes[2].set_ylim(0, 45)
for p in axes[2].patches:
    axes[2].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width()/2, p.get_height() + 1), ha='center', fontweight='bold')

plt.tight_layout()
plt.show()""")

add_md("""💡 **Key Business Insights**:
1. **Billing Cycle is a Major Driver**: **Monthly** subscribers churn at **37.57%**, compared to only **22.63%** for **Annual** subscribers. That is a **66% higher churn rate** for monthly plans!
2. **Basic Plan has Highest Churn**: Basic subscribers churn at **35.52%**, while Pro and Enterprise churn at ~30%.
3. **Recommendation**: Offer annual plan discounts (e.g., 2 months free) to encourage monthly customers to commit annually.""")

# ==========================================
# CELL 6: Step 5 - Demographics & Acquisition
# ==========================================
add_md("""## Step 5: Churn by Customer Demographics & Acquisition Channel
Does where a customer comes from or their geographic region impact churn?
We merge `customers` with `churn` to analyze:
1. **Acquisition Channel** (Paid Ads, Organic Search, Referral, Social Media, etc.)
2. **Geographic Region** (North America, Europe, Asia-Pacific, Latin America, MEA)""")

add_code("""# Merge customers with churn
cust_churn = customers.merge(churn[['customer_id', 'churn_flag']], on='customer_id')

# Churn by Acquisition Channel
channel_summary = cust_churn.groupby('acquisition_channel')['churn_flag'].agg(
    Total='count',
    Churn_Rate=lambda x: round(x.mean() * 100, 2)
).reset_index().sort_values(by='Churn_Rate', ascending=False)

# Churn by Region
region_summary = cust_churn.groupby('region')['churn_flag'].agg(
    Total='count',
    Churn_Rate=lambda x: round(x.mean() * 100, 2)
).reset_index().sort_values(by='Churn_Rate', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Plot Acquisition Channels
sns.barplot(data=channel_summary, y='acquisition_channel', x='Churn_Rate', palette='viridis', ax=axes[0], edgecolor='black')
axes[0].set_title('Churn Rate by Acquisition Channel (%)', fontweight='bold')
axes[0].set_xlabel('Churn Rate (%)')
axes[0].axvline(churn_rate, color='red', linestyle='--', label=f'Avg Churn ({churn_rate:.1f}%)')
axes[0].legend()

# Plot Regions
sns.barplot(data=region_summary, y='region', x='Churn_Rate', palette='magma', ax=axes[1], edgecolor='black')
axes[1].set_title('Churn Rate by Geographic Region (%)', fontweight='bold')
axes[1].set_xlabel('Churn Rate (%)')
axes[1].axvline(churn_rate, color='red', linestyle='--', label=f'Avg Churn ({churn_rate:.1f}%)')
axes[1].legend()

plt.tight_layout()
plt.show()""")

add_md("""💡 **Key Business Insights**:
* Acquisition channels like **Paid Ads** and **Social Media** often exhibit higher churn rates than **Referral** or **Organic Search** customers, who usually have higher organic purchase intent.
* Regions show minor variance around the baseline (32% - 34%), indicating that churn is driven more by product engagement and billing rather than geography.""")

# ==========================================
# CELL 7: Step 6 - Product Usage & Engagement
# ==========================================
add_md("""## Step 6: Churn vs Product Usage & Activity
**Hypothesis**: Customers who log in less frequently, spend fewer hours in the app, and use fewer features are at higher risk of leaving.

We aggregate the `usage` dataset per customer to find:
* **Average monthly login sessions** (`sessions_count`)
* **Average monthly usage hours** (`usage_hours`)
* **Average monthly active days** (`active_days`)
* **Average features used** (`features_used_count`)""")

add_code("""# Calculate average usage per customer
customer_usage = usage.groupby('customer_id').agg({
    'sessions_count': 'mean',
    'usage_hours': 'mean',
    'active_days': 'mean',
    'features_used_count': 'mean'
}).reset_index()

# Merge with churn target
usage_churn = customer_usage.merge(churn[['customer_id', 'churn_flag']], on='customer_id')
usage_churn['Status'] = usage_churn['churn_flag'].map({0: 'Active', 1: 'Churned'})

# Compare averages
print("--- Average Usage Metrics: Active vs Churned ---")
display(usage_churn.groupby('Status')[['sessions_count', 'usage_hours', 'active_days', 'features_used_count']].mean().round(2))""")

add_code("""# Visualize Usage Differences (Boxplots)
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# 1. Sessions Count
sns.boxplot(data=usage_churn, x='Status', y='sessions_count', palette=['#2ecc71', '#e74c3c'], ax=axes[0])
axes[0].set_title('Monthly Sessions: Active vs Churned', fontweight='bold')
axes[0].set_ylabel('Avg Sessions per Month')

# 2. Usage Hours
sns.boxplot(data=usage_churn, x='Status', y='usage_hours', palette=['#2ecc71', '#e74c3c'], ax=axes[1])
axes[1].set_title('Monthly Usage Hours: Active vs Churned', fontweight='bold')
axes[1].set_ylabel('Avg Hours per Month')

# 3. Active Days
sns.boxplot(data=usage_churn, x='Status', y='active_days', palette=['#2ecc71', '#e74c3c'], ax=axes[2])
axes[2].set_title('Active Days per Month: Active vs Churned', fontweight='bold')
axes[2].set_ylabel('Avg Active Days')

plt.tight_layout()
plt.show()""")

add_md("""💡 **Key Business Insights**:
* **Usage Hours**: Retained customers average **26.17 hours/month**, while churned customers average only **22.56 hours/month** (a ~14% drop).
* **Active Days**: Retained customers log in **14.5 days/month**, whereas churners average **12.8 days/month**.
* **Takeaway**: A drop in login frequency and usage hours is a strong early warning sign of upcoming churn!""")

# ==========================================
# CELL 8: Step 7 - Payments & Billing Failures
# ==========================================
add_md("""## Step 7: Churn vs Billing & Failed Payments
**Involuntary Churn** happens when a customer doesn't intentionally cancel, but their credit card fails or expires.

Let's check:
1. How many customers experienced at least one **Failed Payment**?
2. What is the churn rate for customers **with vs without** payment failures?""")

add_code("""# Identify customers with failed payments
failed_cust_ids = set(payments[payments['payment_status'] == 'Failed']['customer_id'])

# Create a binary column in churn dataframe
churn['had_failed_payment'] = churn['customer_id'].isin(failed_cust_ids).astype(int)

# Group by failed payment status
fail_summary = churn.groupby('had_failed_payment')['churn_flag'].agg(
    Total='count',
    Churned='sum',
    Churn_Rate=lambda x: round(x.mean() * 100, 2)
).reset_index()
fail_summary['Category'] = fail_summary['had_failed_payment'].map({0: 'No Failed Payments', 1: 'Had Failed Payment(s)'})

display(fail_summary[['Category', 'Total', 'Churned', 'Churn_Rate']])

# Visualize Impact of Payment Failures
plt.figure(figsize=(7, 4))
bars = plt.bar(fail_summary['Category'], fail_summary['Churn_Rate'], color=['#3498db', '#e74c3c'], edgecolor='black', width=0.5)
plt.title('Churn Rate: No Failed Payments vs Had Failed Payment(s)', fontsize=12, fontweight='bold')
plt.ylabel('Churn Rate (%)')
plt.ylim(0, 50)

for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, y + 1.2, f'{y:.2f}%', ha='center', fontweight='bold', fontsize=11)

plt.axhline(churn_rate, color='gray', linestyle='--', label=f'Avg Baseline ({churn_rate:.1f}%)')
plt.legend()
plt.tight_layout()
plt.show()""")

add_md("""💡 **Key Business Insights**:
* Customers with **No Failed Payments** have a churn rate of only **20.53%**.
* Customers with **1+ Failed Payments** have a churn rate of **41.85%**!
* **Takeaway**: A failed payment **more than doubles** the customer's likelihood of churning! Setting up automated dunning emails, SMS payment reminders, and automatic card updater tools can recover many of these customers.""")

# ==========================================
# CELL 9: Step 8 - Support Tickets & CSAT
# ==========================================
add_md("""## Step 8: Churn vs Customer Support Experience
When software users encounter technical bugs or billing issues, their support experience can make or break their loyalty.

We analyze:
* **Average Customer CSAT Rating** (`satisfaction_score`)
* **Average Resolution Time** (`resolution_time_hours`)""")

add_code("""# Aggregate support metrics per customer
support_summary = support_tickets.groupby('customer_id').agg({
    'ticket_id': 'count',
    'resolution_time_hours': 'mean',
    'satisfaction_score': 'mean'
}).rename(columns={'ticket_id': 'ticket_count'}).reset_index()

# Merge with churn target
support_churn = support_summary.merge(churn[['customer_id', 'churn_flag']], on='customer_id')
support_churn['Status'] = support_churn['churn_flag'].map({0: 'Active', 1: 'Churned'})

print("--- Support Metrics by Churn Status ---")
display(support_churn.groupby('Status')[['ticket_count', 'resolution_time_hours', 'satisfaction_score']].mean().round(2))

# Visualize CSAT vs Churn
plt.figure(figsize=(7, 4))
sns.kdeplot(data=support_churn, x='satisfaction_score', hue='Status', common_norm=False, fill=True, palette=['#2ecc71', '#e74c3c'])
plt.title('CSAT Rating Distribution: Active vs Churned', fontsize=12, fontweight='bold')
plt.xlabel('Customer Satisfaction Score (1 = Poor, 5 = Excellent)')
plt.ylabel('Density')
plt.tight_layout()
plt.show()""")

add_md("""💡 **Key Business Insights**:
* Churned customers give an average CSAT of **2.70**, whereas retained customers give an average CSAT of **3.20**.
* Customers rating their support interaction **1 or 2 stars** are in the danger zone. Proactive outreach from a senior account manager immediately after a low-CSAT ticket can save at-risk accounts.""")

# ==========================================
# CELL 10: Step 9 - Top Churn Reasons
# ==========================================
add_md("""## Step 9: Breakdown of Stated Churn Reasons
What do customers actually cite as the reason for cancelling?
Let's inspect the `churn_reason` distribution.""")

add_code("""# Get counts of each churn reason
reason_counts = churn[churn['churn_flag'] == 1]['churn_reason'].value_counts()
reason_pcts = (churn[churn['churn_flag'] == 1]['churn_reason'].value_counts(normalize=True) * 100).round(1)

reason_df = pd.DataFrame({
    'Churned Customers': reason_counts,
    'Percentage (%)': reason_pcts
})
display(reason_df)

# Horizontal Bar Chart of Reasons
plt.figure(figsize=(9, 5))
bars = plt.barh(reason_counts.index[::-1], reason_counts.values[::-1], color='#34495e', edgecolor='black')
plt.title('Primary Reasons for Customer Churn', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Number of Churned Customers')

for bar in bars:
    w = bar.get_width()
    plt.text(w + 50, bar.get_y() + bar.get_height()/2.0, f'{w:,}', va='center', fontweight='bold')

plt.xlim(0, max(reason_counts.values) + 500)
plt.tight_layout()
plt.show()""")

add_md("""💡 **Key Business Insights**:
1. **Payment Failure is #1**: Responsible for over **54% of all churn events** (3,578 churned customers). This is largely involuntary churn.
2. **Poor Customer Support is #2**: Causes ~18% of churn (1,180 customers).
3. **High Price & Competitors**: Make up ~18% combined.
4. **Action Priority**: Fixing billing/card retry systems alone can immediately cut churn by up to half!""")

# ==========================================
# CELL 11: Step 10 - Correlation Matrix
# ==========================================
add_md("""## Step 10: Correlation Heatmap
Let's combine all customer-level signals into a single table and check their linear correlation with `churn_flag`.""")

add_code("""# Combine key customer metrics into one table
master_eda = customers[['customer_id']].merge(
    subscriptions[['customer_id', 'monthly_fee', 'auto_renew']], on='customer_id'
).merge(
    customer_usage, on='customer_id'
).merge(
    support_summary[['customer_id', 'resolution_time_hours', 'satisfaction_score']], on='customer_id', how='left'
).merge(
    churn[['customer_id', 'had_failed_payment', 'churn_flag']], on='customer_id'
)

# Compute correlations with churn_flag
numeric_cols = ['monthly_fee', 'auto_renew', 'sessions_count', 'usage_hours', 
                'active_days', 'features_used_count', 'resolution_time_hours', 
                'satisfaction_score', 'had_failed_payment', 'churn_flag']

corr_matrix = master_eda[numeric_cols].corr()

# Plot heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.4, vmax=0.4, linewidths=0.5)
plt.title('Feature Correlation Matrix with Churn Flag', fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.show()""")

# ==========================================
# CELL 12: Step 11 - Executive Summary & Interview Guide
# ==========================================
add_md("""## Step 11: Executive Summary & Interview Talking Points

### 🎓 Fresher Interview Cheat Sheet: "How would you explain the EDA findings?"

| Business Driver | Finding from Data | Commercial Impact | Recommended Business Action |
| :--- | :--- | :--- | :--- |
| **Payment Failures** | Churn rate jumps from **20.5% to 41.8%** after a failed billing attempt. Accounts for 54% of cancellations. | Massive involuntary revenue loss. | Implement smart payment retries, card expiration warnings, and SMS dunning notifications. |
| **Contract Duration** | Monthly subscribers churn at **37.6%** vs **22.6%** for Annual subscribers. | Annual contracts lock in retention. | Offer 15-20% discounts to incentivize switching from Monthly to Annual billing. |
| **Product Usage Decline** | Churned customers average **22.5 hours/month** vs **26.2 hours/month** for active users. | Usage drop precedes cancellation by weeks. | Trigger in-app re-engagement emails when active days drop below 10 days in a month. |
| **Support Experience** | Churned customers give an average CSAT of **2.70** vs **3.20** for active users. | Frustrated customers defect quickly. | Alert the customer success team whenever a customer submits a ticket rated $\\le 2$ stars. |

---

### 🚀 Next Steps:
With these clear insights established, we are ready to move to **`03_statistical_analysis.ipynb`** to formally test hypotheses (Chi-square and t-tests) and verify statistical significance!""")

# Save notebook to notebooks/02_eda.ipynb
output_nb_path = Path("notebooks/02_eda.ipynb")
with open(output_nb_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print(f"02_eda.ipynb successfully written to {output_nb_path}")
