import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load dataset
file_path = '/Data/Processed/Autism-Merged-Dataset.csv'
try:
    merged_df = pd.read_csv(file_path)
    print(f"✅ Successfully loaded merged dataset with {merged_df.shape[0]} rows and {merged_df.shape[1]} columns")
except FileNotFoundError:
    print(f"❌ Error: File not found at {file_path}. Check the path and try again.")
    exit()

# ✅ Ensure 'class/asd' is binary (0 = Non-Diagnosed, 1 = Diagnosed)
if merged_df['class/asd'].dtype == 'object':
    merged_df['class/asd'] = merged_df['class/asd'].map({'yes': 1, 'no': 0})

# ✅ Drop rows with missing age group data
merged_df = merged_df.dropna(subset=['age_group'])

# ✅ Count of Positive ASD Diagnoses by Age Group
print("\n📊 Positive ASD Diagnoses by Age Group:")
age_group_diagnosis = merged_df.groupby('age_group')['class/asd'].sum()  # Sum of diagnosed cases
print(age_group_diagnosis)

# ✅ Normalized ASD Diagnosis Rate by Age Group
print("\n📊 Normalized ASD Diagnosis Rate by Age Group (%):")
age_group_total = merged_df['age_group'].value_counts()  # Get total cases per age group
age_group_diagnosis_rate = (age_group_diagnosis / age_group_total) * 100  # Convert to percentage
print(age_group_diagnosis_rate)

# ✅ Plot Normalized Diagnosis Rate with Labels
plt.figure(figsize=(6, 4))
ax = sns.barplot(x=age_group_diagnosis_rate.index, y=age_group_diagnosis_rate.values, palette="viridis")
plt.title("Percentage of Positive ASD Diagnoses by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Diagnosis Rate (%)")
plt.ylim(0, 70)

# Add value labels
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

plt.show()

# ✅ Average Screening Score by Age Group
print("\n📊 Average Screening Score by Age Group:")
age_group_scores = merged_df.groupby('age_group')['result'].agg(['mean', 'median'])
print(age_group_scores)

# ✅ Boxplot: Distribution of Screening Scores by Age Group
plt.figure(figsize=(8, 5))
sns.boxplot(data=merged_df, x='age_group', y='result', palette="Set2")
plt.title('Distribution of Screening Scores by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Screening Score (Result)')
plt.show()

###-----------------------------------------------
# Statistical Analysis
###-----------------------------------------------
# ✅ Perform ANOVA to compare AQ-10 scores across age groups
age_groups = merged_df['age_group'].unique()
grouped_scores = [merged_df[merged_df['age_group'] == age]['result'] for age in age_groups]
anova_stat, anova_p = stats.f_oneway(*grouped_scores)

# ✅ Create a contingency table for the Chi-Square Test (raw counts)
contingency_table = pd.crosstab(merged_df['age_group'], merged_df['class/asd'])
chi2_stat, chi2_p, _, _ = stats.chi2_contingency(contingency_table)

# ✅ Display Results
print("\n📊 **ANOVA Test for AQ-10 Scores Across Age Groups**")
print(f"F-statistic: {anova_stat:.4f}, p-value: {anova_p:.4f}")

print("\n📊 **Chi-Square Test for ASD Diagnosis Across Age Groups**")
print(f"Chi-Square statistic: {chi2_stat:.4f}, p-value: {chi2_p:.4f}")

# ✅ Interpretation
if anova_p < 0.05:
    print("\n✅ The ANOVA test suggests a statistically significant difference in AQ-10 scores between age groups.")
else:
    print("\n❌ The ANOVA test suggests no significant difference in AQ-10 scores between age groups.")

if chi2_p < 0.05:
    print("\n✅ The Chi-Square test suggests a significant relationship between age group and ASD diagnosis rates.")
else:
    print("\n❌ The Chi-Square test suggests no significant relationship between age group and ASD diagnosis rates.")
