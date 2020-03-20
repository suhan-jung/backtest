# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:33:55 2020

@author: infomax
"""
# import zipline
import matplotlib
matplotlib.use('Qt5Agg')
# import matplotlib.pyplot as plt

# %matplotlib qt5

import eikon as ek

ek.set_app_key('8ee143628de84818a8b12f4f55be35674e136d08')
df_eikon = ek.get_timeseries(["KRW="],
                             fields="*",
                             start_date="2015-01-01",
                             end_date = "2020-01-11",
                             interval = "daily"
                            )
data = df_eikon[['CLOSE']]
data.columns = ["KRW"]
data = data.tz_localize("UTC")

def initialize(context):
    pass

from zipline.api import order, symbol

def handle_data(context, data):
    order(symbol('KRW'), 1)
    
from zipline.algorithm import TradingAlgorithm
algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(data)

import cufflinks as cf  # Cufflinks
import configparser as cp
cf.set_config_file(offline=True)  # set the plotting mode to offline
result.portfolio_value.iplot(kind='line')

from plotly.offline import plot
import plotly.graph_objs as go

fig = go.Figure(data=[
        go.Line(x=result.index,
                y=result.portfolio_value)
        ])
# fig = go.Figure(data=[{'type': 'scatter', 'y': [2, 1, 4]}])
plot(fig)


import matplotlib.pyplot as plt
plt.plot(result.index, result.portfolio_value)
plt.show()