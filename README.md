# Data Visualisation group 6: Autism Data Project

## Contibutors
1. Naima Ali
2. Anam Ayyub
3. Umme Hani Shafeeq
4. Ayesha Syed Mohammad


## 📊 Project Overview
This project explores autism screening outcomes across different life stages—children, adolescents, and adults—using three related datasets. By analyzing patterns across these age groups, we aim to gain insights into the impact of early diagnosis, behavioral evolution, and the influence of demographic factors on autism screening results.

We utilize datasets from the **UCI Machine Learning Repository**, each representing a distinct age group, to build a comprehensive, interactive visualization dashboard. These visualizations will provide insights into how autism screening patterns change over time and highlight key influencing factors.

## 📂 Project Structure: 
- `Data/`: Contains the original and processed datasets as well as the python scripts for.
- `scripts/`: Scripts for data processing and visualization.
- `styles/`: CSS files for styling the visualizations.
- `libs/d3/`: D3.js library files for creating interactive charts.

## 🚀 How to Run
1. **Clone the repository:**
   ```bash
   git clone <repository-link>
2. Navigate to the project directory:
    cd f21dv_gp_Dubai_6
3. Install dependencies (if applicable):
    pip install -r requirements.txt
4. Run the scripts


## Key Cleaning and Preprocessing Steps (Done by Naima Ali)
📁 Detailed preprocessing report can be found in the data/reports/ folder.

The three autism screening datasets (Adults, Adolescents, Children) were cleaned, standardized, and merged into a unified dataset for analysis and visualization.

✅ Key Cleaning and Preprocessing Steps:
	•	Data Conversion: Converted .arff files to .csv for easier processing.
	•	Missing Values: Filled missing age values with the median, ethnicity with "Unknown", and relation with the mode or "Unknown" if necessary.
	•	Outlier Handling: Replaced unrealistic age values (above 100) with the median.
	•	Standardization: Fixed typos, standardized column names (lowercase, underscores), and unified categorical values (e.g., gender labels).
	•	Dataset Merging: Combined all three datasets and added an age_group column to track the participant group (adult, adolescent, child).
	•	Geographical Data Preparation: Standardized country_of_res for compatibility with map visualizations.

Final Output:
	•	Merged dataset exported as Autism-Merged-Dataset.csv with 1100 records, ready for exploratory analysis and visualization.

