from xgtrader_backtrader.backtrader import backtrader
from xgtrader_backtrader.user_def_data.user_def_data import user_def_data
from xgtrader_backtrader.trader_tool import tdx_indicator
import pandas as pd
from xgtrader_backtrader.trader_tool import jsl_data
from xgtrader_backtrader.trader_tool.dfcf_etf_data import dfcf_etf_data
from xgtrader_backtrader.trader_tool.ths_rq import ths_rq
from tqdm import tqdm
from xgtrader_backtrader.trader_tool.tdx_trader_function import tdx_trader_function
import pandas as pd
class my_backtrader:
    '''
    分析模型
    '''
    def __init__(self,start_date='20200101',end_date='20500101',data_type='D',
                 starting_cash=200000,cash=200000,commission=0.001,index_stock='000300',is_week=False):
        self.start_date=start_date
        self.end_date=end_date
        self.data_type=data_type
        self.starting_cash=starting_cash
        self.commission=commission
        self.index_stock=index_stock
        #这里输入代码就可以
        #导入自定义股票池
        stock_df=pd.read_excel(r'self_define_stock_pools.xlsx',dtype='object')
        stock_df['证券代码']=stock_df['证券代码'].astype(str)
        print(stock_df['证券代码'].tolist())
        print(stock_df['名称'].tolist())
        print(stock_df)
        stock_list=stock_df['证券代码'].tolist()
        #stock_list=['512890']
        stock_list=stock_list
        self.stock_list=stock_list
        self.amount=1000
        self.hold_limit=2000
        #采用目标数量交易
        self.buy_target_volume=10000
        self.sell_target_volume=0
        self.buy_target_value=10000
        self.sell_target_value=0
        self.tdx_trader_function=tdx_trader_function()
        self.is_week=is_week
        self.week_buy_n=2
        self.week_sell_n=1
        self.daily_buy_n=4
        self.daily_sell_n=3
        #一般是-3%为强制
        self.top_sell=-2
        self.trader=backtrader(start_date=self.start_date,end_date=self.end_date,
                               data_type=self.data_type,starting_cash=self.starting_cash,
                               commission=self.commission,cash=cash,index_stock=self.index_stock)
        self.data=user_def_data(start_date=self.start_date,end_date=self.end_date,data_type=self.data_type)
    def add_all_data(self):
        '''
        多线程加载数据
        '''
        self.data.get_thread_add_data(stock_list=self.stock_list)
        self.hist=self.data.hist
        return self.hist
    def add_all_week_data(self):
        '''
        获取全部的周数据
        '''
        self.week_df=pd.DataFrame()
        for i in range(len(self.stock_list)):
            stock=self.stock_list[i]
            df=self.data.data.get_hist_data_em(stock=stock,start_date=self.start_date,end_date=self.end_date,data_type='W')
            df['stock']=stock
            self.week_df=pd.concat([self.week_df,df],ignore_index=True)
        print(self.week_df)
        return self.week_df
    #单线程加载数据，避免数据不成功
    def add_all_data_1(self):
        '''
        单线程加载数据，避免数据不成功
        '''
        for i in tqdm(range(len(self.stock_list))):
            stock=self.stock_list[i]
            stock=str(stock)
            self.data.get_add_data(stock=stock)
        self.hist=self.data.hist
        print(self.hist)
        return self.hist
    def connect_daily_week_data(self):
        '''
        合并日线周线数据
        '''
        self.week_df=self.add_all_week_data()
        self.hist=self.add_all_data_1()
        data=pd.DataFrame()
        for stock in self.stock_list:
            week=self.week_df[self.week_df['stock']==stock]
            week_close=dict(zip(week['date'],week['close']))
            week_open=dict(zip(week['date'],week['open']))
            week_low=dict(zip(week['date'],week['low']))
            week_high=dict(zip(week['date'],week['high']))
            hist=self.hist[self.hist['stock']==stock]
            hist['week_close']=hist['date'].apply(lambda x:week_close.get(x,None))
            hist['week_open']=hist['date'].apply(lambda x:week_open.get(x,None))
            hist['week_low']=hist['date'].apply(lambda x:week_low.get(x,None))
            hist['week_high']=hist['date'].apply(lambda x:week_high.get(x,None))
            hist=hist.fillna(method='ffill')
            data=pd.concat([data,hist])
        return data
    def get_cacal_all_indicators(self):
        '''
        计算全部的指标
        '''
        hist=self.connect_daily_week_data()
        trader_info=pd.DataFrame()
        #拆分数据
        for stock in self.stock_list:
            df=hist[hist['stock']==stock]
            week_df=df[['date','week_close','week_open','week_low','week_high']]
            week_df.columns=['date','close','open','low','high']
            signal_daily,markers=self.tdx_trader_function.six_pulse_excalibur_hist(df)
            signal_week,markers=self.tdx_trader_function.six_pulse_excalibur_hist(week_df)
            df['signal_daily']=signal_daily
            df['signal_week']=signal_week
            trader_info=pd.concat([trader_info,df],ignore_index=True)
        return trader_info
    def run_backtrader(self):
        '''
        运行回测
        '''
        trader_list=self.trader.get_trader_date_list()
        trader_info=self.get_cacal_all_indicators()
        for date in trader_list:
            df=trader_info[trader_info['date']==date]
            stock_list=df['stock'].tolist()
            for stock in stock_list:
                df1=df[df['stock']==stock]
                price=df1['close'].tolist()[-1]
                price=float(price)
                zdf=df1['涨跌幅'].tolist()[-1]
                signal_daily=df1['signal_daily'].tolist()[-1]
                signal_week=df1['signal_week'].tolist()[-1]
                
                '''
                if buy==True:
                    if self.trader.check_stock_is_av_buy(date=date,stock=stock,price=price,amount=self.amount,hold_limit=self.hold_limit):
                        self.trader.buy(date=date,stock=stock,price=price,amount=self.amount)
                    else:
                        self.trader.settle(date=date,stock=stock,price=price)
                elif sell==True:
                    if self.trader.check_stock_is_av_sell(date=date,stock=stock,price=price,amount=self.amount):
                        self.trader.sell(date=date,stock=stock,price=price,amount=self.amount)
                    else:
                        self.trader.settle(date=date,stock=stock,price=price)
                else:
                    self.trader.settle(date=date,stock=stock,price=price)
                '''
                if self.is_week:
                    if signal_week>=self.week_buy_n:
                        if signal_daily>=self.daily_buy_n:
                            result=self.trader.order_target_volume(date=date,stock=stock,amount=self.buy_target_volume,price=price)
                            if result==True:
                                pass
                            else:
                                self.trader.settle(date=date,stock=stock,price=price)
                        else:
                            pass
                    else:
                        print("时间{} 标的{} 不符合周线买入".format(date,stock))
                else:
                    if signal_daily>=self.daily_buy_n:
                        result=self.trader.order_target_volume(date=date,stock=stock,amount=self.buy_target_volume,price=price)
                        if result==True:
                            pass
                        else:
                            self.trader.settle(date=date,stock=stock,price=price)
                    else:
                        pass
                if self.is_week:
                    if signal_week<=self.week_sell_n:
                        result=self.trader.order_target_volume(date=date,stock=stock,amount=self.sell_target_volume,price=price)
                        if result==True:
                            pass
                        else:
                            self.trader.settle(date=date,stock=stock,price=price)
                    else:
                        print("时间{} 标的{} 不符合周线卖出".format(date,stock))
                else:
                    print("时间{} 标的{} 不开启周线卖出".format(date,stock))
                if signal_daily<self.daily_sell_n:
                    result=self.trader.order_target_volume(date=date,stock=stock,amount=self.sell_target_volume,price=price)
                    if result==True:
                        pass
                    else:
                        self.trader.settle(date=date,stock=stock,price=price)
                else:
                    print("时间{} 标的{} 不符合日线卖出".format(date,stock))
                if zdf<=self.top_sell:
                    result=self.trader.order_target_volume(date=date,stock=stock,amount=self.sell_target_volume,price=price)
                    if result==True:
                        pass
                    else:
                        self.trader.settle(date=date,stock=stock,price=price)
                else:
                    print("时 间{} 标的{} 不符合止盈止损卖出".format(date,stock))
                '''
                #目标价值交易
                if buy==True:
                    result=self.trader.order_target_value(date=date,stock=stock,value=self.buy_target_value,price=price)
                    if result==True:
                        pass
                    else:
                        self.trader.settle(date=date,stock=stock,price=price)
                elif sell==True:
                    result=self.trader.order_target_value(date=date,stock=stock,value=self.sell_target_value,price=price)
                    if result==True:
                        pass
                    else:
                        self.trader.settle(date=date,stock=stock,price=price)
                else:
                    self.trader.settle(date=date,stock=stock,price=price)
                '''
if __name__=='__main__':
    trader=my_backtrader(data_type='D', start_date='20240701')
    trader.run_backtrader()
    #获取全部的交易报告
    trader.trader.get_poition_all_trader_report_html()
    #获取策略报告
    trader.trader.get_portfolio_trader_report_html()
    #显示个股的交易图
    trader.trader.get_plot_all_trader_data_figure(limit=1000)
    #显示策略数据
    df=trader.trader.get_portfolio_trader_data_figure(limit=100000)

