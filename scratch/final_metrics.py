import pandas as pd
df = pd.read_csv('data/processed/customer_risk_scores.csv')
print(f"Total MRR: ${df['monthly_fee'].sum():,.2f}")
hrc = df[df['risk_tier'].isin(['High','Critical'])]
print(f"High+Critical Expected Loss: ${hrc['expected_monthly_loss'].sum():,.2f}")
print(f"Total Expected Monthly Loss: ${df['expected_monthly_loss'].sum():,.2f}")
print(f"High+Critical MRR Exposure: ${hrc['monthly_fee'].sum():,.2f}")
failed = df[df['had_failed_payment']==1]
print(f"Failed payment accounts: {len(failed)} / {len(df)}")
monthly = df[df['billing_cycle']=='Monthly']
annual = df[df['billing_cycle']=='Annual']
print(f"Monthly churn prob avg: {monthly['churn_probability'].mean():.3f}")
print(f"Annual churn prob avg: {annual['churn_probability'].mean():.3f}")
print(f"Avg CSAT all: {df['avg_csat'].mean():.2f}")
print(f"Avg CSAT High/Critical: {hrc['avg_csat'].mean():.2f}")
low = df[df['risk_tier']=='Low']
print(f"Avg CSAT Low: {low['avg_csat'].mean():.2f}")
print(f"ARR at Risk: ${hrc['monthly_fee'].sum()*12:,.2f}")
print(f"Total ARR: ${df['monthly_fee'].sum()*12:,.2f}")
