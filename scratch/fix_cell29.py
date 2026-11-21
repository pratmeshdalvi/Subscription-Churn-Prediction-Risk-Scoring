import json
from pathlib import Path

nb_path = Path('notebooks/06_risk_scoring.ipynb')
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])
        if 'output_powerbi' in source:
            cell['source'] = """# 1. Export master customer risk scoring table for Power BI
risk_table_cols = [
    'customer_id', 'plan', 'billing_cycle', 'monthly_fee', 'tenure_months',
    'avg_monthly_hours', 'avg_monthly_sessions', 'avg_active_days', 'usage_trend_ratio',
    'total_payments', 'failed_payments', 'had_failed_payment',
    'total_tickets', 'avg_csat', 'had_low_csat',
    'churn_probability', 'risk_score', 'risk_tier', 'main_risk_driver', 'expected_monthly_loss'
]

risk_table = df[risk_table_cols]

# Safely find data/processed whether kernel runs in notebooks/ or root
output_dir_data = Path('../data/processed') if Path.cwd().name == 'notebooks' else Path('data/processed')
output_dir_data.mkdir(parents=True, exist_ok=True)

output_powerbi = output_dir_data / 'customer_risk_scores.csv'
risk_table.to_csv(output_powerbi, index=False)
print(f"✅ Power BI dataset exported to: {output_powerbi}")

# 2. Priority Action List for Customer Success Team
high_risk_list = df[df['risk_tier'].isin(['High', 'Critical'])].sort_values(
    by='expected_monthly_loss', ascending=False
)[[
    'customer_id', 'risk_score', 'risk_tier', 'monthly_fee', 'expected_monthly_loss',
    'main_risk_driver', 'plan', 'billing_cycle', 'tenure_months', 'avg_csat'
]]

output_dir_out = Path('../outputs') if Path.cwd().name == 'notebooks' else Path('outputs')
output_dir_out.mkdir(parents=True, exist_ok=True)

output_retention = output_dir_out / 'high_risk_retention_list.csv'
high_risk_list.to_csv(output_retention, index=False)
print(f"✅ Priority Retention List exported to: {output_retention}")
print(f"   Total Accounts in Priority Outreach: {len(high_risk_list)}")"""

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('Updated 06_risk_scoring.ipynb successfully.')
