import pandas
import requests
import json
import time

# f = open('stock_data.csv')

df = pandas.read_csv('stock_names.csv', encoding='ISO-8859-1')
print(df)
stocks = df.iloc[:, 0].values.tolist()
cols = ['Symbol', 'open', 'high', 'low', 'volume', 'close']
# result_df = pandas.DataFrame(columns=cols)
useful_keys = ['symbol', 'open', 'high', 'preMarket', 'volume', 'close', 'low']
dict_list = []
for idx, name in enumerate(stocks):
    if idx > 350:
        break
    result = requests.get(
        "https://api.polygon.io/v1/open-close/{}/2020-10-14?unadjusted=true&apiKey=Tm1gd7o0zNMQBXBVemdd6uQls4JprGDH".format(
            name))
    time.sleep(13)
    data = result.json()
    if result.status_code != 200 or not all(k in data for k in useful_keys):
        continue
    close_val = 1 if data['open'] < data['close'] else 0
    dict_list.append(
        {'symbol': data['symbol'], 'open': data['open'] / data['preMarket'], 'high': data['high'] / data['open'],
         'low': data['low'] / data['open'],
         'volume': data['volume'], 'close': close_val})
result_df = pandas.DataFrame(dict_list)
result_df.to_csv('stock_data.csv')
