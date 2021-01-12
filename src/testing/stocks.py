from alpha_vantage.timeseries import TimeSeries
import pprint


key = 'E6H2MXTA1P7JD4II'
ts = TimeSeries(key)

v, v_meta = ts.get_intraday('V', '15min')

print(sorted(list(v.keys()), reverse=True)[0])