from pybit import spot
import pandas as pd
import ta
api_key = ''
api_secret =''
session =spot.HTTP(endpoint="https://api.bybit.com",api_key='',api_secret ='')
def klines(symbol):
    kline = session.query_kline(symbol =symbol,interval="1h")
    kline =kline["result"]
    df=pd.DataFrame(kline)

    return kline
klines('BTCUSDT')
print(klines('BTCUSDT'))
order=session.place_active_order(symbol='BTCUSDT',side='Buy',type='MARKET',qty=10,timInForce="GTC")
print(order)
