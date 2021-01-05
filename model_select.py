# Script to explore financial data and build models to design trading algorithm
# By Jack Beautz 01/01/21

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split

from datapull import daily_master, tickers
'''
#Set time period to base predictions
# i.e. t = 7 will use week before to make prediction for next day.
t = 2

for ticker in tickers:
    for k in range(1,t+1):
            daily_master['{}_open_{}'.format(ticker, k)] = daily_master['{}_open'.format(ticker)].shift(k)
            daily_master['{}_close_{}'.format(ticker, k)] = daily_master['{}_close'.format(ticker)].shift(k)
            daily_master['{}_delta_{}'.format(ticker, k)] = daily_master['{}_delta'.format(ticker)].shift(k)
            daily_master['{}_vol_{}'.format(ticker, k)] = daily_master['{}_vol'.format(ticker)].shift(k)


daily_master = daily_master.drop(index=range(t))
daily_master = daily_master.dropna()

X = daily_master.drop(['CORN_close','CORN_delta', 'date'], axis=1)
y = daily_master['CORN_delta']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=14)

print(sum(y), len(y))

lm = LinearRegression().fit(X_train, y_train)


plt.hist([np.array(lm.predict(X_test))- np.array(y_test)])
plt.show()
plt.clf()

print('MAE: ', sum(abs(np.array(logm.predict(X_test))- np.array(y_test))))
'''

def MAE(t, daily_master, tickers, mod, tick):
    for ticker in tickers:
        for k in range(1,t+1):
                daily_master['{}_open_{}'.format(ticker, k)] = daily_master['{}_open'.format(ticker)].shift(k)
                daily_master['{}_close_{}'.format(ticker, k)] = daily_master['{}_close'.format(ticker)].shift(k)
                daily_master['{}_delta_{}'.format(ticker, k)] = daily_master['{}_delta'.format(ticker)].shift(k)
                daily_master['{}_vol_{}'.format(ticker, k)] = daily_master['{}_vol'.format(ticker)].shift(k)


    daily_master = daily_master.drop(index=range(t))
    daily_master = daily_master.dropna()

    X = daily_master.drop(['{}_close'.format(tick),'{}_delta'.format(tick), 'date'], axis=1)
    y = daily_master['{}_close'.format(tick)]


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=14)

    mod = mod.fit(X_train, y_train)

    return sum(abs(np.array(mod.predict(X_test))- np.array(y_test)))


lm = LinearRegression()

MAE_df = pd.DataFrame()

for ticker in tickers:
    MAE_t = []
    for t in range(30):
        MAE_t.append(MAE(t, daily_master, tickers, lm, ticker))

    MAE_df[ticker] = MAE_t

MAE_df['avg'] = MAE_df.mean(numeric_only=True, axis=1)

plt.plot(range(30), MAE_df['SPY'])
plt.show()
plt.clf()
