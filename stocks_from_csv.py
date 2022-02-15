'''Get Top Stocks from csv file'''

from msilib.schema import Error
import pandas as pd
import logging

csv_filename = 'american_stocks.csv'
    
def get_stock_list(number: int) -> tuple[list[dict], Exception]:
    # Get stock list by decresing daily turnover
    stocks = []
    df = pd.DataFrame()
    columns = ['Ticker', 'Exchange', 'Sector']
    try:
        df = pd.read_csv(csv_filename, usecols=columns, nrows=number)
        df.rename(columns={'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
        for idx, row in df.iterrows():
            stocks.append({"symbol":row["symbol"], "exchange":row["exchange"]})
        logging.info(f'Number of Stocks read from csv: {len(stocks)}')
        return stocks, None
    except Exception as e:
        logging.error(f"Could not get stock list. Error msg:{e}")
        return stocks, e

if __name__ == "__main__":
    stocks, err = get_stock_list(5)
    if err:
        print(err)
        exit()
    print(stocks)