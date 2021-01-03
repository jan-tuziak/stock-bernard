import logging

from src.av_stocks_data import AVStocksData
from src.money_spyder_email import MoneySpyderEmail

if __name__ == "__main__":
    # Config logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
    #Print App Header
    logging.info("Money Spyder's Lighthouse starting.")
    
    # get list of stocks
    av = AVStocksData()
    av.get_stocks(min_daily_turnover=2000000)
    
    # Create TradingViewList String from stocks
    stocks_to_observe = av.get_tv_list()
    
    # Send Email with promising stocks
    mse = MoneySpyderEmail()
    mse.send_lh_email('jan.tuziak@outlook.com', stocks_to_observe)
