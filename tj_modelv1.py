# Model to select stock most-likely to increase on
#   given day
# By Jack Beautz 8/30/21

import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np

#def lgmodel(today_data, tickers):

# First, open the API connection
api = tradeapi.REST(
    'PKONN73J1ZJN9R8DSMOJ',
    'Cq4OVqETPhEwBMwyk4kQ4eoMF1fu9ho76F70R2jX',
    'https://paper-api.alpaca.markets', api_version='v2'
)

account = api.get_account()

tickers = ['FB', 'GOOG']
rows = 1000

raw_data = api.get_barset(tickers, 'day', limit=rows)

df_list = []
cols = []

# Cleans historical data
for tick in tickers:
    for day in range(rows):
        this_day = vars(raw_data[tick][day])['_raw']
        for key in this_day.keys():
            df_list.append(this_day[key])

labels=list(this_day.keys())
cols = []

for tick in tickers:
    for l in labels:
        cols.append(f'{tick}_{l}')

c = len(this_day.keys())*2
r = 1000

df_list = np.reshape(df_list, (r, c))
df = pd.DataFrame(df_list, columns=cols)

for tick in tickers:
    df = df.drop(f'{tick}_t', axis=1)

for tick in tickers:
    df[f'{tick}_t'] = df[f'{tick}_c'].shift(-1)

df = df.dropna()
