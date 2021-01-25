# Script to pull and format financial data to feed backtesting
# By Jack Beautz 01/24/21

from sklearn.linear_model import LogisticRegression
from datapull_model_build import daily_master, tickers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#tickers = ['FANG', 'SLB', 'HES', 'NOV']

tick = 'GOOGL'

X = daily_master.drop(['date'], axis=1)
#DROP ALL DELTAS FOR THAT DAY
for ticker in tickers:
    X = X.drop(['{}_delta'.format(ticker)], axis=1)

y = daily_master['{}_delta'.format(tick)]>0

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=69)

LogReg = LogisticRegression().fit(X_train, y_train)

bt = daily_master
bt['predict'] = list(LogReg.predict(X))

trader = [0]
value = [0]


for day in range(len(bt)):
    delta = list(bt['{}_delta'.format(tick)])[day]
    value.append(value[day] + delta)

    if list(bt['predict'])[day]:
        trader.append(trader[day] + delta)
    else:
        trader.append(trader[day])


bt['trader'] = trader[1:]
bt['value'] = value[1:]

plt.plot(bt['value'], color='blue', label='ACTUAL')
plt.plot(bt['trader'], color = 'red', label='TRADE BOT')
plt.legend()
plt.show()
plt.clf()

print(bt)
