import os
import psycopg2
import logging

import criterias

DATABASE_URL = os.environ['DATABASE_URL']
STOCK_LIST_TABLE_NAME = 'ms_stock_list'
STOCKS_DATA_TABLE_NAME = 'ms_stocks_data'
DIAG_TABLE_NAME = 'ms_diagnostics'

def _connect():
    err = None
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
    except Exception as e:
        err = e
        logging.error(f"Could not connect to database. Error msg: {err}")
    return conn, cur, err

def _disconnect(conn, cur) -> None:
    cur.close()
    conn.close()

def _get_stock_list(cur) -> tuple[list[dict], Exception]:
    try:
        cur.execute(f'SELECT * FROM {STOCK_LIST_TABLE_NAME}')
        data = cur.fetchall()
        stocks = []
        for row in data:
            stocks.append({'exchange':row[1], 'symbol':row[2]})
        return stocks, None
    except Exception as e:
        logging.error(f'Could not get stock list from database. Error msg: {e}')
        return [], e

def _add_evaluated_stocks_data_to_db(stocks_data:list[dict]) -> Exception:
    err = None
    conn, cur, err = _connect()
    if err: 
        return err
    try:
        # Execute a command: this creates a new table
        cur.execute(f"CREATE TABLE IF NOT EXISTS {STOCKS_DATA_TABLE_NAME} (ID serial PRIMARY KEY, EXCHANGE varchar, SYMBOL varchar, SMA12xDAILY varchar, SMA36xDAILY varchar, SMA130xDAILY varchar, SMAS36xDAILY varchar, SMAS12xDAILY varchar, LIGHTHOUSE_LONG bool, LIGHTHOUSE_SHORT bool);")
        cur.execute(f"DELETE FROM {STOCKS_DATA_TABLE_NAME};")
        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no more SQL injections!)
        values_str = []
        for std in stocks_data:
            # values_str.append(f"('{std['exchange']}', '{std['symbol']}')")
            values_str.append(f"('{std['exchange']}', '{std['symbol']}', '{str(std['sma12xDaily'])}', '{str(std['sma36xDaily'])}', '{str(std['sma130xDaily'])}', '{str(std['smas36xDaily'])}', '{str(std['smas12xDaily'])}', '{str(std['lighthouse_long'])}', '{str(std['lighthouse_short'])}')")
        values_str = ", ".join(values_str)
        # for st_data in stocks_data:
        cur.execute(f"INSERT INTO {STOCKS_DATA_TABLE_NAME} (EXCHANGE, SYMBOL, SMA12xDAILY, SMA36xDAILY, SMA130xDAILY, SMAS36xDAILY, SMAS12xDAILY, LIGHTHOUSE_LONG, LIGHTHOUSE_SHORT) VALUES {values_str}")
        # Make the changes to the database persistent
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Could not add stocks data to database. Error msg: {e}")
        err = e
    _disconnect(conn, cur)
    return err

def _get_diagnostics_from_db(cur) -> tuple[str, Exception]:
    try:
        cur.execute(f'SELECT * FROM {DIAG_TABLE_NAME}')
        data = cur.fetchall()
        return data, None
    except Exception as e:
        logging.error(f'Could not get diagnostics data from database. Error msg: {e}')
        return '', e

def _add_failed_stocks_to_db(failed_stocks:list[dict]) -> Exception:
    err = None
    conn, cur, err = _connect()
    if err: 
        return err
    try:
        # Execute a command: this creates a new table
        cur.execute(f"CREATE TABLE IF NOT EXISTS {DIAG_TABLE_NAME} (ID serial PRIMARY KEY, DIAG_NAME varchar, DIAG_VALUE varchar);")
        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no more SQL injections!)
        failed_stocks_str = []
        for fs in failed_stocks:
            failed_stocks_str.append(f"{fs['exchange']}:{fs['symbol']}")
        failed_stocks_str = ", ".join(failed_stocks_str)
        cur.execute(f"DELETE FROM {DIAG_TABLE_NAME} WHERE DIAG_NAME = 'failed_symbols';")
        cur.execute(f"INSERT INTO {DIAG_TABLE_NAME} (DIAG_NAME, DIAG_VALUE) VALUES (%s, %s);", ("failed_symbols", failed_stocks_str))
        # Make the changes to the database persistent
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Could not add failed stocks data to database. Error msg: {e}")
        err = e
    _disconnect(conn, cur)
    return err

def _get_lighthouse_results(long:bool=True) -> tuple[list[dict], Exception]:
    if long:
        col_name = 'LIGHTHOUSE_LONG'
    else:
        col_name = 'LIGHTHOUSE_SHORT'
    err = None
    data = []
    data_dict = []
    conn, cur, err = _connect()
    if err: 
        return {}, err
    try:
        cur.execute(f'SELECT (EXCHANGE, SYMBOL) FROM {STOCKS_DATA_TABLE_NAME} WHERE {col_name} = true')
        data = cur.fetchall()
        for row in data:
            row_str = str(row[0])
            row_lst = list(map(str, row_str.split(',')))
            for i in range(len(row_lst)):
                row_lst[i] = row_lst[i].replace("(", "")
                row_lst[i] = row_lst[i].replace(")", "")
            # data_dict.append(f'{row_lst[0]}:{row_lst[1]}')
            data_dict.append({
                'exchange': row_lst[0],
                'symbol': row_lst[1]
            })
    except Exception as e:
        logging.error(f'Could not get {col_name} results from database. Error msg: {e}')
        err = e
    _disconnect(conn, cur)
    return data_dict, err

def add_stock_list(stocks:list[dict]) -> Exception:
    err = None
    conn, cur, err = _connect()
    if err: 
        return err
    try:
        # Execute a command: this creates a new table
        cur.execute(f"CREATE TABLE IF NOT EXISTS {STOCK_LIST_TABLE_NAME} (ID serial PRIMARY KEY, exchange varchar, symbol varchar);")
        cur.execute(f"DELETE FROM {STOCK_LIST_TABLE_NAME};")
        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no more SQL injections!)
        # for stock in stocks:
        values_str = []
        for st in stocks:
            values_str.append(f"('{st['exchange']}', '{st['symbol']}')")
        values_str = ", ".join(values_str)
        cur.execute(f"INSERT INTO {STOCK_LIST_TABLE_NAME} (exchange, symbol) VALUES {values_str}")
        # Make the changes to the database persistent
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Could not add stock list to database. Error msg: {e}")
        err = e
    _disconnect(conn, cur)
    return err

def add_stock_parameters() -> Exception:
    '''Add necessary stock data (parameters) to database'''
    last_symbol = ''
    conn, cur, err = _connect()
    if err: 
        return err
    try:
        pass
        # get stock list
        stocks,err = _get_stock_list(cur)
        if err:
            return err
        # for each stock get stock data
        stocks_data = []
        failed_stocks = []
        for stock in stocks:
            stock_data, err = criterias.get_evaluated_stock_data(stock['symbol'])
            if err:
                failed_stocks.append(stock)
                continue
            stocks_data.append(stock | stock_data)
        # save evaluated stocks to database
        err = _add_evaluated_stocks_data_to_db(stocks_data)
        if err:
            return err
        err = _add_failed_stocks_to_db(failed_stocks)
    except Exception as e:
        conn.rollback()
        logging.error(f"Could not add stock data to database for symbol {last_symbol}. Error msg: {e}")
    _disconnect(conn, cur)
    return None

def add_execution_time(executionTimeStr:str) -> Exception:
    err = None
    conn, cur, err = _connect()
    if err: 
        return err
    try:
        # Execute a command: this creates a new table
        cur.execute(f"CREATE TABLE IF NOT EXISTS {DIAG_TABLE_NAME} (ID serial PRIMARY KEY, DIAG_NAME varchar, DIAG_VALUE varchar);")
        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no more SQL injections!)
        cur.execute(f"DELETE FROM {DIAG_TABLE_NAME} WHERE DIAG_NAME = 'dh_execution_time';")
        cur.execute(f"INSERT INTO {DIAG_TABLE_NAME} (DIAG_NAME, DIAG_VALUE) VALUES (%s, %s);", ("dh_execution_time", executionTimeStr))
        # Make the changes to the database persistent
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Could not add DH execution time to database. Error msg: {e}")
        err = e
    _disconnect(conn, cur)
    return err

def get_lighthouse_long_results() -> tuple[list[dict], Exception]:
    return _get_lighthouse_results(True)

def get_lighthouse_short_results() -> tuple[list[dict], Exception]:
    return _get_lighthouse_results(False)

if __name__ == "__main__":
    #pass
    # GET LIGHTHOUSE RESULTS
    data, err = get_lighthouse_short_results()
    if err:
        exit()
    print(data)

    # GET STOCK LIST TEST
    # conn, cur, err = _connect()
    # if err: 
    #     exit()
    # stocks, err = _get_stock_list(cur)
    # print(stocks)
    # _disconnect(conn, cur)
    


    # # ADD AND GET FAILED SYMBOLS TEST
    # failedsymbols = [
    #     {'exchange':'NYSE', 'symbol':'AAPL'},
    #     {'exchange':'NYSE', 'symbol':'GOOGL'},
    #     {'exchange':'NASDAQ', 'symbol':'MSFT'},
    #     {'exchange':'aaa', 'symbol':'bbb'}
    # ]
    # _add_failed_stocks_to_db(failedsymbols)
    # err = None
    # conn, cur, err = _connect()
    # if err: 
    #     exit()
    # try:
    #     data, err = _get_diagnostics_from_db(cur)
    #     print(data)
    # except Exception as e:
    #     conn.rollback()
    #     logging.error(f"ERROR. Error msg: {e}")
    #     err = e
    # _disconnect(conn, cur)

    
    # # ADD AND GET EXECUTION TIME TEST
    # err = None
    # err = add_execution_time("00:00:00")
    # if err:
    #     exit()
    # conn, cur, err = _connect()
    # if err: 
    #     exit()
    # try:
    #     data, err = _get_diagnostics_from_db(cur)
    #     print(data)
    # except Exception as e:
    #     conn.rollback()
    #     logging.error(f"ERROR. Error msg: {e}")
    #     err = e
    # _disconnect(conn, cur)