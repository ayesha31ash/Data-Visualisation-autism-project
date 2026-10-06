import pandas as pd

# Load CSV files
base_path = '/Users/naimaali/Downloads/Autism_Datasets/f-2-xdv-gp-campus-group-6/'  # Update this path if needed

# Load each dataset
adult_df = pd.read_csv(base_path + 'Autism-Adult-Data.csv')
adolescent_df = pd.read_csv(base_path + 'Autism-Adolescent-Data.csv')
child_df = pd.read_csv(base_path + 'Autism-Child-Data.csv')

# Function to inspect datasets
def inspect_dataset(df, name):
    print(f"\n🔍 Dataset: {name}")
    print("-" * 40)
    print("Basic Info:")
    print(df.info())
    print("\nFirst 5 Rows:")
    print(df.head())
    print("\nMissing Values:")
    print(df.isnull().sum())

# Inspect all datasets
inspect_dataset(adult_df, "Adult")
inspect_dataset(adolescent_df, "Adolescent")
inspect_dataset(child_df, "Child")

# 🔥Step 2.1: Fix Data Types & Decode Byte Strings
# Function to decode byte strings
def decode_columns(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: x.strip("b'") if isinstance(x, str) else x)
    return df

# Apply decoding to all datasets
adult_df = decode_columns(adult_df)
adolescent_df = decode_columns(adolescent_df)
child_df = decode_columns(child_df)

# Inspect to confirm the fix
print("\n✅ Checking if byte strings are removed:")
inspect_dataset(adult_df, "Adult")
inspect_dataset(adolescent_df, "Adolescent")
inspect_dataset(child_df, "Child")

import numpy as np


# 🔥Step 2.2.1: Handle '?' values by converting them to NaN
def convert_question_marks_to_nan(df, dataset_name):
    df.replace('?', np.nan, inplace=True)
    print(f"✅ Replaced '?' with NaN in {dataset_name} dataset.")
    return df


# Step 2.2.2: Fix unrealistic ages by replacing outliers with median age
def fix_age_outliers(df, dataset_name):
    max_valid_age = 100  # Assuming age above 100 is unrealistic
    invalid_ages = df[df['age'] > max_valid_age]

    if not invalid_ages.empty:
        print(f"\n❌ Unrealistic ages detected in {dataset_name} dataset:\n")
        print(invalid_ages[['age']])

        # Replace outliers with the median of valid ages
        median_age = df[df['age'] <= max_valid_age]['age'].median()
        df.loc[df['age'] > max_valid_age, 'age'] = median_age
        print(f"✅ Replaced unrealistic ages with median age ({median_age}) in {dataset_name} dataset.")
    else:
        print(f"\n✅ No unrealistic ages detected in {dataset_name} dataset.")

    return df


# Step 2.2.3: Handle missing values for age, ethnicity, and relation
def handle_missing_values(df, dataset_name):
    # Fill missing age values with median
    if 'age' in df.columns:
        median_age = df['age'].median()
        df['age'].fillna(median_age, inplace=True)
        print(f"✅ Filled missing age values with median ({median_age}) for {dataset_name} dataset.")

    # Fill missing ethnicity with 'Unknown'
    if 'ethnicity' in df.columns:
        df['ethnicity'].fillna('Unknown', inplace=True)
        print(f"✅ Filled missing ethnicity values with 'Unknown' for {dataset_name} dataset.")

    # Fill missing relation values using hybrid strategy
    if 'relation' in df.columns:
        missing_count = df['relation'].isnull().sum()
        mode_relation = df['relation'].mode()[0]

        if missing_count > 0:
            # If a relation appears in >60% of cases, fill with mode
            if df['relation'].value_counts(normalize=True).max() > 0.6:
                df['relation'].fillna(mode_relation, inplace=True)
                print(f"✅ Filled missing relation values with mode ({mode_relation}) for {dataset_name} dataset.")
            else:
                df['relation'].fillna('Unknown', inplace=True)
                print(f"✅ Filled missing relation values with 'Unknown' for {dataset_name} dataset.")

    return df


# Step 2.2.4: Function to verify missing values
def list_missing_values(df, dataset_name):
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        print(f"\n❌ Missing values in {dataset_name} dataset:")
        print(missing_values)
    else:
        print(f"\n✅ No missing values found in {dataset_name} dataset.")


# ✅ Applying the cleaning steps to all datasets
# Convert '?' to NaN
adult_df = convert_question_marks_to_nan(adult_df, "Adult")
adolescent_df = convert_question_marks_to_nan(adolescent_df, "Adolescent")
child_df = convert_question_marks_to_nan(child_df, "Child")

# Fix age outliers
adult_df = fix_age_outliers(adult_df, "Adult")
adolescent_df = fix_age_outliers(adolescent_df, "Adolescent")
child_df = fix_age_outliers(child_df, "Child")

# Handle missing values
adult_df = handle_missing_values(adult_df, "Adult")
adolescent_df = handle_missing_values(adolescent_df, "Adolescent")
child_df = handle_missing_values(child_df, "Child")

# Final check for missing values
list_missing_values(adult_df, "Adult")
list_missing_values(adolescent_df, "Adolescent")
list_missing_values(child_df, "Child")

# 🔥Step 2.3: Standardize Column Names
# Step 2.3.1: Standardize column names
def standardize_column_names(df):
    df.columns = (
        df.columns
        .str.lower()  # Convert to lowercase
        .str.replace(' ', '_')  # Replace spaces with underscores
        .str.replace('jundice', 'jaundice')  # Fix typos
        .str.replace('austim', 'autism')
        .str.replace('contry_of_res', 'country_of_res')
    )
    return df


# Step 2.3.2: Standardize categorical values
def standardize_categorical_values(df):
    categorical_columns = ['gender', 'relation', 'ethnicity', 'age_desc', 'class/asd', 'country_of_res']

    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

            # Handle common category variations
            if col == 'gender':
                df[col] = df[col].replace({'m': 'male', 'f': 'female'})

    return df


# Apply to all datasets
adult_df = standardize_column_names(adult_df)
adolescent_df = standardize_column_names(adolescent_df)
child_df = standardize_column_names(child_df)

adult_df = standardize_categorical_values(adult_df)
adolescent_df = standardize_categorical_values(adolescent_df)
child_df = standardize_categorical_values(child_df)

# Confirm standardization
print("\n✅ Standardized column names and categorical values:")
print(adult_df.head())
print(adolescent_df.head())
print(child_df.head())


# 🔥Step 2.4: Merging the datasets
# Step 2.4.1: Add an age group column
adult_df['age_group'] = 'adult'
adolescent_df['age_group'] = 'adolescent'
child_df['age_group'] = 'child'

# Step 2.4.2: Merge datasets
merged_df = pd.concat([adult_df, adolescent_df, child_df], ignore_index=True)

# Step 2.4.3: Verify the merged dataset
print("\n✅ Merged Dataset Overview:")
print(merged_df.info())
print("\n🔍 First 5 Rows of the Merged Dataset:")
print(merged_df.head())

# Step 2.4.4: Check value counts of the new age_group column
print("\n📊 Age Group Distribution:")
print(merged_df['age_group'].value_counts())

# Export the merged dataset to a CSV file
output_path = '/Users/naimaali/Downloads/Autism_Datasets/f-2-xdv-gp-campus-group-6/Autism-Merged-Dataset.csv'
merged_df.to_csv(output_path, index=False)
print(f"✅ Merged dataset successfully exported to {output_path}")
