from ..trader_tool.unification_data import unification_data
from tqdm import tqdm
from threading import Thread
import pandas as pd
class user_def_data:
    def __init__(self,start_date='20210105',end_date='20230101',data_type='D'):
        '''
        数据源支持股票/可转债/etf
        data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
        数据格式
          date   open  close   high    low   volume           成交额    振幅   涨跌幅   涨跌额   换手率    证券代码
        0    2021-01-04  34.04  33.59  34.80  33.19  1027586  3.603294e+09  4.77 -0.53 -0.18  1.21  600031
        1    2021-01-05  33.30  35.34  35.59  33.09  1072169  3.824581e+09  7.44  5.21  1.75  1.26  600031
        2    2021-01-06  35.37  35.75  36.25  34.79  1097482  4.029568e+09  4.13  1.16  0.41  1.29  600031
        3    2021-01-07  36.29  39.18  39.45  36.07  1401786  5.461736e+09  9.45  9.59  3.43  1.65  600031
        4    2021-01-08  39.18  39.16  40.17  37.80  1459535  5.862015e+09  6.05 -0.05 -0.02  1.72  600031
        '''
        self.data_type=data_type
        self.start_date=start_date
        self.end_date=end_date
        self.unification_data=unification_data(trader_tool='ths')
        self.data=self.unification_data.get_unification_data()
        self.hist=pd.DataFrame()
        #通过这个结算收益
        self.hist_return=dict()
    def get_add_data(self,stock='600031'):
        '''
        添加数据自带数据
        '''
        try:
            df=self.data.get_hist_data_em(stock=stock,start_date=self.start_date,end_date=self.end_date,data_type=self.data_type)
            df['stock']=stock
            self.hist=pd.concat([self.hist,df],ignore_index=True)
            print('{}数据建立成功'.format(stock))
            self.hist_return[stock]=dict(zip(df['date'],df['涨跌幅']/100))
            return self.hist
        except:
            print('{}数据建立失败'.format(stock))
    def get_thread_add_data(self,stock_list=['600031','600111']):
        '''
        添加数据自带数据
        多线程
        stock_list股票列表
        '''
        thread_list=[]
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            t=Thread(target=self.get_add_data, args=(stock,))
            thread_list.append(t)
        #启动全部
        for j in thread_list:
            j.start()
        # 等待所有线程执行完毕
        #  join() 等待线程终止，要不然一直挂起
        for m in thread_list:
            m.join()

    def get_add_user_def_data_xlsx(self,path=''):
        '''
        自定义excel表数据
        '''
        df=pd.read_excel(r'{}'.format(path),dtype='object')
        self.hist=pd.concat([self.hist,df],ignore_index=True)
        return self.hist
    def get_thread_user_def_data_xlsx(self,path_list=[]):
        '''
        添加数据自定义excel表数据
        多线程
        path_list文件路径列表
        '''
        thread_list=[]
        for i in tqdm(range(len(path_list))):
            path=path_list[i]
            t=Thread(target=self.get_add_user_def_data_xlsx, args=(path,))
            thread_list.append(t)
        #启动全部
        for j in thread_list:
            j.start()
        # 等待所有线程执行完毕
        #  join() 等待线程终止，要不然一直挂起
        for m in thread_list:
            m.join()
    def get_add_user_def_data_csv(self,path=''):
        '''
        自定义csv表数据
        '''
        df=pd.read_csv(r'{}'.format(path),dtype='object')
        self.hist=pd.concat([self.hist,df],ignore_index=True)
        return self.hist
    def get_thread_user_def_data_csv(self,path_list=[]):
        '''
        添加数据自定义csv表数据
        多线程
        path_list文件路径列表
        '''
        thread_list=[]
        for i in tqdm(range(len(path_list))):
            path=path_list[i]
            t=Thread(target=self.get_add_user_def_data_csv, args=(path,))
            thread_list.append(t)
        #启动全部
        for j in thread_list:
            j.start()
        # 等待所有线程执行完毕
        #  join() 等待线程终止，要不然一直挂起
        for m in thread_list:
            m.join()
    def get_add_other_data(self,df=''):
        '''
        添加其他数据比如涨停板
        '''
        self.hist=pd.concat([self.hist,df],ignore_index=True)
        return self.hist
    def get_thread_add_other_data(self,df_list=[]):
        '''
        添加数据自定义excel表数据
        多线程
        path_list文件路径列表
        '''
        thread_list=[]
        for i in tqdm(range(len(df_list))):
            df=df_list[i]
            t=Thread(target=self.get_add_user_def_data_xlsx, args=(df,))
            thread_list.append(t)
        #启动全部
        for j in thread_list:
            j.start()
        # 等待所有线程执行完毕
        #  join() 等待线程终止，要不然一直挂起
        for m in thread_list:
            m.join()
