import requests
import time
import pandas as pd
import numpy as np
import json
import yagmail
from datetime import datetime
import warnings
#通达信指标
warnings.filterwarnings(action='ignore')
import requests
from finta import TA
from tqdm import tqdm
from  .tdx_data import tdx_data
#股票核心数据
class stock_data_ths:
    def __init__(self,qq='1029762153@qq.com'):
        self.qq=qq
        self.tdx_data=tdx_data()
        self.tdx_data.connect()
    def get_stock_hist_data_em(self,stock='600031',start_date='20210105',end_date='20500101',data_type='D',count=8000):
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
        try:
            data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
            klt=data_dict[data_type]
            secid='{}.{}'.format(0,stock)
            url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?'
            params = {
                'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'beg': start_date,
                'end': end_date,
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'rtntype':end_date,
                'secid': secid,
                'klt':klt,
                'fqt': '1',
                'cb': 'jsonp1668432946680'
            }
            res = requests.get(url=url, params=params)
            text = res.text[19:len(res.text) - 2]
            json_text = json.loads(text)
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
            data.sort_index(ascending=True,ignore_index=True,inplace=True)
            return data
        except:
            try:
                data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
                klt=data_dict[data_type]
                secid='{}.{}'.format(1,stock)
                url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?'
                params = {
                    'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
                    'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                    'beg': start_date,
                    'end': end_date,
                    'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                    'rtntype':end_date,
                    'secid': secid,
                    'klt':klt,
                    'fqt': '1',
                    'cb': 'jsonp1668432946680'
                }
                res = requests.get(url=url, params=params)
                text = res.text[19:len(res.text) - 2]
                json_text = json.loads(text)
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
                data.sort_index(ascending=True,ignore_index=True,inplace=True)
                return data
            except:
                '''
                0 5分钟K线
                1 15分钟K线 
                2 30分钟K线 
                3 1小时K线 
                4 日K线
                7 1分钟
                8 1分钟K线
                '''
                data_dict = {'1': '8', '5': '0', '15': '1', '30': '2', '60': '3', 'D': '4', '7': '7',}
                n=data_dict[data_type]
                data=self.tdx_data.get_security_minute_data(stock=stock,n=n,count=count)
                data['date']=data['datetime'].apply(lambda x:str(x)[:10])
                data['volume']=data['vol']
                data['涨跌幅']=data['close'].pct_change()*100
                data['涨跌额']=data['close']-data['open']
                data['振幅']=(data['high']-data['low'])/data['low']*100
                return data
    def cacal_zig_data_func(self,df='',x=0.05):
        '''
        计算之字转向
        x=5%之子转向
        :return:
        '''
        df=df
        ZIG_STATE_START = 0
        ZIG_STATE_RISE = 1
        ZIG_STATE_FALL = 2
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
        return z
    def get_ETF_fund_hist_data(self,stock='159805',end='20500101',limit='10000',
                                data_type='D',fqt='1'):
        '''
        获取ETF基金历史数据
        stock 证券代码
        end结束时间
        limit数据长度
        data_type数据类型：
           1 1分钟
           5 5分钟
           15 15分钟
           30 30分钟
           60 60分钟
           D 日线数据
           W 周线数据
           M 月线数据
        fqt 复权
        fq=0股票除权
        fq=1前复权
        fq=2后复权
        '''
        if stock[0]=='5':
            stock='1.'+stock
        else:
            stock='0.'+stock
        data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
        klt=data_dict[data_type]
        params={
            'secid':stock,
            'klt':klt,
            'fqt':fqt,
            'lmt':limit,
            'end':end,
            'iscca': '1',
            'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
            'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
            'ut': 'f057cbcbce2a86e2866ab8877db1d059',
            'forcect': '1',
        }
        url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
        res = requests.get(url=url, params=params)
        text = res.text
        json_text = json.loads(text)
        df = pd.DataFrame(json_text['data']['klines'])
        df.columns = ['数据']
        data_list = []
        for i in df['数据']:
            data_list.append(i.split(','))
        data = pd.DataFrame(data_list)
        columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
        data.columns = columns
        del data['_']
        for m in columns[1:-3]:
            data[m] = pd.to_numeric(data[m])
        data1=data.sort_index(ascending=True,ignore_index=True)
        return data1
    def get_fund_etf_spot_em(self,fund='159755'):
        '''
        获取ETF基金实时行情
        :param fund:
        :return:
        '''
        quotation = easyquotation.use('jsl')
        df=quotation.etfindex()
        data=df[fund]
        return data
    def get_ETF_fund_hist_data_jsl(fund='159647'):
        '''
        历史数据,备用
        '''
        url='https://www.jisilu.cn/data/etf/detail_hists/'
        params={
            '___jsl':'LST___t=1679452650523'
        }
        data={
            'is_search':'0',
            'fund_id':fund,
            'rp':'50',
            'page':'1'
        }
        res=requests.post(url=url,params=params,data=data)
        text=res.json()
        df=pd.DataFrame(text['rows'])
        data=pd.DataFrame()
        for i in df['cell'].tolist():
            df1=pd.DataFrame(i,index=[0])
            data=pd.concat([data,df1],ignore_index=True)
        data['date']=pd.to_datetime(data['hist_dt'])
        data.index=data['date']
        data1=data.sort_index(ascending=True)
        return data1
    def get_stock_all_trader_data(self,stock='600031'):
        '''
        获取股票全部分时交易数据
        备用
        :param stock:
        :return:
        '''
        market,stock=self.tdx_data.rename_stock_type_1(stock)
        url='http://push2ex.eastmoney.com/getStockFenShi?'
        params = {
            'pagesize': '10000',#144
            'ut': '7eea3edcaed734bea9cbfc24409ed989',
            'dpt': 'wzfscj',
            'cb': 'jQuery1124032472207483171633_1633697823102',
            'pageindex': '0',
            'id': '{}'.format(stock,market),
            'sort': '1',
            'ft': '1',
            'code': '{}'.format(stock),
            'market': '{}'.format(market),
            '_': '1633697823103'
        }
        try:
            res=requests.get(url=url,params=params)
            text=res.text[43:len(res.text)-2]
            json_text=json.loads(text)
            df=pd.DataFrame(json_text['data']['data'])
            columns=['date','价格','成交量','买卖数量']
            df.columns=columns
            df['价格']=df['价格']/1000
            df['close']=df['价格']
            return df
        except:
            data=self.tdx_data.get_trader_data(stock=stock,start=0,count=9000)
            data['价格']=data['price']/10
            data['涨跌幅']=(data['价格'].pct_change()*100).cumsum()
            data['实时涨跌幅']=data['涨跌幅']-data['涨跌幅'].shift(1)
            return data
    def get_stock_mi_data_em(self,stock='600031'):
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
        if stock[0] == '6':
            stock = '1.' + stock
        else:
            stock = '0.' + stock
        url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?'
        params = {
            'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'beg': '',
            'end':'20500322',
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'rtntype': '',
            'secid': stock,
            'klt':' 1',
            'fqt': '1',
            'cb': 'jsonp1668432946680'
        }
        res = requests.get(url=url, params=params)
        text = res.text[19:len(res.text) - 2]
        json_text = json.loads(text)
        df = pd.DataFrame(json_text['data']['klines'])
        df.columns = ['数据']
        data_list = []
        for i in df['数据']:
            data_list.append(i.split(','))
        data = pd.DataFrame(data_list)
        columns_list = ['date', 'open', 'close', 'high', 'low', 'volume', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
        data.columns = columns_list
        for columns in columns_list[1:]:
            data[columns]=pd.to_numeric(data[columns])
        return data
    def seed_emial_qq(self,text='交易完成'):
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text1=json.loads(com)
        try:
            password=text1['qq掩码']
            seed_qq=text1['发送qq']
            yag = yagmail.SMTP(user='{}'.format(seed_qq), password=password, host='smtp.qq.com')
            m = self.qq
            text = text
            yag.send(to=m, contents=text, subject='邮件')
            print('邮箱发生成功')
        except:
            print('qq发送失败可能用的人多')
    def get_trader_date_list(self):
        '''
        获取交易日历
        :return:
        '''
        df=self.get_stock_hist_data_em()
        date_list=df['date'].tolist()
        return date_list
    def get_stock_now_data(self,code='600031'):
        """
        东方财富网-沪深京 A 股-实时行情
        https://quote.eastmoney.com/center/gridlist.html#hs_a_board
        :return: 实时行情
        :rtype: pandas.DataFrame
        """
        url = "http://82.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "50000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
            "_": "1623833739532",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        if not data_json["data"]["diff"]:
            return pd.DataFrame()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_df.columns = [
            "_",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "换手率",
            "市盈率-动态",
            "量比",
            "5分钟涨跌",
            "代码",
            "_",
            "名称",
            "最高",
            "最低",
            "今开",
            "昨收",
            "总市值",
            "流通市值",
            "涨速",
            "市净率",
            "60日涨跌幅",
            "年初至今涨跌幅",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
        ]
        temp_df.reset_index(inplace=True)
        temp_df["index"] = temp_df.index + 1
        temp_df.rename(columns={"index": "序号"}, inplace=True)
        temp_df = temp_df[
            [
                "序号",
                "代码",
                "名称",
                "最新价",
                "涨跌幅",
                "涨跌额",
                "成交量",
                "成交额",
                "振幅",
                "最高",
                "最低",
                "今开",
                "昨收",
                "量比",
                "换手率",
                "市盈率-动态",
                "市净率",
                "总市值",
                "流通市值",
                "涨速",
                "5分钟涨跌",
                "60日涨跌幅",
                "年初至今涨跌幅",
            ]
        ]
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
        temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
        temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
        temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
        temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
        temp_df["涨速"] = pd.to_numeric(temp_df["涨速"], errors="coerce")
        temp_df["5分钟涨跌"] = pd.to_numeric(temp_df["5分钟涨跌"], errors="coerce")
        temp_df["60日涨跌幅"] = pd.to_numeric(temp_df["60日涨跌幅"], errors="coerce")
        temp_df["年初至今涨跌幅"] = pd.to_numeric(temp_df["年初至今涨跌幅"], errors="coerce")
        df=temp_df
        df1=df[df['证券代码']==code]
        return df1
    def check_is_trader_date(self):
        '''
        检测是不是交易时间
        '''
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        #利用通用时间，不考虑中午不交易
        is_trader=''
        wo=loc.tm_wday
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        trader_time=text['交易时间段']
        start_date=text['交易开始时间']
        end_date=text['交易结束时间']
        if wo<=trader_time:
            if (tm_hour>=start_date) and (tm_hour<=end_date):
                is_trader=True
                return True
            else:
                is_trader=False
                return False
        else:
            print('周末')
            return False
    def check_is_trader_date_1(self):
        '''
        检测是不是交易时间
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        trader_time=text['交易时间段']
        start_date=text['交易开始时间']
        end_date=text['交易结束时间']
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        if tm_hour==start_date and tm_min<30:
            is_tradre=False
        elif tm_hour==start_date and tm_min>30:
            is_tradre=True
        elif tm_hour>=start_date and tm_hour<=end_date:
            is_tradre=True
        else:
            is_tradre=False
        #利用通用时间，不考虑中午不交易
        wo=loc.tm_wday
        if wo<=trader_time:
            if (is_tradre) and (tm_hour<=end_date):
                return True
            else:
                return False
        else:
            print('周末')
            return False
    def cacal_zig_data(self,stock='600031',x=0.05):
        '''
        计算之字转向
        x=5%之子转向
        :return:
        '''
        df=self.get_stock_hist_data_em(start_date='20210105',end_date='20500101',stock=stock)
        ZIG_STATE_START = 0
        ZIG_STATE_RISE = 1
        ZIG_STATE_FALL = 2
        df=df
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
                result.append('无')
        df['买卖点']=result
        return df
    def cacal_zig_data_ETF(self,stock='159805',x=0.02):
        '''
        计算之字转向
        x=5%之子转向
        :return:
        '''
        df=self.get_ETF_fund_hist_data(stock=stock)
        ZIG_STATE_START = 0
        ZIG_STATE_RISE = 1
        ZIG_STATE_FALL = 2
        df=df
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
                result.append('无')
        df['买卖点']=result
        df1=df.sort_index(ascending=False,ignore_index=True)
        return df1
    def get_ETF_spot_em(self,stock='515790'):
        """
        东方财富-ETF 实时行情
        https://quote.eastmoney.com/center/gridlist.html#fund_etf
        :return: ETF 实时行情
        :rtype: pandas.DataFrame
        """
        url = "http://88.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "2000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "wbp2u": "|0|0|0|web",
            "fid": "f3",
            "fs": "b:MK0021,b:MK0022,b:MK0023,b:MK0024",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
            "_": "1672806290972",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_df.rename(
            columns={
                "f12": "代码",
                "f14": "名称",
                "f2": "最新价",
                "f4": "涨跌额",
                "f3": "涨跌幅",
                "f5": "成交量",
                "f6": "成交额",
                "f17": "开盘价",
                "f15": "最高价",
                "f16": "最低价",
                "f18": "昨收",
                "f8": "换手率",
                "f21": "流通市值",
                "f20": "总市值",
            },
            inplace=True,
        )
        temp_df = temp_df[
            [
                "代码",
                "名称",
                "最新价",
                "涨跌额",
                "涨跌幅",
                "成交量",
                "成交额",
                "开盘价",
                "最高价",
                "最低价",
                "昨收",
                "换手率",
                "流通市值",
                "总市值",
            ]
        ]
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"], errors="coerce")
        temp_df["最高价"] = pd.to_numeric(temp_df["最高价"], errors="coerce")
        temp_df["最低价"] = pd.to_numeric(temp_df["最低价"], errors="coerce")
        temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
        df= temp_df
        df['证券代码']=df['证券代码'].astype(str)
        df1=df[df['证券代码']==stock]
        #最新价
        return df1
    def cacal_zig_data_bond_cov(self,stock='113016',x=0.05,data_type='D'):
        '''
        计算之字转向
        x=5%之子转向
        :return:
        '''
        df=self.get_cov_bond_hist_data(stock=stock,data_type=data_type)
        ZIG_STATE_START = 0
        ZIG_STATE_RISE = 1
        ZIG_STATE_FALL = 2
        df=df
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
        df=df.sort_index(ascending=False,ignore_index=True)
        df['结果']=z
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
                result.append('无')
        df['买卖点']=result
        return df
    def get_cov_bond_hist_data(self,stock='113016',end='20500101',limit='10000',
                                data_type='D',fqt='1'):
        '''
        可转债历史数据
        stock 证券代码
        end结束时间
        limit数据长度
        data_type数据类型：
           1 1分钟
           5 5分钟
           15 15分钟
           30 30分钟
           60 60分钟
           D 日线数据
           W 周线数据
           M 月线数据
        fqt 复权
        fq=0股票除权
        fq=1前复权
        fq=2后复权
        '''
        try:
            data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
            klt=data_dict[data_type]
            params={
                'secid':'1.{}'.format(stock),
                'klt':klt,
                'fqt':fqt,
                #'start':'',
                'lmt':limit,
                'end':end,
                'iscca': '1',
                'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                'ut':'f057cbcbce2a86e2866ab8877db1d059',
                'forcect':'1'
            }
            url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
            res = requests.get(url=url, params=params)
            text = res.text
            json_text = json.loads(text)
            df = pd.DataFrame(json_text['data']['klines'])
            df.columns = ['数据']
            data_list = []
            for i in df['数据']:
                data_list.append(i.split(','))
            data = pd.DataFrame(data_list)
            columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                        '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
            data.columns = columns
            del data['_']
            for m in columns[1:-3]:
                data[m] = pd.to_numeric(data[m])
            data1=data.sort_index(ascending=True,ignore_index=True)
            return data1
        except:
            data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
            klt=data_dict[data_type]
            params={
                'secid':'0.{}'.format(stock),
                'klt':klt,
                'fqt':fqt,
                #'start':'',
                'lmt':limit,
                'end':end,
                'iscca': '1',
                'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                'ut':'f057cbcbce2a86e2866ab8877db1d059',
                'forcect':'1'
            }
            url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
            res = requests.get(url=url, params=params)
            text = res.text
            json_text = json.loads(text)
            df = pd.DataFrame(json_text['data']['klines'])
            df.columns = ['数据']
            data_list = []
            for i in df['数据']:
                data_list.append(i.split(','))
            data = pd.DataFrame(data_list)
            columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                    '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
            data.columns = columns
            del data['_']
            for m in columns[1:-3]:
                data[m] = pd.to_numeric(data[m])
            data1=data.sort_index(ascending=True,ignore_index=True)
            return data1
    def get_cov_bond_spot(self,stock='113016'):
        '''
        获取可转债实时数据
        '''
        try:
            params={
                'cb':'jQuery35107788691587529397_1680967733868',
                'secid':'1.{}'.format(stock),
                'forcect':'1',
                'invt': '2',
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f59,f60,f108,f152,f154,f161,f168,f169,f170,f262,f264,f265,f266,f267,f424,f426,f427,f428,f429,f432',
                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                '_': '1680967733870',
            }
            url='https://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text[41:len(res.text)-2]
            json_text=json.loads(text)['data']
            data_dict={}
            data_dict['最新价']=json_text['f43']/1000
            data_dict['最高价']=json_text['f44']/1000
            data_dict['最低价']=json_text['f45']/1000
            data_dict['总手']=json_text['f47']
            data_dict['金额']=json_text['f48']
            data_dict['量比']=json_text['f50']/100
            data_dict['外盘']=json_text['f49']
            data_dict['涨停价']=json_text['f51']/1000
            data_dict['跌停价']=json_text['f52']/1000
            data_dict['涨停收盘价']=json_text['f60']/1000
            data_dict['涨跌幅']=json_text['f170']/100
            data_dict['名称']=json_text['f264']
            return data_dict
        except:
            params={
            'cb':'jQuery35107788691587529397_1680967733868',
            'secid':'0.{}'.format(stock),
            'forcect':'1',
            'invt': '2',
            'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f59,f60,f108,f152,f154,f161,f168,f169,f170,f262,f264,f265,f266,f267,f424,f426,f427,f428,f429,f432',
            'ut': 'f057cbcbce2a86e2866ab8877db1d059',
            '_': '1680967733870',
        }
        url='https://push2.eastmoney.com/api/qt/stock/get?'
        res=requests.get(url=url,params=params)
        text=res.text[41:len(res.text)-2]
        json_text=json.loads(text)['data']
        data_dict={}
        data_dict['最新价']=json_text['f43']/1000
        data_dict['最高价']=json_text['f44']/1000
        data_dict['最低价']=json_text['f45']/1000
        data_dict['总手']=json_text['f47']
        data_dict['金额']=json_text['f48']
        data_dict['量比']=json_text['f50']/100
        data_dict['外盘']=json_text['f49']
        data_dict['涨停价']=json_text['f51']/1000
        data_dict['跌停价']=json_text['f52']/1000
        data_dict['涨停收盘价']=json_text['f60']/1000
        data_dict['涨跌幅']=json_text['f170']/100
        data_dict['名称']=json_text['f264']
        return data_dict
    def cacal_stock_grid_data(self,stock='600031',start_date='20210105',end_date='20500101',data_type='D',n=20):
        '''
        计算股票网格策略
        '''
        df=self.get_stock_hist_data_em(stock=stock,start_date=start_date,end_date=end_date,data_type=data_type)
        df['最高价']=df['close'].rolling(window=n).max()
        df['最低价']=df['close'].rolling(window=n).min()
        data_dict={}
        data_dict['证券代码']=stock
        data_dict['期间天数']=n
        data_dict['期间上限']=df['最高价'].tolist()[-1]
        data_dict['期间下限']=df['最低价'].tolist()[-1]
        data_dict['价格中枢']=(df['最高价'].tolist()[-1]+df['最低价'].tolist()[-1])/2
        data_dict['格子总数']=8
        data_dict['单位格子']=(df['最高价'].tolist()[-1]-df['最低价'].tolist()[-1])/8
        for i in range(1,5):
            data_dict['buy_{}_price'.format(i)]=data_dict['价格中枢']-i*data_dict['单位格子']
            data_dict['buy_{}_volume'.format(i)]=100
        for i in range(1,5):
            data_dict['sell_{}_price'.format(i)]=data_dict['价格中枢']+i*data_dict['单位格子']
            data_dict['sell_{}_volume'.format(i)]=100
        with open(r'股票分析数据\{}.txt'.format(stock),'w+',encoding='utf-8') as f:
            f.write(str(data_dict))
        return data_dict
    def cacal_ETF_grid_data(self,stock='159805',end_date='20500101',limit=10000,data_type='D',n=20):
        '''
        计算ETF网格策略
        '''
        df=self.get_ETF_fund_hist_data(stock=stock,end=end_date,limit=limit,data_type=data_type)
        df['最高价']=df['close'].rolling(window=n).max()
        df['最低价']=df['close'].rolling(window=n).min()
        data_dict={}
        data_dict['证券代码']=stock
        data_dict['期间天数']=n
        data_dict['期间上限']=df['最高价'].tolist()[-1]
        data_dict['期间下限']=df['最低价'].tolist()[-1]
        data_dict['价格中枢']=(df['最高价'].tolist()[-1]+df['最低价'].tolist()[-1])/2
        data_dict['格子总数']=8
        data_dict['单位格子']=(df['最高价'].tolist()[-1]-df['最低价'].tolist()[-1])/8
        for i in range(1,5):
            data_dict['buy_{}_price'.format(i)]=data_dict['价格中枢']-i*data_dict['单位格子']
            data_dict['buy_{}_volume'.format(i)]=100
        for i in range(1,5):
            data_dict['sell_{}_price'.format(i)]=data_dict['价格中枢']+i*data_dict['单位格子']
            data_dict['sell_{}_volume'.format(i)]=100
        print(data_dict)
        with open(r'ETF分析数据\{}.txt'.format(stock),'w+',encoding='utf-8') as f:
            f.write(str(data_dict))
        return data_dict
    def cacal_bond_cov_grid_data(self,stock='159805',end_date='20500101',limit=10000,data_type='D',n=20):
        '''
        计算可转债网格策略
        '''
        df=self.get_cov_bond_hist_data(stock=stock,end=end_date,limit=limit,data_type=data_type)
        df['最高价']=df['close'].rolling(window=n).max()
        df['最低价']=df['close'].rolling(window=n).min()
        data_dict={}
        data_dict['证券代码']=stock
        data_dict['期间天数']=n
        data_dict['期间上限']=df['最高价'].tolist()[-1]
        data_dict['期间下限']=df['最低价'].tolist()[-1]
        data_dict['价格中枢']=(df['最高价'].tolist()[-1]+df['最低价'].tolist()[-1])/2
        data_dict['格子总数']=8
        data_dict['单位格子']=(df['最高价'].tolist()[-1]-df['最低价'].tolist()[-1])/8
        for i in range(1,5):
            data_dict['buy_{}_price'.format(i)]=data_dict['价格中枢']-i*data_dict['单位格子']
            data_dict['buy_{}_volume'.format(i)]=100
        for i in range(1,5):
            data_dict['sell_{}_price'.format(i)]=data_dict['价格中枢']+i*data_dict['单位格子']
            data_dict['sell_{}_volume'.format(i)]=100
        print(data_dict)
        with open(r'可转债分析数据\{}.txt'.format(stock),'w+',encoding='utf-8') as f:
            f.write(str(data_dict))
        return data_dict
    def get_bond_cov_table(self):
        '''
        可转债一览表
        '''
        data=pd.DataFrame()
        for i in range(5):
            try:
                params={
                    'callback':'jQuery1123041828396166958415_1681350237822',
                    'sortColumns':'PUBLIC_START_DATE',
                    'sortTypes':'-1',
                    'pageSize':'5000',
                    'pageNumber':i,
                    'reportName':'RPT_BOND_CB_LIST',
                    'columns':'ALL',
                    'quoteColumns':'f2~01~CONVERT_STOCK_CODE~CONVERT_STOCK_PRICE,f235~10~SECURITY_CODE~TRANSFER_PRICE,f236~10~SECURITY_CODE~TRANSFER_VALUE,f2~10~SECURITY_CODE~CURRENT_BOND_PRICE,f237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO,f239~10~SECURITY_CODE~RESALE_TRIG_PRICE,f240~10~SECURITY_CODE~REDEEM_TRIG_PRICE,f23~01~CONVERT_STOCK_CODE~PBV_RATIO',
                    'quoteType':'0',
                    'source':'WEB',
                    'client':'WEB'
                }
                url='https://datacenter-web.eastmoney.com/api/data/v1/get?'
                res=requests.get(url=url,params=params)
                text=res.text[43:len(res.text)-2]
                json_text=json.loads(text)
                df=pd.DataFrame(json_text['result']['data'])
                df1=df[['ACTUAL_ISSUE_SCALE','CONVERT_STOCK_CODE','SECURITY_NAME_ABBR','CORRECODE_NAME_ABBR',
                        'CURRENT_BOND_PRICE','EXPIRE_DATE','INITIAL_TRANSFER_PRICE','INTEREST_RATE_EXPLAIN',
                        'ISSUE_OBJECT','RATING','REDEEM_CLAUSE','SECURITY_CODE','TRANSFER_PREMIUM_RATIO',
                        'TRANSFER_PRICE','TRANSFER_VALUE','LISTING_DATE']]
                columns=['发行规模','证券代码','正股价','可转债名称','可转债最新价','到期日',
                        '转股价','利息','发行公告','评级','赎回条款','证券代码','转股溢价率',
                        '转股价','转股价值','上市时间']
                df1.columns=columns
                if df1.shape[0]>0:
                    data=pd.concat([data,df1],ignore_index=True)
                else:
                    pass
            except:
                pass
        return data
    def get_bond_cov_table_analysis(self):
        '''
        可转债表分析
        可转债双低值 = 转债价格+转股溢价率*100
        其中：转股溢价率 = （转债最新价 - 转股价值）/ 转股价值
            转股价值 = 转换比例 * 正股收盘价
            转换比例 = 100 / 可转债转股价
        '''
        df=self.get_bond_cov_table()
        #删除没有上市的
        df1=df.dropna()
        #删除没有价格的
        df2=df1[df1['可转债最新价'] !='-']
        #剔除上市不足30天的
        date_list=self.get_trader_date_list()[-30]
        df3=df2[df2['上市时间']<=date_list]
        df3['可转债双低值']=df3['可转债最新价']+df3['转股溢价率']
        df4=df3.sort_values(by='可转债双低值',ignore_index=True)
        df5=df4.drop_duplicates()
        df5.to_excel(r'data.xlsx')
        return df5
    def cacal_stock_wr_indicator(self,stock='000065',start_date='',end_date='20500101',N=10,N1=6,x1=80,x2=20):
        '''
        股票
        计算股票威廉指标,带买卖点
        wr2变化快,小周期，wr1变化慢，大周期
        威廉指标交易特殊，高位死叉买入，低位金叉卖出
        '''
        df=self.get_stock_hist_data_em(stock=stock,start_date=start_date,end_date=end_date)
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        wr1,wr2=tdx_indicator.WR(CLOSE,LOW,HIGH,N=10,N1=6)
        df['wr1']=wr1
        df['wr2']=wr2
        #计算金叉与死叉，小周期周期在前金差
        df['金叉']=np.logical_and(df['wr2'].shift(1)<df['wr1'].shift(1),df['wr2']>=df['wr1'])
        df['死叉']=np.logical_and(df['wr2'].shift(1)>df['wr1'].shift(1),df['wr2']<=df['wr1'])
        result=[]
        for x,y,z in zip(df['wr1'].tolist(),df['金叉'].tolist(),df['死叉'].tolist()):
            if x>=x1 and z==True:
                result.append('buy')
            elif x<=x2 and y==True:
                result.append('sell')
            else:
                result.append('无')
        df['买卖点']=result
        df.to_excel(r'股票分析数据\{}.xlsx'.format(stock))
        print(df)
        return df
    def cacal_ETF_wr_indicator(self,stock='159805',end_date='20500101',limit=1000000,N=10,N1=6,x1=80,x2=20):
        '''
        ETF
        计算股票威廉指标,带买卖点
        wr2变化快,小周期，wr1变化慢，大周期
        威廉指标交易特殊，高位死叉买入，低位金叉卖出
        '''
        df=self.get_ETF_fund_hist_data(stock=stock,end=end_date,limit=limit)
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        wr1,wr2=tdx_indicator.WR(CLOSE,LOW,HIGH,N=10,N1=6)
        df['wr1']=wr1
        df['wr2']=wr2
        #计算金叉与死叉，小周期周期在前金差
        df['金叉']=np.logical_and(df['wr2'].shift(1)<df['wr1'].shift(1),df['wr2']>=df['wr1'])
        df['死叉']=np.logical_and(df['wr2'].shift(1)>df['wr1'].shift(1),df['wr2']<=df['wr1'])
        result=[]
        for x,y,z in zip(df['wr1'].tolist(),df['金叉'].tolist(),df['死叉'].tolist()):
            if x>=x1 and z==True:
                result.append('buy')
            elif x<=x2 and y==True:
                result.append('sell')
            else:
                result.append('无')
        df['买卖点']=result
        df.to_excel(r'ETF分析数据\{}.xlsx'.format(stock))
        print(df)
        return df
    def cacal_cov_bond_wr_indicator(self,stock='113036',end_date='20500101',limit=1000000,N=10,N1=6,x1=80,x2=20):
        '''
        可转债
        计算股票威廉指标,带买卖点
        wr2变化快,小周期，wr1变化慢，大周期
        威廉指标交易特殊，高位死叉买入，低位金叉卖出
        '''
        df=self.get_cov_bond_hist_data(stock=stock,end=end_date,limit=limit)
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        wr1,wr2=tdx_indicator.WR(CLOSE,LOW,HIGH,N=10,N1=6)
        df['wr1']=wr1
        df['wr2']=wr2
        #计算金叉与死叉，小周期周期在前金差
        df['金叉']=np.logical_and(df['wr2'].shift(1)<df['wr1'].shift(1),df['wr2']>=df['wr1'])
        df['死叉']=np.logical_and(df['wr2'].shift(1)>df['wr1'].shift(1),df['wr2']<=df['wr1'])
        result=[]
        for x,y,z in zip(df['wr1'].tolist(),df['金叉'].tolist(),df['死叉'].tolist()):
            if x>=x1 and z==True:
                result.append('buy')
            elif x<=x2 and y==True:
                result.append('sell')
            else:
                result.append('无')
        df['买卖点']=result
        df.to_excel(r'可转债分析数据\{}.xlsx'.format(stock))
        print(df)
        return df
    def cacal_stock_mean_models(self,stock='000065',start_date='',end_date='20500101',n=3):
        '''
        股票均线
        '''
        df=self.get_stock_hist_data_em(stock=stock,start_date=start_date,end_date=end_date)
        df['z'] = df['close'].rolling(window=n).mean()
        df['买点'] = np.logical_and(df['z'].shift(2) > df['z'].shift(1), df['z'].shift(1) < df['z'])
        df['卖点'] = np.logical_and(df['z'].shift(2) < df['z'].shift(1), df['z'].shift(1) > df['z'])
        result=[]
        for x,y in zip(df['买点'].tolist(),df['卖点'].tolist()):
            if x==True:
                result.append('buy')
            elif y==True:
                result.append('sell')
            else:
                result.append('无')
        df['买卖点']=result
        df.to_excel(r'股票分析数据\{}.xlsx'.format(stock))
        print(df)
        return df
    def cacal_ETF_mean_models(self,stock='159805',end_date='20500101',limit=1000000,n=5):
        '''
        ETF均线
        '''
        df=self.get_ETF_fund_hist_data(stock=stock,end=end_date,limit=limit)
        df['z'] = df['close'].rolling(window=n).mean()
        df['买点'] = np.logical_and(df['z'].shift(2) > df['z'].shift(1), df['z'].shift(1) < df['z'])
        df['卖点'] = np.logical_and(df['z'].shift(2) < df['z'].shift(1), df['z'].shift(1) > df['z'])
        result=[]
        for x,y in zip(df['买点'].tolist(),df['卖点'].tolist()):
            if x==True:
                result.append('buy')
            elif y==True:
                result.append('sell')
            else:
                result.append('无')
        df['买卖点']=result
        df.to_excel(r'ETF分析数据\{}.xlsx'.format(stock))
        print(df)
        return df
    def cacal_cov_bond_mean_models(self,stock='113036',end_date='20500101',limit=1000000,n=5):
        '''
        可转债均线
        '''
        df=self.get_cov_bond_hist_data(stock=stock,end=end_date,limit=limit)
        df['z'] = df['close'].rolling(window=n).mean()
        df['买点'] = np.logical_and(df['z'].shift(2) > df['z'].shift(1), df['z'].shift(1) < df['z'])
        df['卖点'] = np.logical_and(df['z'].shift(2) < df['z'].shift(1), df['z'].shift(1) > df['z'])
        result=[]
        for x,y in zip(df['买点'].tolist(),df['卖点'].tolist()):
            if x==True:
                result.append('buy')
            elif y==True:
                result.append('sell')
            else:
                result.append('无')
        df['买卖点']=result
        df.to_excel(r'可转债分析数据\{}.xlsx'.format(stock))
        print(df)
        return df
    def plot_wr_kline_figure(self,data_type='股票',stock='600105',start_date='20220101',end_date='20500101',limit=1000,x1=80,x2=20):
        '''
        data_type=股票/可转债/ETF
        绘制标有买卖点的K线图
        :return:
        '''
        if data_type=='股票':
            df1=self.cacal_stock_wr_indicator(stock=stock,start_date=start_date,end_date=end_date,x1=x1,x2=x2)
        elif data_type=='可转债':
            df1=self.cacal_cov_bond_wr_indicator(stock=stock,end_date=end_date,limit=limit,x1=x1,x2=x2)
        else:
            df1=self.cacal_ETF_wr_indicator(stock=stock,end_date=end_date,limit=limit,x1=x1,x2=x2)
        #拆分买卖点
        sell_list=[]
        buy_list=[]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        #买点
        for close,buy in zip(df1['close'].tolist(),df1['买卖点'].tolist()):
            if buy=='buy':
               buy_list.append(close-close*0.05)
            else:
                buy_list.append(None)
        #买点
        for close,sell in zip(df1['close'].tolist(),df1['买卖点'].tolist()):
            if sell=='sell':
               sell_list.append(close+close*0.05)
            else:
                sell_list.append(None)
        df1['买点']=buy_list
        df1['卖点']=sell_list
        macd = TA.MACD(df1)
        df1.rename(columns={'date': 'Date', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low',
                            'volume': 'Volume'}, inplace=True)
        # 时间格式转换
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False
        df1['Date'] = pd.to_datetime(df1['Date'])
        # 出现设置索引
        df1.set_index(['Date'], inplace=True)
        # 设置股票颜
        mc = mpf.make_marketcolors(up='r', down='g', edge='i')
        # 设置系统
        s = mpf.make_mpf_style(marketcolors=mc)
        add_plot = [mpf.make_addplot(macd['MACD'], panel=1, color='r',title='MACD'),
                    mpf.make_addplot(macd['SIGNAL'], panel=1, color='y'),
                    mpf.make_addplot(df1['wr2'], panel=2, title='WR'),
                    mpf.make_addplot(df1['wr1'], panel=2),
                    mpf.make_addplot(df1['卖点'],panel=0,color='g',type='scatter',marker='v',markersize=60,title='WR_models,{},red is buy,green is sell'.format(stock)),
                    mpf.make_addplot(df1['买点'],panel=0,color='r',type='scatter',marker='^',markersize=60),
                    ]
        # 绘制股票图，5，10，20日均线
        mpf.plot(df1, type='candle', mav=(5, 10, 20),style=s,addplot=add_plot)#mav=(5, 10, 20),
        plt.show()
    def plot_mean_models_kline_figure(self,data_type='股票',stock='600105',start_date='20220601',end_date='20500101',limit=1000,n=3):
        '''
        data_type=股票/可转债/ETF
        绘制标有买卖点的K线图
        :return:
        '''
        if data_type=='股票':
            df1=self.cacal_stock_mean_models(stock=stock,start_date=start_date,end_date=end_date,n=n)
        elif data_type=='可转债':
            df1=self.cacal_cov_bond_mean_models(stock=stock,end_date=end_date,limit=limit,n=n)
        else:
            df1=self.cacal_ETF_mean_models(stock=stock,end_date=end_date,limit=limit,n=n)
        #拆分买卖点
        sell_list=[]
        buy_list=[]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        #买点
        for close,buy in zip(df1['close'].tolist(),df1['买卖点'].tolist()):
            if buy=='buy':
               buy_list.append(close-close*0.05)
            else:
                buy_list.append(None)
        #买点
        for close,sell in zip(df1['close'].tolist(),df1['买卖点'].tolist()):
            if sell=='sell':
               sell_list.append(close+close*0.05)
            else:
                sell_list.append(None)
        df1['买点']=buy_list
        df1['卖点']=sell_list
        macd = TA.MACD(df1)
        df1.rename(columns={'date': 'Date', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low',
                            'volume': 'Volume'}, inplace=True)
        # 时间格式转换
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False
        df1['Date'] = pd.to_datetime(df1['Date'])
        # 出现设置索引
        df1.set_index(['Date'], inplace=True)
        # 设置股票颜
        mc = mpf.make_marketcolors(up='r', down='g', edge='i')
        # 设置系统
        s = mpf.make_mpf_style(marketcolors=mc)
        add_plot = [mpf.make_addplot(macd['MACD'], panel=1, color='r',title='MACD'),
                    mpf.make_addplot(macd['SIGNAL'], panel=1, color='y'),
                    mpf.make_addplot(df1['卖点'],panel=0,color='g',type='scatter',marker='v',markersize=60,title='mean_line_models,{},red is buy,green is sell'.format(stock)),
                    mpf.make_addplot(df1['买点'],panel=0,color='r',type='scatter',marker='^',markersize=60),
                    ]
        # 绘制股票图，5，10，20日均线
        mpf.plot(df1, type='candle', mav=(5, 10, 20),style=s,addplot=add_plot)#mav=(5, 10, 20),
        plt.show()
    def stock_individual_fund_flow_rank(self,indicator: str = "今日") -> pd.DataFrame:
        """
        东方财富网-数据中心-资金流向-排名
        http://data.eastmoney.com/zjlx/detail.html
        :param indicator: choice of {"今日", "3日", "5日", "10日"}
        :type indicator: str
        :return: 指定 indicator 资金流向排行
        :rtype: pandas.DataFrame
        """
        indicator_map = {
            "今日": [
                "f62",
                "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124",
            ],
            "3日": [
                "f267",
                "f12,f14,f2,f127,f267,f268,f269,f270,f271,f272,f273,f274,f275,f276,f257,f258,f124",
            ],
            "5日": [
                "f164",
                "f12,f14,f2,f109,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f257,f258,f124",
            ],
            "10日": [
                "f174",
                "f12,f14,f2,f160,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f260,f261,f124",
            ],
        }
        url = "http://push2.eastmoney.com/api/qt/clist/get"
        params = {
            "fid": indicator_map[indicator][0],
            "po": "1",
            "pz": "6000",
            "pn": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "ut": "b2884a393a59ad64002292a3e90d46a5",
            "fs": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2",
            "fields": indicator_map[indicator][1],
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_df.reset_index(inplace=True)
        temp_df["index"] = range(1, len(temp_df) + 1)
        if indicator == "今日":
            temp_df.columns = [
                "序号",
                "最新价",
                "今日涨跌幅",
                "代码",
                "名称",
                "今日主力净流入-净额",
                "今日超大单净流入-净额",
                "今日超大单净流入-净占比",
                "今日大单净流入-净额",
                "今日大单净流入-净占比",
                "今日中单净流入-净额",
                "今日中单净流入-净占比",
                "今日小单净流入-净额",
                "今日小单净流入-净占比",
                "_",
                "今日主力净流入-净占比",
                "_",
                "_",
                "_",
            ]
            temp_df = temp_df[
                [
                    "序号",
                    "代码",
                    "名称",
                    "最新价",
                    "今日涨跌幅",
                    "今日主力净流入-净额",
                    "今日主力净流入-净占比",
                    "今日超大单净流入-净额",
                    "今日超大单净流入-净占比",
                    "今日大单净流入-净额",
                    "今日大单净流入-净占比",
                    "今日中单净流入-净额",
                    "今日中单净流入-净占比",
                    "今日小单净流入-净额",
                    "今日小单净流入-净占比",
                ]
            ]
        elif indicator == "3日":
            temp_df.columns = [
                "序号",
                "最新价",
                "代码",
                "名称",
                "_",
                "3日涨跌幅",
                "_",
                "_",
                "_",
                "3日主力净流入-净额",
                "3日主力净流入-净占比",
                "3日超大单净流入-净额",
                "3日超大单净流入-净占比",
                "3日大单净流入-净额",
                "3日大单净流入-净占比",
                "3日中单净流入-净额",
                "3日中单净流入-净占比",
                "3日小单净流入-净额",
                "3日小单净流入-净占比",
            ]
            temp_df = temp_df[
                [
                    "序号",
                    "代码",
                    "名称",
                    "最新价",
                    "3日涨跌幅",
                    "3日主力净流入-净额",
                    "3日主力净流入-净占比",
                    "3日超大单净流入-净额",
                    "3日超大单净流入-净占比",
                    "3日大单净流入-净额",
                    "3日大单净流入-净占比",
                    "3日中单净流入-净额",
                    "3日中单净流入-净占比",
                    "3日小单净流入-净额",
                    "3日小单净流入-净占比",
                ]
            ]
        elif indicator == "5日":
            temp_df.columns = [
                "序号",
                "最新价",
                "代码",
                "名称",
                "5日涨跌幅",
                "_",
                "5日主力净流入-净额",
                "5日主力净流入-净占比",
                "5日超大单净流入-净额",
                "5日超大单净流入-净占比",
                "5日大单净流入-净额",
                "5日大单净流入-净占比",
                "5日中单净流入-净额",
                "5日中单净流入-净占比",
                "5日小单净流入-净额",
                "5日小单净流入-净占比",
                "_",
                "_",
                "_",
            ]
            temp_df = temp_df[
                [
                    "序号",
                    "代码",
                    "名称",
                    "最新价",
                    "5日涨跌幅",
                    "5日主力净流入-净额",
                    "5日主力净流入-净占比",
                    "5日超大单净流入-净额",
                    "5日超大单净流入-净占比",
                    "5日大单净流入-净额",
                    "5日大单净流入-净占比",
                    "5日中单净流入-净额",
                    "5日中单净流入-净占比",
                    "5日小单净流入-净额",
                    "5日小单净流入-净占比",
                ]
            ]
        elif indicator == "10日":
            temp_df.columns = [
                "序号",
                "最新价",
                "代码",
                "名称",
                "_",
                "10日涨跌幅",
                "10日主力净流入-净额",
                "10日主力净流入-净占比",
                "10日超大单净流入-净额",
                "10日超大单净流入-净占比",
                "10日大单净流入-净额",
                "10日大单净流入-净占比",
                "10日中单净流入-净额",
                "10日中单净流入-净占比",
                "10日小单净流入-净额",
                "10日小单净流入-净占比",
                "_",
                "_",
                "_",
            ]
            temp_df = temp_df[
                [
                    "序号",
                    "代码",
                    "名称",
                    "最新价",
                    "10日涨跌幅",
                    "10日主力净流入-净额",
                    "10日主力净流入-净占比",
                    "10日超大单净流入-净额",
                    "10日超大单净流入-净占比",
                    "10日大单净流入-净额",
                    "10日大单净流入-净占比",
                    "10日中单净流入-净额",
                    "10日中单净流入-净占比",
                    "10日小单净流入-净额",
                    "10日小单净流入-净占比",
                ]
            ]
        return temp_df
    def stock_individual_fund_flow(self,
        stock= "600094") :
        """
        东方财富网-数据中心-资金流向-个股
        http://data.eastmoney.com/zjlx/detail.html
        :param stock: 证券代码
        :type stock: str
        :param market: 股票市场; 上海证券交易所: sh, 深证证券交易所: sz
        :type market: str
        :return: 近期个股的资金流数据
        :rtype: pandas.DataFrame
        """
        if stock[0]=='6':
            market='sh'
        else:
            market='sz'
        market_map = {"sh": 1, "sz": 0}
        url = "http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        }
        params = {
            "lmt": "0",
            "klt": "101",
            "secid": f"{market_map[market]}.{stock}",
            "fields1": "f1,f2,f3,f7",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
            "ut": "b2884a393a59ad64002292a3e90d46a5",
            "cb": "jQuery183003743205523325188_1589197499471",
            "_": int(time.time() * 1000),
        }
        r = requests.get(url, params=params, headers=headers)
        text_data = r.text
        json_data = json.loads(text_data[text_data.find("{") : -2])
        content_list = json_data["data"]["klines"]
        temp_df = pd.DataFrame([item.split(",") for item in content_list])
        temp_df.columns = [
            "日期",
            "主力净流入净额",
            "小单净流入净额",
            "中单净流入净额",
            "大单净流入净额",
            "超大单净流入净额",
            "主力净流入净占比",
            "小单净流入净占比",
            "中单净流入净占比",
            "大单净流入净占比",
            "超大单净流入净占比",
            "收盘价",
            "涨跌幅",
            "-",
            "-",
        ]
        temp_df = temp_df[
            [
                "日期",
                "收盘价",
                "涨跌幅",
                "主力净流入净额",
                "主力净流入净占比",
                "超大单净流入净额",
                "超大单净流入净占比",
                "大单净流入净额",
                "大单净流入净占比",
                "中单净流入净额",
                "中单净流入净占比",
                "小单净流入净额",
                "小单净流入净占比",
            ]
        ]
        temp_df["主力净流入净额"] = pd.to_numeric(temp_df["主力净流入净额"])
        temp_df["小单净流入净额"] = pd.to_numeric(temp_df["小单净流入净额"])
        temp_df["中单净流入净额"] = pd.to_numeric(temp_df["中单净流入净额"])
        temp_df["大单净流入净额"] = pd.to_numeric(temp_df["大单净流入净额"])
        temp_df["超大单净流入净额"] = pd.to_numeric(temp_df["超大单净流入净额"])
        temp_df["主力净流入净占比"] = pd.to_numeric(temp_df["主力净流入净占比"])
        temp_df["小单净流入净占比"] = pd.to_numeric(temp_df["小单净流入净占比"])
        temp_df["中单净流入净占比"] = pd.to_numeric(temp_df["中单净流入净占比"])
        temp_df["大单净流入净占比"] = pd.to_numeric(temp_df["大单净流入净占比"])
        temp_df["超大单净流入净占比"] = pd.to_numeric(temp_df["超大单净流入净占比"])
        temp_df["收盘价"] = pd.to_numeric(temp_df["收盘价"])
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
        return temp_df
    def get_stock_set_bidding(self,stock='600031'):
        '''
        获取股票集合竞价数据
        在集合竞价挂牌使用
        :param stock:
        :return:
        '''
        if stock[0]=='6':
            market='1'
        else:
            market='0'
        def select_data(x):
            if int(x)==1:
                return '卖盘'
            elif int(x)==2:
                return '买盘'
            else:
                return x
        url='http://push2ex.eastmoney.com/getStockFenShi?'
        params = {
            'pagesize': '1000000',#144
            'ut': '7eea3edcaed734bea9cbfc24409ed989',
            'dpt': 'wzfscj',
            'cb': 'jQuery1124032472207483171633_1633697823102',
            'pageindex': '0',
            'id': '{}'.format(stock,market),
            'sort': '1',
            'ft': '1',
            'code': '{}'.format(stock),
            'market': '{}'.format(market),
            '_': '1633697823103'
        }
        res=requests.get(url=url,params=params)
        text=res.text[43:len(res.text)-2]
        json_text=json.loads(text)
        df=pd.DataFrame(json_text['data']['data'])
        columns=['时间','价格','成交量','买卖性质']
        df.columns=columns
        df['价格']=df['价格']/1000
        df['时间']=df['时间'].astype(int)
        # 选择集合竞价数据
        df['实时涨跌幅']=df['价格'].pct_change()*100
        spot_data=self.get_stock_spot_data(stock=stock)
        df['昨日收盘价']=spot_data['昨收']
        df['涨跌幅']=((df['价格']-df['昨日收盘价'])/df['昨日收盘价'])*100
        df['实时成交额']=(df['价格']*df['成交量'])*100
        df['流通市值']=spot_data['流通市值']
        df['总市值']=spot_data['总市值']
        df['量比']=spot_data['量比']
        df['实时换手率']=(df['实时成交额']/df['流通市值'])*100
        df['证券代码']=spot_data['证券代码']
        df['股票名称']=spot_data['股票名称']
        #df['累计换手率']=df['实时换手率'].cumsum()
        df['买卖性质']=df['买卖性质'].apply(select_data)
        return df
    def get_stock_spot_cash_flow(self,stock='600031'):
        '''
        获取股票实时资金流入数据
        '''
        if stock[0]=='6':
            stock='1.'+stock
        else:
            stock='0.'+stock
        try:
            params={
                'cb': 'jQuery112302664421249343738_1683855841168',
                'lmt': '0',
                'klt': '1',
                'fields1': 'f1,f2,f3,f7',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65',
                'ut': 'b2884a393a59ad64002292a3e90d46a5',
                'secid':stock,
                '_': '1683855841182'
            }
            url='https://push2.eastmoney.com/api/qt/stock/fflow/kline/get?'
            res=requests.get(url=url,params=params)
            text=res.text[42:len(res.text)-2]
            json_text=json.loads(text)
            df=pd.DataFrame(json_text['data']['klines'])
            df.columns=['数据']
            data_list=[]
            for i in df['数据']:
                data_list.append(i.split(','))
            data=pd.DataFrame(data_list)
            columns=['data','今日主力净流入','今日小单净流入','今日中单净流入',
                        '今日大单净流入','今日超大单净流入']
            data.columns=columns
            for column in columns:
                try:
                    data[column]=pd.to_numeric(data[column])
                except:
                    pass
            return data
        except:
            return False

    def stock_zt_pool_em(self,date= "20220426"):
        """
        东方财富网-行情中心-涨停板行情-涨停股池
        http://quote.eastmoney.com/ztb/detail#type=ztgc
        :return: 涨停股池
        :rtype: pandas.DataFrame
        """
        url = "http://push2ex.eastmoney.com/getTopicZTPool"
        params = {
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "dpt": "wz.ztzt",
            "Pageindex": "0",
            "pagesize": "10000",
            "sort": "fbt:asc",
            "date": date,
            "_": "1621590489736",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        if data_json["data"] is None:
            return pd.DataFrame()
        temp_df = pd.DataFrame(data_json["data"]["pool"])
        temp_df.reset_index(inplace=True)
        temp_df["index"] = range(1, len(temp_df) + 1)
        temp_df.columns = [
            "序号",
            "代码",
            "_",
            "名称",
            "最新价",
            "涨跌幅",
            "成交额",
            "流通市值",
            "总市值",
            "换手率",
            "连板数",
            "首次封板时间",
            "最后封板时间",
            "封板资金",
            "炸板次数",
            "所属行业",
            "涨停统计",
        ]
        temp_df["涨停统计"] = (
                temp_df["涨停统计"].apply(lambda x: dict(x)["days"]).astype(str)
                + "/"
                + temp_df["涨停统计"].apply(lambda x: dict(x)["ct"]).astype(str)
        )
        temp_df = temp_df[
            [
                "序号",
                "代码",
                "名称",
                "涨跌幅",
                "最新价",
                "成交额",
                "流通市值",
                "总市值",
                "换手率",
                "封板资金",
                "首次封板时间",
                "最后封板时间",
                "炸板次数",
                "涨停统计",
                "连板数",
                "所属行业",
            ]
        ]
        temp_df["首次封板时间"] = temp_df["首次封板时间"].astype(str).str.zfill(6)
        temp_df["最后封板时间"] = temp_df["最后封板时间"].astype(str).str.zfill(6)
        temp_df["最新价"] = temp_df["最新价"] / 1000
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
        temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"])
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"])
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"])
        temp_df["封板资金"] = pd.to_numeric(temp_df["封板资金"])
        temp_df["炸板次数"] = pd.to_numeric(temp_df["炸板次数"])
        temp_df["连板数"] = pd.to_numeric(temp_df["连板数"])

        return temp_df
    def get_stock_spot_data(self,stock='002858'):
        '''
        获取股票实时数据
        '''
        maker,stock=self.tdx_data.rename_stock_type_1(stock=stock)
        secid='{}.{}'.format(maker,stock)
        params={
            'invt':'2',
            'fltt':'1',
            'cb':'jQuery3510180390237681324_1685191053405',
            'fields':'f58,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f47,f48,f161,f49,f171,f50,f86,f177,f111,f51,f52,f168,f116,f117,f167,f162,f262',
            'secid': secid,
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'wbp2u': '1452376043169950|0|1|0|web',
            '_': '1685191053406',
        }
        try:
            
            url='http://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text
            text=text[40:len(text)-2]
            json_text=json.loads(text)
            data=json_text['data']
            result={}
            result['最新价']=data['f43']/100
            result['最高价']=data['f44']/100
            result['最低价']=data['f45']/100
            result['今开']=data['f46']/100
            result['成交量']=data['f47']
            result['成交额']=data['f48']
            result['量比']=data['f50']/100
            result['涨停']=data['f51']/100
            result['跌停']=data['f52']/100
            result['证券代码']=data['f57']
            result['股票名称'] = data['f58']
            result['昨收']=data['f60']/100
            result['总市值']=data['f116']
            result['流通市值']=data['f117']
            result['换手率']=data['f168']/100
            result['涨跌幅']=data['f170']/100
            return result
        except:
            json_text=self.tdx_data.get_security_quotes_none(stock=stock)
            data_dict={}
            data_dict['最新价']=json_text['price'].tolist()[-1]
            data_dict['最高价']=json_text['high'].tolist()[-1]
            data_dict['最低价']=json_text['low'].tolist()[-1]
            data_dict['今开']=json_text['open'].tolist()[-1]
            return data_dict
    def get_stock_jhjj_analysis(self,stock='002229'):
        '''
        股票集合竞价分析获取9:25最后一笔
        资金为买盘
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        df=self.get_stock_set_bidding(stock=stock)
        df1=df[df['时间']<=92600]
        #print(df1)
        #开盘金额
        max_cash=text['集合竞价资金上限']
        min_cash=text['集合竞价资金下限']
        cash_select=''
        cash=df1['实时成交额'].tolist()[-1]
        #9：25交易性质
        trader_type=df1['买卖性质'].tolist()[-1]
        #print(trader_type)
        if cash>=min_cash and cash<=max_cash:# and trader_type=='买盘':
            cash_select=True
        else:
            cash_select=False
        print(stock,cash_select,trader_type,cash)
        return cash_select
    def get_stock_jhjj_tx(self,stock='605580',pages=1):
        '''
        腾讯财经集合竞价
        '''
        if stock[0]=='6':
            stock='sh'+stock
        else:
            stock='sz'+stock
        all_data=pd.DataFrame()
        for page in tqdm(range(pages)):
            try:
                params={
                    'appn': 'detail',
                    'action': 'data',
                    'c':stock,
                    'p':page
                }
                url='https://stock.gtimg.cn/data/index.php?'
                res=requests.get(url=url,params=params)
                text=res.text
                text=text[27:len(text)-2]
                text1=text.split('|')
                result=[]
                for i in text1:
                    result.append(i.split('/'))
                data=pd.DataFrame(result)
                data.columns=['序号','时间','价格','价格变动','成交量','成交金额','买卖性质']
                def select_data(x):
                    if x=='B':
                        return "买盘"
                    elif x=='S':
                        return "卖盘"
                    else:
                        return '中性盘'
                data['买卖性质']=data['买卖性质'].apply(select_data)
                data['价格']=pd.to_numeric(data['价格'])
                data['价格变动']=pd.to_numeric(data['价格变动'])
                data['成交金额']=pd.to_numeric(data['成交金额'])
                data['成交量']=pd.to_numeric(data['成交量'])
                all_data=pd.concat([all_data,data],ignore_index=True)
            except:
                pass
        return all_data
    def get_stock_jhjj_analysis_tx(self,stock='605580',pages=1):
        '''
        腾讯集合竞价分析
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        df1=self.get_stock_jhjj_tx(stock=stock,pages=pages)
        if df1.shape[0]>0:
            #开盘金额
            max_cash=text['集合竞价资金上限']
            min_cash=text['集合竞价资金下限']
            cash_select=''
            cash=df1['成交金额'].tolist()[0]
            #9：25交易性质
            trader_type=df1['买卖性质'].tolist()[0]
            #print(trader_type)
            if cash>=min_cash and cash<=max_cash and trader_type=='买盘':
                cash_select=True
            else:
                cash_select=False
            print(cash_select,trader_type)
            return cash_select
        else:
            return False
    def surge_and_fall_overfall_rebound(self,stock='000037',min_return=7,max_down=-2,max_df=-5,ft_return=3):
        '''
        冲高回落--超跌反弹
        min_return冲高的涨跌幅
        max_down最大的回撤
        #超跌反弹
        max_df最大跌幅
        ft_return反弹收益
        '''
        df=self.get_stock_set_bidding(stock=stock)
        #最大涨跌幅
        max_return_ratio=max(df['涨跌幅'].tolist())
        #现在的涨跌幅
        now_return_ratio=df['涨跌幅'].tolist()[-1]
        #目前的收益回撤
        max_down_ratio=now_return_ratio-max_return_ratio
        if max_return_ratio>min_return and max_down_ratio<=-2:
            text='冲高回落，股票{} 最大涨跌幅{} 现在的涨跌幅{} 收益回撤{}'.format(stock,max_return_ratio,now_return_ratio,max_down_ratio)
            return '冲高回落',True,text
        else:
            text='不符合冲高回落，股票{} 最大涨跌幅{} 现在的涨跌幅{} 收益回撤{}'.format(stock,max_return_ratio,now_return_ratio,max_down_ratio)
            return '冲高回落',False,text
        #最小涨跌幅
        min_return_ratio=min(df['涨跌幅'].tolist())
        #反弹收益
        ft_return_ratio=now_return_ratio-min_return_ratio
        if min_return_ratio<max_df and ft_return_ratio >ft_return:
            text='超跌反弹，股票{} 最大跌幅{} 现在的涨跌幅{} 收益反弹{}'.format(stock, min_return_ratio,now_return_ratio,ft_return_ratio)
            return '超跌反弹',True,text
        else:
            text='不符合超跌反弹，股票{} 最大跌幅{} 现在的涨跌幅{} 收益反弹{}'.format(stock, min_return_ratio,now_return_ratio,ft_return_ratio)
            return "超跌反弹",False,text
if __name__=='__main__':
    models=stock_data()
    models.get_stock_all_trader_data()








