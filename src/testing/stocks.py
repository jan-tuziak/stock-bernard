import requests
import json

functions = {
    'hourly': 'TIME_SERIES_INTRADAY&interval=60min',
    'daily': 'TIME_SERIES_DAILY',
    'weekly': 'TIME_SERIES_WEEKLY'
}

site = 'www.alphavantage.co'
key = 'ICWCMQTW2MFNXIOS'
ticker = 'MSFT'
# hourly - https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=60min&outputsize=full&apikey=ICWCMQTW2MFNXIOS
# daily - https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=ICWCMQTW2MFNXIOS
# weekly - https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=MSFT&outputsize=full&apikey=ICWCMQTW2MFNXIOS

query = 'https://%s/query?function=%s&symbol=%s&outputsize=full&apikey=%s' % (
    site, functions['daily'], ticker, key)

response = requests.get(query)
data = json.loads(response.text)

print(data)