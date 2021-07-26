# Methods for stock_picker.py
# By Jack Beautz 01/31/21

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
from yahoofinancials import YahooFinancials
import pandas as pd

# A function which returns algorithm performance on a set
def model(tickers, start_date, end_date):

    daily_master = daily_data(tickers, start_date, end_date)

    n= int(.80 * len(daily_master))
    m = len(daily_master) - n

    X = daily_master.drop(['date'], axis=1)

    bt = X[n:]

    #DROP ALL DELTAS FOR THAT DAY
    for ticker in tickers:
        X = X.drop([f'{ticker}_delta'], axis=1)

    X1 = X[:n]
    X2 = X[n:]


    for tick in tickers:
        y = daily_master[f'{tick}_delta'][:n]> 0 #daily_master[f'{tick}_open'][:n]*.025
        LogReg = LogisticRegression(max_iter=100000).fit(X1, y)

        bt[f'{tick}_predict'] = LogReg.predict_proba(X2)[:,1]

    trader = [1000]
    value = [1000]

    cnt_right_guess = 0
    cnt_beat_actual = 0


    for day in range(len(bt)):
        delta = 0
        dollar = 1000/len(tickers)
        max_tick = tickers[0]
        max_delta = -10000
        for tick in tickers:
            if list(bt[f'{tick}_delta'])[day] > max_delta:
                max_tick = tick
            open = list(bt[f'{tick}_open'])[day]
            delta += list(bt[f'{tick}_delta'])[day]*dollar/open

        value.append(value[day] + delta)

        max_prob = 0
        tdelta = 0
        max_prob_tick = ""


        for tick in tickers:
            prob = list(bt[f'{tick}_predict'])[day]
            open = list(bt[f'{tick}_open'])[day]
            if prob>=max_prob and prob>.5:
                max_prob = prob
                max_prob_tick = tick

            if len(max_prob_tick)>0:
                tdelta = list(bt[f'{max_prob_tick}_delta'])[day]*1000/open


        trader.append(trader[day] + tdelta)
        if max_prob_tick == max_tick:
            cnt_right_guess += 1
        if tdelta >= delta:
            cnt_beat_actual += 1

    trader_return = np.round((trader[-1]-1000)/10, 2)
    averaging_return = np.round((value[-1]-1000)/10, 2)
    return trader_return, averaging_return

# Function to clean data extracts
def clean_stock_data(stock_data_list):
    new_list = []
    for rec in stock_data_list:
        if 'type' not in rec.keys():
            new_list.append(rec)
    return new_list


def daily_data(tickers, start_date, end_date):
    freq = 'daily'

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
                daily_master[f'{ticker}_delta_{k}'] = daily_master[f'{ticker}_delta'].shift(k)

    #Remove NaN from dataset after creating lag and return
    return daily_master.dropna()



# Retrieves data to feed the model
def aux_data(tickers, start_date, end_date):
        freq = 'daily'

        # Construct yahoo financials objects for data extraction
        financial = {}
        aux_daily = {}

        for ticker in tickers:
            financial[ticker] = YahooFinancials(ticker)
            tick = financial[ticker].get_historical_price_data(start_date, end_date, freq)[ticker]['prices']
            tick = pd.DataFrame(clean_stock_data(tick))[['volume','open']]
            aux_daily[ticker] = tick.rename(columns={'open': f'{ticker}_open', \
                'volume': f'{ticker}_volume'})

        # Join into one daily master dataset
        aux = pd.DataFrame()

        for ticker in tickers:
            aux = aux.merge(aux_daily[ticker], how='outer', left_index=True, right_index=True)

        #Find correlation between opening price of pair
        vols = pd.DataFrame()
        opens = pd.DataFrame()

        vol_dict = {}
        open_dict = {}

        for ticker in tickers:
            vols[ticker] = aux[f'{ticker}_volume']

            vol_dict[f'{ticker}_std'] = np.std(aux[f'{ticker}_volume'])
            vol_dict[f'{ticker}_avg'] = np.mean(aux[f'{ticker}_volume'])

        vol_cor = np.mean(np.mean(vols.corr()))

        aux_data = [vol_cor, list(vol_dict.values())]

        return aux_data
