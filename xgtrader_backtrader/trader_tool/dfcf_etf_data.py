import pandas as pd
import json

import requests
class dfcf_etf_data:
    def __init__(self):
        '''
        东方财富数据
        '''
        pass
    def get_all_etf_data(self,ps=1000):
        '''
        获取全部的etf数据
        '''
        params={
            'type': 'RPTA_APP_FUNDSELECT',
            'sty': 'ETF_TYPE_CODE,SECUCODE,SECURITY_CODE,CHANGE_RATE_1W,CHANGE_RATE_1M,CHANGE_RATE_3M,YTD_CHANGE_RATE,DEC_TOTALSHARE,DEC_NAV,SECURITY_NAME_ABBR,DERIVE_INDEX_CODE,INDEX_CODE,INDEX_NAME,NEW_PRICE,CHANGE_RATE,CHANGE,VOLUME,DEAL_AMOUNT,PREMIUM_DISCOUNT_RATIO,QUANTITY_RELATIVE_RATIO,HIGH_PRICE,LOW_PRICE,STOCK_ID,PRE_CLOSE_PRICE',
            'extraCols':'' ,
            'source': 'FUND_SELECTOR',
            'client': 'APP',
            'sr': '-1,-1,1',
            'st': 'CHANGE_RATE,CHANGE,SECURITY_CODE',
            'filter': '(ETF_TYPE_CODE="ALL")',
            'extraCols': '',
            'p': '1',
            'ps':ps,
            'isIndexFilter': '1'
        }
        url='https://datacenter.eastmoney.com/stock/fundselector/api/data/get?'
        res=requests.get(url=url,params=params)
        text=res.json()
        df=pd.DataFrame(text['result']['data'])
        columns=['_','_','基金代码','周涨跌幅','月涨跌幅','3月涨跌幅','年涨跌幅','市值','现在市值',
        '基金名称','_','_','主题',"价格",'涨跌幅','涨跌额','成交量','成交额','折价率','_',
        "最高价",'最低价','_','前收盘价']
        df.columns=columns
        df['折价率']=df['折价率'].replace('-',0)
        df['折价率']=df['折价率'].astype(float)
        df['溢价率']=0-df['折价率']
        del df['_']
        return df
    def get_all_etf_data_1(self):
        '''
        获取全部的etf数据
        '''
        
        url='https://datacenter.eastmoney.com/securities/api/data/get?sty=SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR&source=FUND_SELECTOR&client=APP&p=1&ps=1000&sr=-1,1&st=f402,SECURITY_CODE&filter=&extraCols=f2~09~SECURITY_CODE~f2,f148~09~SECURITY_CODE~f148,f3~09~SECURITY_CODE~f3,f402~09~SECURITY_CODE~f402,f14~09~SECURITY_CODE~f14,f4~09~SECURITY_CODE~f4&p=1&ps=10&type=RPT_FUND_ETFLIST'
        res=requests.get(url=url)
        text=res.json()
        df=pd.DataFrame(text['result']['data'])
        df.columns=['证券代码','基金代码','基金名称','最新价','市场','涨跌幅','折价率','主题','涨跌额']
        df['折价率']=df['折价率'].replace('-',0)
        df['溢价率']=0-df['折价率'].astype(float)
        return df
    def get_sz_sh_etf(self,ps=1000):
        '''
        沪深ETF
        '''
        params={
            'type': 'RPTA_APP_FUNDSELECT',
            'sty': 'ETF_TYPE_CODE,SECUCODE,SECURITY_CODE,CHANGE_RATE_1W,CHANGE_RATE_1M,CHANGE_RATE_3M,YTD_CHANGE_RATE,DEC_TOTALSHARE,DEC_NAV,SECURITY_NAME_ABBR,DERIVE_INDEX_CODE,INDEX_CODE,INDEX_NAME,NEW_PRICE,CHANGE_RATE,CHANGE,VOLUME,DEAL_AMOUNT,PREMIUM_DISCOUNT_RATIO,QUANTITY_RELATIVE_RATIO,HIGH_PRICE,LOW_PRICE,STOCK_ID,PRE_CLOSE_PRICE',
            'extraCols':'' ,
            'source': 'FUND_SELECTOR',
            'client': 'APP',
            'sr': '-1,-1,1',
            'st': 'CHANGE_RATE,CHANGE,SECURITY_CODE',
            'filter': '(ETF_TYPE_CODE in ("006","007","008"))',
            'extraCols': '',
            'p': '1',
            'ps':ps,
            'isIndexFilter': '1'
        }
        url='https://datacenter.eastmoney.com/stock/fundselector/api/data/get?'
        res=requests.get(url=url,params=params)
        text=res.json()
        df=pd.DataFrame(text['result']['data'])
        columns=['_','_','基金代码','周涨跌幅','月涨跌幅','3月涨跌幅','年涨跌幅','市值','现在市值',
        '基金名称','_','_','主题',"价格",'涨跌幅','涨跌额','成交量','成交额','折价率','_',
        "最高价",'最低价','_','前收盘价']
        df.columns=columns
        df['折价率']=df['折价率'].replace('-',0)
        df['折价率']=df['折价率'].astype(float)
        df['溢价率']=0-df['折价率']
        del df['_']
        return df
    def get_wp_etf_data(self,ps=1000):
        '''
        外盘etf
        '''
        params={
            'type': 'RPTA_APP_FUNDSELECT',
            'sty': 'ETF_TYPE_CODE,SECUCODE,SECURITY_CODE,CHANGE_RATE_1W,CHANGE_RATE_1M,CHANGE_RATE_3M,YTD_CHANGE_RATE,DEC_TOTALSHARE,DEC_NAV,SECURITY_NAME_ABBR,DERIVE_INDEX_CODE,INDEX_CODE,INDEX_NAME,NEW_PRICE,CHANGE_RATE,CHANGE,VOLUME,DEAL_AMOUNT,PREMIUM_DISCOUNT_RATIO,QUANTITY_RELATIVE_RATIO,HIGH_PRICE,LOW_PRICE,STOCK_ID,PRE_CLOSE_PRICE',
            'extraCols':'' ,
            'source': 'FUND_SELECTOR',
            'client': 'APP',
            'sr': '-1,-1,1',
            'st': 'CHANGE_RATE,CHANGE,SECURITY_CODE',
            'filter': '(ETF_TYPE_CODE="002")',
            'extraCols': '',
            'p': '1',
            'ps':ps,
            'isIndexFilter': '1'
        }
        url='https://datacenter.eastmoney.com/stock/fundselector/api/data/get?'
        res=requests.get(url=url,params=params)
        text=res.json()
        df=pd.DataFrame(text['result']['data'])
        columns=['_','_','基金代码','周涨跌幅','月涨跌幅','3月涨跌幅','年涨跌幅','市值','现在市值',
        '基金名称','_','_','主题',"价格",'涨跌幅','涨跌额','成交量','成交额','折价率','_',
        "最高价",'最低价','_','前收盘价']
        df.columns=columns
        df['溢价率']=0-df['折价率']
        del df['_']
        return df
    def get_bond_etf_data(self,ps=1000):
        '''
        债券etf
        '''
        params={
            'type': 'RPTA_APP_FUNDSELECT',
            'sty': 'ETF_TYPE_CODE,SECUCODE,SECURITY_CODE,CHANGE_RATE_1W,CHANGE_RATE_1M,CHANGE_RATE_3M,YTD_CHANGE_RATE,DEC_TOTALSHARE,DEC_NAV,SECURITY_NAME_ABBR,DERIVE_INDEX_CODE,INDEX_CODE,INDEX_NAME,NEW_PRICE,CHANGE_RATE,CHANGE,VOLUME,DEAL_AMOUNT,PREMIUM_DISCOUNT_RATIO,QUANTITY_RELATIVE_RATIO,HIGH_PRICE,LOW_PRICE,STOCK_ID,PRE_CLOSE_PRICE',
            'extraCols':'' ,
            'source': 'FUND_SELECTOR',
            'client': 'APP',
            'sr': '-1,-1,1',
            'st': 'CHANGE_RATE,CHANGE,SECURITY_CODE',
            'filter': '(ETF_TYPE_CODE="003")',
            'extraCols': '',
            'p': '1',
            'ps':ps,
            'isIndexFilter': '1'
        }
        url='https://datacenter.eastmoney.com/stock/fundselector/api/data/get?'
        res=requests.get(url=url,params=params)
        text=res.json()
        df=pd.DataFrame(text['result']['data'])
        columns=['_','_','基金代码','周涨跌幅','月涨跌幅','3月涨跌幅','年涨跌幅','市值','现在市值',
        '基金名称','_','_','主题',"价格",'涨跌幅','涨跌额','成交量','成交额','折价率','_',
        "最高价",'最低价','_','前收盘价']
        df.columns=columns
        df['折价率']=df['折价率'].replace('-',0)
        df['折价率']=df['折价率'].astype(float)
        df['溢价率']=0-df['折价率']
        del df['_']
        return df
    def get_sp_etf_data(self,ps=1000):
        '''
        商品etf
        '''
        params={
            'type': 'RPTA_APP_FUNDSELECT',
            'sty': 'ETF_TYPE_CODE,SECUCODE,SECURITY_CODE,CHANGE_RATE_1W,CHANGE_RATE_1M,CHANGE_RATE_3M,YTD_CHANGE_RATE,DEC_TOTALSHARE,DEC_NAV,SECURITY_NAME_ABBR,DERIVE_INDEX_CODE,INDEX_CODE,INDEX_NAME,NEW_PRICE,CHANGE_RATE,CHANGE,VOLUME,DEAL_AMOUNT,PREMIUM_DISCOUNT_RATIO,QUANTITY_RELATIVE_RATIO,HIGH_PRICE,LOW_PRICE,STOCK_ID,PRE_CLOSE_PRICE',
            'extraCols':'' ,
            'source': 'FUND_SELECTOR',
            'client': 'APP',
            'sr': '-1,-1,1',
            'st': 'CHANGE_RATE,CHANGE,SECURITY_CODE',
            'filter': '(ETF_TYPE_CODE="004")',
            'extraCols': '',
            'p': '1',
            'ps':ps,
            'isIndexFilter': '1'
        }
        url='https://datacenter.eastmoney.com/stock/fundselector/api/data/get?'
        res=requests.get(url=url,params=params)
        text=res.json()
        df=pd.DataFrame(text['result']['data'])
        columns=['_','_','基金代码','周涨跌幅','月涨跌幅','3月涨跌幅','年涨跌幅','市值','现在市值',
        '基金名称','_','_','主题',"价格",'涨跌幅','涨跌额','成交量','成交额','折价率','_',
        "最高价",'最低价','_','前收盘价']
        df.columns=columns
        df['折价率']=df['折价率'].replace('-',0)
        df['折价率']=df['折价率'].astype(float)
        df['溢价率']=0-df['折价率']
        del df['_']
        return df
    def get_hot_spot_investment(self,pageSize=100):
        '''
        热点投资
        '''
        params={
            'reportName': 'RPT_FUND_GLLIST',
            'columns': 'BOARD_CODE,BOARD_NAME',
            'quoteColumns': 'f3~05~BOARD_CODE~BOARD_YILED,f127~05~BOARD_CODE~BOARD_YILED_3DAYS',
            'filter':'' ,
            'distinct': 'BOARD_CODE',
            'pageNumber': '1',
            'pageSize': pageSize,
            'sortTypes': '-1',
            'sortColumns': 'BOARD_YILED',
            'source': 'SECURITIES',
            'client': 'APP',
        }
        url='https://datacenter.eastmoney.com/securities/api/data/v1/get?'
        res=requests.get(url=url,params=params)
        text=res.json()
        df=pd.DataFrame(text['result']['data'])
        df.columns=['行业代码','行业名称','涨跌幅','3天涨跌幅']
        return df
    def get_hot_spot_investment_etf(self,code='BK0437'):
        '''
        热门投资的etf
        '''
        params={
            'reportName': 'RPT_FUND_GLLIST',
            'columns':'SECURITY_INNER_CODE,SECURITY_CODE,BOARD_CODE,BOARD_NAME,SECUCODE,SECURITY_NAME_ABBR,IS_MARGININFO',
            'quoteColumns': 'f148~09~SECURITY_CODE~STOCK_ID,f2~09~SECURITY_CODE~FUND_NEW,f3~09~SECURITY_CODE~FUND_YILED,f6~09~SECURITY_CODE~FUND_AMOUNT,f3~05~BOARD_CODE~BOARD_YILED,f127~05~BOARD_CODE~BOARD_YILED_3DAYS',
            'filter': '(BOARD_CODE="{}")'.format(code),
            'pageNumber': '1',
            'pageSize': '8',
            'sortTypes': '-1',
            'sortColumns': 'FUND_AMOUNT',
            'source': 'SECURITIES',
            'client': 'APP'
        }
        url='https://datacenter.eastmoney.com/securities/api/data/v1/get?'
        res=requests.get(url=url,params=params)
        text=res.json()
        df=pd.DataFrame(text['result']['data'])
        return df