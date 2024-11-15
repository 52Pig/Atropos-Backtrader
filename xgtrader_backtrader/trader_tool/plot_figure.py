import json
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from finta import TA
import mplfinance as mpf
# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
def get_stock_hist_data_em(stock='600031',start_date='20210105',end_date='20500101',data_type='D'):
        '''
        获取股票数据
        start_date=''默认上市时间
        - ``1`` : 分钟
            - ``5`` : 5 分钟
            - ``15`` : 15 分钟
            - ``30`` : 30 分钟
            - ``60`` : 60 分钟
            - ``101`` : 日
            - ``102`` : 周
            - ``103`` : 月
        fq=0股票除权
        fq=1前复权
        fq=2后复权
        '''
        data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
        klt = data_dict[data_type]
        fq='1'
        if stock[0] == '6':
            stock = '1.' + stock
        else:
            stock = '0.' + stock
        url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?'
        params = {
            'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'beg': start_date,
            'end': end_date,
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'rtntype': end_date,
            'secid': stock,
            'klt': klt,
            'fqt': fq,
            'cb': 'jsonp1668432946680'
        }
        res = requests.get(url=url, params=params)
        text = res.text[19:len(res.text) - 2]
        json_text = json.loads(text)
        try:
            df = pd.DataFrame(json_text['data']['klines'])
            df.columns = ['数据']
            data_list = []
            for i in df['数据']:
                data_list.append(i.split(','))
            data = pd.DataFrame(data_list)
            columns = ['date', 'open', 'close', 'high', 'low', 'volume', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
            data.columns = columns
            for m in columns[1:]:
                data[m] = pd.to_numeric(data[m])
            data.sort_index(ascending=False,ignore_index=True,inplace=True)
            return data
        except:
            pass
def cacal_zig_data(stock='600031',start_date='20210105',end_date='20500101',data_type='D',x=0.05):
        '''
        计算之字转向
        x=5%之子转向
        :return:
        '''
        ZIG_STATE_START = 0
        ZIG_STATE_RISE = 1
        ZIG_STATE_FALL = 2
        df=get_stock_hist_data_em(stock=stock,start_date=start_date,end_date=end_date)
        # print(list(df["close"]))
        df = df[::-1]
        df = df.reset_index(drop=True)
        # df = df.iloc[-100:]
        x = x
        k = df["close"]
        d = df["date"]
        peer_i = 0
        candidate_i = None
        scan_i = 0
        peers = [0]
        z = np.zeros(len(k))
        state = ZIG_STATE_START
        while True:
            scan_i += 1
            if scan_i == len(k) - 1:
                # 扫描到尾部
                if candidate_i is None:
                    peer_i = scan_i
                    peers.append(peer_i)
                else:
                    if state == ZIG_STATE_RISE:
                        if k[scan_i] >= k[candidate_i]:
                            peer_i = scan_i
                            peers.append(peer_i)
                        else:
                            peer_i = candidate_i
                            peers.append(peer_i)
                            peer_i = scan_i
                            peers.append(peer_i)
                    elif state == ZIG_STATE_FALL:
                        if k[scan_i] <= k[candidate_i]:
                            peer_i = scan_i
                            peers.append(peer_i)
                        else:
                            peer_i = candidate_i
                            peers.append(peer_i)
                            peer_i = scan_i
                            peers.append(peer_i)
                break
            if state == ZIG_STATE_START:
                if k[scan_i] >= k[peer_i] * (1 + x):
                    candidate_i = scan_i
                    state = ZIG_STATE_RISE
                elif k[scan_i] <= k[peer_i] * (1 - x):
                    candidate_i = scan_i
                    state = ZIG_STATE_FALL
            elif state == ZIG_STATE_RISE:
                if k[scan_i] >= k[candidate_i]:
                    candidate_i = scan_i
                elif k[scan_i] <= k[candidate_i] * (1 - x):
                    peer_i = candidate_i
                    peers.append(peer_i)
                    state = ZIG_STATE_FALL
                    candidate_i = scan_i
            elif state == ZIG_STATE_FALL:
                if k[scan_i] <= k[candidate_i]:
                    candidate_i = scan_i
                elif k[scan_i] >= k[candidate_i] * (1 + x):
                    peer_i = candidate_i
                    peers.append(peer_i)
                    state = ZIG_STATE_RISE
                    candidate_i = scan_i
        for i in range(len(peers) - 1):
            peer_start_i = peers[i]
            peer_end_i = peers[i + 1]
            start_value = k[peer_start_i]
            end_value = k[peer_end_i]
            a = (end_value - start_value) / (peer_end_i - peer_start_i)  # 斜率
            for j in range(peer_end_i - peer_start_i + 1):
                z[j + peer_start_i] = start_value + a * j
        df['结果']=z
        return df
def cacal_zig_buy_sell_position(stock='600031',start_date='20210105',end_date='20500101',data_type='D'):
        '''
        计算之字转向买卖点
        :return:
        '''
        df=cacal_zig_data(stock=stock,start_date=start_date,end_date=end_date)
        #检查拐点，利用3天的数据
        #前天
        line_1=df['结果'].shift(2)
        #昨天
        line_2=df['结果'].shift(1)
        #今天
        line_3=df['结果'].shift(0)
        result=[]
        for x,y,z in zip(line_1,line_2,line_3):
            if x<y and y>z:
                result.append('sell')
            elif x>y and y<z:
                result.append('buy')
            else:
                result.append(None)
        df['买卖点']=result
        return df
def plot_kline_figure(stock='600031',start_date='20230101',end_date='20500101',data_type='D'):
        '''
        绘制标有买卖点的K线图
        :return:
        '''
        df1=cacal_zig_buy_sell_position(stock=stock,start_date=start_date,end_date=end_date)
        #拆分买卖点
        sell_list=[]
        buy_list=[]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        #买点
        for close,buy in zip(df1['close'].tolist(),df1['买卖点'].tolist()):
            if buy=='buy':
               buy_list.append(close)
            else:
                buy_list.append(None)
        #买点
        for close,sell in zip(df1['close'].tolist(),df1['买卖点'].tolist()):
            if sell=='sell':
               sell_list.append(close)
            else:
                sell_list.append(None)
        df1['买点']=buy_list
        df1['卖点']=sell_list
        macd = TA.MACD(df1)
        boll = TA.BBANDS(df1)
        rsi = TA.RSI(df1)
        df1.rename(columns={'date': 'Date', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low',
                            'volume': 'Volume'}, inplace=True)
        # 时间格式转换
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False
        df1['Date'] = pd.to_datetime(df1['Date'])
        # 出现设置索引
        df1.set_index(['Date'], inplace=True)
        # 设置股票颜
        mc = mpf.make_marketcolors(up='r', down='g', edge='i',volume='i')
        # 设置系统
        s = mpf.make_mpf_style(marketcolors=mc)
        add_plot = [mpf.make_addplot(macd['MACD'], panel=1, color='r'),
                    mpf.make_addplot(macd['SIGNAL'], panel=1, color='y'),
                    mpf.make_addplot(rsi, panel=2, title='RSI'),
                    mpf.make_addplot(df1['卖点'],panel=0,color='g',type='scatter',marker='v',markersize=60),
                    mpf.make_addplot(df1['买点'],panel=0,color='r',type='scatter',marker='^',markersize=60),
                    mpf.make_addplot(df1['结果'],panel=0,color='r',title='zig***+{}'.format(stock))]
        # 绘制股票图，5，10，20日均线
        mpf.plot(df1, type='candle', style=s,addplot=add_plot)#mav=(5, 10, 20),
        plt.show()
#pyinstaller -F C:\Users\Admin\Desktop\之字转向\main.py
#pyinstaller -D -p C:\Users\Admin\AppData\Local\Programs\Python\Python38\Lib\site-packages main.py
plot_kline_figure(stock='002642')