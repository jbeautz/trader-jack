# Script to find sets of correlated stocks in s&p500
# By Jack Beautz 01/17/21

import pandas as pd
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt
import random
import numpy as np
from datapull_model_build import delta_master, tickers

cor = []
sets = []

theset = []
themax = 0
for i in range(1000000):
    set = random.sample(list(tickers['Symbol']), 4)
    sets.append(set)
    d = pd.DataFrame()
    for ticker in set:
        d[ticker] = delta_master['{}_delta'.format(ticker)]
    thiscor = np.mean(np.mean(abs(d.corr())))
    cor.append(thiscor)
    if thiscor > themax:
        theset = set
        themax = thiscor



ind = np.argpartition(cor, -10)[-10:]
for i in in d:
    print(sets[i])
    print(cor[i])
    print()
