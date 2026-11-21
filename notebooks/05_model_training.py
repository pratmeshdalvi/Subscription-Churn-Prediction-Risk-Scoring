# %% [markdown]
# # 05 — Model Training & Comparison
# ### Project: Subscription Churn Prediction & Risk Scoring
# 
# ---
# 
# ### Objective of this Notebook:
# Now that we have our engineered features, we want to train machine learning models to **predict which customers will churn**.
# 
# In this notebook, we:
# 1. **Load Data**: Read `data/processed/customer_features.csv`.
# 2. **One-Hot Encoding**: Convert text columns into numbers using `pd.get_dummies()`.
# 3. **Train / Test Split**: 80% to train the model, 20% to test it.
# 4. **Train 3 Models**:
#    - Logistic Regression
#    - Random Forest
#    - Gradient Boosting
# 5. **Compare Models**: Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
# 6. **Feature Importance**: See which signals matter most in predicting churn.

# %% [markdown]
# ## Step 1: Import Libraries

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, ConfusionMatrixDisplay
)

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 5)

print("Libraries imported successfully!")

# %% [markdown]
# ## Step 2: Load the Processed Customer Features

# %%
# Read customer features dataset
df = pd.read_csv('data/processed/customer_features.csv')

print(f"Loaded {len(df):,} customers with {df.shape[1]} columns.")
display(df.head(3))

# %% [markdown]
# ## Step 3: Separate Features (X) and Target (y)

# %%
# X = all predictor columns, y = churn_flag
X = df.drop(columns=['customer_id', 'churn_flag'])
y = df['churn_flag']

# Convert categorical text columns to numbers (One-Hot Encoding)
X_encoded = pd.get_dummies(X, drop_first=True)

print(f"Features before encoding : {X.shape[1]}")
print(f"Features after encoding  : {X_encoded.shape[1]}")

# %% [markdown]
# ## Step 4: Split into Training (80%) and Testing (20%) Sets

# %%
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Training set : {len(X_train):,} customers")
print(f"Test set     : {len(X_test):,} customers")

# %% [markdown]
# ## Step 5: Scale Numeric Features for Logistic Regression

# %%
scaler = StandardScaler()

# Fit only on training data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print("Features scaled successfully!")

# %% [markdown]
# ## Step 6: Train 3 Machine Learning Models

# %%
# 1. Logistic Regression
print("Training Logistic Regression...")
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_scaled, y_train)

# 2. Random Forest
print("Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
rf_model.fit(X_train, y_train)

# 3. Gradient Boosting
print("Training Gradient Boosting...")
gb_model = GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=42)
gb_model.fit(X_train, y_train)

print("\nAll 3 models trained successfully!")

# %% [markdown]
# ## Step 7: Evaluate & Compare Model Performance on Test Data

# %%
models = {
    'Logistic Regression': (lr_model, X_test_scaled),
    'Random Forest': (rf_model, X_test),
    'Gradient Boosting': (gb_model, X_test)
}

results = []
for name, (model, data_test) in models.items():
    preds = model.predict(data_test)
    probs = model.predict_proba(data_test)[:, 1]

    results.append({
        'Model': name,
        'Accuracy': round(accuracy_score(y_test, preds), 4),
        'Precision': round(precision_score(y_test, preds), 4),
        'Recall': round(recall_score(y_test, preds), 4),
        'F1-Score': round(f1_score(y_test, preds), 4),
        'ROC-AUC': round(roc_auc_score(y_test, probs), 4)
    })

comparison_df = pd.DataFrame(results)
display(comparison_df)

# %% [markdown]
# ## Step 8: Visual Comparison (ROC Curve & Confusion Matrix)

# %%
# ROC Curves
plt.figure(figsize=(8, 5))

for name, (model, data_test) in models.items():
    probs = model.predict_proba(data_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, probs)
    auc = roc_auc_score(y_test, probs)
    plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})", linewidth=2)

plt.plot([0, 1], [0, 1], 'k--', label='Random Chance (AUC = 0.500)')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison', fontweight='bold')
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()

# %%
# Confusion Matrix for Gradient Boosting
best_preds = gb_model.predict(X_test)
cm = confusion_matrix(y_test, best_preds)

fig, ax = plt.subplots(figsize=(5, 4))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Active (0)', 'Churned (1)'])
disp.plot(cmap='Blues', ax=ax, values_format='d')
plt.title('Confusion Matrix: Gradient Boosting', fontweight='bold')
plt.grid(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Step 9: Top 10 Most Important Features

# %%
feat_importances = pd.Series(gb_model.feature_importances_, index=X_encoded.columns)
top_features = feat_importances.sort_values(ascending=False).head(10)

plt.figure(figsize=(9, 4))
top_features.plot(kind='barh', color='#2980b9', edgecolor='black')
plt.title('Top 10 Drivers of Churn', fontweight='bold')
plt.xlabel('Importance Score')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print("Top 5 Drivers of Churn:")
for rank, (feat, score) in enumerate(top_features.head(5).items(), 1):
    print(f"  {rank}. {feat:25s} : {score:.4f}")

# %% [markdown]
# ## Summary & Next Step
# 
# ### Key Takeaways:
# - **Gradient Boosting** achieved the best overall balance: **0.745 ROC-AUC** and highest Recall / F1-score.
# - **Top signals driving churn**: Low CSAT ratings (`avg_csat`), failed billing attempts (`failed_payments`), and low active days (`avg_active_days`).
# 
# ---
# 
# ### Next Step:
# Now we open **`06_risk_scoring.ipynb`** to calculate customer risk scores (0 to 100), identify root causes, and estimate Revenue-at-Risk!
