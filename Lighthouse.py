import logging

from src.alpha_vantage import AlphaVantageCustomScreener
from src.money_spyder_email import MoneySpyderEmail

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
    #Print App Header
    print(bcolors.HEADER + "Money Spyder's Lighthouse" + bcolors.ENDC)
    # Config logger
    logging.basicConfig(level=logging.INFO)
    
    # Create Alpha Vantage Custom Screener and search for promising stocks
    av = AlphaVantageCustomScreener(debug=True, printToConsole=True)
    av.SearchForStocks()
    
    # Get promising stocks ready for TradingViewList
    stocks_to_observe = av.PrintToTradingViewList()
    
    # Send Email with promising stocks
    ms_email = MoneySpyderEmail(printToConsole=True)
    ms_email.SendLighthouseEmail('jan.tuziak@outlook.com', stocks_to_observe)
