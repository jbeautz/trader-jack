# Model to select stock most-likely to increase on
#   given day
# By Jack Beautz 8/30/21

import alpaca_trade_api as tradeapi
import pandas as pd

#def lgmodel(today_data, tickers):

# First, open the API connection
api = tradeapi.REST(
    'PKONN73J1ZJN9R8DSMOJ',
    'Cq4OVqETPhEwBMwyk4kQ4eoMF1fu9ho76F70R2jX',
    'https://paper-api.alpaca.markets', api_version='v2'
)

account = api.get_account()

raw_data = api.get_barset(tickers, 'day', limit=1000)

df = pd.Dataframe()

# Cleans historical data
for tick in tickers:
    for day in range(2,1000):
        for d in range(1,3):
            this_day = vars(raw_hist_data[tick][day])['_raw']
            for key in this_day.keys():
                df[f'{tick}_{key}_{day-d}'] = this_day[key]

print(df)
