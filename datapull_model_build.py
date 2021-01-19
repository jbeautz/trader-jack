# Script to pull and format financial data to aid in model selection
# By Jack Beautz 01/01/21

from yahoofinancials import YahooFinancials
import pandas as pd
import matplotlib.pyplot as plt


# Select Tickers and stock history dates

tickers = pd.read_csv('sandp.csv')
#tickers = ['AAPL', 'MSFT','FB','AMZN', 'SPY', 'DOW']
freq = 'daily'
start_date = '2020-10-03'
end_date = '2021-01-15'


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
fails = []

for ticker in tickers['Symbol']:
    try:
        financial[ticker] = YahooFinancials(ticker)
        tick = financial[ticker].get_historical_price_data(start_date, end_date, freq)[ticker]['prices']
        tick = pd.DataFrame(clean_stock_data(tick))[['formatted_date','open','close']]
        tick = tick.rename(columns={'formatted_date': 'date', 'close': '{}_close'.format(ticker), \
            'open': '{}_open'.format(ticker)})
        daily[ticker] = tick.set_index('date')
    except:
        print(ticker)
        fails.append(ticker)

# Join into one daily master dataset
daily_master = pd.DataFrame()
delta_master = pd.DataFrame()

tickers['Symbol'] = [tick for tick in tickers['Symbol'] if tick not in fails]

for ticker in tickers['Symbol']:
    daily_master = daily_master.merge(daily[ticker], how='outer', left_index=True, right_index=True)
    delta_master['{}_delta'.format(ticker)] = daily_master['{}_close'.format(ticker)]-daily_master['{}_open'.format(ticker)]

#Reset Index so that we can create a lag
daily_master = delta_master.reset_index()

#Create 1 Day Lag Feature
for ticker in tickers['Symbol']:
    daily_master['{}_delta_1'.format(ticker)] = daily_master['{}_delta'.format(ticker)].shift(1)
    daily_master['{}_delta_2'.format(ticker)] = daily_master['{}_delta'.format(ticker)].shift(2)

#Remove NaN from dataset after creating lag
daily_master = daily_master.dropna()





'''
plt.plot(daily_master['date'],daily_master[['DE_open', 'DE_close']])
plt.show()
plt.clf()

# Plot correlation heat map of feature set
sns.heatmap(data=daily_master.corr())

plt.show()
plt.clf()
'''
