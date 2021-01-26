# Script to backtest potential trading algorithms
# By Jack Beautz 01/01/21

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA

from datapull_backtest import daily

from model_select import ebm


class compete(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

        buyORsell = ebm.predict(self.I(SMA, close, ))

    def next(self):
        if topCompete(self.sma1, self.sma2):
            self.sell()
        elif topCompete(self.sma2, self.sma1):
            self.buy()


bt = Backtest(daily('2000-01-03', '2020-12-01')['NOV'], compete,
              cash=10000, commission=0,
              exclusive_orders=True)

output = bt.run()
bt.plot()
