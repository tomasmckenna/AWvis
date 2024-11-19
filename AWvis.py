"""AWvis 1.4"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into a Pandas DataFrame
file_path = '/Users/admin/Desktop/Docs/CS/apple_health_export/HeartWatch-20241009-to-20241118.csv'
data = pd.read_csv(file_path)

# Inspect the first few rows
print("Data Preview:")
print(data.head())
print("Columns in the dataset:", data.columns)

# Ensure numeric columns are parsed correctly
numeric_columns = ['Daily-Avg.-bpm', 'Daily-lo-bpm', 'Daily-hi-bpm', 'Move-Cals', 'Distance-km']
for col in numeric_columns:
    if col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert to float, replacing errors with NaN
    else:
        print(f"Warning: Column '{col}' is missing from the dataset and will be skipped.")

# Ensure the ISO column is parsed as datetime
data['ISO'] = pd.to_datetime(data['ISO'], errors='coerce')

# Group by Date
if 'Date' not in data.columns:
    raise KeyError("The 'Date' column is missing from the dataset. Ensure it exists for grouping.")
grouped = data.groupby('Date')

# Calculate statistics
stats = grouped.agg({
    'Daily-Avg.-bpm': ['mean', 'min', 'max'],
    'Daily-lo-bpm': 'min',
    'Daily-hi-bpm': 'max',
    'Move-Cals': 'mean',
    'Distance-km': ['mean', 'max'],
})

# Rename columns for better readability
stats.columns = [
    'Avg HR', 'Min HR', 'Max HR',
    'Min Lo HR', 'Max Hi HR',
    'Avg Calories', 'Avg Distance (km)', 'Max Distance (km)'
]
stats = stats.sort_values(by='Avg Calories', ascending=False)

# Display the summary statistics
print("\nDaily Statistics Summary:")
print(stats)

# Plot 1: Average Heart Rate by Date
plt.figure(figsize=(10, 6))
stats['Avg HR'].plot(kind='bar', color='skyblue')
plt.title('Average Heart Rate by Date')
plt.ylabel('Heart Rate (BPM)')
plt.xlabel('Date')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Plot 2: Calories Burned by Date
plt.figure(figsize=(10, 6))
stats['Avg Calories'].plot(kind='bar', color='orange')
plt.title('Average Calories Burned by Date')
plt.ylabel('Calories')
plt.xlabel('Date')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Plot 3: Distance Covered by Date
plt.figure(figsize=(10, 6))
stats['Avg Distance (km)'].plot(kind='bar', color='green')
plt.title('Average Distance Covered by Date')
plt.ylabel('Distance (km)')
plt.xlabel('Date')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Additional visualization: Calories vs. Heart Rate Scatter Plot
plt.figure(figsize=(10, 6))
if 'Daily-Avg.-bpm' in data.columns and 'Move-Cals' in data.columns:
    plt.scatter(data['Daily-Avg.-bpm'], data['Move-Cals'], alpha=0.6, color='purple')
    plt.title('Calories Burned vs. Average Heart Rate')
    plt.xlabel('Average Heart Rate (BPM)')
    plt.ylabel('Calories Burned')
    plt.grid()
    plt.tight_layout()
    plt.show()
else:
    print("Cannot plot scatter plot: Required columns 'Daily-Avg.-bpm' or 'Move-Cals' are missing.")
