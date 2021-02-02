av_key = "E6H2MXTA1P7JD4II"

poly_key = "3U413sHUAdFisFvcp6TReoTsEZ_GgpLp"

stocks_filename = "data/stocks.json"

logger = {
        "format":"%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s"
    }

stocks_csv = "american_stocks.csv"

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

criterias = [
    {"x_timeframe":timeframes[1], "x_period":300, "y_timeframe":timeframes[1], "y_period":100},
    {"x_timeframe":timeframes[0], "x_period":900, "y_timeframe":timeframes[0], "y_period":300}
]

def sma_str(period):
    return f"sma{period}"

def data_str(timeframe):
    return f"data{timeframe['multiplier']}{timeframe['timespan']}"

def criteria_str(criteria):
    return f"sma{criteria['x_period']}x{criteria['x_timeframe']['multiplier']}{criteria['x_timeframe']['timespan']} > sma{criteria['y_period']}x{criteria['y_timeframe']['multiplier']}{criteria['y_timeframe']['timespan']}"
