# Script to pull and format financial data to feed trading algorithm
# By Jack Beautz 01/01/21

from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Select Tickers and stock history dates
tickers = ['CANE','SOYB','CORN', 'DE', 'CNHI','CAT','AGCO', 'BRFS', 'TSN','TSLA', 'ADM', 'FPI', 'CB', 'BRF','SPY']
freq = 'daily'
start_date = '2010-10-01'
end_date = '2020-01-01'


# Function to clean data extracts
def clean_stock_data(stock_data_list):
    new_list = []
    for rec in stock_data_list:
        if 'type' not in rec.keys():
            new_list.append(rec)
    return new_list

# Construct yahoo financials objects for data extraction
financial = {}
daily = {}

for ticker in tickers:
    financial[ticker] = YahooFinancials(ticker)
    tick = financial[ticker].get_historical_price_data(start_date, end_date, freq)[ticker]['prices']
    tick = pd.DataFrame(clean_stock_data(tick))[['formatted_date','open','adjclose']]
    tick = tick.rename(columns={'formatted_date': 'date', 'adjclose': '{}_close'.format(ticker), 'open': '{}_open'.format(ticker)})
    daily[ticker] = tick.set_index('date')


# Join into one daily master dataset
daily_master = pd.DataFrame()
delta_master = pd.DataFrame()

for ticker in tickers:
    daily_master = daily_master.merge(daily[ticker], how='outer', left_index=True, right_index=True)
    daily_master['{}_delta'.format(ticker)] = daily_master['{}_close'.format(ticker)]-daily_master['{}_open'.format(ticker)]

'''
# Plot correlation heat map of feature set
sns.heatmap(data=daily_master.corr())

plt.show()
plt.clf()
'''
