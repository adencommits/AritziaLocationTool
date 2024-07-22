# crimerate_data_clean.py is a Python script that cleans
# and processes crime rate data for Toronto.

import pandas as pd

# Load the data
df = pd.read_csv('toronto_crime_data.csv')

# Identify the relevant columns
relevant_columns = ['AREA_NAME', 'POPULATION_2023'] + [col for col in df.columns if '2023' in col and 'RATE' not in col]

# Drop the irrelevant columns
df = df[relevant_columns]

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_toronto_crime_data.csv', index=False)