# Script to pull and format financial data to feed backtesting
# By Jack Beautz 01/24/21

from sklearn.linear_model import LogisticRegression
from datapull_model_build import daily_master, tickers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

n= int(.80 * len(daily_master))
m = len(daily_master) - n

X = daily_master.drop(['date'], axis=1)

bt = X[n:]

#DROP ALL DELTAS FOR THAT DAY
for ticker in tickers:
    X = X.drop([f'{ticker}_delta'], axis=1)

X1 = X[:n]
X2 = X[n:]


for tick in tickers:
    y = daily_master[f'{tick}_delta'][:n]> 0 #daily_master[f'{tick}_open'][:n]*.025

    LogReg = LogisticRegression(max_iter=100000).fit(X1, y)

    bt[f'{tick}_predict'] = LogReg.predict_proba(X2)[:,1]


trader = [1000]
value = [1000]

cnt_right_guess = 0
cnt_beat_actual = 0


for day in range(len(bt)):
    print(f"DAY {day}")
    print()
    delta = 0
    dollar = 1000/len(tickers)
    max_tick = tickers[0]
    max_delta = -10000
    for tick in tickers:
        if list(bt[f'{tick}_delta'])[day] > max_delta:
            max_tick = tick
        open = list(bt[f'{tick}_open'])[day]
        delta += list(bt[f'{tick}_delta'])[day]*dollar/open
        print(f"ACTUAL: Buying ${dollar} of of {tick}")
        print(f"        Resulting in change of {list(bt[f'{tick}_delta'])[day]*dollar/open}")
    print()
    print(f"ACTUAL: Day {day} : Daily Change {delta}")
    print()
    print()
    value.append(value[day] + delta)

    max_prob = 0
    tdelta = 0
    max_prob_tick = ""


    for tick in tickers:
        prob = list(bt[f'{tick}_predict'])[day]
        open = list(bt[f'{tick}_open'])[day]
        if prob>=max_prob and prob>.5:
            tdelta = list(bt[f'{tick}_delta'])[day]*1000/open
            max_prob = list(bt[f'{tick}_predict'])[day]
            max_prob_tick = tick
    print(f"TRADER: Buying $1000 of Best stock pick ({max_tick}) with probability ({np.round(max_prob,4)}) of increase")
    print(f"TRADER: Day {day}: Daily Change {tdelta}")
    print()
    print()
    trader.append(trader[day] + tdelta)
    if max_prob_tick == max_tick:
        cnt_right_guess += 1
    if tdelta >= delta:
        cnt_beat_actual += 1


bt['trader'] = trader[1:]
bt['value'] = value[1:]

print(f"Bot beats average: {np.round(cnt_beat_actual/m*100, 2)}%")
print(f"Bot guesses best stock: {np.round(cnt_right_guess/m*100, 2)}%")

print()

print()

print(f"Bot gives {np.round((trader[-1]-1000)/10, 2)}% return over {len(trader)-1} trading days")
print(f"Averagings gives {np.round((value[-1]-1000)/10, 2)}% return over {len(trader)-1} trading days")

plt.plot(trader, color = 'red', label='TRADER JACK')
plt.plot(value, color='blue', label='AVERAGING')
plt.hlines(trader[-1], color = 'red', xmin=0, xmax=m, linestyles='dashed')
plt.hlines(value[-1], color='blue', xmin=0, xmax=m, linestyles='dashed')
plt.legend()
plt.show()
plt.clf()
