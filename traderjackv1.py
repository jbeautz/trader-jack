# A Real-time Simulated Trading Version of Trader Jack bot on
# Alpaca's paper trading simulation
# By Jack Beautz 03/27/21

import alpaca_trade_api as tradeapi
import pandas as pd
import datetime

# First, open the API connection
api = tradeapi.REST(
    'PKONN73J1ZJN9R8DSMOJ',
    'Cq4OVqETPhEwBMwyk4kQ4eoMF1fu9ho76F70R2jX',
    'https://paper-api.alpaca.markets', api_version='v2'
)

account = api.get_account()


# Version 1 will chose between trading on Facebook and Google stock
tickers = ['FB','GOOG']


# Loop occurs once every 24 hours until program is stopped
#while True:

# Get raw historical data from alpaca api
raw_hist_data = api.get_barset(tickers, 'day', limit=2)

# Create new dictionary for cleaned and shaped data row for day
hist_data = {}

# Cleans historical data
for tick in tickers:
    for day in [0,1]:
        this_day = vars(raw_hist_data[tick][day])['_raw']
        for key in this_day.keys():
            hist_data[f'{tick}_{key}_{day}'] = this_day[key]

# Plugs todays data into model
todays_stock = lgmodel(hist_data)

# Find current portfolio value
total = float(account.equity)

if yesterdays_stock is not null:
    api.submit_order(
        symbol=yesterdays_stock,
        notional=total,
        side='sell',
        type='market',
        time_in_force='day'
    )

if todays_stock is not null:
    api.submit_order(
        symbol=todays_stock,
        notional=quant,
        side='buy',
        type='market',
        time_in_force='day'
    )

yesterdays_stock = todays_stock

# Code waits 24 hours to repeat
#time.sleep(60*60*24)
