import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from itertools import combinations
import numpy as np
from statsmodels.stats.multitest import multipletests

# Load dataset
merged_df = pd.read_csv('/Data/Processed/Autism-Merged-Dataset.csv')

# ✅ Ensure 'class/asd' is binary (0 = Non-Diagnosed, 1 = Diagnosed)
if merged_df['class/asd'].dtype == 'object':
    merged_df['class/asd'] = merged_df['class/asd'].map({'yes': 1, 'no': 0})

# ✅ Ensure country column exists and clean missing values
if 'country_of_res' not in merged_df.columns:
    raise KeyError("Column 'country_of_res' not found in dataset.")

# ✅ Count samples per country
country_counts = merged_df['country_of_res'].value_counts()

# ✅ Filter for countries with ≥20 participants
valid_countries = country_counts[country_counts >= 20].index
filtered_df = merged_df[merged_df['country_of_res'].isin(valid_countries)]

print(f"\n📌 Removed {len(country_counts) - len(valid_countries)} countries with fewer than 20 participants.")
print(f"📌 Remaining countries in analysis: {len(valid_countries)}")

# ✅ Compute Mean AQ-10 Score and Standard Deviation by Country
region_stats = filtered_df.groupby('country_of_res')['result'].agg(['mean', 'std', 'count']).reset_index()
region_stats.columns = ['Country', 'Mean_AQ10_Score', 'Std_AQ10_Score', 'Sample_Size']

# ✅ Compute Weighted Diagnosis Rate
diagnosis_rate = filtered_df.groupby('country_of_res')['class/asd'].mean().reset_index()
diagnosis_rate.columns = ['Country', 'Diagnosis_Rate']
diagnosis_rate['Diagnosis_Rate'] *= 100  # Convert to percentage

# ✅ Merge both datasets for visualization
final_stats = region_stats.merge(diagnosis_rate, on='Country')

# ✅ Display computed data
print("\n📊 Weighted Mean AQ-10 Scores by Region (Countries with ≥20 participants):")
print(final_stats[['Country', 'Mean_AQ10_Score', 'Std_AQ10_Score', 'Sample_Size']])

print("\n📊 Weighted Diagnosis Rate by Region (Countries with ≥20 participants):")
print(final_stats[['Country', 'Diagnosis_Rate']])

# **📊 Statistical Analysis: Chi-Square Test for Diagnosis Rate Differences**
diagnosis_table = pd.crosstab(filtered_df['country_of_res'], filtered_df['class/asd'])
chi2_stat, p_value, dof, expected = stats.chi2_contingency(diagnosis_table)

print(f"\n📊 Chi-Square Test for Geographic Differences in Diagnosis Rates:")
print(f"Chi-Square statistic: {chi2_stat:.4f}, p-value: {p_value:.4f}")

if p_value < 0.05:
    print("✅ Statistically significant difference in ASD diagnosis rates across countries.")
else:
    print("❌ No statistically significant difference in ASD diagnosis rates across countries.")

# -----------------------------------
# **📊 Post-hoc Analysis: Pairwise Chi-Square Comparisons**
# -----------------------------------

# Generate all country pairs for pairwise comparison
country_pairs = list(combinations(valid_countries, 2))
p_values = []

for country1, country2 in country_pairs:
    sub_table = diagnosis_table.loc[[country1, country2]]  # Subset for the two countries
    chi2, p = stats.chi2_contingency(sub_table)[0:2]  # Get Chi-square and p-value
    p_values.append(p)

# Apply Bonferroni correction for multiple comparisons
adjusted_p_values = multipletests(p_values, method='bonferroni')[1]

# Store significant results
significant_pairs = [(country1, country2, p_adj) for (country1, country2), p_adj in zip(country_pairs, adjusted_p_values) if p_adj < 0.05]

print("\n📊 Significant Country Differences in ASD Diagnosis Rates (Post-hoc Chi-Square with Bonferroni Correction):")
if significant_pairs:
    for pair in significant_pairs:
        print(f"✅ {pair[0]} vs {pair[1]} → Adjusted p-value: {pair[2]:.4f}")
else:
    print("❌ No significant pairwise differences after Bonferroni correction.")

# -----------------------------------
# **📊 Visualization: Bar Charts**
# -----------------------------------
sns.set(style="whitegrid")

# **📊 Mean AQ-10 Scores by Country**
plt.figure(figsize=(14, 6))
sns.barplot(data=final_stats.sort_values(by='Mean_AQ10_Score', ascending=False),
            x='Country', y='Mean_AQ10_Score', palette="Blues_r")

plt.xticks(rotation=30, ha='right', fontsize=10)  # Rotate labels for readability
plt.xlabel("")
plt.ylabel("Mean AQ-10 Score", fontsize=12)
plt.title("Mean AQ-10 Scores by Region (Countries with ≥20 Participants)", fontsize=14)
plt.subplots_adjust(bottom=0.25)  # Adjust bottom margin for better label visibility
plt.show()

# **📊 Weighted Diagnosis Rate by Country**
plt.figure(figsize=(14, 6))
sns.barplot(data=final_stats.sort_values(by='Diagnosis_Rate', ascending=False),
            x='Country', y='Diagnosis_Rate', palette="Reds_r")

plt.xticks(rotation=30, ha='right', fontsize=10)
plt.xlabel("")
plt.ylabel("Weighted Diagnosis Rate (%)", fontsize=12)
plt.title("Weighted Diagnosis Rate by Region (Countries with ≥20 Participants)", fontsize=14)
plt.subplots_adjust(bottom=0.25)
plt.show()

# **🗺 Choropleth Map: Mean AQ-10 Scores**
fig_aq10 = px.choropleth(final_stats, locations="Country",
                         locationmode="country names",
                         color="Mean_AQ10_Score",
                         hover_name="Country",
                         color_continuous_scale="Blues",
                         title="Global Distribution of Mean AQ-10 Scores")
fig_aq10.show()

# **🗺 Choropleth Map: Weighted Diagnosis Rate**
fig_diag = px.choropleth(final_stats, locations="Country",
                         locationmode="country names",
                         color="Diagnosis_Rate",
                         hover_name="Country",
                         color_continuous_scale="Reds",
                         title="Global Distribution of Weighted Diagnosis Rate (%)")
fig_diag.show()
