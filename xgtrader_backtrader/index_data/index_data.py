import pandas as pd
import requests
import json
class index_data:
    def __init__(self,stock='000300',start_date='20200101',end_date='20500101',data_type='D'):
        '''
        获取指数数据
        '''
        self.stock=stock
        self.start_date=start_date
        self.start_date=start_date
        self.end_date=end_date
        self.data_type=data_type
    def get_index_hist_data(self,):
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
            klt=data_dict[self.data_type]
            url='http://41.push2his.eastmoney.com/api/qt/stock/kline/get?'
            params={
                #cb: jQuery351024921066704183614_1689062296597
                'secid': '1.'+self.stock,
                'ut':'fa5fd1943c7b386f172d6893dbfba10b',
                'fields1':'f1,f2,f3,f4,f5,f6',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'klt':klt,
                'fqt': '1',
                'beg':self.start_date,
                'end': self.end_date,
                #'lmt':'12',
                '_': '1689062296608'
            }
            res=requests.get(url=url,params=params)
            json_text = res.json()
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
                data.sort_index(ascending=True,ignore_index=True,inplace=True)
                return data
            except:
                params={
                #cb: jQuery351024921066704183614_1689062296597
                'secid': '0.'+self.stock,
                'ut':'fa5fd1943c7b386f172d6893dbfba10b',
                'fields1':'f1,f2,f3,f4,f5,f6',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'klt':klt,
                'fqt': '1',
                'beg':self.start_date,
                'end': self.end_date,
                #'lmt':'12',
                '_': '1689062296608'
            }
            res=requests.get(url=url,params=params)
            json_text = res.json()
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
                data.sort_index(ascending=True,ignore_index=True,inplace=True)
                return data
            except:
                pass
if __name__=='__main__':
    models=index_data()
    print(models.get_index_hist_data())