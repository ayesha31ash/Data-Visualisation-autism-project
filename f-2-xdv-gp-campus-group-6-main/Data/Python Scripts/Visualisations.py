import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the merged dataset
file_path = '/Data/Processed/Autism-Merged-Dataset.csv'
merged_df = pd.read_csv(file_path)

# Ensure 'class/asd' is binary (0 = Non-Diagnosed, 1 = Diagnosed)
if merged_df['class/asd'].dtype == 'object':
    merged_df['class/asd'] = merged_df['class/asd'].map({'yes': 1, 'no': 0})

# ---------------------------
# 📊 Mirrored Bar Chart: Gender Diagnosis Rate
# ---------------------------
gender_diagnosis_rate = merged_df.groupby('gender')['class/asd'].value_counts(normalize=True).unstack() * 100
gender_diagnosis_rate.columns = ["Non-Diagnosed", "Diagnosed"]

fig, ax = plt.subplots(figsize=(8, 5))

# Plot mirrored bars
ax.barh(gender_diagnosis_rate.index, gender_diagnosis_rate["Non-Diagnosed"], color="blue", label="Non-Diagnosed")
ax.barh(gender_diagnosis_rate.index, -gender_diagnosis_rate["Diagnosed"], color="red", label="Diagnosed")

# Formatting
ax.set_xlabel("Percentage (%)")
ax.set_title("Mirrored Bar Chart: ASD Diagnosis Rate by Gender")
ax.axvline(0, color="black", linewidth=1)  # Center line
ax.legend()
plt.show()

# ---------------------------
# 📊 Mirrored Bar Chart: Ethnicity Diagnosis Rate
# ---------------------------
ethnicity_diagnosis_rate = merged_df.groupby('ethnicity')['class/asd'].value_counts(normalize=True).unstack() * 100
ethnicity_diagnosis_rate.columns = ["Non-Diagnosed", "Diagnosed"]

fig, ax = plt.subplots(figsize=(10, 6))

# Plot mirrored bars
ax.barh(ethnicity_diagnosis_rate.index, ethnicity_diagnosis_rate["Non-Diagnosed"], color="blue", label="Non-Diagnosed")
ax.barh(ethnicity_diagnosis_rate.index, -ethnicity_diagnosis_rate["Diagnosed"], color="red", label="Diagnosed")

# Formatting
ax.set_xlabel("Percentage (%)")
ax.set_title("Mirrored Bar Chart: ASD Diagnosis Rate by Ethnicity")
ax.axvline(0, color="black", linewidth=1)  # Center line
ax.legend()
plt.show()

# ---------------------------
# 📊 Grouped Bar Chart with Error Bars: AQ-10 Scores by Gender
# ---------------------------
gender_stats = merged_df.groupby(['gender', 'class/asd'])['result'].agg(['mean', 'std']).reset_index()
gender_stats['class/asd'] = gender_stats['class/asd'].map({0: "Non-Diagnosed", 1: "Diagnosed"})

plt.figure(figsize=(8, 5))
sns.barplot(data=gender_stats, x='gender', y='mean', hue='class/asd',
            palette={"Non-Diagnosed": "blue", "Diagnosed": "red"},
            capsize=0.2, ci=None)

# Add error bars
for i, row in gender_stats.iterrows():
    plt.errorbar(x=i//2, y=row['mean'], yerr=row['std'], fmt='none', capsize=5, color='black')

plt.title("Grouped Bar Chart with Error Bars: AQ-10 Scores by Gender")
plt.xlabel("Gender")
plt.ylabel("Mean AQ-10 Score")
plt.legend(title="Diagnosis")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# ---------------------------
# 📊 Grouped Bar Chart with Error Bars: AQ-10 Scores by Ethnicity
# ---------------------------
ethnicity_stats = merged_df.groupby(['ethnicity', 'class/asd'])['result'].agg(['mean', 'std']).reset_index()
ethnicity_stats['class/asd'] = ethnicity_stats['class/asd'].map({0: "Non-Diagnosed", 1: "Diagnosed"})

plt.figure(figsize=(10, 5))
sns.barplot(data=ethnicity_stats, x='ethnicity', y='mean', hue='class/asd',
            palette={"Non-Diagnosed": "blue", "Diagnosed": "red"},
            capsize=0.2, ci=None)

# Add error bars
for i, row in ethnicity_stats.iterrows():
    plt.errorbar(x=i//2, y=row['mean'], yerr=row['std'], fmt='none', capsize=5, color='black')

plt.title("Grouped Bar Chart with Error Bars: AQ-10 Scores by Ethnicity")
plt.xlabel("Ethnicity")
plt.ylabel("Mean AQ-10 Score")
plt.xticks(rotation=45, ha='right')
plt.legend(title="Diagnosis")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
