from xgtrader_backtrader.data.data import data
from xgtrader_backtrader.portfolio.portfolio import portfolio
from xgtrader_backtrader.position.position import position
from xgtrader_backtrader.indicators.indicators import indicators
from xgtrader_backtrader.trader_tool.stock_data import stock_data
import quantstats as qs
import pandas as pd
from finta import TA
import mplfinance as mpf
import matplotlib.pyplot as plt
from xgtrader_backtrader.index_data.index_data import index_data
import os
import math
class backtrader:
    def __init__(self,start_date='20210105',end_date='20500101',data_type='D',
                 starting_cash=2000,cash=2000,commission=0.001,index_stock='003000'):
        self.start_date=start_date
        self.end_date=end_date
        self.data_type=data_type
        self.commission=commission
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.data=data(start_date=self.start_date,end_date=self.end_date)
        self.position=position(start_date=self.start_date,end_date=self.end_date,starting_cash=starting_cash,
                               data_type=self.data_type,commission=commission,cash=cash)
        self.portfolio=portfolio(starting_cash=starting_cash,cash=cash)
        self.stock_data=stock_data()
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.index_data=index_data(stock=index_stock,start_date=self.start_date,end_date=self.end_date,data_type=self.data_type)
    def check_is_creat_data(self,date='20230101',stock='60031',price=1,amount=100,trader_type='buy'):
        '''
        检查是否建立数据
        '''
        #建立账户
        if  stock  in list(self.position.position.keys()):
            #print('{} {}数据已经建立'.format(date,stock))
            #print('{} {}数据账户建立'.format(date,stock))
            return True
        else:
            #添加数据
            print('{}数据没有建立开始建立'.format(stock))
            self.data.get_add_data(stock=stock)
            print('{}账户没有建立开始建立'.format(stock))
            self.position.creat_position(stock=stock,start_date=date,price=price,amount=amount,trader_type='buy')
            return False
    def buy(self,date='20230101',stock='600031',price=1,amount=100,trader_type='buy'):
        '''
        买入
        date交易时间
        stock股票代码
        price交易价格
        amount数量
        trader_type交易类型
        '''
        #检查数据是否加载
        if self.check_is_creat_data(date=date,stock=stock,price=price,amount=amount)==True:
            self.position.adjust_position_data(trader_type=trader_type,stock=stock,date=date,price=price,amount=amount)
            return True, date ,stock,price,amount,trader_type
        else:
            print('数据没有建立建立数据{}'.format(stock,date))
            return False, date ,stock,price,amount,trader_type
    def sell(self,date='20230101',stock='600031',price=1,amount=100,trader_type='sell'):
        '''
        卖出
        date交易时间
        stock股票代码
        price交易价格
        amount数量
        trader_type交易类型
        '''
        #检查数据是否加载
        if self.check_is_creat_data(date=date,stock=stock,price=price,amount=amount)==True:
            self.position.adjust_position_data(trader_type=trader_type,stock=stock,date=date,price=price,amount=amount)
            return True, date ,stock,price,amount,trader_type
        else:
            print('数据没有建立建立数据{}'.format(stock,date))
            return False, date ,stock,price,amount,trader_type
    def settle(self,date='20230101',stock='600031',price=1,trader_type='settle',amount=100,):
        '''
        结算函数,持股结算
        只有持有账户价值变化
        date交易时间
        stock股票代码
        price交易价格
        amount数量这个不需要为了兼容保留
        trader_type交易类型
        '''
        #检查数据是否加载
        if self.check_is_creat_data(date=date,stock=stock,price=price,amount=amount)==True:
            self.position.adjust_position_data(trader_type=trader_type,stock=stock,date=date,price=price,amount=amount)
            return True, date ,stock,price,amount,trader_type
        else:
            print('数据没有建立建立数据{}'.format(stock,date))
            return False, date ,stock,price,amount,trader_type
    def get_trader_date_list(self):
        '''
        获取交易日历
        '''
        trader_time=self.stock_data.get_trader_date_list(start_date=self.start_date,end_date=self.end_date)
        return trader_time
    def get_position_dict_data(self):
        '''
        获取持股数据字典类型的数据
        '''
        dict_data=self.position.position
        return dict_data
    def get_position_dict_data_by_stock(self,stock='600031'):
        '''
        获取持股数据字典类型的数据通过代码
        '''
        if stock in  list(self.position.position.keys()):
            dict_data=self.position.position[stock]
            return dict_data
        else:
            print('{}没有建立持股'.format(stock))
            return {}
    def get_position_pandas_data_by_stock(self,stock='600031'):
        '''
        获取持股数据字典类型的数据
        '''
        if stock in  list(self.position.position.keys()):
            dict_data=self.position.position[stock]
            df=pd.DataFrame(dict_data)
            return df
        else:
            print('{}没有建立持股'.format(stock))
            df=pd.DataFrame()
            return df
    def get_total_position_pandas_data(self):
        '''
        合并总持股数据
        '''
        df=self.position.get_total_position()
        return df
    def get_position_all_trader_data(self):
        '''
        获取全部交易数据
        '''
        df=self.position.get_total_position_trader()
        return df
    def get_total_portfolio_dict_data(self):
        '''
        获取总账户字典数据
        '''
        df=self.position.portfolio.total_portfolio
        return df
    def get_total_portfolio_pandas_data(self):
        '''
        获取总账户字典数据
        '''
        df=self.position.portfolio.get_portfolio_data_to_pandas()
        return df
    def get_portfolio_last_data(self):
        '''
        获取账户最新的数据
        '''
        df=self.get_total_portfolio_pandas_data()
        data_dict={}
        data_dict['date']=df['date'].tolist()[-1]
        data_dict['stock_total_value']=df['stock_total_value'].tolist()[-1]
        data_dict['available_cash']=df['available_cash'].tolist()[-1]
        data_dict['ups_downs_value']=df['ups_downs_value'].tolist()[-1]
        data_dict['reference_profit']=df['reference_profit'].tolist()[-1]
        data_dict['host_cost']=df['host_cost'].tolist()[-1]
        data_dict['cumsum_host_cost']=df['cumsum_host_cost'].tolist()[-1]
        data_dict['total_value']=df['total_value'].tolist()[-1]
        data_dict['return_ratio']=df['return_ratio'].tolist()[-1]
        data_dict['cumsum_return_ratio']=df['cumsum_return_ratio'].tolist()[-1]
        return data_dict
    def get_position_last_data_by_stock(self,stock='600031'):
        '''
        获取个股最新持股数据
        '''
        if stock in  list(self.position.position.keys()):
            data_dict={}
            df=self.get_position_pandas_data_by_stock(stock=stock)
            data_dict['stock']=df['stock'].tolist()[-1]
            data_dict['price']=df['price'].tolist()[-1]
            data_dict['date']=df['date'].tolist()[-1]
            data_dict['host_cost']=df['host_cost'].tolist()[-1]
            data_dict['cumsum_hold_cost']=df['cumsum_hold_cost'].tolist()[-1]
            data_dict['amount']=df['amount'].tolist()[-1]
            data_dict['trader_amount']=df['trader_amount'].tolist()[-1]
            data_dict['trader_value']=df['trader_value'].tolist()[-1]
            data_dict['value']=df['value'].tolist()[-1]
            data_dict['price_limit']=df['price_limit'].tolist()[-1]
            data_dict['ups_downs_value']=df['ups_downs_value'].tolist()[-1]
            data_dict['return']=df['return'].tolist()[-1]
            data_dict['cumsum_return']=df['cumsum_return'].tolist()[-1]
            data_dict['trader_type']=df['trader_type'].tolist()[-1]
            return data_dict
        else:
            print('{}没有建立持股'.format(stock))
            return {}
    def check_stock_is_av_buy(self,date='',stock='128036',price='156.700',amount=100,hold_limit=800):
        '''
        检查是否可用买入
        '''
        account=self.get_portfolio_last_data()
        hold_stock=self.get_position_last_data_by_stock(stock=stock)
        if len(hold_stock)<=0:
            hold_amount=0
        else:
            hold_amount=hold_stock['amount']
        if stock not in  list(self.position.position.keys()):
            print('时间{} {}没有持股直接买入'.format(date,stock))
            return True
        else:
            if hold_amount>=hold_limit:
                print('时间{} {}不允许买入 持有数量大于{} 持股限制{}'.format(date,stock,hold_amount,hold_limit))
                return False
            else:
                buy_value=price*amount
                av_cash=account['available_cash']
                com=price*amount*self.commission
                if av_cash>=buy_value+com:
                    print('时间{} {}允许买入 可用资金{} 买入价值{} 手续费{}'.format(date,stock,av_cash,buy_value,com))
                    return True
                else:
                    print('时间{} {}不允许买入 可用资金{} 小于买入价值{} 加手续费{}'.format(date,stock,av_cash,buy_value,com))
                    return False
    def check_stock_is_av_sell(self,date='',stock='128036',price='156.700',amount=10):
        '''
        检查是否可用卖出
        '''
        hold_stock=self.get_position_last_data_by_stock(stock=stock)
        if stock not in  list(self.position.position.keys()):
            print('时间{} {}没有持股不允许卖出'.format(date,stock))
            return False
        else:
            sell_amount=amount
            hold_amount=hold_stock['amount']
            if hold_amount>=sell_amount:
                print('时间{} {} 允许卖出 持有数量{} 卖出数量{}'.format(date,stock,hold_amount,sell_amount))
                return True
            else:
                print('时间{} {} 不允许卖出 持有数量{} 小于卖出数量{}'.format(date,stock,hold_amount,sell_amount))
                return False
    def get_portfolio_trader_report_html(self,name='策略报告'):
        '''
        获取账户收益报告
        '''
        try:
            df=self.position.get_total_position_trader()
            df=df.groupby(by='date').mean()
            df.index=pd.to_datetime(df.index)
            index=self.index_data.get_index_hist_data()
            index_size=index.shape[0]
            df_size=df.shape[0]
            if index_size>=df_size:
                index=index[-df_size:]
            else:
                df_size=df_size[-index_size:]
            df['index']=index['close'].tolist()
            qs.reports.html(returns=df['return'],benchmark=df['index'].pct_change(),output=r'{}\交易报告\{}.html'.format(self.path,name))
        except Exception as e:
            print(e)
    def get_portfolio_trader_report_html_1(self,name='策略报告'):
        '''
        获取账户收益报告
        '''
        try:
            df=self.get_total_portfolio_pandas_data()
            df.index=pd.to_datetime(df['date'])
            qs.reports.html(returns=df['return_ratio'],output=r'{}\交易报告\{}.html'.format(self.path,name))
        except Exception as e:
            print(e)
    def get_position_trader_report_html_by_stock(self,stock='600031'):
        '''
        获取个股交易报告
        '''
        index=self.index_data.get_index_hist_data()
        index_size=index.shape[0]
        df=self.get_position_pandas_data_by_stock(stock=stock)
        df_size=df.shape[0]
        if index_size>=df_size:
            index=index[-df_size:]
        else:
            df_size=df_size[-index_size:]
        if df.shape[0]>0:
            #df.index=pd.to_datetime(df['date'])
            index.index=pd.to_datetime(index['date'])
            #df['index']=index['close'].tolist()
            index['return']=df['return'].tolist()
            qs.reports.html(returns=index['return'],benchmark=index['close'].pct_change(),output=r'{}\交易报告\{}交易报告.html'.format(self.path,stock))
        else:
            print('{}没有交易记录'.format(stock))
    def get_poition_all_trader_report_html(self):
        '''
        过去全部个股的交易报告
        '''
        stock_list=self.position.position.keys()
        for stock in stock_list:
            try:
                self.get_position_trader_report_html_by_stock(stock=stock)
            except Exception as e:
                print(e)
                print('{}个股的交易报告有问题'.format(stock))
    def get_plot_trader_data_figure_by_stock(self,stock='600031',limit=100):
        hist=self.position.data.hist
        hist=hist[hist['stock']==stock]
        trader_df=self.get_position_pandas_data_by_stock(stock=stock)[-limit:]
        trader_df=trader_df.drop_duplicates(subset=['date'])
        result=pd.DataFrame()
        #统一数据
        for date in trader_df['date'].tolist():
            df=hist[hist['date']==date]
            result=pd.concat([result,df],ignore_index=True)
        result['trader_type']=trader_df['trader_type'].tolist()
        buy_list=[]
        sell_list=[]
        for price,trader_type in zip(result['close'].tolist(),result['trader_type'].tolist()):
            if trader_type=='buy':
                buy_list.append(price*0.99)
            else:
                buy_list.append(None)
        for price,trader_type in zip(result['close'].tolist(),result['trader_type'].tolist()):
            if trader_type=='sell':
                sell_list.append(price*1.01)
            else:
                sell_list.append(None)       
        result['buy']=buy_list
        result['sell']=sell_list
        result['amount']=trader_df['amount'].tolist()
        result['value']=trader_df['value'].tolist()
        result['cumsum_return']=trader_df['cumsum_return'].tolist()
        result['cumsum_hold_cost']=trader_df['cumsum_hold_cost'].tolist()
        df1=result
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
        add_plot = [ 
            mpf.make_addplot(df1['buy'],panel=0,color='r',type='scatter',marker='^',markersize=60),
            mpf.make_addplot(df1['sell'],panel=0,color='g',type='scatter',marker='v',markersize=60),
            mpf.make_addplot(df1['cumsum_return']*100,panel=2,color='r',title='cumsum_return%'),
            mpf.make_addplot(df1['amount'],panel=3,color='y',title='hold_amount'),
            mpf.make_addplot(df1['value'],panel=4,color='r',title='hold_value'),
            mpf.make_addplot(df1['cumsum_hold_cost'],panel=5,color='r',title='cumsum_hold_cost')]
        
        # 绘制股票图，5，10，20日均线
        mpf.plot(df1, type='candle', mav=(5, 10, 20),style=s,figratio=(800, 650),
                 addplot=add_plot,volume=True,
                 title='xg_backtrader sub_position_stock:{} start_date:{} end_date:{}'.format(stock,self.start_date,self.end_date))#,
        plt.show()
    
    def get_plot_all_trader_data_figure(self,limit=100):
        '''
        获取全部子持股的图片
        '''
        stock_list=list(self.position.position.keys())
        for stock in stock_list:
            try:
                self.get_plot_trader_data_figure_by_stock(stock=stock,limit=limit)
            except Exception as e:
                print(e)
                print('{}全部子持股的图片有问题'.format(stock))
    def get_portfolio_trader_data_figure(self,limit=100):
        '''
        获取策略图形
        '''
        try:
            hist=self.index_data.get_index_hist_data()
            trader_df=self.get_total_portfolio_pandas_data()[-limit:]
            #统一数据
            result=pd.DataFrame()
            for date in trader_df['date'].tolist():
                df=hist[hist['date']==date]
                result=pd.concat([result,df],ignore_index=True)
            df1=result
            df1['stock_total_value']=trader_df['stock_total_value'].tolist()[-df1.shape[0]:]
            df1['available_cash']=trader_df['available_cash'].tolist()[-df1.shape[0]:]
            df1['reference_profit']=trader_df['reference_profit'].tolist()[-df1.shape[0]:]
            df1['cumsum_host_cost']=trader_df['cumsum_host_cost'].tolist()[-df1.shape[0]:]
            df1['total_value']=trader_df['total_value'].tolist()[-df1.shape[0]:]
            df1['cumsum_return_ratio']=(trader_df['cumsum_return_ratio']).tolist()[-df1.shape[0]:]
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
            add_plot = [ 
                mpf.make_addplot(df1['cumsum_return_ratio']*100,panel=2,color='r',title='cumsum_return_ratio%'),
                mpf.make_addplot(df1['reference_profit'],panel=3,color='r',title='reference_profit'),
                mpf.make_addplot(df1['total_value'],panel=4,color='r',title='total_value'),
                mpf.make_addplot(df1['stock_total_value'],panel=5,color='r',title='stock_total_value'),
                mpf.make_addplot(df1['available_cash'],panel=6,color='r',title='available_cash'),
                mpf.make_addplot(df1['cumsum_host_cost'],panel=7,color='r',title='cumsum_host_cost')]
            
            # 绘制股票图，5，10，20日均线
            mpf.plot(df1, type='candle', mav=(5, 10, 20),style=s,figratio=(800, 650),
                    addplot=add_plot,volume=True,
                    title='xg_backtrader_account stock:{} start_date:{} end_date:{}'.format('00300',self.start_date,self.end_date))#,
            plt.show()
        except Exception as e:
            print(e)
    def order_target_volume(self,date='',stock='501018',amount=1000,price=12):
        '''
        目标数量下单
        stock: 标的代码
        amount: 期望的最终数量
        price:价格
        trader_type针对买入账户没有持股的股票，一般不改动
        '''
        target_volume=amount
        hold_stock=self.get_position_last_data_by_stock(stock=stock)
        if len(hold_stock)>0:
            stock=str(stock)
            #持有数量
            hold_num=hold_stock['amount']
            #买卖的差额
            buy_sell_num=amount-float(hold_num)
            #存在买入差额
            if buy_sell_num>0:
                self.buy(date=date,stock=stock,price=price,amount=int(buy_sell_num))
                print('目标交易数量股票{} 时间{} 目标数量{} 持有数量{} 买入数量{}'.format(stock,date,target_volume,hold_num,buy_sell_num))
                return True
            #存在卖出空间：
            elif buy_sell_num <0:
                    #可以卖出的数量多
                self.sell(date=date,stock=stock,price=price,amount=abs(int(buy_sell_num)))
                print('目标交易数量股票{} 时间{} 目标数量{} 持有数量{} 卖出数量{}'.format(stock,date,target_volume,hold_num,buy_sell_num))
                return True
            else:
                print('目标交易数量股票{}时间{} 目标数量{} 持有数量{} 不存在差额'.format(stock,date,target_volume,hold_num))
                return False
        else:
            self.buy(date=date,stock=stock,price=price,amount=amount)
            print('目标交易数量股票{}时间{} 目标数量{} 持有数量0 直接买入 不存在差额'.format(stock,date,target_volume,amount))
            return True
    def order_value(self,date='',stock='501018',value=1000,price=1.33,trader_type='buy'):
        '''
        按金额下单
        stock: 证券代码
        value下单金额
        value大于0买入，小0卖出
        prive交易的的价格
        '''
        order_value=value
        hold_stock=self.get_position_last_data_by_stock(stock=stock)
        if len(hold_stock)>0:
            #可以使用的数量兼容t0
            hold_value=hold_stock['value']
            #买卖价值差转成数量
            amount=math.floor(value/price)
            amount=self.adjust_amount(stock=str(stock),amount=amount)
            if amount==0:
                print('金额交易时间{} 买入价值 可以买入的数量小于0'.format(date,order_value))
                return False
            else:
                if amount>0:
                    if trader_type=='buy':
                        self.buy(security=stock,amount=int(amount),price=price)
                        print('金额交易股票{} 时间{} 买入金额{} 买入数量{}'.format(stock,date,order_value,amount))
                        return True
                    else:
                        self.sell(security=stock,amount=int(amount),price=price)
                        print('金额交易股票{} 时间{} 卖出金额{} 卖出数量{}'.format(stock,date,order_value,amount))
    def adjust_amount(self,stock='',amount=''):
        '''
        调整数量
        '''           
        if stock[:3] in ['110','113','123','127','128','111'] or stock[:2] in ['11','12']:
            amount=math.floor(amount/10)*10
        else:
            amount=math.floor(amount/100)*100
        return amount
    def order_target_value(self,date='',stock='501018',value=1000,price=1.33):
        '''
        目标价值下单
        stock: 股票名字
        value: 股票价值，value = 最新价 * 手数 * 保证金率（股票为1） * 乘数（股票为100）
        prive交易的的价格
        '''
        target_value=value
        hold_stock=self.get_position_last_data_by_stock(stock=stock)
        #买卖价值差转成数量
        amount=math.floor(value/price)
        amount=self.adjust_amount(stock=str(stock),amount=amount)
        if len(hold_stock)>0:
            #可以使用的数量兼容t0
            hold_num=hold_stock['value']
            buy_sell_num=math.floor(amount-float(hold_num))
            buy_sell_num=self.adjust_amount(stock=str(stock),amount=buy_sell_num)
            #存在买入差额
            if buy_sell_num>=100:
                self.buy(date=date,stock=stock,price=price,amount=int(buy_sell_num))
                print('目标价值交易股票{} 时间{} 目标价值{} 持有价值{} 买入数量{}'.format(stock,date,target_value,hold_num,buy_sell_num))
                return True
            #存在卖出空间：
            elif buy_sell_num <=-100:
                #可以卖出的数量多
                self.sell(date=date,stock=stock,price=price,amount=abs(int(buy_sell_num)))
                print('目标价值交易股票{} 时间{} 目标价值{} 持有价值{} 卖出数量{}'.format(stock,date,target_value,hold_num,buy_sell_num))
                return True
            else:
                print('目标价值交易股票{}时间{} 目标价值{} 持有价值{} 不存在差额'.format(stock,date,target_value,hold_num))
                return False
        else:
            self.buy(date=date,stock=stock,price=price,amount=amount)
            print('目标价值交易股票{}时间{} 目标价值{} 持有数量0 直接买入{} 不存在差额'.format(stock,date,target_value,target_value,amount))
            return True
    
    def check_av_target_trader(self,data_type='数量',trader_type='buy',amount=1000,limit_volume=2000,
                value=2000,limit_value=4000,stock='501018',price=2.475):
        '''
        检查模块资金分配
        data_type='数量'/资金,
        trader_type='buy',交易类型
        amount=1000,每次交易的数量股
        limit_volume=2000,单一标的持股限制
        value=2000,每次交易金额
        limit_value=4000,单一标的金额限制
        stock='501018',代码
        price=2.475交易的价格
        '''
        self.get_check_not_trader_today_entrusts()
        #stock=self.adjust_stock(stock=stock)
        stock=stock[:6]
        self.open_set=''
        try:
            hold_stock=self.position()
        except:
            hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        if data_type=='数量':
            if hold_stock.shape[0]>0:
                stock=str(stock)
                if trader_type=='buy':
                    df1=hold_stock[hold_stock['证券代码']==stock]
                    #标的有持股
                    if df1.shape[0]>0:
                        #可以使用的数量兼容t0
                        av_num=df1['可用余额'].tolist()[-1]
                        #持有数量
                        hold_num=df1['股票余额'].tolist()[-1]
                        #委托数量
                        entrusts_amount,entrusts_df=self.get_check_not_trader_today_entrusts(stock=stock,trader_type='buy',data_type=data_type)
                        #买卖的差额
                        av_buy_sell=limit_volume-hold_num-entrusts_amount
                        #持股限制大于现在的持有数量
                        #可以买入的数量大于每次交易的数量
                        if av_buy_sell>=amount:
                            amount=self.adjust_amount(stock=stock,amount=amount)
                            if amount<=0:
                                print('数量模块1{} 可以买入的数量{} 小于0'.format(stock,amount))
                                return '','',''
                            else:
                                return 'buy',amount,price
                        else:
                            #可以买入的数量小于每次交易的数量
                            msg='数量模块2{} 可以买入的数量{} 小于每次交易数量{}不交易'.format(stock,av_buy_sell,amount)
                            print(msg)
                            return '',amount,price
                    else:
                        #如果没有持股，直接买入，
                        #持有数量为0
                        #委托数量
                        entrusts_amount,entrusts_df=self.get_check_not_trader_today_entrusts(stock=stock,trader_type='buy',data_type=data_type)
                        av_buy_sell=limit_volume-0-entrusts_amount
                        #持股限制大于现在的持有数量
                        #可以买入的数量大于每次交易的数量
                        if av_buy_sell>=amount:
                            amount=self.adjust_amount(stock=stock,amount=amount)
                            if amount<=0:
                                print('数量模块3{} 可以买入的数量{} 小于0'.format(stock,amount))
                                return '',amount,price
                            else:
                                return 'buy',amount,price
                        else:
                            #可以买入的数量小于每次交易的数量
                            msg='数量模块4{} 可以买入的数量{} 小于每次交易数量{}不交易'.format(stock,av_buy_sell,amount)
                            print(msg)
                            return '',amount,price
                #单一标的有持股卖出
                else:
                    #卖
                    df1=hold_stock[hold_stock['证券代码']==stock]
                    #有持股
                    if df1.shape[0]>0:
                        #可以使用的数量兼容t0
                        av_num=df1['可用余额'].tolist()[-1]
                        #持有数量
                        hold_num=df1['股票余额'].tolist()[-1]
                        #可以卖出的数量
                        #委托数量
                        entrusts_amount,entrusts_df=self.get_check_not_trader_today_entrusts(stock=stock,trader_type='sell',data_type=data_type)
                        av_buy_sell=hold_num-amount-entrusts_amount
                        av_num=self.adjust_amount(stock,amount=av_num)
                        if av_buy_sell>=amount:
                            return 'sell',amount,price
                        else:
                            if av_num>0:
                                return 'sell',av_num,price
                            else:
                                print('数量模块5不卖出 可以数量0 小于固定交易数量{} '.format(amount))
                                return '',amount,price
                    else:
                        print('数量模块6持股卖出没有持股 可以数量0 小于固定交易数量{} '.format(amount))
                        return '',amount,price
                        
            #账户没有持股，为空
            else:
                if trader_type=='buy':
                    #委托数量
                    entrusts_amount,entrusts_df=self.get_check_not_trader_today_entrusts(stock=stock,trader_type=trader_type,data_type=data_type)
                    av_buy_sell=limit_volume-0-entrusts_amount
                    #持股限制大于现在的持有数量
                    #可以买入的数量大于每次交易的数量
                    if av_buy_sell>=amount:
                        amount=self.adjust_amount(stock=stock,amount=amount)
                        if amount<=0:
                            print('数量模块7{} 可以买入的数量{} 小于0'.format(stock,amount))
                            return '',amount,price
                        else:
                            return 'buy',amount,price
                    else:
                        #可以买入的数量小于每次交易的数量
                        msg='数量模块8{} 可以买入的数量{} 小于每次交易数量{}不交易'.format(stock,av_buy_sell,amount)
                        print(msg)
                        return '',amount,price 
                else:
                    print('数量模块9{} 账户持股为空不能卖出'.format(stock))
                    return '',amount,price
        else:
            #金额
            amount=value/price
            amount=self.adjust_amount(amount=amount)
            limit_volume=limit_value/price
            limit_volume=self.adjust_amount(amount=limit_volume)
            if hold_stock.shape[0]>0:
                stock=str(stock)
                df1=hold_stock[hold_stock['证券代码']==stock]
                stock=str(stock)
                if trader_type=='buy':
                    df1=hold_stock[hold_stock['证券代码']==stock]
                    #单一标的有持股
                    if df1.shape[0]>0:
                        #可以使用的数量兼容t0
                        av_num=df1['可用余额'].tolist()[-1]
                        #持有数量
                        hold_num=df1['股票余额'].tolist()[-1]
                        hold_value=df1['市值'].tolist()[-1]
                        hold_num=self.adjust_amount(stock=stock,amount=hold_value/price)
                        if hold_value>=limit_value:
                            print('资金模块1{} 持股的价值{}大于持股价值{}限制不交易'.format(stock,hold_value,limit_value))
                            return '',price,''
                        else:
                            #买卖的差额
                            #委托数量
                            entrusts_amount,entrusts_df=self.get_check_not_trader_today_entrusts(stock=stock,trader_type=trader_type,data_type='金额')
                            av_buy_sell=limit_volume-hold_num-entrusts_amount
                            if av_buy_sell>=amount:
                                amount=self.adjust_amount(stock=stock,amount=amount)
                                if amount<=0:
                                    print('资金模块2{} 可以买入的数量{} 小于0'.format(stock,amount))
                                    return '','',''
                                else:
                                    return 'buy',amount,price
                            else:
                                #可以买入的数量小于每次交易的数量
                                msg='资金模块3{} 可以买入的数量{} 小于每次交易数量{}不交易'.format(stock,av_buy_sell,amount)
                                print(msg)
                                return '',amount,price
                    #单一标的账户没有持股买入
                    else:
                        amount=value/price
                        amount=self.adjust_amount(stock,amount=amount)
                        limit_volume=limit_value/price
                        limit_volume=self.adjust_amount(amount=limit_volume)
                        #委托数量
                        entrusts_amount,entrusts_df=self.get_check_not_trader_today_entrusts(stock=stock,trader_type=trader_type,data_type='金额')
                        av_buy_sell=limit_volume-0-entrusts_amount
                        if av_buy_sell>=amount:
                            if amount<=0:
                                    print('资金模块4{} 可以买入的数量{} 小于0'.format(stock,av_buy_sell))
                                    return '',amount,price
                            else:
                                return 'buy',amount,price
                        else:
                            #可以买入的数量小于每次交易的数量
                            msg='资金模块5{} 可以买入的数量{} 小于每次交易数量{}不交易'.format(stock,av_buy_sell,amount)
                            print(msg)
                            return '',amount,price
                #单一有持股卖出
                else:
                    #卖
                    df1=hold_stock[hold_stock['证券代码']==stock]
                    if df1.shape[0]>0:
                        #可以使用的数量兼容t0
                        amount=value/price
                        amount=self.adjust_amount(amount=amount)
                        limit_volume=limit_value/price
                        limit_volume=self.adjust_amount(amount=limit_volume)
                        stock=str(stock)
                        av_num=df1['可用余额'].tolist()[-1]
                        #持有数量
                        hold_num=df1['股票余额'].tolist()[-1]
                        hold_value=df1['市值'].tolist()[-1]
                        hold_num=self.adjust_amount(stock=stock,amount=hold_value/price)
                        #委托数量
                        entrusts_amount,entrusts_df=self.get_check_not_trader_today_entrusts(stock=stock,trader_type='sell',data_type='金额')
                        #可以卖出的数量
                        av_buy_sell=hold_num-amount-entrusts_amount
                        if av_buy_sell>=amount:
                            return 'sell',amount,price
                        else:
                            if av_num>0:
                                return 'sell',av_num,price
                            else:
                                #可以买入的数量小于每次交易的数量
                                msg='资金模块6持股卖出{} 可用数量{}小于0'.format(stock,av_num)
                                print(msg)
                                return '',amount,price
                    else:
                        msg='资金模块7有持股卖出{} 可用数量小于0'.format(stock)
                        print(msg)
                        return '',amount,price
            #账户没有持股买入
            else:
                if trader_type=='buy':
                    amount=value/price
                    amount=self.adjust_amount(stock,amount=amount)
                    limit_volume=limit_value/price
                    limit_volume=self.adjust_amount(amount=limit_volume)
                    #委托数量
                    entrusts_amount,entrusts_df=self.get_check_not_trader_today_entrusts(stock=stock,trader_type=trader_type,data_type='金额')
                    av_buy_sell=limit_volume-0-entrusts_amount
                    if av_buy_sell>=amount:
                        if amount<=0:
                            print('资金模块8{} 可以买入的数量{} 小于0'.format(stock,av_buy_sell))
                            return '',amount,price
                        else:
                            return 'buy',amount,price
                    else:
                        #可以买入的数量小于每次交易的数量
                        msg='资金模块9持股买入{} 可以买入的数量{} 小于每次交易数量{}不交易'.format(stock,av_buy_sell,amount)
                        print(msg)
                        return '',amount,price
                else:
                    print('资金模块10持股为空{}不卖出'.format(stock))
                    return '','',''      
    def get_all_data(self):
        '''
        获取全部数据
        '''
        self.get_poition_all_trader_report_html()
        self.get_portfolio_trader_report_html()
        self.get_plot_all_trader_data_figure()
        self.get_portfolio_trader_data_figure()


    



      


            

    



    
    

    



            

        

            


    
    
    
