import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
TSLA_2=pd.read_csv("Tesla 15th oct 2024- 5th nov 2024.csv")
print(TSLA_2.head())
TSLA_3=pd.read_csv("TSLA_period3.csv")
TSLA_2.columns = TSLA_2.columns.str.strip()
sma2=TSLA_2['Close'].mean()
print(f"The SMA for period 2 is: {sma2}")

# Calculate the Exponential Moving Average (EMA)
ema2 = TSLA_2['Close'].ewm(span=20, adjust=False).mean()

# Print the last few EMA values
print(f"The last few EMA values for period 2 are: \n{ema2.head()}")
TSLA_3.columns = TSLA_3.columns.str.strip()
sma3=TSLA_3['Close'].mean()
print(f"The SMA for period 3 is: {sma3}")

# Calculate the Exponential Moving Average (EMA)
ema3 = TSLA_3['Close'].ewm(span=20, adjust=False).mean()

# Print the last few EMA values
print(f"The last few EMA values for period 3 are: \n{ema3.head()}")
