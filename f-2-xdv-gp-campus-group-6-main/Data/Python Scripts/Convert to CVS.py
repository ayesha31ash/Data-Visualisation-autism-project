import pandas as pd
from scipy.io import arff
import os

# Function to convert ARFF to CSV
def convert_arff_to_csv(input_path, output_path):
    data, meta = arff.loadarff(input_path)
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Successfully converted {input_path} to {output_path}")

# Define the file paths (update these paths to match your directory structure)
base_path = '/Users/naimaali/Downloads/Autism_Datasets/f-2-xdv-gp-campus-group-6/'



# File mappings
datasets = {
    "Autism-Adult-Data.arff": "Autism-Adult-Data.csv",
    "Autism-Adolescent-Data.arff": "Autism-Adolescent-Data.csv",
    "Autism-Child-Data.arff": "Autism-Child-Data.csv"
}

# Convert all files
for arff_file, csv_file in datasets.items():
    input_path = os.path.join(base_path, arff_file)
    output_path = os.path.join(base_path, csv_file)
    convert_arff_to_csv(input_path, output_path)
