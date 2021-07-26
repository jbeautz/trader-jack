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

#while True:
tickers = ['FB','GOOG']

raw_hist_data = api.get_barset(tickers, 'day', limit=2)
hist_data = {}
for tick in tickers:
    for day in [0,1]:
        this_day = vars(raw_hist_data[tick][day])['_raw']
        for key in this_day.keys():
            hist_data[f'{tick}_{key}_{day}'] = this_day[key]

print(hist_data)

'''

# Calculate Dollar Amount Available to each trade remaining
total = float(account.equity)
print(total)
quant = total/len(stocks)
# Submit a market order to buy 1 share of each stock
for ticker in stocks:
    api.submit_order(
        symbol=ticker,
        notional=quant,
        side='buy',
        type='market',
        time_in_force='day'
    )


    # Code waits 24 hours to repeat
    #time.sleep(60*60*24)
'''
