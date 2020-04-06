
# coding: utf-8

# # Backtest Template

# 주요 라이브러리를 import합니다.

# In[3]:


# import libraries

import pandas as pd
# import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt


# 10년 국채 일자별 데이터파일(.csv)을 dataframe으로 로드합니다.

# In[4]:


#data = web.DataReader("AAPL", "yahoo", start, end)
data = pd.read_csv("./data/daily/lktb.csv", index_col=0, parse_dates=True)


# In[5]:


data = data[['CLOSE']]
data.columns = ['LKTB']
data = data.tz_localize('UTC')
data.tail()


# In[6]:


start = datetime.datetime(2012,1,1)
end = datetime.datetime(2019,12,31)

data = data[start:end]


# In[7]:


data


# In[8]:


from zipline.api import order_target, record, symbol, set_commission, commission, set_slippage, slippage


# In[9]:


import zipline


# In[10]:


def initialize(context):
    context.i = 0
    context.sym = symbol('LKTB')
    context.hold = False
    set_commission(commission.PerShare(cost=0.000008))
    set_slippage(slippage.FixedSlippage(spread=0))


# In[11]:


def handle_data(context, data):
    context.i += 1
    if context.i < 20:
        return
    
    buy = False
    sell = False
    
    ma5 = data.history(context.sym, 'price', 5, '1d').mean()
    ma20 = data.history(context.sym, 'price', 20, '1d').mean()
    
    if ma5 > ma20 and context.hold == False:
        order_target(context.sym, 100)
        context.hold = True
        buy = True
    elif ma5 < ma20 and context.hold == True:
        order_target(context.sym, -100)
        context.hold = False
        sell = True
        
    record(LKTB=data.current(context.sym, "price"), ma5=ma5, ma20=ma20, buy=buy, sell=sell)


# In[12]:


# from zipline.algorithm import TradingAlgorithm


# In[13]:


from trading_calendars import get_calendar
trading_calendar=get_calendar('XKRX')


# In[14]:


from zipline import run_algorithm

start = datetime.datetime(2012, 1, 2)
end = datetime.datetime(2019,12,30)

start_utc = start.replace(tzinfo = datetime.timezone.utc)
end_utc = end.replace(tzinfo = datetime.timezone.utc)

result = run_algorithm(
    start = start_utc, 
    end = end_utc, 
    initialize = initialize, 
    capital_base = 1000, 
    handle_data = handle_data, 
    trading_calendar=trading_calendar,
    data = data
)


# In[15]:


start_utc


# In[16]:


'''
from zipline.utils.factory import create_simulation_parameters
algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data, trading_calendar=trading_calendar)
# algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(data)
'''


# In[17]:


plt.plot(result.index, result.portfolio_value)
plt.show()


# In[18]:


result.info()


# In[19]:


plt.plot(result.index, result.LKTB)
plt.plot(result.index, result.ma5)
plt.plot(result.index, result.ma20)

plt.legend(loc='best')

plt.plot(result[result.buy == True].index, result.LKTB[result.buy == True], '^')
plt.plot(result[result.sell == True].index, result.LKTB[result.sell == True], 'v')
plt.show()


# In[20]:


result[['starting_cash', 'ending_cash', 'ending_value', 'portfolio_value', 'LKTB', 'capital_used']].head(50)


# In[21]:


result.tail()


# In[23]:


import pyfolio as pf


# In[24]:


returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(result)


# In[25]:


pf.plot_drawdown_periods(returns, top=5).set_xlabel('Date')


# In[26]:


transactions


# In[27]:


#pf.create_simple_tear_sheet(returns, positions=positions, transactions=transactions, live_start_date='2019-02-10')
#pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions, live_start_date='2019-02-10', round_trips=True)
#pf.create_simple_tear_sheet(returns, positions=positions, transactions=transactions,live_start_date='2019-02-10')
sheets = pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions)


# In[ ]:


sheets


# In[ ]:



returns.shape


# In[ ]:


returns.head()


# In[ ]:


type(returns)


# In[ ]:


returns.index = returns.index.date


# In[ ]:


returns


# In[ ]:


#pf.create_simple_tear_sheet(returns, positions=positions, transactions=transactions, live_start_date='2019-02-10')
pf.create_simple_tear_sheet(returns)

