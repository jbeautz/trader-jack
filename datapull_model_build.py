# Script to pull and format financial data to aid in model selection
# By Jack Beautz 01/01/21

from yahoofinancials import YahooFinancials
import pandas as pd
import matplotlib.pyplot as plt


# Select Tickers and stock history dates

#ALL S&P500
#tickers = pd.read_csv('sandp.csv')['Symbol']

#Software
tickers = ['MSFT', 'AAPL']

#LIFE INSURANCE
#tickers = ['FANG', 'SLB', 'HES', 'NOV']

#ENERGY
#tickers = ['XOM', 'CVX', 'RDS.A', 'RDS.B']

#CARS
#tickers = ['TM', 'F', 'HMC', 'GM']

#INSURANCE
#tickers = ['ALL', 'PGR', 'TRV', 'MET']

#RANDOM
#tickers = ['DE', 'NFLX', 'MET', 'XOM']


freq = 'daily'
start_date = '2020-01-03'
end_date = '2021-01-27'


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

for ticker in tickers:
    try:
        financial[ticker] = YahooFinancials(ticker)
        tick = financial[ticker].get_historical_price_data(start_date, end_date, freq)[ticker]['prices']
        tick = pd.DataFrame(clean_stock_data(tick))[['formatted_date','open','close']]
        tick = tick.rename(columns={'formatted_date': 'date', 'close': f'{ticker}_close', \
            'open': f'{ticker}_open'})
        daily[ticker] = tick.set_index('date')
    except:
        print(ticker)
        fails.append(ticker)

# Join into one daily master dataset
daily_master = pd.DataFrame()
delta_master = pd.DataFrame()

tickers = [tick for tick in tickers if tick not in fails]

for ticker in tickers:
    daily_master = daily_master.merge(daily[ticker], how='outer', left_index=True, right_index=True)
    delta_master[f'{ticker}_delta'] = daily_master[f'{ticker}_close']-daily_master[f'{ticker}_open']
    delta_master[f'{ticker}_open'] = daily_master[f'{ticker}_open']


#Reset Index so that we can create a lag
daily_master = delta_master.reset_index()


#Set time period to base predictions
# i.e. t = 7 will use week before to make prediction for next day.
t = 2

#Create new features which have open, close, delta, and volume of stock for last t days
for ticker in tickers:
    for k in range(1,t+1):
            #daily_master['{}_open_{}'.format(ticker, k)] = daily_master['{}_open'.format(ticker)].shift(k)
            #daily_master['{}_close_{}'.format(ticker, k)] = daily_master['{}_close'.format(ticker)].shift(k)
            daily_master[f'{ticker}_delta_{k}'] = daily_master[f'{ticker}_delta'].shift(k)
            #daily_master['{}_vol_{}'.format(ticker, k)] = daily_master['{}_vol'.format(ticker)].shift(k)

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
