av_key = "44V1UXEX9HBN0RST"

json_path = "data/stocks.json"

execute_time_path = "data/execute_time.json"

failed_symbols_path = "data/failed_symbols.json"

csv_path = "data/american_stocks.csv"

num_of_stocks_to_read = 1000

logger = {
        "format":"%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s"
    }

#Data Handler working hours in UTC timezone
dh_opening_hour = [0, 00]   #[HOUR, MINUTE]
dh_closing_hour = [1, 00]

#Allowed intervals: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'
criterias = [
    {"type":"sma_x > sma_y", "parameters":{"time_period_x":12, "interval_x":"daily", "time_period_y":36, "interval_y":"daily"}},
    {"type":"sma_x > sma_y", "parameters":{"time_period_x":12, "interval_x":"daily", "time_period_y":130, "interval_y":"daily"}},
    {"type":"sma_x > sma_y 1inMany", "parameters":{"time_period_x":36, "interval_x":"daily", "time_period_y":12, "interval_y":"daily", "lookback":[5]}}
]
