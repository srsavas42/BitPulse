import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the base directory and paths
base_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of `explore.py`
data_dir = os.path.join(base_dir, '../Data/CleanData')  # Navigate to the Data folder
combined_path = os.path.join(data_dir, 'combined/combined_data.csv')
pricing_path = os.path.join(data_dir, 'pricing/coin_metrics.csv')
# text_metrics_path = os.path.join(data_dir, 'text/cleaned_Bitcoin_new_comments.csv')

# Load datasets
combined_data = pd.read_csv(combined_path)
pricing_data = pd.read_csv(pricing_path)
# text_data = pd.read_csv(text_metrics_path)

# # Inspect the data
# print("Combined Data Sample:\n", combined_data.head())
# print("Pricing Data Sample:\n", pricing_data.head())

# # Check for missing values
# print("Missing Values in Combined Data:\n", combined_data.isnull().sum())
# print("Missing Values in Pricing Data:\n", pricing_data.isnull().sum())

# Only check text data if it is uncommented and loaded
# if 'text_data' in locals():
#     print("Missing Values in Text Metrics:\n", text_data.isnull().sum())

# Drop missing values and fill NaNs
combined_data.dropna(subset=['Bitcoin_Return', 'Bitcoin_Vol'], inplace=True)
pricing_data.dropna(subset=['Bitcoin_Return', 'Bitcoin_Vol'], inplace=True)
combined_data.fillna({'weight': 0, 'conviction avg': 0}, inplace=True)

# Aligning dates
# Convert date columns to datetime
combined_data['Date'] = pd.to_datetime(combined_data['Date'], errors='coerce')
pricing_data['Date'] = pd.to_datetime(pricing_data['Date'], format='%d/%m/%Y', errors='coerce')

# Drop rows with invalid dates
combined_data.dropna(subset=['Date'], inplace=True)
pricing_data.dropna(subset=['Date'], inplace=True)

# Merge datasets
merged_data = pd.merge(combined_data, pricing_data, on='Date', how='inner')

# # Inspect merged data
# print("Merged Data Sample:\n", merged_data.head())

# Explorations
# print(merged_data.columns)

# Define relevant numeric columns
numeric_cols = [
    'Bitcoin_Return_x', 'Bitcoin_Vol_x',
    'BNB_Return_x', 'BNB_Vol_x',
    'Ethereum_Return_x', 'Ethereum_Vol_x'
]

# Compute correlation matrix
correlation_matrix = merged_data[numeric_cols].corr()

# Plot correlation heatmap
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# Plot Bitcoin Return and Volatility over time
plt.figure(figsize=(12, 6))
plt.plot(merged_data['Date'], merged_data['Bitcoin_Return_x'], label='Bitcoin Return')
plt.plot(merged_data['Date'], merged_data['Bitcoin_Vol_x'], label='Bitcoin Volatility', alpha=0.7)
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Bitcoin Return and Volatility Trends')
plt.legend()
plt.show()

# Scatter plot: Weighted conviction vs Bitcoin Returns
sns.scatterplot(
    x='weighted conviction', 
    y='Bitcoin_Return_x', 
    data=merged_data, 
    alpha=0.7
)
plt.title('Weighted Conviction vs Bitcoin Returns')
plt.xlabel('Weighted Conviction')
plt.ylabel('Bitcoin Returns')
plt.show()

# Compute rolling mean for Bitcoin volatility and returns
merged_data['Rolling_Bitcoin_Vol'] = merged_data['Bitcoin_Vol_x'].rolling(window=30).mean()
merged_data['Rolling_Bitcoin_Return'] = merged_data['Bitcoin_Return_x'].rolling(window=30).mean()

# Plot Rolling Averages
plt.figure(figsize=(12, 6))
plt.plot(merged_data['Date'], merged_data['Rolling_Bitcoin_Vol'], label='Rolling Bitcoin Volatility', alpha=0.8)
plt.plot(merged_data['Date'], merged_data['Rolling_Bitcoin_Return'], label='Rolling Bitcoin Returns', alpha=0.8)
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Rolling Bitcoin Volatility and Returns (30-day Window)')
plt.legend()
plt.show()

# Sentiment part
metrics_path = os.path.join(data_dir, 'text/metrics/metrics.csv')
metrics_data = pd.read_csv(metrics_path)

# Convert date to datetime format
metrics_data['date'] = pd.to_datetime(metrics_data['date'], errors='coerce')

# Drop rows with invalid dates
metrics_data.dropna(subset=['date'], inplace=True)

print("Metrics Data Sample:\n", metrics_data.head())

# Plot Weighted Conviction Over Time
plt.figure(figsize=(12, 6))
plt.plot(metrics_data['date'], metrics_data['weighted conviction'], label='Weighted Conviction', color='blue')
plt.xlabel('Date')
plt.ylabel('Weighted Conviction')
plt.title('Weighted Conviction Over Time')
plt.legend()
plt.show()

# Weighted conviction by sentiment type
metrics_data['sentiment_type'] = metrics_data['weighted conviction'].apply(
    lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Neutral'
)

sentiment_counts = metrics_data['sentiment_type'].value_counts()

plt.figure(figsize=(8, 6))
sentiment_counts.plot(kind='bar', color=['green', 'red', 'grey'])
plt.xlabel('Sentiment Type')
plt.ylabel('Number of Posts/Comments')
plt.title('Weighted Conviction by Sentiment Type')
plt.show()
