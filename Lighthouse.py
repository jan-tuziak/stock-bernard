import logging

from src.alpha_vantage import AlphaVantageCustomScreener
from src.money_spyder_email import MoneySpyderEmail

if __name__ == "__main__":
    # Config logger
    logging.basicConfig(level=logging.INFO)
    
    # Create Alpha Vantage Custom Screener and search for promising stocks
    av = AlphaVantageCustomScreener(debug=True)
    av.SearchForStocks()
    
    # Get promising stocks ready for TradingViewList
    stocks_to_observe = av.PrintToTradingViewList()
    
    # Send Email with promising stocks
    ms_email = MoneySpyderEmail()
    ms_email.SendLighthouseEmail('jan.tuziak@outlook.com', stocks_to_observe)
