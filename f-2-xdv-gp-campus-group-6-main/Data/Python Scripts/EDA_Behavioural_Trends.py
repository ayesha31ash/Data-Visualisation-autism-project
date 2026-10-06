import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

# Load the merged dataset
file_path = '/Data/Processed/Autism-Merged-Dataset.csv'
merged_df = pd.read_csv(file_path)

# ✅ Ensure 'class/asd' is binary (0 = Non-Diagnosed, 1 = Diagnosed)
if merged_df['class/asd'].dtype == 'object':
    merged_df['class/asd'] = merged_df['class/asd'].map({'yes': 1, 'no': 0})

# ✅ Extract AQ-10 question columns dynamically
aq10_columns = [col for col in merged_df.columns if col.startswith("a") and col.endswith("_score")]

### ------------------------------------------
### **Step 1: AQ-10 Scores by Diagnosis Status**
### ------------------------------------------

# ✅ Compute mean and median screening scores by diagnosis status
diagnosis_stats = merged_df.groupby('class/asd')['result'].agg(['mean', 'median'])
diagnosis_stats.index = ['Non-Diagnosed', 'Diagnosed']

print("\n📊 AQ-10 Score Summary by Diagnosis Status:")
print(diagnosis_stats)

# ✅ Normalized Histogram of AQ-10 Scores by Diagnosis Status
sns.set_style("whitegrid")
plt.figure(figsize=(8, 5))

# Define bins
bins = list(range(0, 12))

# Plot histograms as percentages
sns.histplot(merged_df[merged_df['class/asd'] == 0]['result'], bins=bins, color="blue", label="Non-Diagnosed", alpha=0.6, kde=False, stat="percent", element="step")
sns.histplot(merged_df[merged_df['class/asd'] == 1]['result'], bins=bins, color="red", label="Diagnosed", alpha=0.6, kde=False, stat="percent", element="step")

# Formatting
plt.title('Normalized AQ-10 Score Distribution by Diagnosis Status', fontsize=14)
plt.xlabel('AQ-10 Score (Result)', fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(range(0, 11))
plt.legend(title="Diagnosis", labels=["Non-Diagnosed", "Diagnosed"])
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

### -----------------------------------------------------
### **Step 2: Mean & Standard Deviation by Age & Diagnosis**
### -----------------------------------------------------

# ✅ Compute mean and standard deviation of AQ-10 scores by age group & diagnosis status
summary_stats = merged_df.groupby(['age_group', 'class/asd'])['result'].agg(['mean', 'std']).reset_index()

# ✅ Print computed values for report inclusion
print("\n📊 Mean AQ-10 Scores by Age Group & Diagnosis Status:")
print(summary_stats.pivot(index='age_group', columns='class/asd', values='mean'))

print("\n📊 Standard Deviation of AQ-10 Scores by Age Group & Diagnosis Status:")
print(summary_stats.pivot(index='age_group', columns='class/asd', values='std'))

# ✅ Extract means and standard deviations for visualization
mean_scores = summary_stats.pivot(index='age_group', columns='class/asd', values='mean')
std_dev = summary_stats.pivot(index='age_group', columns='class/asd', values='std')

# ✅ Rename columns for clarity
mean_scores.columns = ['Non-Diagnosed', 'Diagnosed']
std_dev.columns = ['Non-Diagnosed', 'Diagnosed']

# ✅ Bar Chart: Mean AQ-10 Scores by Age Group & Diagnosis (with Error Bars)
plt.figure(figsize=(8, 5))
mean_scores.plot(kind='bar', yerr=std_dev, capsize=5, color=["blue", "red"], edgecolor="black", figsize=(8, 5))

# Formatting
plt.title('Mean AQ-10 Scores by Age Group & Diagnosis Status (with Error Bars)', fontsize=14)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Mean AQ-10 Score', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title="Diagnosis", labels=['Non-Diagnosed (Blue)', 'Diagnosed (Red)'])
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

### -----------------------------------------------------
### **Step 3: Logistic Regression for Predicting ASD Diagnosis**
### -----------------------------------------------------

# ✅ Define features (X) and target variable (y)
X = merged_df[aq10_columns]  # AQ-10 responses as predictors
y = merged_df['class/asd']   # ASD diagnosis as the target variable

# ✅ Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ✅ Train Logistic Regression with L2 Regularization
logit_model = LogisticRegression(penalty='l2', solver='liblinear', max_iter=500)
logit_model.fit(X_train, y_train)

# ✅ Model Predictions
y_pred_prob = logit_model.predict_proba(X_test)[:, 1]  # Probabilities for ASD (class 1)
y_pred = logit_model.predict(X_test)  # Binary Predictions

# ✅ Model Performance Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_prob)

print("\n📊 Model Performance Metrics:")
print(f"✅ Accuracy: {accuracy:.4f}")
print(f"✅ Precision: {precision:.4f}")
print(f"✅ Recall: {recall:.4f}")
print(f"✅ ROC-AUC Score: {roc_auc:.4f}")

# ✅ Extract Coefficients
coefficients = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': logit_model.coef_[0],
    'Odds Ratio': np.exp(logit_model.coef_[0])
}).sort_values(by='Odds Ratio', ascending=False)

print("\n📊 Logistic Regression: Feature Importance (Odds Ratios):")
print(coefficients)

# ✅ Plot Coefficients
plt.figure(figsize=(10, 6))
sns.barplot(x=coefficients['Feature'], y=coefficients['Odds Ratio'], palette="coolwarm")
plt.xticks(rotation=45, ha="right")
plt.xlabel("AQ-10 Questions")
plt.ylabel("Odds Ratio")
plt.title("Logistic Regression: Odds Ratios for ASD Prediction")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
