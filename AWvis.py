"""AWvis 1.0"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into a Pandas DataFrame
# Replace 'your_data.csv' with the actual file path
file_path = 'your_data.csv'
data = pd.read_csv(file_path)

# Inspect the first few rows to understand the structure
print("Data Preview:")
print(data.head())

# Ensure numeric columns are parsed correctly
numeric_columns = ['bpm-Avg.', 'bpm-lo', 'bpm-hi', 'Cals', 'km']
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert to float, replacing errors with NaN

# Ensure the ISO column is parsed as datetime
data['ISO'] = pd.to_datetime(data['ISO'], errors='coerce')

# Group by workout type
grouped = data.groupby('Type')

# Calculate statistics
stats = grouped.agg({
    'bpm-Avg.': ['mean', 'min', 'max'],
    'bpm-lo': 'min',
    'bpm-hi': 'max',
    'Cals': 'mean',
    'km': ['mean', 'max'],
    'Duration': 'count'
})

# Rename columns for better readability
stats.columns = [
    'Avg HR', 'Min HR', 'Max HR',
    'Min Lo HR', 'Max Hi HR',
    'Avg Calories', 'Avg Distance (km)', 'Max Distance (km)', 'Session Count'
]
stats = stats.sort_values(by='Session Count', ascending=False)

# Display the summary statistics
print("\nWorkout Statistics Summary:")
print(stats)

# Plot 1: Average Heart Rate by Workout Type
plt.figure(figsize=(10, 6))
stats['Avg HR'].plot(kind='bar', color='skyblue')
plt.title('Average Heart Rate by Workout Type')
plt.ylabel('Heart Rate (BPM)')
plt.xlabel('Workout Type')
plt.grid(axis='y')
plt.show()

# Plot 2: Calories Burned by Workout Type
plt.figure(figsize=(10, 6))
stats['Avg Calories'].plot(kind='bar', color='orange')
plt.title('Average Calories Burned by Workout Type')
plt.ylabel('Calories')
plt.xlabel('Workout Type')
plt.grid(axis='y')
plt.show()

# Plot 3: Distance Covered by Workout Type
plt.figure(figsize=(10, 6))
stats['Avg Distance (km)'].plot(kind='bar', color='green')
plt.title('Average Distance Covered by Workout Type')
plt.ylabel('Distance (km)')
plt.xlabel('Workout Type')
plt.grid(axis='y')
plt.show()

# Additional visualization: Calories vs. Heart Rate Scatter Plot
plt.figure(figsize=(10, 6))
plt.scatter(data['bpm-Avg.'], data['Cals'], alpha=0.6, color='purple')
plt.title('Calories Burned vs. Average Heart Rate')
plt.xlabel('Average Heart Rate (BPM)')
plt.ylabel('Calories Burned')
plt.grid()
plt.show()
