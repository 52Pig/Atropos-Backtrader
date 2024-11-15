import pandas as pd
from ..finta import TA
class indicators:
    def __init__(self,data=''):
        '''
        计算技术指标
        '''
        self.data=data
        self.indicators_data=pd.DataFrame()
    def calculating_technical_indicators(self,name='MACD'):
        '''
        技术技术指标
        date一定要利用时间为合并的keys
        '''
        stock_list=list(set(self.data['证券代码'].tolist()))
        for stock in stock_list:
            df=self.data[self.data['证券代码']==stock]
            if df.shape[0]>0:
                func='TA.{}(df)'.format(name)
                indicators=eval(func)
                indicators['date']=df['date']
            try:
                result=pd.merge(df,indicators,on='date')
            except:
                data=pd.DataFrame()
                data[name]=indicators
                data['date']=df['date']
                indicators=data
                result=pd.merge(df,indicators,on='date')
            self.indicators_data=pd.concat([self.indicators_data,result],ignore_index=True)
        return self.indicators_data
    def func_ma_5(self,n=5):
        pass
    def user_def_calculating_technical_indicators(self,columns='close',func_list=['func_ma_5(n=5)','func_ma_5(n=5)'],name_list=['5日均线','10日均线']):
        '''
        自定义的指标
        自己直接该源代码
        columns运行的名称
        func_list函数列表
        name_list函数名称
        '''
        stock_list=list(set(self.data['证券代码'].tolist()))
        for stock in stock_list:
            df=self.data[self.data['证券代码']==stock]
            if df.shape[0]>0:
                for func,name in zip(func_list,name_list):
                    df[name]=df[columns].apply(func)
            self.indicators_data=pd.concat([self.indicators_data,df],ignore_index=True)
        return self.indicators_data
    def user_def_calculating_technical_indicators_data(self,data=''):
        '''
        自己技术的指标数据
        data pandas 数据
        '''
        self.indicators_data=data
        return self.indicators_data
        
            



