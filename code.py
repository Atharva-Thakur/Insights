import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('test_data.csv')

# Check the correlation between 'Air temperature [K]' and 'Target'
corr = df['Air temperature [K]'].corr(df['Target'])

# Plot the scatter plot
sns.scatterplot(x='Air temperature [K]', y='Target', data=df)
plt.show()

# Print the correlation coefficient
print('Correlation coefficient:', corr)