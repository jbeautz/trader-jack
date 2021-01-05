# Script to explore financial data and build models to design trading algorithm
# By Jack Beautz 01/01/21

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from datapull import daily_master, tickers

#Set time period to base predictions
# i.e. t = 7 will use week before to make prediction for next day.
t = 2

for ticker in tickers:
    for k in range(1,t+1):
            daily_master['{}_open_{}'.format(ticker, k)] = daily_master['{}_open'.format(ticker)].shift(k)
            daily_master['{}_close_{}'.format(ticker, k)] = daily_master['{}_close'.format(ticker)].shift(k)
            daily_master['{}_delta_{}'.format(ticker, k)] = daily_master['{}_delta'.format(ticker)].shift(k)

daily_master = daily_master.drop(index=range(t))
daily_master = daily_master.dropna()

X = daily_master.drop(['DE_close','DE_delta', 'date'], axis=1)
y = daily_master['SPY_delta']

print(y)
print(sum(y), len(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=14)


#LogisticRegression(random_state=14).fit(X_train, y_train)
