# Script to explore financial data and build models to design trading algorithm
# By Jack Beautz 01/01/21

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from interpret.glassbox import ExplainableBoostingClassifier, LogisticRegression
from interpret import show

from datapull_model_build import daily_master, tickers
#Set time period to base predictions
# i.e. t = 7 will use week before to make prediction for next day.
t = 2

#Create new features which have open, close, delta, and volume of stock for last t days
for ticker in tickers:
    for k in range(1,t+1):
            #daily_master['{}_open_{}'.format(ticker, k)] = daily_master['{}_open'.format(ticker)].shift(k)
            #daily_master['{}_close_{}'.format(ticker, k)] = daily_master['{}_close'.format(ticker)].shift(k)
            daily_master['{}_delta_{}'.format(ticker, k)] = daily_master['{}_delta'.format(ticker)].shift(k)
            #daily_master['{}_vol_{}'.format(ticker, k)] = daily_master['{}_vol'.format(ticker)].shift(k)

#Remove NaN from dataset after creating lag
daily_master = daily_master.dropna()

test_lst = []
train_lst = []
for tick in tickers:
    X = daily_master.drop(['{}_delta'.format(tick), 'date'], axis=1)
    y = daily_master['{}_delta'.format(tick)]>0

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=2)

    ebm = LogisticRegression().fit(X_train, y_train)

    test_lst.append(sum(ebm.predict(X_test)==y_test)/len(y_test))
    train_lst.append(sum(ebm.predict(X_train)==y_train)/len(y_train))


ebm_global = ebm.explain_global()

score_df = pd.DataFrame()
score_df['Stocks'] = tickers
score_df['test_scores'] = test_lst
score_df['train_scores'] = train_lst

plt.bar(score_df['Stocks'],score_df['train_scores'], label='Training', alpha=.6)
plt.bar(score_df['Stocks'],score_df['test_scores'], label='Testing', alpha=.6)
plt.legend()
plt.show()
plt.clf()


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
    MAE_t.append()

    MAE_df[ticker] = MAE(t, daily_master, tickers, lm, ticker)

MAE_df['avg'] = MAE_df.mean(numeric_only=True, axis=1)

plt.plot(range(30), MAE_df['SPY'])
plt.show()
plt.clf()

'''
