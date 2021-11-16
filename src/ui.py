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

        <link rel="stylesheet" href="css/styles.css?v=1.0">
        
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

def ui_lighthouse(stocks_to_observe):
    html_content = ui_common("Lighthouse", "Stocks to Analyze", stocks_to_observe)
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