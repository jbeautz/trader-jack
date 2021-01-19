# Script to explore financial data and build models to design trading algorithm
# By Jack Beautz 01/01/21

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from interpret.glassbox import ExplainableBoostingClassifier, ClassificationTree, LinearRegression,LogisticRegression
from interpret import show

from sklearn.metrics import confusion_matrix

from datapull_model_build import daily_master, tickers

test_lst = []
train_lst = []
for tick in tickers:
    X = daily_master.drop('date', axis=1)
    for ticker in tickers:
        X = X.drop('{}_delta'.format(ticker), axis=1)
    y = daily_master['{}_delta'.format(tick)]>abs(daily_master['{}_delta_1'.format(tick)] )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=2)

    ebm = LogisticRegression().fit(X_train, y_train)
    test_lst.append(sum(ebm.predict(X_test)==y_test)/len(y_test))
    train_lst.append(sum(ebm.predict(X_train)==y_train)/len(y_train))
    '''
    test_lst.append(sum(abs((ebm.predict(X_test)-y_test))))
    train_lst.append(sum(abs(ebm.predict(X_train)==y_train)))
    '''
    print(confusion_matrix(y_test, ebm.predict(X_test)))


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
