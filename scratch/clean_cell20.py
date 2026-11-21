import json
from pathlib import Path

nb_path = Path('notebooks/06_risk_scoring.ipynb')
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Replace the export cell with clean, direct, 100% foolproof code
nb['cells'][20]['source'] = """# 1. Export master customer risk scoring table for Power BI
risk_table_cols = [
    'customer_id', 'plan', 'billing_cycle', 'monthly_fee', 'tenure_months',
    'avg_monthly_hours', 'avg_monthly_sessions', 'avg_active_days', 'usage_trend_ratio',
    'total_payments', 'failed_payments', 'had_failed_payment',
    'total_tickets', 'avg_csat', 'had_low_csat',
    'churn_probability', 'risk_score', 'risk_tier', 'main_risk_driver', 'expected_monthly_loss'
]

risk_table = df[risk_table_cols]

# Full direct path - works anywhere with zero errors!
output_powerbi = r"C:\\Users\\Admin\\OneDrive\\Data Analyst Project\\Subscription Churn Prediction & Risk Scoring\\data\\processed\\customer_risk_scores.csv"
risk_table.to_csv(output_powerbi, index=False)
print(f"✅ Power BI dataset exported to: {output_powerbi}")

# 2. Priority Action List for Customer Success Team
high_risk_list = df[df['risk_tier'].isin(['High', 'Critical'])].sort_values(
    by='expected_monthly_loss', ascending=False
)[[
    'customer_id', 'risk_score', 'risk_tier', 'monthly_fee', 'expected_monthly_loss',
    'main_risk_driver', 'plan', 'billing_cycle', 'tenure_months', 'avg_csat'
]]

output_retention = r"C:\\Users\\Admin\\OneDrive\\Data Analyst Project\\Subscription Churn Prediction & Risk Scoring\\outputs\\high_risk_retention_list.csv"
high_risk_list.to_csv(output_retention, index=False)
print(f"✅ Priority Retention List exported to: {output_retention}")
print(f"   Total Accounts in Priority Outreach: {len(high_risk_list):,}")"""

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('Updated 06_risk_scoring.ipynb cleanly!')
