import requests
import json
import pandas as pd
from tqdm import tqdm
class dfcf_theme:
    def __init__(self) -> None:
        pass
    def market_style(self,n='3'):
        '''
        市场风格
        '''
        data_dict={'1':'fenggeindex','3':'fengge/3','5':'fengge/3'}
        url='https://quote.eastmoney.com/zhuti/api/{}'.format(data_dict[n])
        res=requests.get(url=url)
        text=res.json()
        df=pd.DataFrame(text['result'][0]['MarketStyle'])
        return df
    def today_opportunity(self):
        '''
        今日机会
        '''
        url='https://quote.eastmoney.com/zhuti/api/todayopportunity'
        res=requests.get(url=url)
        text=res.json()
        text1=text['result'][0]['Data']
        result=[]
        for i in text1:
            data_list=i.split('|')
            result.append(data_list)
        df=pd.DataFrame(result)
        columns=['涨跌幅','代码','题材','3','概念','题材1','新闻',
                 '证券代码','股票名称','9','10','11','12','13','14']
        df.columns=columns
        return df
    def recet_hot(self):
        '''
        最近热点
        '''
        url='https://quote.eastmoney.com/zhuti/api/recenthot'
        res=requests.get(url=url)
        text=res.json()
        text1=text['result'][0]['Data']
        result=[]
        for i in text1:
            data_list=i.split('|')
            result.append(data_list)
        df=pd.DataFrame(result)
        columns=['代码','题材','2','3','涨跌幅','证券代码','股票名称','7','8']
        df.columns=columns
        return df
    def hot_theme(self):
        '''
        热门主题
        '''
        url='https://quote.eastmoney.com/zhuti/api/hottheme?'
        params={
            'startIndex':'1',
            'pageSize':'20000000',
        }
        res=requests.get(url=url,params=params)
        text=res.json()
        text1=text['result'][0]['Data']
        result=[]
        for i in text1:
            data_list=i.split('|')
            result.append(data_list)
        df=pd.DataFrame(result)
        columns=['代码','题材','2','3','涨跌幅','证券代码','股票名称','7','8']
        df.columns=columns
        return df
    def return_dict(self,df):
        '''
        返回字典
        '''
        stock_dict=dict(zip(df['题材'].tolist(),df['证券代码'].tolist()))
        return stock_dict
    def today_opportunity_stock(self,name='代糖概念'):
        '''
        今日机会成分股
        '''
        df=self.today_opportunity()
        stock_dict=self.return_dict(df=df)
        code=stock_dict[name]
        url='http://quote.eastmoney.com/zhuti/api/themerelatestocks?'
        params={
            'CategoryCode': code,
            'startIndex': '1',
            'pageSize':'200000000',
        }
        res=requests.get(url=url,params=params)
        text=res.json()
        text1=text['result'][0]['Data']
        result=[]
        for i in text1:
            data_list=i.split('|')
            result.append(data_list)
        df=pd.DataFrame(result)
        columns=['题材代码','证券代码','股票名称','3','入选理由',
                 '理由','6','最新价','涨跌幅','9']
        df.columns=columns
        df['题材']=name
        text2=text['result'][1]['Data']
        stats_dict=dict(zip(['上涨','下跌','平'],text2[0].split('|')))
        theme_qd=float(stats_dict['上涨'])/(float(stats_dict['上涨'])+float(stats_dict['下跌'])+float(stats_dict['平']))
        stats_dict['题材强度']=theme_qd
        return df,stats_dict
    def recet_hot_stock(self,name='太阳能'):
        '''
        最近热点成分股
        '''
        df=self.recet_hot()
        stock_dict=self.return_dict(df=df)
        code=stock_dict[name]
        url='http://quote.eastmoney.com/zhuti/api/themerelatestocks?'
        params={
            'CategoryCode':code,
            'startIndex':'1',
            'pageSize':'20000000',
        }
        res=requests.get(url=url,params=params)
        text=res.json()
        text1=text['result'][0]['Data']
        result=[]
        for i in text1:
            data_list=i.split('|')
            result.append(data_list)
        df=pd.DataFrame(result)
        columns=['题材代码','证券代码','股票名称','3','入选理由',
                 '5','6,','最新价','涨跌幅','统计']
        df.columns=columns
        df['题材']=name
        text2=text['result'][1]['Data']
        stats_dict=dict(zip(['上涨','下跌','平'],text2[0].split('|')))
        theme_qd=float(stats_dict['上涨'])/(float(stats_dict['上涨'])+float(stats_dict['下跌'])+float(stats_dict['平']))
        stats_dict['题材强度']=theme_qd
        return df,stats_dict
    def hot_theme_stock(self,name='锗'):
        '''
        热门主题成分股
        '''
        df=self.hot_theme()
        stock_dict=self.return_dict(df=df)
        code=stock_dict[name]
        url='http://quote.eastmoney.com/zhuti/api/themerelatestocks?'
        params={
            'CategoryCode':code,
            'startIndex':'1',
            'pageSize':'2000000',
        }
        res=requests.get(url=url,params=params)
        text=res.json()
        text1=text['result'][0]['Data']
        result=[]
        for i in text1:
            data_list=i.split('|')
            result.append(data_list)
        df=pd.DataFrame(result)
        columns=['题材代码','证券代码','股票名称','3','入选理由',
                 '5','6,','最新价','涨跌幅','统计']
        df.columns=columns
        df['题材']=name
        text2=text['result'][1]['Data']
        stats_dict=dict(zip(['上涨','下跌','平'],text2[0].split('|')))
        theme_qd=float(stats_dict['上涨'])/(float(stats_dict['上涨'])+float(stats_dict['下跌'])+float(stats_dict['平']))
        stats_dict['题材强度']=theme_qd
        return df,stats_dict
    def hot_them_rank_analysis(self,n=100):
        '''
        热门主题分析排序
        '''
        df=self.hot_theme()[:n]
        name_list=df['题材'].tolist()
        #上涨
        up_list=[]
        #下跌
        down_list=[]
        #平
        p_list=[]
        #题材强度
        qd_list=[]
        for i in tqdm(range(len(name_list))):
            name=name_list[i]
            try:
                df1,stats_dict=self.hot_theme_stock(name=name)
                up=stats_dict['上涨']
                down=stats_dict['下跌']
                p=stats_dict['平']
                qd=stats_dict['题材强度']
                up_list.append(up)
                down_list.append(down)
                p_list.append(p)
                qd_list.append(qd)
            except:
                print('{}有问题'.format(name))
                up_list.append(None)
                down_list.append(None)
                p_list.append(None)
                qd_list.append(None)
        df['上涨']=up_list
        df['下跌']=down_list
        df['平']=p_list
        df['题材强度']=qd_list
        df.to_excel(r'热门主题.xlsx')
        return df
    def hot_them_stock_analysis(self,n=100):
        '''
        热门题材成分股分析
        '''
        df=self.hot_theme()[:n]
        name_list=df['题材'].tolist()
        data=pd.DataFrame()
        for i in tqdm(range(len(name_list))):
            name=name_list[i]
            try:
                df1,stats_dict=self.hot_theme_stock(name=name)
                data=pd.concat([data,df1],ignore_index=True)
            except:
                print('{}有问题'.format(name))
        return data
    def today_opportunity_rank_analysis(self):
        '''
        今日机会排行分析
        '''
        df=self.today_opportunity()
        name_list=df['题材'].tolist()
        #上涨
        up_list=[]
        #下跌
        down_list=[]
        #平
        p_list=[]
        #题材强度
        qd_list=[]
        for i in tqdm(range(len(name_list))):
            name=name_list[i]
            try:
                df1,stats_dict=self.today_opportunity_stock(name=name)
                up=stats_dict['上涨']
                down=stats_dict['下跌']
                p=stats_dict['平']
                qd=stats_dict['题材强度']
                up_list.append(up)
                down_list.append(down)
                p_list.append(p)
                qd_list.append(qd)
            except:
                print('{}有问题'.format(name))
                up_list.append(None)
                down_list.append(None)
                p_list.append(None)
                qd_list.append(None)
        df['上涨']=up_list
        df['下跌']=down_list
        df['平']=p_list
        df['题材强度']=qd_list
        return df
    def today_opportunity_stock_analysis(self):
        '''
        热门题材成分股分析
        '''
        df=self.today_opportunity()
        name_list=df['题材'].tolist()
        data=pd.DataFrame()
        for i in tqdm(range(len(name_list))):
            name=name_list[i]
            try:
                df1,stats_dict=self.today_opportunity_stock(name=name)
                data=pd.concat([data,df1],ignore_index=True)
            except:
                print('{}有问题'.format(name))
        return data
    def recet_hot_rank_analysis(self):
        '''
        最近热点排行分析
        '''
        df=self.recet_hot()
        name_list=df['题材'].tolist()
        #上涨
        up_list=[]
        #下跌
        down_list=[]
        #平
        p_list=[]
        #题材强度
        qd_list=[]
        for i in tqdm(range(len(name_list))):
            name=name_list[i]
            try:
                df1,stats_dict=self.recet_hot_stock(name=name)
                up=stats_dict['上涨']
                down=stats_dict['下跌']
                p=stats_dict['平']
                qd=stats_dict['题材强度']
                up_list.append(up)
                down_list.append(down)
                p_list.append(p)
                qd_list.append(qd)
            except:
                print('{}有问题'.format(name))
                up_list.append(None)
                down_list.append(None)
                p_list.append(None)
                qd_list.append(None)
        df['上涨']=up_list
        df['下跌']=down_list
        df['平']=p_list
        df['题材强度']=qd_list
        return df
    def recet_hot_stock_analysis(self):
        '''
        最近热点成分股分析
        '''
        df=self.recet_hot()
        name_list=df['题材'].tolist()
        data=pd.DataFrame()
        for i in tqdm(range(len(name_list))):
            name=name_list[i]
            try:
                df1,stats_dict=self.recet_hot_stock(name=name)
                data=pd.concat([data,df1],ignore_index=True)
            except:
                print('{}有问题'.format(name))
        return data
