import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

class MyStrategy(bt.Strategy):
    params = dict(period=20)

    def __init__(self):

        sma = btind.SimpleMovingAverage(self.datas[0], period=self.params.period)

    ...

cerebro = bt.Cerebro()

...

data = btfeeds.MyFeed(...)
cerebro.adddata(data)

...

cerebro.addstrategy(MyStrategy, period=30)

...