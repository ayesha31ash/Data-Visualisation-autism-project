import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Load the merged dataset
file_path = '/Data/Processed/Autism-Merged-Dataset.csv'
merged_df = pd.read_csv(file_path)

# ✅ Ensure 'class/asd' is binary (0 = Non-Diagnosed, 1 = Diagnosed)
if merged_df['class/asd'].dtype == 'object':
    merged_df['class/asd'] = merged_df['class/asd'].map({'yes': 1, 'no': 0})

# -----------------------------------
# 📊 Mean AQ-10 Scores by Gender & Diagnosis
# -----------------------------------
gender_stats = merged_df.groupby(['gender', 'class/asd'])['result'].agg(['mean', 'std']).reset_index()
gender_stats['class/asd'] = gender_stats['class/asd'].map({0: "Non-Diagnosed", 1: "Diagnosed"})

# Print computed values
print("\n📊 Mean AQ-10 Scores by Gender & Diagnosis Status:")
print(gender_stats.to_string(index=False))

# Plot: Mean AQ-10 Scores by Gender
plt.figure(figsize=(8, 5))
sns.barplot(data=gender_stats, x='gender', y='mean', hue='class/asd',
            palette={"Non-Diagnosed": "blue", "Diagnosed": "red"}, capsize=0.2)
plt.title('Mean AQ-10 Scores by Gender & Diagnosis Status')
plt.xlabel('Gender')
plt.ylabel('Mean AQ-10 Score')
plt.legend(title="Diagnosis")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# -----------------------------------
# 📊 Mean AQ-10 Scores by Ethnicity & Diagnosis
# -----------------------------------
ethnicity_stats = merged_df.groupby(['ethnicity', 'class/asd'])['result'].agg(['mean', 'std']).reset_index()
ethnicity_stats['class/asd'] = ethnicity_stats['class/asd'].map({0: "Non-Diagnosed", 1: "Diagnosed"})

# Print computed values
print("\n📊 Mean AQ-10 Scores by Ethnicity & Diagnosis Status:")
print(ethnicity_stats.to_string(index=False))

# Plot: Mean AQ-10 Scores by Ethnicity
plt.figure(figsize=(10, 5))
sns.barplot(data=ethnicity_stats, x='ethnicity', y='mean', hue='class/asd',
            palette={"Non-Diagnosed": "blue", "Diagnosed": "red"}, capsize=0.2)
plt.title('Mean AQ-10 Scores by Ethnicity & Diagnosis Status')
plt.xlabel('Ethnicity')
plt.ylabel('Mean AQ-10 Score')
plt.xticks(rotation=45, ha='right')
plt.legend(title="Diagnosis")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# -----------------------------------
# 📊 Diagnosis Rate by Gender (Normalized)
# -----------------------------------
gender_diagnosis_rate = merged_df.groupby('gender')['class/asd'].value_counts(normalize=True).unstack() * 100
gender_diagnosis_rate.columns = ["Non-Diagnosed", "Diagnosed"]

# Print computed values
print("\n📊 Diagnosis Rate by Gender (%):")
print(gender_diagnosis_rate.to_string())

# Plot: Diagnosis Rate by Gender
plt.figure(figsize=(8, 5))
gender_diagnosis_rate.plot(kind='bar', color=["blue", "red"], edgecolor="black")
plt.title('Diagnosis Rate by Gender (Normalized)')
plt.xlabel('Gender')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=0)
plt.legend(title="Diagnosis", labels=["Non-Diagnosed", "Diagnosed"])
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# -----------------------------------
# 📊 Diagnosis Rate by Ethnicity (Normalized)
# -----------------------------------
ethnicity_diagnosis_rate = merged_df.groupby('ethnicity')['class/asd'].value_counts(normalize=True).unstack() * 100
ethnicity_diagnosis_rate.columns = ["Non-Diagnosed", "Diagnosed"]

# Print computed values
print("\n📊 Diagnosis Rate by Ethnicity (%):")
print(ethnicity_diagnosis_rate.to_string())

# Plot: Diagnosis Rate by Ethnicity
plt.figure(figsize=(10, 5))
ethnicity_diagnosis_rate.plot(kind='bar', color=["blue", "red"], edgecolor="black")
plt.title('Diagnosis Rate by Ethnicity (Normalized)')
plt.xlabel('Ethnicity')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=45, ha='right')
plt.legend(title="Diagnosis", labels=["Non-Diagnosed", "Diagnosed"])
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# -----------------------------------
# 📊 Chi-Square Test: Diagnosis Rate Differences Across Genders
# -----------------------------------
gender_contingency = merged_df.groupby('gender')['class/asd'].value_counts().unstack().fillna(0)
chi2_gender, p_gender, _, _ = stats.chi2_contingency(gender_contingency)

print("\n📊 Chi-Square Test for Gender Differences in Diagnosis Rates:")
print(f"Chi-Square statistic: {chi2_gender:.4f}, p-value: {p_gender:.4f}")

if p_gender < 0.05:
    print("✅ Statistically significant difference in ASD diagnosis rates between genders.")
else:
    print("❌ No statistically significant difference in ASD diagnosis rates between genders.")

# -----------------------------------
# 📊 Chi-Square Test: Diagnosis Rate Differences Across Ethnicities
# -----------------------------------
ethnicity_contingency = merged_df.groupby('ethnicity')['class/asd'].value_counts().unstack().fillna(0)
chi2_ethnicity, p_ethnicity, _, _ = stats.chi2_contingency(ethnicity_contingency)

print("\n📊 Chi-Square Test for Ethnic Differences in Diagnosis Rates:")
print(f"Chi-Square statistic: {chi2_ethnicity:.4f}, p-value: {p_ethnicity:.4f}")

if p_ethnicity < 0.05:
    print("✅ Statistically significant difference in ASD diagnosis rates between ethnic groups.")
else:
    print("❌ No statistically significant difference in ASD diagnosis rates between ethnic groups.")

