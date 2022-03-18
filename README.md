# Stock Bernard
 
Technical S&P500 EOD stocks screener. This app aims to fill in the gap of TradingView's built-in screener, which is very sparce when it comes to technical rules. Stock Bernard focues on those technical rules. 

## Example
Stock Bernard can give you a list of S&P500 stocks that meet ALL of these rules:
- `sma12xDaily > sma36xDaily`
- `sma12xDaily > sma130xDaily`
- `smas36xDaily > smas12xDaily 5 candles earlier`
