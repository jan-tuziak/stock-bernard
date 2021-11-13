av_key = "44V1UXEX9HBN0RST"

poly_key = "3U413sHUAdFisFvcp6TReoTsEZ_GgpLp"

json_path = "data/stocks.json"

csv_path = "data/american_stocks.csv"

num_of_stocks_to_read = 500

logger = {
        "format":"%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s"
    }

#Data Handler working hours in UTC timezone
dh_opening_hour = [0, 00]   #[HOUR, MINUTE]
dh_closing_hour = [1, 00]

#Allowed intervals: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'
criterias = [
    {"type":"sma_x > sma_y", "parameters":{"time_period_x":300, "interval_x":"15min", "time_period_y":900, "interval_y":"15min"}},
    {"type":"sma_x > sma_y", "parameters":{"time_period_x":300, "interval_x":"15min", "time_period_y":130, "interval_y":"daily"}},
    {"type":"sma_x > sma_y 1inMany", "parameters":{"time_period_x":900, "interval_x":"15min", "time_period_y":300, "interval_y":"15min", "lookback":[50,100,150,200]}}
    
]