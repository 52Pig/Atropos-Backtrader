import pandas as pd
import json
import requests
class ths_rq:
    def __init__(self):
        '''
        同花顺人气
        '''
        pass
    def get_headers(self):
        '''
        请求头
        '''
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        }
        return headers

    def get_hot_stock_rank(self,data_type='大家都在看',date='hour'):
        '''
        同花顺热股排行
        data_dict={'大家都在看':'normal','快速飙升中':'skyrocket',
                   "技术交易派":"tech",'价值投资派':'value','趋势投资派':'trend'}
        date=hour 1小时实时数据
        data=day 1天实时数据
        只是，快速飙升中，大家都在看才有小时数据
        '''
        data_dict={'大家都在看':'normal','快速飙升中':'skyrocket',
                   "技术交易派":"tech",'价值投资派':'value','趋势投资派':'trend'}
        list_type=data_dict[data_type]
        if list_type=='normal' and date=='hour':
            Type='hour'
        elif list_type=='skyrocket' and date=='hour':
            Type='hour'
        if list_type=='normal' and date=='day':
            Type='day'
        elif list_type=='skyrocket' and date=='day':
            Type='hour'
        elif list_type=='tech':
            Type='day'
        elif list_type=='value':
            Type='day'
        elif list_type=='trend':
            Type='day'
        else:
            pass
        url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/stock?'
        params={
            'stock_type': 'a',
            'type': Type,
            'list_type': list_type
        }
        headers=self.get_headers()
        
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        status_code=text['status_code']
        if status_code==0:
            try:
                df=pd.DataFrame(text['data']['stock_list'])
                columns=['市场','证券代码','热度','涨跌幅','股票名称',
                        '分析','热度变化','目标','排序','分析主题']
                df.columns=columns
                return df
            except:
                df=pd.DataFrame(text['data']['stock_list'])
                columns=['市场','证券代码','热度','涨跌幅','股票名称',
                        '分析','热度变化','目标','排序','分析主题','更新时间']
                df.columns=columns
                return df
        else:
            print('{}获取失败'.format(data_type))
            return False
    def get_stock_concept_rot_rank(self):
        '''
        获取股票概念热度排行
        '''
        url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/plate?'
        params={
            'type': 'concept'
        }
        headers=self.get_headers()
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        status_code=text['status_code']
        if int(status_code)==0:
            df=pd.DataFrame(text['data']['plate_list'])
            #columns=['热度','概念代码','涨跌幅','上榜统计','热度变化',
                     #'市场id','概念名称','概念统计','排序','etf_rise_and_fall',
                     #'etf_product_id','etf_name','etf_market_id']
            df=df.rename(columns={"code":"概念代码","name":"概念名称"})
            #df.columns=columns
            return df
        else:
            print('获取失败')
            return False
    def get_stock_industry_rot_rank(self):
        '''
        获取股票行业热度排行
        '''
        url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/plate?'
        params={
            'type': 'industry'
        }
        headers=self.get_headers()
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        status_code=text['status_code']
        if status_code==0:
            df=pd.DataFrame(text['data']['plate_list'])
            columns=['行业代码','热度','涨跌幅','行业名称','热度变化',
                     '市场id','上榜统计','行业统计','排序','etf_rise_and_fall',
                     'etf_product_id','etf_name','etf_market_id']
            df.columns=columns
            return df
        else:
            print('获取失败')
            return False
    def get_etf_hot_rank(self):
        '''
        ETF热度排行
        '''
        url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/etf'
        headers=self.get_headers()
        res=requests.get(url=url,headers=headers)
        text=res.json()
        status_code=text['status_code']
        if status_code==0:
            df=pd.DataFrame(text['data']['list'])
            columns=['市场','代码','热度','涨跌幅','名称']
            df.columns=columns
            return df
        else:
            print('获取失败')
            return False
    def get_cov_bond_rot_rank(self):
        '''
        可转债热度排行
        '''
        headers=self.get_headers()
        try:
            url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/bond'
            res=requests.get(url=url,headers=headers)
            text=res.json()
            status_code=text['status_code']
            if status_code==0:
                df=pd.DataFrame(text['data'])
                columns=['市场','代码','涨跌幅','名称','热度','排行']
                df.columns=columns
                return df
            else:
                print('获取失败')
                return False
        except:
            url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/bond'
            res=requests.get(url=url,headers=headers)
            text=res.json()
            status_code=text['status_code']
            if status_code==0:
                df=pd.DataFrame(text['data'])
                columns=['市场','代码','涨跌幅','名称','热度','排行']
                df.columns=columns
                return df
            else:
                print('获取失败')
                return False
        
    def get_HK_stock_rot_rank(self):
        '''
        港股热度排行
        '''
        headers=self.get_headers()
        url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/stock?'
        params={
            'stock_type': 'hk',
            'type': 'day',
            'list_type': 'normal'
        }
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        status_code=text['status_code']
        if status_code==0:
            df=pd.DataFrame(text['data']['stock_list'])
            columns=['市场','代码','热度','涨跌幅','名称','排行']
            df.columns=columns
            return df
        else:
            print('获取失败')
            return False
    def get_US_stock_rot_rank(self):
        '''
        美股热度排行
        '''
        headers=self.get_headers()
        url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/stock?'
        params={
            'stock_type': 'usa',
            'type': 'day',
            'list_type': 'normal'
        }
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        status_code=text['status_code']
        if status_code==0:
            df=pd.DataFrame(text['data']['stock_list'])
            columns=['市场','代码','热度','涨跌幅','名称','排行']
            df.columns=columns
            return df
        else:
            print('获取失败')
            return False
    def get_futurn_hot_rank(self):
        '''
        热期货排行
        '''
        headers=self.get_headers()
        url='https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/future'
        res=requests.get(url=url,headers=headers)
        text=res.json()
        status_code=text['status_code']
        if status_code==0:
            df=pd.DataFrame(text['data']['futures_list'])
            print(df)
            columns=['市场','代码','热度','涨跌幅','名称','相关股票','基金','排名']
            df.columns=columns
            return df
        else:
            print('获取失败')
            return False
    def get_hot_fund_rank(self):
        '''
        热基金排行
        '''
        url=' https://ai.iwencai.com/index/urp/getdata/basic?tag=%E5%90%8C%E8%8A%B1%E9%A1%BA%E7%83%AD%E6%A6%9C_%E7%83%AD%E5%9F%BA&userid=0&appName=thsHotList&filter=%7B%22offset%22:0,%22limit%22:100,%22sort%22:[[%22list_rank_1d%22,%22ASC%22]],%22where%22:%7B%22list_rank_1d%22:%7B%22$lte%22:200%7D,%22class_name%22:%7B%22$eq%22:%22%E4%BA%BA%E6%B0%94%22%7D%7D%7D&hexin-v=AxsaHFel-wYuJAfywpP3WvRFqnSW8C80KQTzpg1Y95ox7DVqlcC_QjnUg_8e'
        res=requests.get(url=url)
        print(res.text)
if __name__=='__main__':
    #同花顺热度排行
    data=ths_rq()
    #同花顺热度排行
    df5=data.get_cov_bond_rot_rank()
    print(df5)
    '''
    df1=data.get_hot_stock_rank()
    print(df1)
    df1.to_excel(r'同花顺热度排行.xlsx')
    #概念热度排行
    df2=data.get_stock_concept_rot_rank()
    print(df2)
    df2.to_excel(r'概念热度排行.xlsx')
    #行业热度排行
    df3=data.get_stock_industry_rot_rank()
    print(df3)
    df3.to_excel(r'行业热度排行.xlsx')
    #ETF热度排行
    df4=data.get_etf_hot_rank()
    print(df4)
    df4.to_excel(r'ETF热度排行.xlsx')
    #可转债热度排行
    print(df5)
    df5.to_excel(r'可转债热度排行.xlsx')
    #港股热度排行
    df6=data.get_HK_stock_rot_rank()
    print(df6)
    df6.to_excel(r'港股热度排行.xlsx')
    #美股热度排行
    df7=data.get_HK_stock_rot_rank()
    print(df7)
    df7.to_excel(r'美股热度排行.xlsx')
    #期货热度排行
    df8=data.get_futurn_hot_rank()
    print(df8)
    p=df8.to_excel(r'期货热度排行.xlsx')
    '''
    a=ths_rq()
    a.get_cov_bond_rot_rank()