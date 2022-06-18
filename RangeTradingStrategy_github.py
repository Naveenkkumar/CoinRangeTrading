import pandas as pd
#import python-binance
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from IPython.display import display
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.stats import norm
import statistics as sts
from plyer import notification
import time
import numpy as np

# Connecting to Binance
api_key = 'your api key'
api_secret = 'your secret code'
client = Client(api_key, api_secret)
#data_coins = client.get_all_tickers()
#print(data_coins)

'''
data_coins_all = pd.json_normalize(data_coins)
all_symbols = data_coins_all['symbol']
all_USDT_pairs = all_symbols[all_symbols.str.endswith('USDT')] ##342 pairs currently
all_USDT_pairs = all_USDT_pairs.reset_index()
all_USDT_pairs = all_USDT_pairs['symbol']
print('All USDT pairs',len(all_USDT_pairs))
'''


def find_relevant_pairs():
    '''Not_trading_pairs = ['AAVEDOWNUSDT','AAVEUPUSDT','BCCUSDT','VENUSDT','PAXUSDT','BCHABCUSDT','BCHSVUSDT','USDSUSDT','USDSBUSDT','ERDUSDT','NPXSUSDT','STORMUSDT','HCUSDT','MCOUSDT','BULLUSDT','BEARUSDT','ETHBULLUSDT','ETHBEARUSDT','EOSBULLUSDT','EOSBEARUSDT','XRPBULLUSDT','XRPBEARUSDT','STRATUSDT','BNBBULLUSDT','BNBBEARUSDT','XZCUSDT','LENDUSDT','BKRWUSDT','DAIUSDT']
    Not_trading_pairs = pd.Series(Not_trading_pairs)
    print('lenght of Not trading pairs',len(Not_trading_pairs))
    
    
    all_USDT_pairs1 = all_USDT_pairs
    all_USDT_pairs_trading = all_USDT_pairs1[~all_USDT_pairs1.isin(Not_trading_pairs)]
    print('All USDT pairs trading', len(all_USDT_pairs_trading))
    '''

    # These are enough volume pairs
    all_USDT_pairs_trading = ['DOTUSDT']
                              ''','XRPUSDT','ETHUSDT','BTCUSDT','ADAUSDT','MATICUSDT','ATOMUSDT','LTCUSDT','LINKUSDT','1INCHUSDT','IOTXUSDT','SOLUSDT','BNBUSDT'
                              ,'ONEUSDT','GRTUSDT','DATAUSDT','COTIUSDT','UNIUSDT','RUNEUSDT','CHESSUSDT','MANAUSDT','FTMUSDT','LUNAUSDT','SANDUSDT','GALAUSDT'
                              ,'AVAXUSDT','CRVUSDT','FILUSDT','YFIUSDT','ROSEUSDT','ALGOUSDT','AXSUSDT','THETAUSDT','ENJUSDT','AAVEUSDT','FTTUSDT','DASHUSDT'
                              ,'RENUSDT','CHZUSDT','ICPUSDT']'''
    all_USDT_pairs_trading = pd.Series(all_USDT_pairs_trading)
    '''for i in Not_trading_pairs:
        indexx = pd.Index(all_USDT_pairs_trading).get_loc(i)
        #print(indexx)
        all_USDT_pairs_trading = all_USDT_pairs_trading.drop(index = indexx)
        all_USDT_pairs_trading = all_USDT_pairs_trading.reset_index()
        all_USDT_pairs_trading = all_USDT_pairs_trading['symbol']'''

    
    #print(all_USDT_pairs_trading.to_string())
    return all_USDT_pairs_trading


relevant_pairs = find_relevant_pairs()

def rangetrading():

    #currentprice = relevant_data2['Close'].iloc(-1)
    ghigherextreme = relevant_data2['Close'].max()
    glowerextreme =  relevant_data2['Close'].min()

    i = len(relevant_data2['Close'])
    list = []
    j= 1
    all_ranges = np.array(list)
    for i in range(len(relevant_data2['Close']), 0, -30):
        print(f'{j}th interval')
        interval_end = i
        print('interval end',interval_end)
        interval_start = interval_end-30
        
        interval_values = relevant_data2['Close'].iloc[interval_start : interval_end]
        print('interval values',interval_values)
        higherextreme = float(interval_values.max())
        lowerextreme =  float(interval_values.min())
        value_range = higherextreme-lowerextreme
        print('Value range', value_range)
        all_ranges = np.append(all_ranges, values = value_range)
        j += 1
        #i = i-30

    print('all ranges',all_ranges)
    all_ranges = np.sort(all_ranges, axis = 0)
    all_ranges_new = all_ranges[:len(all_ranges)-1]
    #print(all_ranges)
    #print(all_ranges_new)
    mean_ranges = np.mean(all_ranges_new)
    print('mean of ranges',mean_ranges)
    max_range = np.max(all_ranges)

    if max_range > mean_ranges*(2) :
        print('Pair is not in range')

    else:
        print('Pair is in range')
        notification.notify(title = title, message = message, app_icon = None, timeout=20, toast = False)


#rangetrading()

    

# Get data for the known pair
## Setting up start time and end time
end_time = datetime.today()  # 
end_timestamp = int(end_time.timestamp()*1000)
#start_time = end_time - timedelta(hours=75, minutes=0) #getting data for last 3 days and 3 hours
start_time = end_time - timedelta(hours=25, minutes=0)
start_timestamp = int(start_time.timestamp()*1000)
j = 0
for j in range(0, len(relevant_pairs)):
    title = relevant_pairs.iloc[j] + ' Coin is in Range'
    message = 'Hurry! Hurry! First condition of this pair is satisfied, look into the chart quickly.'
            
    data = client.get_klines(symbol = relevant_pairs.iloc[j], interval ='5m', startTime = start_timestamp, endTime = end_timestamp, limit = 1000)
    data_formated = pd.DataFrame(data, columns = ['Open time','Open','High','Low','Close','Volume','Close Time','Quote Asset Volume','Number of Trades','junk1','junk2','junk3'])
    relevant_data = data_formated[['Open','High','Low','Close','Volume']]

    #Calculating SMA(Simple Moving Averages)
    sma = relevant_data['Close'].rolling(15).mean()
    sma1 = sma.rename('15sma')

    #print(type(sma))
    relevant_data2 = pd.concat([relevant_data, sma1], axis = 1)
    #interval_values = relevant_data2['Close'].loc[30 : 60]
    #print(len(relevant_data2['Close'])-1)
    #print(relevant_data2.to_string())
    print('Length of relevant pairs', len(relevant_pairs))
    print('Current pair index', j)
    print('Pair:',relevant_pairs.iloc[j])
    rangetrading()
    

print('Checked all pairs')
        
         




        
        

        

    
    


            

