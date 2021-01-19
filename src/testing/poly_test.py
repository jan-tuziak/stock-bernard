import time
#from polygon import WebSocketClient, STOCKS_CLUSTER
import requests
import pandas as pd
import json
import datetime
import pytz
import dateutil


key = '3U413sHUAdFisFvcp6TReoTsEZ_GgpLp'
response = requests.get('https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/minute/2021-01-10/2021-01-14?unadjusted=true&sort=desc&limit=10000&apiKey=3U413sHUAdFisFvcp6TReoTsEZ_GgpLp')
data = json.loads(response.text)

# close_list = [d['c'] for d in data['results']]
# vol_list = [d['v'] for d in data['results']]
# t_list = [d['t'] for d in data['results']]

# new_t_list = [datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S') for ts in t_list]

# print(close_list)

opening_hours = datetime.time(9, 30)
closing_hours = datetime.time(16, 00)

T_CONST = 1610585940000
date1 = datetime.datetime.utcfromtimestamp(T_CONST/1000) - datetime.timedelta(hours=5) #Subtract 5 hours from UTC for Eastern Time    #.strftime('%Y-%m-%d %H:%M:%S')
#date2 = datetime.utcfromtimestamp(T_CONST/1000).astimezone(dateutil.tz.gettz('US/Eastern'))#.strftime('%Y-%m-%d %H:%M:%S')
#print(date1.time())
date2 = date1 - datetime.timedelta(hours=9)
print(date1)
print(date2)

print(date1.time() >= opening_hours and date1.time() <= closing_hours)
print(date2.time() >= opening_hours and date2.time() <= closing_hours)

df = pd.DataFrame(data['results'])

for idx,row in df.iterrows():
    df.at[idx, 'date_time'] = datetime.datetime.utcfromtimestamp(row['t']/1000) - datetime.timedelta(hours=5) #.astimezone(dateutil.tz.gettz('US/Eastern'))#.strftime('%Y-%m-%d %H:%M:%S')

print()

# print(df[df.t_str.str.contains('2021-01-11')])
#print(df[df['o'] == 128.67])
#print( df[ df['o'] == 129.01 & df['c'] == 129.11 ] )
#print( df[ df['o'] == 129.01 ] )
#print( df[ df['c'] == 129.11 ] )

idx_rem = []
for idx, row in df.iterrows():
    if row['date_time'].time() >= opening_hours and row['date_time'].time() <= closing_hours: continue
    idx_rem.append(idx)
df.drop(idx_rem, inplace=True)
#print(df[ df['datetime'] >= opening_hours & df['datetime'] <= closing_hours ] )
#print(df)
start_date = datetime.datetime(2021, 1, 12, 0, 0, 0)
end_date = datetime.datetime(2021, 1, 12, 23, 59, 59)
mask = (df['date_time'] > start_date) & (df['date_time'] <= end_date)
print(df.loc[mask])
