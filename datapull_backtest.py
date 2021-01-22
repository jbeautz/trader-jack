# Script to pull and format financial data to feed backtesting
# By Jack Beautz 01/01/21

from yahoofinancials import YahooFinancials
import pandas as pd
import matplotlib.pyplot as plt


# Select Tickers and stock history dates

tickers = ['FANG', 'SLB', 'HES', 'NOV']

def daily(start_date, end_date):
    #tickers = ['AAPL', 'MSFT','FB','AMZN', 'SPY', 'DOW']
    freq = 'daily'


    # Function to clean data extracts
    def clean_stock_data(stock_data_list):
        new_list = []
        for rec in stock_data_list:
            if 'type' not in rec.keys():
                new_list.append(rec)
        return new_list


    # Construct yahoo financials objects for data extraction
    financial = {}
    d = {}

    for ticker in tickers:
        financial[ticker] = YahooFinancials(ticker)
        tick = financial[ticker].get_historical_price_data(start_date, end_date, freq)[ticker]['prices']
        tick = pd.DataFrame(clean_stock_data(tick))[['formatted_date','open','close', 'low','high']]
        tick = tick.rename(columns={'formatted_date': 'Date', 'close': 'Close', \
            'open': 'Open', 'low': 'Low', 'high': 'High'})
        tick['Datetime'] = pd.to_datetime(tick['Date'])
        d[ticker] = tick.set_index('Datetime')

    return d

df = daily('2000-01-03', '2020-12-01')

for ticker in tickers:
    plt.plot(df[ticker]['High'])


plt.show()
plt.clf()
