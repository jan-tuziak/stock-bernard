import requests
import json
import logging
import csv

functions = {
    'list': 'LISTING_STATUS',
    '1min-ly': 'TIME_SERIES_INTRADAY&interval=1min',
    'hourly': 'TIME_SERIES_INTRADAY&interval=60min',
    'daily': 'TIME_SERIES_DAILY',
    'weekly': 'TIME_SERIES_WEEKLY'
}

site = 'www.alphavantage.co'
key = 'B451TTOLQ2VOY99L'
ticker = 'MSFT'
# hourly - https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=60min&outputsize=full&apikey=ICWCMQTW2MFNXIOS
# daily - https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=ICWCMQTW2MFNXIOS
# weekly - https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=MSFT&outputsize=full&apikey=ICWCMQTW2MFNXIOS

query = 'https://%s/query?function=%s&symbol=%s&outputsize=full&apikey=%s' % (
    site, functions['list'], ticker, key)

response = requests.get(query)
#data = json.loads(response.text)

#stocks_list = response.text.split('\r\n')
# headers = stocks_list.pop(0)
# headers = headers.split(',')
# print(headers)
# print(stocks_list[0])
# stocks = []

# for s in stocks_list:
#     elements = s.split(',')
#     stocks.append(
#         {
#             headers
#         }
#     )

with open('stocks.csv', 'w') as f:
    f.write(response.text)



with open("stocks.csv", "r") as f:
    reader = csv.DictReader(f)
    a = list(reader)



# reader = csv.DictReader(response.text, delimiter=',')
# a = list(reader)
for one in a:
    print(one)