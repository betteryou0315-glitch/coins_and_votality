#주제: 여러 코인 간 가격 상관관계 & 변동성 분석
import pandas as pd
import ccxt
import matplotlib.pyplot as plt
import seaborn as sns

exchange = ccxt.binance()

symbols = ['BTC/USDT' , 'ETH/USDT' , 'XRP/USDT']
timeframe = '1d'
limit = 365

close = {}
for symbol in symbols:
    ohlcv = exchange.fetch_ohlcv(symbol , timeframe , limit=limit)
    df = pd.DataFrame(ohlcv , columns=['timestamp' , 'open' , 'high' , 'low' , 'close' , 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'] , unit='ms' , utc=True).dt.tz_convert("Asia/Seoul")
    close[symbol] = df['close']

close_df = pd.DataFrame(close)

close_change = close_df.pct_change() #일별 수익률

close_corr = close_change.corr() #corr 매서드는 상관관계를 나타내준다

close_std = close_change.std()

print(close_std)
print(close_corr)

sns.barplot(x=close_std.index , y=close_std.values)
plt.show()


#============정리=========================
#상관관계: BTC , ETH , XRP 모두 0.8 이상으로 양의 상관관계 -> 방향성은 비슷하게 움직인다 
#상관관계가 높게 나온 이유는 모두 비트코인을 중심으로 따라가려는 경향이 있는 것 같기 때문이다
#변동성: BTC(2.37%) , ETH(3.37%) , XRP(3.53%) -> 크기는 다르게 움직인다
#종합해석 : 분산투자 관점에서 보면 상관관계가 높기 때문에 세 코인을 같이 들고 있어도 리스크 분산 효과는 크지 않을 수 있다