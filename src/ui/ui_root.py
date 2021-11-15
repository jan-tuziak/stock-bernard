from fastapi.responses import HTMLResponse

def ui_root():
    html_content = """
    <html>
        <head>
            <title>Money Spyder</title>
        </head>
        <body>
            <h1>Money Spyder</h1>
            <h3>Services</h3>
            <a href="/lighthouse">Lighthouse</a>
            <br><br>
            <h3>Diagnostics</h3>
            <a href="/datastocks">Stocks Data</a>
            <br>
            <a href="/failedsymbols">Failed Symbols</a>
            <br>
            <a href="/executiontime">Execution Time</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)