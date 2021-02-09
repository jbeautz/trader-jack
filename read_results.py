# Script to interpret results from stock_picker.property
# By Jack Beautz on 02/01/21

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.inspection import plot_partial_dependence


df = pd.read_csv('results2.csv')

LogReg = LogisticRegression(max_iter = 10000)
RF = RandomForestClassifier(max_depth=4)

X = df.drop(columns=['result', 'sets', 'averaging'])
y = df['result'] > df['averaging']
y = y & df['result']>0

n = int(len(X)*.85)

X_train, X_test = X[:n], X[n:]
y_train, y_test = y[:n], y[n:]

LogReg_model = LogReg.fit(X_train, y_train)
RF_model = RF.fit(X_train, y_train)

print("Logistic Train: ", np.round(LogReg_model.score(X_train,y_train),2))
print("Logistic Test: ", np.round(LogReg_model.score(X_test,y_test), 2))

print()

print("RF Train: ", np.round(RF_model.score(X_train,y_train), 2))
print("RF Test: ", np.round(RF_model.score(X_test,y_test), 2))

print(X.columns)
print(RF_model.feature_importances_)
print(LogReg_model)

plot_partial_dependence(LogReg_model, X, X.columns)
plt.show()

'''
print(df)

sns.jointplot(df['open_avgs'], df['results'], kind='reg')
plt.show()
plt.show()
'''
