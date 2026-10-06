import pandas as pd

# Define the table data
data = {
    "Visualization Type": [
        "Complex Visualization (Unique)",
        "Interactive Visualization (With Interactions)",
        "Positive vs. Negative Facet Visualization",
        "General Visualization (Supporting Chart)"
    ],
    "Description": [
        "A creative and advanced visualization not covered in labs, showcasing complex data relationships or hierarchies.",
        "Allows users to filter, highlight, and interact with data across multiple visualizations.",
        "Two contrasting visualizations showcasing both positive and negative aspects of the same dataset.",
        "A simple visualization that contributes to the overall data story but doesn’t need to be as complex or interactive."
    ],
    "Examples": [
        "Force-Directed Graph (e.g., social networks, relationships)\nSunburst Chart (e.g., hierarchical data)\nRadial Bar Chart (e.g., cyclical data patterns)",
        "Linked Scatter Plot & Bar Chart (e.g., filtering data dynamically)\nBrushing & Linking between charts",
        "Dual Heatmaps (e.g., GDP growth vs. unemployment)\nMirrored Bar Charts (positive vs. negative metrics shown side by side)",
        "Line Chart (e.g., trends over time like CO₂ emissions)\nSimple Bar Chart (e.g., revenue by category)"
    ],
    "Interactions/Features": [
        "Interactive nodes\nZooming and panning\nAnimated transitions",
        "Highlight/filter data within/between charts\nBidirectional filtering\nDynamic tooltips for extra data on hover",
        "Side-by-side comparison\nColor-coded facets (positive in green, negative in red)\nConsistent scale for easy comparison",
        "Basic interactivity (e.g., hover effects, tooltips)\nSmooth animations"
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to an Excel file
file_path = '/Users/naimaali/Downloads/Data_Visualization_Project_Plan.xlsx/'
df.to_excel(file_path, index=False)

file_path
