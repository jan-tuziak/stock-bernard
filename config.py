av_key = "E6H2MXTA1P7JD4II"

poly_key = "3U413sHUAdFisFvcp6TReoTsEZ_GgpLp"

stocks_filename = "data/stocks.json"

logger = {
        "format":"%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s"
    }

stocks_csv = "data/american_stocks.csv"

num_of_stocks_to_read = 500

#NASDAQ working hours in UTC timezone
market_opening_hour = [14, 30]   #[HOUR, MINUTE]
market_closing_hour = [21, 00]

timeframes = [
    {"multiplier":1, "timespan": "minute"},
    {"multiplier":15, "timespan": "minute"}
]
'''Polygon timeframes definitions:
    - multiplier (int)
    - timespan (string) - minute, hour, day, week, month, quarter, year
'''

criterias_old = [
    {"x_timeframe":timeframes[1], "x_period":300, "y_timeframe":timeframes[1], "y_period":100},
    {"x_timeframe":timeframes[0], "x_period":900, "y_timeframe":timeframes[0], "y_period":300}
]

#Allowed intervals: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'
criterias = [
    {"type":"sma_x > sma_y", "parameters":{"time_period_x":300, "interval_x":"15min", "time_period_y":100, "interval_y":"15min"}},
    {"type":"sma_x > sma_y", "parameters":{"time_period_x":900, "interval_x":"1min", "time_period_y":300, "interval_y":"1min"}}
]

def sma_str(period):
    return f"sma{period}"

def data_str(timeframe):
    return f"data{timeframe['multiplier']}{timeframe['timespan']}"

def criteria_str(criteria):
    return f"sma{criteria['x_period']}x{criteria['x_timeframe']['multiplier']}{criteria['x_timeframe']['timespan']} > sma{criteria['y_period']}x{criteria['y_timeframe']['multiplier']}{criteria['y_timeframe']['timespan']}"
