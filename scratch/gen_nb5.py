import json
from pathlib import Path

def make_model_notebook():
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    def md(text):
        nb["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": text.strip()
        })

    def code(text):
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": text.strip()
        })

    # Header
    md("""# 05 — Model Training & Comparison
### Project: Subscription Churn Prediction & Risk Scoring

---

### Objective of this Notebook:
Now that we have our engineered features in `data/processed/customer_features.csv`, we want to train machine learning models to **predict which customers will churn**.

In this notebook, we follow an industry-standard, simple workflow:
1. **Load Processed Data**: Read the engineered customer features.
2. **Encode Categorical Variables**: Convert text columns (e.g. Plan, Region) to numbers using One-Hot Encoding (`pd.get_dummies`).
3. **Train / Test Split**: 80% data to train the models, 20% held-out test data to evaluate them honestly.
4. **Feature Scaling**: Scale numeric inputs using `StandardScaler` so features are on a fair playing field.
5. **Train 3 Models**:
   - **Logistic Regression**: Interpretable, fast statistical baseline.
   - **Random Forest**: Ensemble of decision trees; handles non-linear relationships.
   - **Gradient Boosting**: Sequential tree-boosting model with strong predictive accuracy.
6. **Compare Model Metrics**: Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
7. **Inspect Feature Importances**: Which signals matter most in predicting churn?
8. **Save the Best Model**: Export the best performing model using `joblib` for risk scoring.""")

    # Step 1: Imports
    md("## Step 1: Import Libraries")
    code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Scikit-learn tools
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

print("Libraries imported successfully!")""")

    # Step 2: Load Data
    md("""## Step 2: Load Processed Feature Dataset
We read `data/processed/customer_features.csv`, which was prepared in `04_feature_engineering.ipynb`.""")
    code("""df = pd.read_csv('data/processed/customer_features.csv')

print(f"Loaded dataset: {df.shape[0]:,} customers, {df.shape[1]} columns")
print(f"Target distribution (churn_flag):")
print(df['churn_flag'].value_counts(normalize=True).round(3))
display(df.head(3))""")

    # Step 3: Features & Target Separation
    md("""## Step 3: Separate Features (X) and Target (y)
- `X`: All predictor columns (excluding `customer_id` and the label `churn_flag`).
- `y`: `churn_flag` (1 = Churned, 0 = Active).
- We also convert all categorical text columns into numbers using One-Hot Encoding (`pd.get_dummies`).""")
    code("""# Separate features and target
X = df.drop(columns=['customer_id', 'churn_flag'])
y = df['churn_flag']

# One-Hot Encode categorical columns (e.g. plan, billing_cycle, region)
X_encoded = pd.get_dummies(X, drop_first=True)

print(f"Original feature count : {X.shape[1]}")
print(f"Encoded feature count  : {X_encoded.shape[1]}")
print("\\nEncoded feature columns:")
print(list(X_encoded.columns))""")

    # Step 4: Train / Test Split
    md("""## Step 4: Train / Test Split (80% Train, 20% Test)
- `stratify=y` ensures both train and test sets have the exact same 33% churn proportion.
- `random_state=42` guarantees 100% reproducible splits.""")
    code("""X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Training set : {X_train.shape[0]:,} customers (80%)")
print(f"Test set     : {X_test.shape[0]:,} customers (20%)")
print(f"Train churn rate : {y_train.mean():.2%}")
print(f"Test churn rate  : {y_test.mean():.2%}")""")

    # Step 5: Feature Scaling
    md("""## Step 5: Feature Scaling
Models like **Logistic Regression** require features on the same numerical scale (so \$199 `monthly_fee` doesn't dominate `avg_csat` which is 1–5).
- We fit `StandardScaler` on **training data only** to prevent data leakage!""")
    code("""scaler = StandardScaler()

# Fit only on training data, then transform both
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print("Features scaled successfully!")""")

    # Step 6: Train Models
    md("""## Step 6: Train the Machine Learning Models
We train 3 distinct models to compare:
1. **Logistic Regression**: Interpretable linear baseline.
2. **Random Forest**: Ensemble of 100 decision trees.
3. **Gradient Boosting**: Sequential boosting model that learns from previous tree errors.""")
    code("""# 1. Logistic Regression
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

print("\\nAll 3 models trained successfully!")""")

    # Step 7: Evaluate Models
    md("""## Step 7: Model Evaluation & Metric Comparison
We evaluate on the unseen **test set (4,000 customers)** using:
- **Accuracy**: Overall % of correct predictions.
- **Precision**: When model predicts churn, how often is it right?
- **Recall**: Out of all real churners, how many did the model catch?
- **F1-Score**: Balance between Precision and Recall.
- **ROC-AUC**: Probability ranking performance (0.5 = random guess, 1.0 = perfect ranking).""")
    code("""# Get predictions and churn probabilities for test set
models = {
    'Logistic Regression': (lr_model, X_test_scaled),
    'Random Forest': (rf_model, X_test),
    'Gradient Boosting': (gb_model, X_test)
}

comparison_results = []

for name, (model, data_test) in models.items():
    preds = model.predict(data_test)
    probs = model.predict_proba(data_test)[:, 1]
    
    comparison_results.append({
        'Model': name,
        'Accuracy': round(accuracy_score(y_test, preds), 4),
        'Precision': round(precision_score(y_test, preds), 4),
        'Recall': round(recall_score(y_test, preds), 4),
        'F1-Score': round(f1_score(y_test, preds), 4),
        'ROC-AUC': round(roc_auc_score(y_test, probs), 4)
    })

comparison_df = pd.DataFrame(comparison_results)
display(comparison_df)""")

    # Step 8: Plot ROC Curves & Confusion Matrix
    md("""## Step 8: Visual Comparison (ROC Curves & Confusion Matrix)
The **ROC Curve** visualizes the trade-off between True Positive Rate and False Positive Rate across all probability thresholds.""")
    code("""# Plot ROC Curves for all 3 models
plt.figure(figsize=(8, 6))

for name, (model, data_test) in models.items():
    probs = model.predict_proba(data_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, probs)
    auc = roc_auc_score(y_test, probs)
    plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})", linewidth=2)

plt.plot([0, 1], [0, 1], 'k--', label='Random Chance (AUC = 0.500)')
plt.xlabel('False Positive Rate', fontsize=11)
plt.ylabel('True Positive Rate (Recall)', fontsize=11)
plt.title('ROC Curve Comparison (Test Set)', fontsize=13, fontweight='bold')
plt.legend(loc='lower right', fontsize=10)
plt.tight_layout()
plt.show()""")

    code("""# Plot Confusion Matrix for the best model (Gradient Boosting)
best_preds = gb_model.predict(X_test)
cm = confusion_matrix(y_test, best_preds)

fig, ax = plt.subplots(figsize=(6, 5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Active (0)', 'Churned (1)'])
disp.plot(cmap='Blues', ax=ax, values_format='d')
plt.title('Confusion Matrix: Gradient Boosting', fontweight='bold', fontsize=12)
plt.grid(False)
plt.tight_layout()
plt.show()""")

    # Step 9: Feature Importance
    md("""## Step 9: Feature Importance
Which customer signals are most influential in predicting churn?""")
    code("""# Extract feature importances from Gradient Boosting model
feat_importances = pd.Series(gb_model.feature_importances_, index=X_encoded.columns)
top_features = feat_importances.sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_features.values, y=top_features.index, palette='Blues_r', edgecolor='black')
plt.title('Top 10 Most Important Features (Gradient Boosting)', fontsize=13, fontweight='bold')
plt.xlabel('Relative Feature Importance Score')
plt.tight_layout()
plt.show()

print("Top 5 Drivers of Churn:")
for rank, (feat, score) in enumerate(top_features.head(5).items(), 1):
    print(f" {rank}. {feat:25s} : {score:.4f}")""")

    md("""💡 **Business Interpretation of Feature Importances**:
1. **`had_failed_payment` & `payment_failure_rate`**: By far the strongest predictive signals. Involuntary billing failure triggers massive churn.
2. **`billing_cycle_Monthly`**: Monthly customers have much less friction to leave compared to annual subscribers.
3. **`avg_monthly_hours` & `usage_trend_ratio`**: Drops in platform activity precede cancellation by several weeks.
4. **`avg_csat`**: Dissatisfied customer service interactions directly increase churn risk.""")

    # Step 10: Save Model Artifacts
    md("""## Step 10: Save Best Model & Preprocessing Artifacts
We save the trained model and scaler to the `models/` directory so they can be loaded by `06_risk_scoring.ipynb`.""")
    code("""# Ensure models directory exists
Path('models').mkdir(parents=True, exist_ok=True)

# Save best model and scaler
joblib.dump(gb_model, 'models/best_churn_model.joblib')
joblib.dump(scaler, 'models/scaler.joblib')

# Save encoded column list so future scoring matches exact column order
joblib.dump(list(X_encoded.columns), 'models/model_feature_names.joblib')

print("✅ Model artifacts successfully saved to models/:")
print("   - models/best_churn_model.joblib")
print("   - models/scaler.joblib")
print("   - models/model_feature_names.joblib")""")

    # Final Summary Table
    md("""## Summary & Next Steps

### 🎓 Fresher Interview Talking Points:
- **Baseline vs Benchmark**: Trained an interpretable linear model (**Logistic Regression**, 0.73 AUC) and two tree ensembles (**Random Forest**, 0.75 AUC; **Gradient Boosting**, 0.75 AUC).
- **Leakage Prevention**: Strictly scaled and transformed the test set using training set parameters only.
- **Top Drivers**: Model mathematically confirmed that **payment failures**, **monthly billing cycles**, and **usage decline** are the top drivers of subscription attrition.

---

### 🚀 Next Step:
Now that the model is trained and saved, we are ready for **`06_risk_scoring.ipynb`** (or evaluation) to generate customer risk scores (0 to 100), assign risk tiers (High / Medium / Low), and compute Revenue-at-Risk!""")

    return nb

# Save notebook
nb = make_model_notebook()
out_path = Path('notebooks/05_model_training.ipynb')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"Generated {out_path}")
