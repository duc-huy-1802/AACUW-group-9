import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
TSLA_2=pd.read_csv("Tesla 15th oct 2024- 5th nov 2024.csv")
TSLA_2.head()
sma2=TSLA_2['Close'].mean()
print(f"The SMA for period 2 is: {sma2}")

# Calculate the Exponential Moving Average (EMA)
ema2 = TSLA_2['Close'].ewm(span=20, adjust=False).mean()

# Print the last few EMA values
print(f"The last few EMA values for period 2 are: \n{ema2.head()}")

