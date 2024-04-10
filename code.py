import pandas as pd

# Load the dataset
df = pd.read_csv('test_data.csv')

# Count the number of null values in each column
null_counts = df.isnull().sum()

# Print the total number of null values
print(null_counts.sum())