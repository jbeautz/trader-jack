# Script to select stock sets best suited for correlation algorithm
# By Jack Beautz 01/31/20

from stock_picker_methods import model, daily_data, aux_data
import pandas as pd
import random
import numpy as np

#ALL S&P500
all_tickers = pd.read_csv('sandp.csv')['Symbol']

model_results = pd.DataFrame(columns = ['sets', 'result', 'averaging', \
    'vol_cors','open_cors', 'vol_avg1', 'vol_std1', 'vol_avg2', 'vol_std2', \
    'open_avg1', 'open_std1', 'open_avg2', 'open_avg2'])

start_date = '2011-01-03'
end_date = '2021-01-01'



for idx in range(20000):
    this_set = random.sample(list(all_tickers), 2)

    this_result, this_averaging = model(this_set, start_date, end_date)

    this_vol_cor, this_open_cor, vol_stats, open_stats \
        = aux_data(this_set, start_date, end_date)

    this_result = [this_set, this_result, this_averaging, \
        this_vol_cor, this_open_cor]
    this_result.extend(vol_stats)
    this_result.extend(open_stats)

    model_results.loc[len(model_results)] = this_result

    print(idx+1)

print(np.mean(model_results['result']))
print()
model_results.to_csv('results2.csv')
