# Script to pull and format financial data to feed backtesting
# By Jack Beautz 01/24/21

from sklearn.linear_model import LogisticRegression
from datapull_model_build import daily_master, tickers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

n= .5
X = daily_master.drop(['date'], axis=1)
bt = daily_master

#DROP ALL DELTAS FOR THAT DAY
for ticker in tickers:
    X = X.drop([f'{ticker}_delta'], axis=1)

for tick in tickers:
    y = daily_master[f'{tick}_delta']> 0 #-daily_master[f'{tick}_open']*.0

    X_train, y_train = X[:int(n*len(X))], y[:int(n*len(X))]

    LogReg = LogisticRegression(max_iter=100000).fit(X_train, y_train)

    bt[f'{tick}_predict'] = LogReg.predict_proba(X)[:,1]


trader = [1000]
value = [1000]



for day in range(int(len(bt)*n), len(bt)):
    delta = 0
    dollar = 1000/len(tickers)
    for tick in tickers:
        open = list(bt[f'{tick}_open'])[day]
        delta += list(bt[f'{tick}_delta'])[day]*dollar/open
    value.append(value[day-int(len(bt)*n)] + delta)

    max_prob = 0
    tdelta = 0

    for tick in tickers:
        prob = list(bt[f'{tick}_predict'])[day]
        open = list(bt[f'{tick}_open'])[day]
        if prob>=max_prob and prob>.5:
            tdelta = list(bt[f'{tick}_delta'])[day]*1000/open
            max_prob = list(bt[f'{tick}_predict'])[day]
    trader.append(trader[day-int(len(bt)*n)] + tdelta)


plt.plot(value[int(n*len(X)):], color='blue', label='ACTUAL')
plt.plot(trader[int(n*len(X)):], color = 'red', label='TRADE BOT')
plt.hlines(trader[-1], color = 'red', xmin=0, xmax=int((1-n)*len(bt)), linestyles='dashed')
plt.hlines(value[-1], color='blue', xmin=0, xmax=int((1-n)*len(bt)), linestyles='dashed')
plt.legend()
plt.show()
plt.clf()

print(bt)
