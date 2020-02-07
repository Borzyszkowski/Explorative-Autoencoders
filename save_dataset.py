
from alpha_vantage.timeseries import TimeSeries
#save the company whole time stock prices into csv
def save_dataset(symbol):
    api_key = 'UYC4Z4XMXL3ZYO9I'    #place your onw key here!!!

    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol, outputsize='full')

    data.to_csv(f'./{symbol}_daily.csv')

#sample usage
#save_dataset('MSFT')