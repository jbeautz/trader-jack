# Script to select stock sets best suited for correlation algorithm
# By Jack Beautz 01/31/20

from stock_picker_methods import model, daily_data, aux_data
import pandas as pd
import random
import numpy as np

#ALL S&P500
all_tickers = pd.read_csv('sandp.csv')['Symbol']

model_results = pd.DataFrame(columns = ['sets', 'results', 'vol_cors', \
    'open_cors', 'vol_avgs', 'open_avgs'])

start_date = '2011-01-03'
end_date = '2021-01-27'



for idx in range(10):
    this_set = random.sample(list(all_tickers), 2)

    this_result = model(this_set, start_date, end_date)

    this_vol_cor, this_open_cor, this_vol_avg, this_open_avg \
        = aux_data(this_set, start_date, end_date)

    this_result = {'sets':this_set, 'results':this_result, 'vol_cors':this_vol_cor, \
        'open_cors':this_open_cor, 'vol_avgs':this_vol_avg, 'open_avgs':this_open_avg}

    model_results = model_results.append(this_result, ignore_index=True)

print(model_results)
