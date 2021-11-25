from fastapi.responses import HTMLResponse

def css_style():
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
        width: 80%;
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

def head():
    head = f'''
    <head>
        <title>Money Spyder</title>
        
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <meta name="description" content="Stocks Data Filter App">
        <meta name="author" content="Draxgen">
        
        {css_style()}
    </head>
    '''
    return head

def ui_root():
    html_content = f"""
    <html>
        {head()}
        <body>
            <h1>Money Spyder</h1>
            <h2>Services</h2>
            <a href="/lighthouse" class="button">Lighthouse</a>
            <br><br>
            <h4>Diagnostics</h4>
            <a href="/datastocks" class="diag-button">Stocks Data</a>
            <br><br>
            <a href="/failedsymbols" class="diag-button">Failed Symbols</a>
            <br><br>
            <a href="/executiontime" class="diag-button">Execution Time</a>
            <br><br>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

def ui_common(title, subtitle, body):
    html_content = f"""
    <html>
        {head()}
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

def ui_lighthouse(stocks_to_observe, overview_table_data, sector=""):
    title = "Lighthouse" if len(sector) == 0 else f"Lighthouse - {sector}"
    subtitle = "Stocks to Analyze"
    if len(overview_table_data)==0: 
        table = ""
    else: 
        table = create_overview_table(overview_table_data)

    html_content = f"""
    <html>
        {head()}
        <body>
            <h1>Money Spyder</h1>
            <h2>{title}</h2>
            <h4>{subtitle}</h4>
            <div>{stocks_to_observe}</div>
            <br><br>
            <div>{table}</div>
            <br><br>
            <a href="/" class="button">Back</a>
            <br><br>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

def ui_datastocks(datastocks):
    html_content = ui_common("Stocks Data", "Data acquired and used by Money Spyder", datastocks)
    return HTMLResponse(content=html_content, status_code=200)

def ui_failedsymbols(failed_symbols):
    html_content = ui_common("Failed Symbols", "Symbols for which getting data for resulted in an error", failed_symbols)
    return HTMLResponse(content=html_content, status_code=200)

def ui_executiontime(execute_time):
    html_content = ui_common("Execution Time", "Amount of time Money Spyder took to acquire and analyze given stocks", execute_time)
    return HTMLResponse(content=html_content, status_code=200)

def create_overview_table(overview_table_data):
    table_html = """<table class="overview">
    <tr>
        <th>Symbol</th>
        <th>Name</th>
        <th>Market Cap</th>
        <th>P/E</th>
        <th>Sector</th>
        <th>Exchange</th>
    </tr>"""

    for stock in overview_table_data:
        row_html = f"""
        <tr>
            <td>{stock['symbol']}</td>
            <td>{stock['overview']['Name']}</td>
            <td>{stock['overview']['MarketCapitalization']}</td>
            <td>{stock['overview']['PERatio']}</td>
            <td>{stock['sector']}</td>
            <td>{stock['exchange']}</td>
        </tr>"""
        table_html += row_html

    table_html += "</table>"
    return table_html