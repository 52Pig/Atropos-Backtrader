import pytdx
from pytdx.config import hosts
from pytdx.hq import TdxHq_API
import pandas as pd
from pytdx.reader import base_reader
from pytdx.params import TDXParams
import random
import requests
import json
import random
#通达信数据
class tdx_data(object):
    def __init__(self):
        '''
        当默认的连接不上，随机选择一个连接
        到连接成功
        
        self.df=pd.DataFrame(hosts.hq_hosts)
        self.df.columns=['名称','ip','port']
        self.ip_list=self.df['ip'].tolist()
        self.port_list=self.df['port'].tolist()
        self.name_list=self.df['名称'].tolist()
        self.n=random.randint(0,len(self.name_list))
        self.random_ip=self.ip_list[self.n]
        self.random_port=int(self.port_list[self.n])
        self.random_name=self.name_list[self.n]
        '''
        self.df=pd.DataFrame(hosts.hq_hosts)
        self.df.columns=['name','ip','port']
        self.name_list=self.df['name'].tolist()
        self.ip_list=self.df['ip'].tolist()
        self.port_list=self.df['port'].tolist()
        self.name='招商证券深圳行情'
        self.ip='119.147.212.81'
        self.port=7709
        self.eorr=0
        #self.tdx=TdxHq_API()
        self.api=TdxHq_API()
    def connect(self):
        '''
        连接服务器端口
        '''
        try:
            print('通达信数据连接成功')
            self.api.connect(ip=self.ip,port=self.port)
            return self.api
        except:
            self.next_connect()
    def all_tdx_data(self):
        self.api=TdxHq_API()
        self.api=self.api.connect(ip=self.ip,port=self.port)
        return self.api
    def next_connect(self):
        '''
        如果默认连接不成功使用，一般不用
        '''
        try:
            print('通达信数据连接不成功,随机选择连接')
            n=len(self.name_list)
            #随机选择
            random_name=self.name_list[random.randint(0,n-1)]
            random_port=self.port_list[random.randint(0,n-1)]
            random_ip=self.ip_list[random.randint(0,n-1)]
            self.api.connect(ip=random_ip,port=random_port)
        except:
            random_name=self.name_list[random.randint(0,n-1)]
            random_port=self.port_list[random.randint(0,n-1)]
            random_ip=self.ip_list[random.randint(0,n-1)]
            self.api.connect(ip=random_ip,port=random_port)
    def select_data_type(self,stock='600031'):
        '''
        选择数据类型
        '''
        if stock[:3] in ['110','113','123','127','128','111','118']:
            return 'bond'
        elif stock[:3] in ['510','511','512','513','514','515','516','517','518','588','159','501']:
            return 'fund'
        else:
            return 'stock'
    def adjust_stock(self,stock='600031.SH'):
        '''
        调整代码
        '''
        if stock[-2:]=='SH' or stock[-2:]=='SZ' or stock[-2:]=='sh' or stock[-2:]=='sz':
            stock=stock.upper()
        else:
            if stock[:3] in ['600','601','603','688','510','511',
                             '512','513','515','113','110','118','501'] or stock[:2] in ['11']:
                stock=stock+'.SH'
            else:
                stock=stock+'.SZ'
        return stock
    def rename_stock_type_1(self,stock='600031'):
        '''
        将股票类型格式化
        stock证券代码
        1上海
        0深圳
        '''
        if stock[:3] in ['600','601','603','688','510','511',
                            '512','513','515','113','110','118','501'] or stock[:2] in ['11']:
            marker=1
        else:
            marker=0
        return marker,stock
    def rename_stock_type(self,stock='600031'):
        '''
        将股票类型格式化
        stock证券代码
        1上海
        0深圳
        '''
        if stock[:3] in ['600','601','603','688','510','511',
                            '512','513','515','113','110','118','501'] or stock[:2] in ['11']:
            marker=1
        else:
            marker=0
        result=[(marker,stock)]
        return result
    def marker_type(self,stock='600031'):
        '''
        判断市场类型
        '''
        if stock[:3] in ['600','601','603','688','510','511',
                            '512','513','515','113','110','118','501'] or stock[:2] in ['11']:
            marker=1
        else:
            marker=0
        return marker
    def get_security_quotes_none(self,stock='600031'):
        '''
        
        获取股票行情数据一只
        stock证券代码
        [('market', 0),
              ('code', '000001'),
              ('active1', 2864),
              ('price', 9.19),
              ('last_close', 9.25),
              ('open', 9.23),
              ('high', 9.27),
              ('low', 9.16),
              ('reversed_bytes0', bytearray(b'\xbd\xc9\xec\x0c')),
              ('reversed_bytes1', -919),
              ('vol', 428899),
              ('cur_vol', 30),
              ('amount', 395218880.0),
              ('s_vol', 284703),
              ('b_vol', 144196),
              ('reversed_bytes2', 1),
              ('reversed_bytes3', 698),
              ('bid1', 9.18),
              ('ask1', 9.19),
              ('bid_vol1', 1078),
              ('ask_vol1', 5236),
              ('bid2', 9.17),
              ('ask2', 9.2),
              ('bid_vol2', 8591),
              ('ask_vol2', 3027),
              ('bid3', 9.16),
              ('ask3', 9.21),
              ('bid_vol3', 12638),
              ('ask_vol3', 3557),
              ('bid4', 9.15),
              ('ask4', 9.22),
              ('bid_vol4', 13234),
              ('ask_vol4', 2615),
              ('bid5', 9.14),
              ('ask5', 9.23),
              ('bid_vol5', 5377),
              ('ask_vol5', 6033),
              ('reversed_bytes4', 5768),
              ('reversed_bytes5', 1),
              ('reversed_bytes6', 16),
              ('reversed_bytes7', 83),
              ('reversed_bytes8', 20),
              ('reversed_bytes9', 0),
              ('active2', 2864)])]
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                stock=self.rename_stock_type(stock=stock)
                df=self.api.get_security_quotes(stock)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
        
    def get_security_quotes_more(self,stock_list=['600031','000001']):
        '''
        同时获取多只股票行情数据
        code_list股票列表
        [('market', 0),
              ('code', '000001'),
              ('active1', 2864),
              ('price', 9.19),
              ('last_close', 9.25),
              ('open', 9.23),
              ('high', 9.27),
              ('low', 9.16),
              ('reversed_bytes0', bytearray(b'\xbd\xc9\xec\x0c')),
              ('reversed_bytes1', -919),
              ('vol', 428899),
              ('cur_vol', 30),
              ('amount', 395218880.0),
              ('s_vol', 284703),
              ('b_vol', 144196),
              ('reversed_bytes2', 1),
              ('reversed_bytes3', 698),
              ('bid1', 9.18),
              ('ask1', 9.19),
              ('bid_vol1', 1078),
              ('ask_vol1', 5236),
              ('bid2', 9.17),
              ('ask2', 9.2),
              ('bid_vol2', 8591),
              ('ask_vol2', 3027),
              ('bid3', 9.16),
              ('ask3', 9.21),
              ('bid_vol3', 12638),
              ('ask_vol3', 3557),
              ('bid4', 9.15),
              ('ask4', 9.22),
              ('bid_vol4', 13234),
              ('ask_vol4', 2615),
              ('bid5', 9.14),
              ('ask5', 9.23),
              ('bid_vol5', 5377),
              ('ask_vol5', 6033),
              ('reversed_bytes4', 5768),
              ('reversed_bytes5', 1),
              ('reversed_bytes6', 16),
              ('reversed_bytes7', 83),
              ('reversed_bytes8', 20),
              ('reversed_bytes9', 0),
              ('active2', 2864)])]
        '''
        code_list=stock_list
        stock_list=[]
        for i in code_list:
            stock=self.rename_stock_type(i)
            stock_list.append(stock[0])
        df=self.api.get_security_quotes(all_stock=stock_list)
        result=self.api.to_df(df)
        return result
    def get_security_minute_data(self,n=0,stock='600031',start=0,count=800):
        '''
        获取分钟数据
        n数据类型 
        0 5分钟K线
        1 15分钟K线 
        2 30分钟K线 
        3 1小时K线 
        4 日K线
        7 1分钟
        8 1分钟K线
        marker市场0深圳1上海
        stock证券代码
        start开始位置
        count返回的数据长度
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                marker=self.marker_type(stock=stock)
                df=self.api.get_security_bars(category=n,market=marker,code=stock,start=start,count=count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_security_week_data(self,stock='600031',start=0,count=100):
        '''
        获取股票周线数据
        stock证券代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                n=self.marker_type(stock=stock)
                df=self.api.get_security_bars(5,n,stock,start,count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_security_moth_data(self,stock='600031',start=0,count=100):
        '''
        获取股票月线数据
        stock证券代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                n=self.marker_type(stock=stock)
                df=self.api.get_security_bars(6,n,stock,start,count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_security_daily_data(self,stock='600031',start=0,count=100):
        '''
        获取股票日线数据
        stock证券代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                n=self.marker_type(stock=stock)
                df=self.api.get_security_bars(9,n,stock,start,count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
            
            
    def get_security_quarter_data(self,stock='600031',start=0,count=100):
        '''
        获取股票季线数据
        stock证券代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                n=self.marker_type(stock=stock)
                df=self.api.get_security_bars(10,n,stock,start,count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_security_year_data(self,stock='600031',start=0,count=100):
        '''
        获取股票年线数据
        注意count返回的长度
        stock证券代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                n=self.marker_type(stock=stock)
                df=self.api.get_security_bars(11,n,stock,start,count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_index_minute_data(self,n=7,marker=1,index_code='000001',start=0,count=100):
        '''
        获取指数数据
        n数据类型 0 5分钟K线 
        1 15分钟K线
        2 30分钟K线 
        3 1小时K线 
        4 日K线
        7 1分钟
        8 1分钟K线
        index_code指数代码
        marker市场类型0深圳，1上海
        '''
        i=0
        while i!=1:
            try:
                df=self.api.get_index_bars(category=n,market=marker,code=index_code,start=start,count=count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_index_week_data(self,marker=1,index_code='000001',start=0,count=100):
        '''
        获取指数周线数据
        index_code指数代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                df=self.api.get_security_bars(5,market=marker,code=index_code,start=start,count=count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_index_moth_data(self,marker=1,index_code='000001',start=0,count=100):
        '''
        获取指数月线数据
        index_code指数代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                df=self.api.get_security_bars(6,market=marker,code=index_code,start=start,count=count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_index_daily_data(self,marker=1,index_code='000001',start=0,count=100):
        '''
        获取指数月线数据
        index_code指数代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                df=self.api.get_security_bars(4,market=marker,code=index_code,start=start,count=count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_index_quarter_data(self,marker=1,index_code='000001',start=0,count=100):
        '''
        获取指数季度线数据
        index_code指数代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                df=self.api.get_security_bars(10,market=marker,code=index_code,start=start,count=count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_index_year_data(self,marker=1,index_code='000001',start=0,count=100):
        '''
        获取指数周线数据
        index_code指数代码
        count返回长度
        '''
        i=0
        while i!=1:
            try:
                df=self.api.get_security_bars(11,market=marker,code=index_code,start=start,count=count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_minute_time_data(self,stock='600031'):
        '''
        查询分时行情
        stock证券代码
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                n=self.marker_type(stock=stock)
                df=self.api.get_minute_time_data(market=n,code=stock)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def marker_params(self,stock='600031'):
        if stock[:3] in ['600','601','603','688','510','511',
                            '512','513','515','113','110','118','501'] or stock[:2] in ['11']:
            marker=1
        else:
            marker=0
        return marker
    def get_history_minute_time_data(self,stock='600031',date='20220920'):
        '''
        查询历史分时行情
        stock证券代码
        date交易日
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                market=self.marker_params(stock)
                df=self.api.get_history_minute_time_data(market=market,code=stock,date=date)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.connect()
    def get_trader_data(self,stock='600031',start=0,count=10000):
        '''
        查询分笔成交
        stock证券代码
        start开始位置
        count结束位置
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                market=self.marker_params(stock=stock)
                df=self.api.get_transaction_data(market=market,code=stock,start=start,count=count)
                result=self.api.to_df(df)
                i=1
                return result
            except:
               self.connect()
    def get_history_trader_data(self,stock='600031',start=0,count=100,date='20220920'):
        '''
        查询流逝分笔成交
        stock证券代码
        start开始位置
        count结束位置
        date时间
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                marker=self.marker_params(stock=stock)
                df=self.api.get_history_transaction_data(market=marker,code=stock,start=start,count=count,date=date)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_company_info_category(self,stock='600031'):
        '''
        查询公司信息目录
        stock证券代码
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                marker=self.marker_params(stock=stock)
                df=self.api.get_company_info_category(market=marker,code=stock)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_xdxr_info(self,stock='600031'):
        '''
        读取除权除息信息
        stock证券代码
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                marker=self.marker_params(stock=stock)
                df=self.api.get_xdxr_info(marker=marker,code=stock)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_finance_info(self,stock='600031'):
        '''
        读取财务信息
        stock证券代码
        '''
        i=0
        while i!=1:
            try:
                stock=stock[:6]
                marker=self.marker_params(stock=stock)
                df=self.api.get_finance_info(marker=marker,code=stock)
                result=self.api.to_df(df)
                i=1
                return result
            except:
                self.next_connect()
    def get_stock_hist_data_em(self,stock='600031',start_date='20210105',end_date='20500101',data_type='D'):
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
        klt=data_dict[data_type]
        if stock[0] =='6':
            stock = '1.' +stock
        else:
            stock = '0.' + stock
        url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?'
        params = {
            'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'beg': start_date,
            'end': end_date,
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'rtntype':end_date,
            'secid': stock,
            'klt':klt,
            'fqt': '0',
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