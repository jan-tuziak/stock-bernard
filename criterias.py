'''Add necessary data for stock and assert if it meets the Lighthouse criteria'''

import av_data

def get_evaluated_stock_data(stock:str="GOOGL") -> tuple[dict, Exception]:
    stock_data = {}
    stock_data['sma12xDaily'], err = av_data.get_latest_sma(stock, 'daily', 12)
    if err: return {}, err
    stock_data['sma36xDaily'], err = av_data.get_latest_sma(stock, 'daily', 36)
    if err: return {}, err
    stock_data['sma130xDaily'], err = av_data.get_latest_sma(stock, 'daily', 130)
    if err: return {}, err
    stock_data['smas36xDaily'], err = av_data.get_smas(stock, 'daily', 36, [5])
    if err: return {}, err
    stock_data['smas12xDaily'], err = av_data.get_smas(stock, 'daily', 12, [5])
    if err: return {}, err

    crit1 = stock_data['sma12xDaily'] > stock_data['sma36xDaily']
    crit2 = stock_data['sma12xDaily'] > stock_data['sma130xDaily']
    crit3 = []
    for i in range(len(stock_data['smas36xDaily'])):
        crit3.append(stock_data['smas36xDaily'][i] > stock_data['smas12xDaily'][i])
    crit3 = any(crit3)

    stock_data['lighthouse_long'] = crit1 and crit2 and crit3
    stock_data['lighthouse_short'] = not crit1 and not crit2 and not crit3

    return stock_data, None

