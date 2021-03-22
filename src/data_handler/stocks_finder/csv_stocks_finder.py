'''Get Top Stocks from csv file'''

from src.data_handler.stocks_finder.i_stocks_finder import IStocksFinder

class CSVStocksFinder(IStocksFinder):
    def __init__(self, csv_path):
        # self.main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # self.csv_path = os.path.join(self.main_dir, config.stocks_csv)
        self.csv_path = csv_path
    
    def get_top_stocks_by_daily_turnover(self, number):
        #logging.info(f'Getting stocks from {config.stocks_csv}')
        stocks = []
        df = pd.DataFrame()
        columns = ['Ticker', 'Exchange']
        df = pd.read_csv(self.csv_path, usecols=columns, nrows=number)
        df.rename(columns={'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
        for idx, row in df.iterrows():
            stocks.append({"symbol":row["symbol"], "exchange":row["exchange"]})
        logging.info(f'Number of Stocks read from csv: {len(stocks)}')
        del df
        return stocks