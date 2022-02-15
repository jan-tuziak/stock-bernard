from fastapi.responses import HTMLResponse

def _css_style() -> str:
    css = '''
    <style>
    body  {
        text-align: center;
        font-family: Consolas;
    }

    .button {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 12px;
    }

    .diag-button {
        background-color: #A9A9A9; /* Grey */
        border: none;
        color: white;
        padding: 12px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        border-radius: 12px;
    }

    div {
        white-space: pre-wrap;
    }   

    /* Table Styling */
    .overview {
        border-collapse: collapse;
        width: 5%;
        margin-left: auto;
        margin-right: auto;
    }

    .overview td, .overview th {
        border: 1px solid #ddd;
        padding: 8px;
    }

    .overview tr:nth-child(even){background-color: #f2f2f2;}

    .overview tr:hover {background-color: #ddd;}

    .overview th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #4CAF50;
        color: white;
    }

    </style>
    '''
    return css

def _head() -> str:
    head = f'''
    <head>
        <title>Money Spyder</title>
        
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <meta name="description" content="Stocks Data Filter App">
        <meta name="author" content="Draxgen">
        
        {_css_style()}
    </head>
    '''
    return head

def _string_for_tradingview(stocks:list[dict]) -> str:
    if len(stocks) == 0:
        return ""
    tv_list = []
    for st in stocks:
        sym = st['symbol']
        exch = st['exchange']
        #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as part of "AMEX" exchange
        if exch == 'NYSE ARCA': exch = 'AMEX'
        tv_list.append(f"{exch}:{sym}")
    return ", ".join(tv_list)

def _create_stocks_table(stocks:list[dict]) -> str:
    if len(stocks) == 0:
        return ""
    table_html = """<table class="overview">
    <tr>
        <th>#</th>
        <th>Exchange</th>
        <th>Symbol</th>
    </tr>"""
    num = 1
    for stock in stocks:
        row_html = f"""
        <tr>
            <td>{num}</td>
            <td>{stock.get('exchange')}</td>
            <td>{stock.get('symbol')}</td>
        </tr>"""
        table_html += row_html
        num+=1
    table_html += "</table>"
    return table_html

def root() -> HTMLResponse:
    #Removed Diagnostics Menu
    # <h4>Diagnostics</h4>
    # <a href="/datastocks" class="diag-button">Stocks Data</a>
    # <br><br>
    # <a href="/failedsymbols" class="diag-button">Failed Symbols</a>
    # <br><br>
    # <a href="/executiontime" class="diag-button">Execution Time</a>
    # <br><br>
    
    html_content = f"""
    <html>
        {_head()}
        <body>
            <h1>Money Spyder</h1>
            <h2>Services</h2>
            <a href="/lighthouse_long" class="button">Lighthouse Long</a>
            <br><br>
            <a href="/lighthouse_short" class="button">Lighthouse Short</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

def common(title:str, subtitle:str, body:str) -> str:
    html_content = f"""
    <html>
        {_head()}
        <body>
            <h1>Money Spyder</h1>
            <h2>{title}</h2>
            <h4>{subtitle}</h4>
            <div>{body}</div>
            <br><br>
            <a href="/" class="button">Back</a>
            <br><br>
        </body>
    </html>
    """
    return html_content

def lighthouse(stocks:list[dict], long:bool=True) -> HTMLResponse:
    if long:
        title = "Lighthouse Long"
    else:
        title = "Lighthouse Short"
    subtitle = f"{len(stocks)} Stocks found"
    
    str_for_tv = _string_for_tradingview(stocks)
    table = _create_stocks_table(stocks)

    html_content = f"""
    <html>
        {_head()}
        <body>
            <h1>Money Spyder</h1>
            <h2>{title}</h2>
            <h4>{subtitle}</h4>
            <div>{str_for_tv}</div>
            <br><br>
            <div>{table}</div>
            <br><br>
            <a href="/" class="button">Back</a>
            <br><br>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

def datastocks(datastocks):
    html_content = common("Stocks Data", "Data acquired and used by Money Spyder", datastocks)
    return HTMLResponse(content=html_content, status_code=200)

def failedsymbols(failed_symbols):
    html_content = common("Failed Symbols", "Symbols for which getting data for resulted in an error", failed_symbols)
    return HTMLResponse(content=html_content, status_code=200)

def executiontime(execute_time):
    html_content = common("Execution Time", "Amount of time Money Spyder took to acquire and analyze given stocks", execute_time)
    return HTMLResponse(content=html_content, status_code=200)

def error(err:Exception) -> HTMLResponse:
    html_content = common("Error Occurred!", "Sorry, something went wrong", err)
    return HTMLResponse(content=html_content, status_code=404)