#统一同花顺
from .xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from .xtquant.xttype import StockAccount
from .xtquant import xtconstant
import time
import pandas as pd
import random
import math
import json
from .qmt_data import qmt_data
import math
def conv_time(ct):
    '''
    conv_time(1476374400000) --> '20161014000000.000'
    '''
    local_time = time.localtime(ct / 1000)
    data_head = time.strftime('%Y%m%d%H%M%S', local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = '%s.%03d' % (data_head, data_secs)
    return time_stamp
class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        """
        连接断开
        :return:
        """
        print("connection lost")
    def on_stock_order(self, order):
        """
        委托回报推送
        :param order: XtOrder对象
        :return:
        """
        print("on order callback:")
        print(order.stock_code, order.order_status, order.order_sysid)
    def on_stock_asset(self, asset):
        """
        资金变动推送
        :param asset: XtAsset对象
        :return:
        """
        print("on asset callback")
        print(asset.account_id, asset.cash, asset.total_asset)
    def on_stock_trade(self, trade):
        """
        成交变动推送
        :param trade: XtTrade对象
        :return:
        """
        print("on trade callback")
        print(trade.account_id, trade.stock_code, trade.order_id)
    def on_stock_position(self, position):
        """
        持仓变动推送
        :param position: XtPosition对象
        :return:
        """
        print("on position callback")
        print(position.stock_code, position.volume)
    def on_order_error(self, order_error):
        """
        委托失败推送
        :param order_error:XtOrderError 对象
        :return:
        """
        print("on order_error callback")
        print(order_error.order_id, order_error.error_id, order_error.error_msg)
    def on_cancel_error(self, cancel_error):
        """
        撤单失败推送
        :param cancel_error: XtCancelError 对象
        :return:
        """
        print("on cancel_error callback")
        print(cancel_error.order_id, cancel_error.error_id, cancel_error.error_msg)
    def on_order_stock_async_response(self, response):
        """
        异步下单回报推送
        :param response: XtOrderResponse 对象
        :return:
        """
        print("on_order_stock_async_response")
        print(response.account_id, response.order_id, response.seq)


class qmt_trader_ths:
    def __init__(self,path= r'D:/国金QMT交易端模拟/userdata_mini',
                  session_id = 123456,account='55009640',account_type='STOCK',
                  is_slippage=True,slippage=0.01) -> None:
        self.xt_trader=''
        self.acc=''
        self.path=path
        self.session_id=int(self.random_session_id())
        self.account=account
        self.account_type=account_type
        if is_slippage==True:
            self.slippage=slippage
        else:
            self.slippage=0
        self.data=qmt_data()
    def random_session_id(self):
        '''
        随机id
        '''
        session_id=''
        for i in range(0,9):
            session_id+=str(random.randint(1,9))
        return session_id
    def select_slippage(self,stock='600031',price=15.01,trader_type='buy'):
        '''
        选择滑点
        安价格来滑点，比如0.01就是一块
        etf3位数,股票可转债2位数
        '''
        stock=self.adjust_stock(stock=stock)
        data_type=self.select_data_type(stock=stock)
        if data_type=='fund' or data_type=='bond':
            slippage=self.slippage/10
            if trader_type=='buy' or trader_type==23:
                price=price+slippage
            else:
                price=price-slippage
        else:
            slippage=self.slippage
            if trader_type=='buy' or trader_type==23:
                price=price+slippage
            else:
                price=price-slippage
        return price
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
        start_mi=text['开始交易分钟']
        jhjj=text['是否参加集合竞价']
        if jhjj=='是':
            jhjj_time=15
        else:
            jhjj_time=30
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        wo=loc.tm_wday
        if wo<=trader_time:
            if tm_hour>=start_date and tm_hour<=end_date:
                if tm_hour==9 and tm_min<jhjj_time:
                    return False
                elif tm_min>=start_mi:
                    return True
                else:
                    return False
            else:
                return False    
        else:
            print('周末')
            return False
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
    def adjust_hold_data(self,stock='603918',trader_type='sell',price=12,amount=100):
        '''
        模拟持股数据
        '''
        #stock=self.adjust_stock(stock=stock)
        price=float(price)
        amount=float(amount)
        try:
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            del df['Unnamed: 0']
        except:
            try:
                df=pd.read_excel(r'持股数据.xlsx',dtype='object')
            except:
                df=self.position()
        df.index=df['证券代码']
        df1=df[df['证券代码']==stock]
        if df1.shape[0]>0:
            #可用余额
            available_balance=df1['可用余额'].tolist()[-1]
            #股票余额
            stock_balance=df1['股票余额'].tolist()[-1]
            if trader_type=='buy':
                stock_balance+=float(amount)
                available_balance+=float(amount)
            elif trader_type=='sell':
                available_balance-=float(amount)
                stock_balance-=float(amount)
                if available_balance<=0:
                    available_balance=0
                stock_balance-=float(amount)
                if stock_balance<=0:
                    stock_balance=0
            else:
                pass
            df1['可用余额']=[available_balance]
            df1['股票余额']=[stock_balance]
            data=df.drop(stock,axis=0)
            data=pd.concat([data,df1],ignore_index=True)
            try:
                data.to_excel(r'持股数据\持股数据.xlsx')
                print('持股数据调整成功')
                return data
            except:
                data.to_excel(r'持股数据.xlsx')
                return data
        else:
            df2=pd.DataFrame()
            df2['明细']=['0']
            df2['证券代码']=[stock]
            df2['证券名称']=['0']
            df2['股票余额']=[amount]
            df2['可用余额']=[amount]
            df2['冻结数量']=[0]
            df2['成本价']=[price]
            df2['市价']=[price]
            df2['盈亏']=[0]
            df2['盈亏比(%)']=[0]
            df2['市值']=[amount*price]
            df2['当日买入']=[0]
            df2['当日卖出']=[0]
            df2['交易市场']=[0]
            df2['持股天数']=[0]
            data=pd.concat([df,df2],ignore_index=True)
            try:
                data.to_excel(r'持股数据\持股数据.xlsx')
                print('持股数据调整成功')													
                print('{}没有持股'.format(stock))
                return data
            except:
                data.to_excel(r'持股数据.xlsx')
                return data
    def adjust_account_cash(self,stock='128036',trader_type='buy',price=123,amount=10):
        '''
        调整账户资金
        '''
        #stock=self.adjust_stock(stock=stock)
        price=float(price)
        amount=float(amount)
        try:
            df=pd.read_excel(r'账户数据\账户数据.xlsx',dtype='object')
            del df['Unnamed: 0']
        except:
            try:
                df=pd.read_excel(r'账户数据.xlsx',dtype='object')
            except:
                df=self.balance()
        value=price*amount
        #可用余额
        av_user_cash=float(df['可用金额'].tolist()[-1])
        if trader_type=='buy' and av_user_cash >=value+5:
            av_user_cash-=value
        elif trader_type=='buy' and av_user_cash <value+5:
            print('调整失败买入{}可用资金{}不足'.format(value,av_user_cash))
            av_user_cash=av_user_cash
        elif trader_type=='sell':
            av_user_cash+=value
        else:
            av_user_cash=av_user_cash
        df['可用金额']=[av_user_cash]
        try:
            df.to_excel(r'账户数据\账户数据.xlsx')
            print('账户资金调整完成')
            return df
        except:
            df.to_excel(r'账户数据.xlsx')
            print('账户资金调整完成')
            return df
    def check_cov_bond_av_trader(self,stock='128106'):
        '''
        检查可转债是否可以交易
        '''
        with open(r'分析配置.json',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        del_select=text['是否剔除强制赎回']
        del_stock=text['可转债黑名单']
        del_trader_stock=text['交易黑名单']
        yjl=pd.read_excel(r'可转债全部数据\可转债全部数据.xlsx')
        try:
            del yjl['Unnamed: 0']
        except:
            pass
        if stock not in del_stock or stock not in del_trader_stock:
            if stock in yjl_list:
                print('{}不允许交易 不在溢价率范围'.format(stock))
                return False
            else:
                if del_select=='是':
                    select_df=pd.read_excel(r'非强制赎回\非强制赎回.xlsx',dtype='object')
                else:
                    select_df=pd.read_excel(r'强制赎回\强制赎回.xlsx',dtype='object')
                try:
                    del select_df['Unnamed: 0']
                except:
                    pass
                stock_list=select_df['cell.bond_id'].tolist()
                if stock in stock_list:
                    print('{}非强制赎回可以交易'.format(stock))
                    return True
                else:
                    print('{}强制赎回/靠近强制赎回不可以交易'.format(stock))
                    return False
        else:
            print('{}可转债黑名单'.format(stock))
            return False
    def check_stock_is_av_buy(self,stock='128036',price='156.700',amount=10,hold_limit=100):
        '''
        检查是否可以买入
        '''
        #stock=self.adjust_stock(stock=stock)
        price=float(price)
        buy_value=price*amount
        try:
            cash_df=pd.read_excel(r'账户数据\账户数据.xlsx',dtype='object')
            del cash_df['Unnamed: 0'] 
        except:
            try:
                cash_df=pd.read_excel(r'账户数据.xlsx',dtype='object')
            except:   
                cash_df=self.balance()
        stock=self.adjust_stock(stock=stock)
        try:
            hold_data=self.position()
        except:
            try:
                hold_data=pd.read_excel(r'持股数据.xlsx',dtype='object')
            except:
                hold_data=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        av_user_cash=cash_df['可用金额'].tolist()[-1]
        if stock in hold_data['证券代码'].tolist():
            hold_num=hold_data[hold_data['证券代码']==stock]['股票余额'].tolist()[-1]
        else:
            hold_num=0
        if hold_num>=hold_limit:
            print('不允许买入超过持股: 代码{} 可用资金{} 买入价值{}'.format(stock,av_user_cash,buy_value))
        elif av_user_cash>=buy_value and hold_num<hold_limit:
            print('允许买入: 代码{} 可用资金{} 买入价值{}'.format(stock,av_user_cash,buy_value))
            return True
        else:
            print('不允许买入可用资金不足: 代码{} 可用资金{} 买入价值{}'.format(stock,av_user_cash,buy_value))
            return False
    def check_stock_is_av_sell(self,stock='128036',amount=10):
        '''
        检查是否可以卖出
        '''
        #stock=self.adjust_stock(stock=stock)
        try:
            hold_data=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        except:
            try:
                hold_data=pd.read_excel(r'持股数据.xlsx',dtype='object')
            except:
                hold_data=self.position()
        stock_list=hold_data['证券代码'].tolist()
        if stock in stock_list:
            hold_num=hold_data[hold_data['证券代码']==stock]['可用余额'].tolist()[-1]
            if hold_num>=amount:
                print('允许卖出：{} 持股{} 卖出{}'.format(stock,hold_num,amount))
                return True
            else:
                print('不允许卖出持股不足：{} 持股{} 卖出{}'.format(stock,hold_num,amount))
                return False
        else:
            print('不允许卖出没有持股：{} 持股{} 卖出{}'.format(stock,0,amount))
            return False
    def connect(self):
        '''
        连接
        path qmt userdata_min是路径
        session_id 账户的标志,随便
        account账户,
        account_type账户内类型
        '''
        print('链接qmt')
        # path为mini qmt客户端安装目录下userdata_mini路径
        path = self.path
        # session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号
        session_id = self.session_id
        xt_trader = XtQuantTrader(path, session_id)
        # 创建资金账号为1000000365的证券账号对象
        account=self.account
        account_type=self.account_type
        acc = StockAccount(account_id=account,account_type=account_type)
        # 创建交易回调类对象，并声明接收回调
        callback = MyXtQuantTraderCallback()
        xt_trader.register_callback(callback)
        # 启动交易线程
        xt_trader.start()
        # 建立交易连接，返回0表示连接成功
        connect_result = xt_trader.connect()
        if connect_result==0:
            # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
            subscribe_result = xt_trader.subscribe(acc)
            print(subscribe_result)
            self.xt_trader=xt_trader
            self.acc=acc
            return xt_trader,acc
        else:
            print('qmt连接失败')
    def order_stock(self,stock_code='600031.SH', order_type=xtconstant.STOCK_BUY,
                    order_volume=100,price_type=xtconstant.FIX_PRICE,price=20,strategy_name='',order_remark=''):
            '''
            下单，统一接口
            :param account: 证券账号
                :param stock_code: 证券代码, 例如"600000.SH"
                :param order_type: 委托类型, 23:买, 24:卖
                :param order_volume: 委托数量, 股票以'股'为单位, 债券以'张'为单位
                :param price_type: 报价类型, 详见帮助手册
                :param price: 报价价格, 如果price_type为指定价, 那price为指定的价格, 否则填0
                :param strategy_name: 策略名称
                :param order_remark: 委托备注
                :return: 返回下单请求序号, 成功委托后的下单请求序号为大于0的正整数, 如果为-1表示委托失败
            '''
        
            # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
            subscribe_result = self.xt_trader.subscribe(self.acc)
            print(self.xt_trader.query_stock_asset_async(account=self.acc,callback=subscribe_result))
            #print(subscribe_result)
            stock_code = self.adjust_stock(stock=stock_code)
            price=self.select_slippage(stock=stock_code,price=price,trader_type=order_type)
            # 使用指定价下单，接口返回订单编号，后续可以用于撤单操作以及查询委托状态
            fix_result_order_id = self.xt_trader.order_stock(account=self.acc,stock_code=stock_code, order_type=order_type,
                                                            order_volume=order_volume, price_type=price_type,
                                                            price=price, strategy_name=strategy_name, order_remark=order_remark)
            print('交易类型{} 代码{} 价格{} 数量{} 订单编号{}'.format(order_type,stock_code,price,order_volume,fix_result_order_id))
            return fix_result_order_id
    def buy(self,security='600031.SH', order_type=xtconstant.STOCK_BUY,
                    amount=100,price_type=xtconstant.FIX_PRICE,price=20,strategy_name='',order_remark=''):
        '''
        单独独立股票买入函数
        '''
        # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
        subscribe_result = self.xt_trader.subscribe(self.acc)
        print(self.xt_trader.query_stock_asset_async(account=self.acc,callback=subscribe_result))
        #print(subscribe_result)
        stock_code =self.adjust_stock(stock=security)
        price=self.select_slippage(stock=security,price=price,trader_type='buy')
        order_volume=amount
        # 使用指定价下单，接口返回订单编号，后续可以用于撤单操作以及查询委托状态
        if order_volume>0:
            fix_result_order_id = self.xt_trader.order_stock_async(account=self.acc,stock_code=stock_code, order_type=order_type,
                                                                order_volume=order_volume, price_type=price_type,
                                                                price=price, strategy_name=strategy_name, order_remark=order_remark)
            print('交易类型{} 代码{} 价格{} 数量{} 订单编号{}'.format(order_type,stock_code,price,order_volume,fix_result_order_id))
            return fix_result_order_id
        else:
            print('买入 标的{} 价格{} 委托数量{}小于0有问题'.format(stock_code,price,order_volume))
    def sell(self,security='600031.SH', order_type=xtconstant.STOCK_SELL,
                    amount=100,price_type=xtconstant.FIX_PRICE,price=20,strategy_name='',order_remark=''):
        '''
        单独独立股票卖出函数
        '''
        # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
        subscribe_result = self.xt_trader.subscribe(self.acc)
        print(self.xt_trader.query_stock_asset_async(account=self.acc,callback=subscribe_result))
        #print(subscribe_result)
        stock_code =self.adjust_stock(stock=security)
        price=self.select_slippage(stock=security,price=price,trader_type='sell')
        order_volume=amount
        # 使用指定价下单，接口返回订单编号，后续可以用于撤单操作以及查询委托状态
        if order_volume>0:
            fix_result_order_id = self.xt_trader.order_stock(account=self.acc,stock_code=stock_code, order_type=order_type,
                                                                order_volume=order_volume, price_type=price_type,
                                                                price=price, strategy_name=strategy_name, order_remark=order_remark)
            print('交易类型{} 代码{} 价格{} 数量{} 订单编号{}'.format(order_type,stock_code,price,order_volume,fix_result_order_id))
            return fix_result_order_id
        else:
            print('卖出 标的{} 价格{} 委托数量{}小于0有问题'.format(stock_code,price,order_volume))
    def reverse_repurchase_of_treasury_bonds(self,security='131810.SZ',buy_ratio=0.00001, order_type=xtconstant.STOCK_SELL
                                             ,price_type=xtconstant.FIX_PRICE,strategy_name='',order_remark=''):
        '''
        国债逆回购
        '''
        # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
        account=self.balance()
        av_cash=account['可用金额'].tolist()[-1]
        av_cash=float(av_cash)
        av_cash=av_cash*buy_ratio
        spot_data=self.data.get_full_tick(code_list=[security])
        print('{}实时数据'.format(security),spot_data)
        price=spot_data[security]['lastPrice']
        price=float(price)
        amount=math.floor((av_cash/price)/10)*10
        subscribe_result = self.xt_trader.subscribe(self.acc)
        print(self.xt_trader.query_stock_asset_async(account=self.acc,callback=subscribe_result))
        #print(subscribe_result)
        stock_code =self.adjust_stock(stock=security)
        #price=self.select_slippage(stock=security,price=price,trader_type='sell')
        order_volume=amount
        # 使用指定价下单，接口返回订单编号，后续可以用于撤单操作以及查询委托状态
        if order_volume>0:
            fix_result_order_id = self.xt_trader.order_stock(account=self.acc,stock_code=stock_code, order_type=order_type,
                                                                order_volume=order_volume, price_type=price_type,
                                                                price=price, strategy_name=strategy_name, order_remark=order_remark)
            text='国债逆回购交易类型{} 代码{} 价格{} 数量{} 订单编号{}'.format(order_type,stock_code,price,order_volume,fix_result_order_id)
            return '交易成功',text
        else:
            text='国债逆回购卖出 标的{} 价格{} 委托数量{}小于0有问题'.format(stock_code,price,order_volume)
            return '交易失败',text

    def order_stock_async(self,stock_code='600031.SH', order_type=xtconstant.STOCK_BUY,
                    order_volume=100,price_type=xtconstant.FIX_PRICE,price=20,strategy_name='',order_remark=''):
        '''
         释义 
        - 对股票进行异步下单操作，异步下单接口如果正常返回了下单请求序号seq，会收到on_order_stock_async_response的委托反馈
        * 参数
        - account - StockAccount 资金账号
        - stock_code - str 证券代码， 如'600000.SH'
        - order_type - int 委托类型
        - order_volume - int 委托数量，股票以'股'为单位，债券以'张'为单位
        - price_type - int 报价类型
        - price - float 委托价格
        - strategy_name - str 策略名称
        - order_remark - str 委托备注
        '''
        # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
        subscribe_result = self.xt_trader.subscribe(self.acc)
        print(self.xt_trader.query_stock_asset_async(account=self.acc,callback=subscribe_result))
        #print(subscribe_result)
        stock_code = self.adjust_stock(stock=stock_code)
        price=self.select_slippage(stock=stock_code,price=price,trader_type=order_type)
        # 使用指定价下单，接口返回订单编号，后续可以用于撤单操作以及查询委托状态
        fix_result_order_id = self.xt_trader.order_stock_async(account=self.acc,stock_code=stock_code, order_type=order_type,
                                                            order_volume=order_volume, price_type=price_type,
                                                            price=price, strategy_name=strategy_name, order_remark=order_remark)
        print('交易类型{} 代码{} 价格{} 数量{} 订单编号{}'.format(order_type,stock_code,price,order_volume,fix_result_order_id))
        return fix_result_order_id
    def cancel_order_stock(self,order_id=12):
        '''
        :param account: 证券账号
            :param order_id: 委托编号, 报单时返回的编号
            :return: 返回撤单成功或者失败, 0:成功,  -1:委托已完成撤单失败, -2:未找到对应委托编号撤单失败, -3:账号未登陆撤单失败
        '''
        # 使用订单编号撤单
        cancel_order_result = self.xt_trader.cancel_order_stock(account=self.acc,order_id=order_id)
        if cancel_order_result==0:
            print('成功')
        elif cancel_order_result==-1:
            print('委托已完成撤单失败')
        elif cancel_order_result==-2:
            print('找到对应委托编号撤单失败')
        elif cancel_order_result==-3:
            print('账号未登陆撤单失败')
        else:
            pass
        return cancel_order_result
    def cancel_order_stock_async(self,order_id=12):
        '''
        * 释义 
        - 根据订单编号对委托进行异步撤单操作
        * 参数
        - account - StockAccount  资金账号 
        - order_id - int 下单接口返回的订单编号
        * 返回 
        - 返回撤单请求序号, 成功委托后的撤单请求序号为大于0的正整数, 如果为-1表示委托失败
        * 备注
        - 如果失败，则通过撤单失败主推接口返回撤单失败信息
        '''
        # 使用订单编号撤单
        cancel_order_result = self.xt_trader.cancel_order_stock_async(account=self.acc,order_id=order_id)
        if cancel_order_result==0:
            print('成功')
        elif cancel_order_result==-1:
            print('委托已完成撤单失败')
        elif cancel_order_result==-2:
            print('找到对应委托编号撤单失败')
        elif cancel_order_result==-3:
            print('账号未登陆撤单失败')
        else:
            pass
        return cancel_order_result
    def query_stock_asset(self):
        '''
        :param account: 证券账号
            :return: 返回当前证券账号的资产数据
        '''
        # 查询证券资产
        
        asset = self.xt_trader.query_stock_asset(account=self.acc)
        data_dict={}
        if asset:
            data_dict['账号类型']=asset.account_type
            data_dict['资金账户']=asset.account_id
            data_dict['可用金额']=asset.cash
            data_dict['冻结金额']=asset.frozen_cash
            data_dict['持仓市值']=asset.market_value
            data_dict['总资产']=asset.total_asset
            return data_dict
        else:
            print('获取失败资金')
            data_dict['账号类型']=[None]
            data_dict['资金账户']=[None]
            data_dict['可用金额']=[None]
            data_dict['冻结金额']=[None]
            data_dict['持仓市值']=[None]
            data_dict['总资产']=[None]
            return  data_dict
    def balance(self):
        '''
        对接同花顺
        '''
        try:
            asset = self.xt_trader.query_stock_asset(account=self.acc)
            df=pd.DataFrame()
            if asset:
                df['账号类型']=[asset.account_type]
                df['资金账户']=[asset.account_id]
                df['可用金额']=[asset.cash]
                df['冻结金额']=[asset.frozen_cash]
                df['持仓市值']=[asset.market_value]
                df['总资产']=[asset.total_asset]
                return df
        except:
            print('获取账户失败，读取上次数据，谨慎使用')
            df=pd.read_excel(r'账户数据\账户数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            return df
    def query_stock_orders(self):
        '''
        当日委托
         :param account: 证券账号
        :param cancelable_only: 仅查询可撤委托
        :return: 返回当日所有委托的委托对象组成的list
        '''
        orders = self.xt_trader.query_stock_orders(self.acc)
        print("委托数量", len(orders))
        data=pd.DataFrame()
        if len(orders) != 0:
            for i in range(len(orders)):
                df=pd.DataFrame()
                df['账号类型']=[orders[i].account_type]
                df['资金账号']=[orders[i].account_id]
                df['证券代码']=[orders[i].stock_code]
                df['证券代码']=df['证券代码'].apply(lambda x:str(x)[:6])
                df['订单编号']=[orders[i].order_id]
                df['柜台合同编号']=[orders[i].order_sysid]
                df['报单时间']=[orders[i].order_time]
                df['委托类型']=[orders[i].order_type]
                df['委托数量']=[orders[i].order_volume]
                df['报价类型']=[orders[i].price_type]
                df['委托价格']=[orders[i].price]
                df['成交数量']=[orders[i].traded_volume]
                df['成交均价']=[orders[i].traded_price]
                df['委托状态']=[orders[i].order_status]
                df['委托状态描述']=[orders[i].status_msg]
                df['策略名称']=[orders[i].strategy_name]
                df['委托备注']=[orders[i].order_remark]
                data=pd.concat([data,df],ignore_index=True)
            data['报单时间']=pd.to_datetime(data['报单时间'],unit='s')
            return data
        else:
            print('目前没有委托')
            return data
    def today_entrusts(self):
        '''
        对接同花顺
        今天委托
        '''
        orders = self.xt_trader.query_stock_orders(self.acc)
        print("委托数量", len(orders))
        data=pd.DataFrame()
        if len(orders) != 0:
            for i in range(len(orders)):
                df=pd.DataFrame()
                df['账号类型']=[orders[i].account_type]
                df['资金账号']=[orders[i].account_id]
                df['证券代码']=[orders[i].stock_code]
                df['证券代码']=df['证券代码'].apply(lambda x:str(x)[:6])
                df['订单编号']=[orders[i].order_id]
                df['柜台合同编号']=[orders[i].order_sysid]
                df['报单时间']=[orders[i].order_time]
                df['委托类型']=[orders[i].order_type]
                df['委托数量']=[orders[i].order_volume]
                df['报价类型']=[orders[i].price_type]
                df['委托价格']=[orders[i].price]
                df['成交数量']=[orders[i].traded_volume]
                df['成交均价']=[orders[i].traded_price]
                df['委托状态']=[orders[i].order_status]
                df['委托状态描述']=[orders[i].status_msg]
                df['策略名称']=[orders[i].strategy_name]
                df['委托备注']=[orders[i].order_remark]
                data=pd.concat([data,df],ignore_index=True)
            data['报单时间']=df['报单时间'].apply(conv_time)
            return data
        else:
            print('目前没有委托')
            return data
    def cancel_order_stock_async_by_code(self,cancel_type='all',stock='600031.SH',num='all'):
        '''
        通过证券代码来撤单
        类型cancel_type=all/buy/sell/one
        在有多个单时候选择怎么样撤单num=0/all
        '''
        # 使用订单编号撤单
        entrusts=self.today_entrusts()
        if entrusts.shape[0]>0:
            stock=self.adjust_stock(stock=stock)
            stock_list=entrusts['证券代码'].tolist()
            if stock in stock_list:
                if cancel_type=='all':
                    order_id_list=entrusts['订单编号'].tolist()
                    for order_id in order_id_list:
                        self.cancel_order_stock_async(order_id=order_id)
                elif cancel_type=='buy':
                    entrusts_buy=entrusts[entrusts['委托类型']==xtconstant.STOCK_BUY]
                    order_id_list=entrusts_buy['订单编号'].tolist()
                    for order_id in order_id_list:
                        self.cancel_order_stock_async(order_id=order_id)
                elif cancel_type=='sell':
                    entrusts_sell=entrusts[entrusts['委托类型']==xtconstant.STOCK_SELL]
                    order_id_list=entrusts_sell['订单编号'].tolist()
                    for order_id in order_id_list:
                        self.cancel_order_stock_async(order_id=order_id)
                else:
                    entrusts_on=entrusts[entrusts['证券代码']==stock]
                    if num=='all':
                        order_id_list=entrusts_on['订单编号'].tolist()
                        for order_id in order_id_list:
                            self.cancel_order_stock_async(order_id=order_id)
                    else:
                        order_id_list=entrusts_on['订单编号'].tolist()
                        self.cancel_order_stock_async(order_id=order_id_list[num])
    def query_stock_trades(self):
        '''
        当日成交
        '''
        trades = self.xt_trader.query_stock_trades(self.acc)
        print("成交数量:", len(trades))
        data=pd.DataFrame()
        if len(trades) != 0:
            for i in range(len(trades)):
                df=pd.DataFrame()
                df['账号类型']=[trades[i].account_type]
                df['资金账号']=[trades[i].account_id]
                df['证券代码']=[trades[i].stock_code]
                df['证券代码']=df['证券代码'].apply(lambda x:str(x)[:6])
                df['委托类型']=[trades[i].order_type]
                df['成交编号']=[trades[i].traded_id]
                df['成交时间']=[trades[i].traded_time]
                df['成交均价']=[trades[i].traded_price]
                df['成交数量']=[trades[i].traded_volume]
                df['成交金额']=[trades[i].traded_amount]
                df['订单编号']=[trades[i].order_id]
                df['柜台合同编号']=[trades[i].order_sysid]
                df['策略名称']=[trades[i].strategy_name]
                df['委托备注']=[trades[i].order_remark]
                data=pd.concat([data,df],ignore_index=True)
            data['成交时间']=pd.to_datetime(data['成交时间'],unit='s')
            return data
        else:
            print('今日没有成交')     
            return False
    def today_trades(self):
        '''
        对接同花顺
        今日成交
        '''
        trades = self.xt_trader.query_stock_trades(self.acc)
        print("成交数量:", len(trades))
        data=pd.DataFrame()
        if len(trades) != 0:
            for i in range(len(trades)):
                df=pd.DataFrame()
                df['账号类型']=[trades[i].account_type]
                df['资金账号']=[trades[i].account_id]
                df['证券代码']=[trades[i].stock_code]
                df['证券代码']=df['证券代码'].apply(lambda x:str(x)[:6])
                df['委托类型']=[trades[i].order_type]
                df['成交编号']=[trades[i].traded_id]
                df['成交时间']=[trades[i].traded_time]
                df['成交均价']=[trades[i].traded_price]
                df['成交数量']=[trades[i].traded_volume]
                df['成交金额']=[trades[i].traded_amount]
                df['订单编号']=[trades[i].order_id]
                df['柜台合同编号']=[trades[i].order_sysid]
                df['策略名称']=[trades[i].strategy_name]
                df['委托备注']=[trades[i].order_remark]
                data=pd.concat([data,df],ignore_index=True)
            data['成交时间']=pd.to_datetime(data['成交时间'],unit='s')
            return data
        else:
            print('今日没有成交')     
            return False
    def query_stock_positions(self):
        '''
        查询账户所有的持仓
        '''
        positions = self.xt_trader.query_stock_positions(self.acc)
        print("持仓数量:", len(positions))
        data=pd.DataFrame()
        if len(positions) != 0:
            for i in range(len(positions)):
                df=pd.DataFrame()
                df['账号类型']=[positions[i].account_type]
                df['资金账号']=[positions[i].account_id]
                df['证券代码']=[positions[i].stock_code]
                df['证券代码']=df['证券代码'].apply(lambda x:str(x)[:6])
                df['持仓数量']=[positions[i].volume]
                df['可用数量']=[positions[i].can_use_volume]
                df['平均建仓成本']=[positions[i].open_price]
                df['市值']=[positions[i].market_value]
                data=pd.concat([data,df],ignore_index=True)
            return data
        else:
            print('没有持股')
            df=pd.DataFrame()
            df['账号类型']=[None]
            df['资金账号']=[None]
            df['证券代码']=[None]
            df['持仓数量']=[None]
            df['可用数量']=[None]
            df['平均建仓成本']=[None]
            df['市值']=[None]
            return df
    def position(self):
        '''
        对接同花顺
        持股
        '''
        try:
            positions = self.xt_trader.query_stock_positions(self.acc)
            print("持仓数量:", len(positions))
            data=pd.DataFrame()
            if len(positions) != 0:
                for i in range(len(positions)):
                    df=pd.DataFrame()
                    df['账号类型']=[positions[i].account_type]
                    df['资金账号']=[positions[i].account_id]
                    df['证券代码']=[positions[i].stock_code]
                    df['证券代码']=df['证券代码'].apply(lambda x:str(x)[:6])
                    df['股票余额']=[positions[i].volume]
                    df['可用余额']=[positions[i].can_use_volume]
                    df['成本价']=[positions[i].open_price]
                    df['市值']=[positions[i].market_value]
                    data=pd.concat([data,df],ignore_index=True)
                return data
            else:
                df=pd.DataFrame()
                df['账号类型']=None
                df['资金账号']=None
                df['证券代码']=None
                df['股票余额']=None
                df['可用余额']=None
                df['成本价']=None
                df['市值']=None
                df['选择']=None
                df['持股天数']=None
                df['交易状态']=None
                df['明细']=None
                df['证券名称']=None
                df['冻结数量']=None
                df['市价']=None
                df['盈亏']=None
                df['盈亏比(%)']=None
                df['当日买入']=None	
                df['当日卖出']=None
                df.to_excel(r'持股数据\持股数据.xlsx')
                return df
                
        except:
            print('获取持股失败，读取上次数据，谨慎使用')
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            return df
    def query_stock_position(self,stock_code='600031.SH'):
        '''
        通过证券代码查持股
        '''
        stock_code =self.adjust_stock(stock=stock_code)
        position = self.xt_trader.query_stock_position(self.acc, stock_code)
        df={}
        if position:
            df['账号类型']=position.account_type
            df['资金账号']=position.account_id
            df['证券代码']=position.stock_code
            df['证券代码']=df['证券代码'].apply(lambda x:str(x)[:6])
            df['持仓数量']=position.volume
            df['可用数量']=position.can_use_volume
            df['平均建仓成本']=position.open_price
            df['市值']=position.market_value
            return df
        else:
            print('没有持股')
            return False
    def query_stock_ipo_data(self):
        '''
        获取股票新可转债ipo数据
        dict 新股新债信息数据集

        { stock1: info1, stock2: info2, ... }

        stock - str 品种代码，例如 '301208.SZ'
        info - dict 新股信息
        name - str 品种名称
        type - str 品种类型
        STOCK - 股票，BOND - 债券
        minPurchaseNum / maxPurchaseNum - int 最小 / 最大申购额度
        单位为股（股票）/ 张（债券）
        purchaseDate - str 申购日期
        issuePrice - float 发行价
        '''
        try:
            data=self.xt_trader.query_ipo_data()
            df=pd.DataFrame(data).T
            df['证券代码']=df.index
            df.columns=['品种名称','品种类型','最大申购额度','最小申购额度','申购日期','发行价','证券代码']
            return df
        except:
            print('没有数据/处理出现错误')
            df=pd.DataFrame()
            df['品种名称']=None
            df['品种类型']=None
            df['最小申购额度']=None
            df['最大申购额度']=None
            df['申购日期']=None
            df['发行价']=None
            df['证券代码']=None
            return df
    def get_buy_stock_ipo(self):
        '''
        可转债新股一起申购
        '''
        df=self.query_stock_ipo_data()
        for trader_type,name,stock,amount,price in zip(df['品种类型'],df['品种名称'],df['证券代码'],df['最大申购额度'],df['发行价']):
            self.buy(security=stock,amount=amount,price=price)
            print('新股/可转债申购 交易类型{} 名称{} 代码{} 数量{} 价格{}'.format(trader_type,name,stock,amount,price))
    def query_stock_new_purchase_limit(self):
        '''
        释义
        查询新股申购额度
        参数
        account - StockAccount 资金账号
        返回
        dict 新股申购额度数据集
        { type1: number1, type2: number2, ... }
        type - str 品种类型
        KCB - 科创板，SH - 上海，SZ - 深圳
        number - int 可申购股数
        备注
        数据仅代表股票申购额度，债券的申购额度固定10000张
        '''
        #有问题
        print(self.account)
        df=self.xt_trader.query_new_purchase_limit(account=self.account)
        print(df)
    def run_forever(self):
        '''
        阻塞线程，接收交易推送
        '''
        self.xt_trader.run_forever()
    def stop(self):
        self.xt_trader.stop()
    def query_credit_detail(self):
        '''
        ``
        * 释义
        - 查询信用资金账号对应的资产
        * 参数
        - account - StockAccount 资金账号
        * 返回
        - 该信用账户对应的资产对象XtCreditDetail组成的list或者None
        * 备注
        - None表示查询失败
        - 通常情况下一个资金账号只有一个详细信息数据
        '''
        datas = self.xt_trader.query_credit_detail(self.acc)
        return datas
    def order_target_volume(self,stock='501018',amount=1000,price=12,trader_type='buy'):
        '''
        目标数量下单
        stock: 标的代码
        amount: 期望的最终数量
        price:价格
        trader_type针对买入账户没有持股的股票，一般不改动
        '''
        stats=''
        stock=self.adjust_stock(stock=stock)
        hold_stock=self.position()
        try:
            del hold_stock['Unnamed: 0']
        except:
            pass
        account=self.balance()
        try:
            del account['Unnamed: 0']
        except:
            pass
        if hold_stock.shape[0]>0:
            stock=str(stock)
            df1=hold_stock[hold_stock['证券代码']==stock]
            if df1.shape[0]>0:
                #可以使用的数量兼容t0
                av_num=df1['可用余额'].tolist()[-1]
                #持有数量
                hold_num=df1['股票余额'].tolist()[-1]
                #买卖的差额
                buy_sell_num=amount-float(hold_num)
                #存在买入差额
                if buy_sell_num>0:
                    self.buy(security=stock,amount=int(buy_sell_num),price=price)
                    stats='buy'
                #存在卖出空间：
                elif buy_sell_num <0:
                    #可以卖出的数量多
                    if av_num>=buy_sell_num:
                        buy_sell_num=abs(buy_sell_num)
                        self.sell(security=stock,amount=int(buy_sell_num),price=price)
                        stats='sell'
                    else:
                        #可以卖出的不足卖出全部可以卖出的
                        stats=self.sell(stock=stock,amount=int(av_num),price=price)
                        stats='sell'
                else:
                    print('目标交易{}不存在交易差额'.format(stock))
                    stats=''
            else:
                print('{}没有持股,启动默认交易'.format(stock))
                if trader_type=='buy':
                    self.buy(security=stock,amount=int(amount),price=price)
                    stats='buy'
        else:
            print('{}账户没有持股'.format(stock))
            stats=''
        return stats
    def order_value(self,stock='501018',value=1000,price=1.33):
        '''
        按金额下单
        stock: 证券代码
        value下单金额
        value大于0买入，小0卖出
        prive交易的的价格
        '''
        stats=''
        stock=self.adjust_stock(stock=stock)
        hold_stock=self.position()
        if hold_stock.shape[0]>0:
            stock=str(stock)
            df1=hold_stock[hold_stock['证券代码']==stock]
            if df1.shape[0]>0:
                #可以使用的数量兼容t0
                av_num=df1['可用余额'].tolist()[-1]
                #持有数量
                hold_num=df1['股票余额'].tolist()[-1]
                #持有的价值
                hold_value=df1['市值'].tolist()[-1]
                #买卖价值差转成数量
                amount=math.floor(value/price)
                #可转债最新10
                if stock[:3] in ['110','113','123','127','128','111']:
                    amount=math.floor(amount/10)*10
                else:
                    amount=math.floor(amount/100)*100
                if amount==0:
                    print('交易数量为0不交易')
                else:
                    if amount>0:
                        self.buy(security=stock,amount=int(amount),price=price)
                        stats='buy'
                    else:
                        amount=abs(amount)
                        self.sell(security=stock,amount=int(amount),price=price)
                        stats='sell'
        return stats
    def adjust_amount(self,stock='',amount=''):
        '''
        调整数量
        '''           
        if stock[:3] in ['110','113','123','127','128','111'] or stock[:2] in ['11','12']:
            amount=math.floor(amount/10)*10
        else:
            amount=math.floor(amount/100)*100
        return amount
    def order_target_value(self,stock='501018',value=1000,price=1.33,trader_type='buy'):
        '''
        目标价值下单
        stock: 股票名字
        value: 股票价值，value = 最新价 * 手数 * 保证金率（股票为1） * 乘数（股票为100）
        prive交易的的价格
        '''
        stats=''
        stock=self.adjust_stock(stock=stock)
        hold_stock=self.position()
        try:
            del hold_stock['Unnamed: 0']
        except:
            pass
        account=self.balance()
        try:
            del account['Unnamed: 0']
        except:
            pass
        if hold_stock.shape[0]>0:
            stock=str(stock)
            df1=hold_stock[hold_stock['证券代码']==stock]
            if df1.shape[0]>0:
                #可以使用的数量兼容t0
                av_num=df1['可用余额'].tolist()[-1]
                #持有数量
                hold_num=df1['股票余额'].tolist()[-1]
                #持有的价值
                hold_value=df1['市值'].tolist()[-1]
                #买卖价值差转成数量
                amount=math.floor(value/price)
                #可转债最新10
                if stock[:3] in ['110','113','123','127','128','111']:
                    amount=math.floor(amount/10)*10
                else:
                    amount=math.floor(amount/100)*100
                #买卖的差额
                buy_sell_num=math.floor(amount-float(hold_num))
                #存在买入差额
                if buy_sell_num>0:
                    buy_sell_num=self.adjust_amount(stock=stock,amount=buy_sell_num)
                    stats=self.buy(security=stock,amount=int(buy_sell_num),price=price)
                    stats='buy',buy_sell_num
                #存在卖出空间：
                elif buy_sell_num <0:
                    #可以卖出的数量多
                    if av_num>=buy_sell_num:
                        buy_sell_num=abs(buy_sell_num)
                        buy_sell_num=self.adjust_amount(stock=stock,amount=buy_sell_num)
                        self.sell(security=stock,amount=int(buy_sell_num),price=price)
                        stats='sell',buy_sell_num
                    else:
                        #可以卖出的不足卖出全部可以卖出的
                        av_num=self.adjust_amount(stock=stock,amount=av_num)
                        stats=self.sell(stock=stock,amount=int(av_num),price=price)
                        stats='sell',av_num
                        
                else:
                    print('目标交易{}不存在交易差额'.format(stock))
                    return '',''
            else:
                print('{}没有持股,启动默认交易'.format(stock))
                if trader_type=='buy':
                    av_num=self.adjust_amount(stock=stock,amount=av_num)
                    self.buy(security=stock,amount=int(av_num),price=price)
                    stats='buy',av_num
                else:
                    return '',''
        else:
            print('{}账户没有持股'.format(stock))
            return '',''
        return stats
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
        #stock=self.adjust_stock(stock=stock)
        self.open_set=''
        hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        if data_type=='数量':
            if hold_stock.shape[0]>0:
                stock=str(stock)
                if trader_type=='buy':
                    df1=hold_stock[hold_stock['证券代码']==stock]
                    if df1.shape[0]>0:
                        #可以使用的数量兼容t0
                        av_num=df1['可用余额'].tolist()[-1]
                        #持有数量
                        hold_num=df1['股票余额'].tolist()[-1]
                        #买卖的差额
                        av_buy_sell=limit_volume-hold_num
                        if av_buy_sell>=amount:
                            amount=self.adjust_amount(stock=stock,amount=amount)
                            if amount<=0:
                                return '','',''
                            else:
                                return 'buy',amount,price
                        else:
                            av_buy_sell=self.adjust_amount(stock=stock,amount=av_buy_sell)
                            stock_type=self.select_data_type(stock=stock[:6])
                            if stock_type=='bond':
                                if av_buy_sell>=10:
                                    return 'buy',av_buy_sell,price
                                else:
                                    return '','',''
                            elif stock_type=='stock' or stock_type=='fund':
                                if av_buy_sell>=100:
                                    return 'buy',av_buy_sell,price
                                else:
                                    return '','',''
                            else:
                                return '','',''
                    else:
                        av_buy_sell=limit_volume-0
                        if av_buy_sell>=amount:
                            amount=self.adjust_amount(stock=stock,amount=amount)
                            if amount<=0:
                                
                                return '','',''
                            else:
                                
                                return 'buy',amount,price
                        else:
                            av_buy_sell=self.adjust_amount(stock=stock,amount=av_buy_sell)
                            stock_type=self.select_data_type(stock=stock[:6])
                            if stock_type=='bond':
                                if av_buy_sell>=10:
                                    
                                    return 'buy',av_buy_sell,price
                                else:
                                    
                                    return '','',''
                            elif stock_type=='stock' or stock_type=='fund':
                                if av_buy_sell>=100:
                                    
                                    return 'buy',av_buy_sell,price
                                else:
                                    
                                    return '','',''
                            else:
                                
                                return '','',''
                else:
                    #卖
                    df1=hold_stock[hold_stock['证券代码']==stock]
                    if df1.shape[0]>0:
                        #可以使用的数量兼容t0
                        av_num=df1['可用余额'].tolist()[-1]
                        #持有数量
                        hold_num=df1['股票余额'].tolist()[-1]
                        #可以卖出的数量
                        if av_num>=amount and av_num>0 and amount>0:
                            return 'sell',amount,price
                        else:
                            av_num=self.adjust_amount(stock,amount=av_num)
                            if av_num>0:
                                return 'sell',av_num,price
                            else:
                                return '','',''  
                    else:
            
                        return '','',''   
            else:
                if trader_type=='buy':
                    amount=self.adjust_amount(stock,amount=amount)
                    if amount<=limit_volume:
                        return 'buy',amount,price
                    else:
                        return '','',''    
                else:
                    return '','',''  
        else:
            #金融
            if hold_stock.shape[0]>0:
                stock=str(stock)
                df1=hold_stock[hold_stock['证券代码']==stock]
                amount=value/price
                amount=self.adjust_amount(amount=amount)
                limit_volume=limit_value/price
                limit_volume=self.adjust_amount(amount=limit_volume)
                stock=str(stock)
                if trader_type=='buy':
                    df1=hold_stock[hold_stock['证券代码']==stock]
                    if df1.shape[0]>0:
                        #可以使用的数量兼容t0
                        av_num=df1['可用余额'].tolist()[-1]
                        #持有数量
                        hold_num=df1['股票余额'].tolist()[-1]
                        #买卖的差额
                        av_buy_sell=limit_volume-hold_num
                        if av_buy_sell>=amount:
                            amount=self.adjust_amount(stock=stock,amount=amount)
                            if amount<=0:
                                stock_type=self.select_data_type(stock=stock[:6])
                                if stock_type=='bond':
                                    amount=10
                                else:
                                    amount=100
                                return 'buy',amount,price
                            else:
                                return 'buy',amount,price
                        else:
                            av_buy_sell=self.adjust_amount(stock=stock,amount=av_buy_sell)
                            stock_type=self.select_data_type(stock=stock[:6])
                            if stock_type=='bond':
                                if av_buy_sell>=10:
                                    return 'buy',av_buy_sell,price
                                else:
                                    return 'buy',10,price
                            elif stock_type=='stock' or stock_type=='fund':
                                if av_buy_sell>=100:
                                    return 'buy',av_buy_sell,price
                                else:
                                    return 'buy',100,price
                            else:
                                return '','',''
                    else:
                        amount=value/price
                        amount=self.adjust_amount(stock,amount=amount)
                        limit_volume=limit_value/price
                        limit_volume=self.adjust_amount(amount=limit_volume)
                        if limit_volume>=amount:
                            amount=self.adjust_amount(stock=stock,amount=amount)
                            if amount<=0:
                                stock_type=self.select_data_type(stock=stock[:6])
                                if stock_type=='bond':
                                    amount=10
                                else:
                                    amount=100
                                return 'buy',amount,price
                            else:
                                return 'buy',amount,price
                        else:
                            return '','',''
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
                        #可以卖出的数量
                        if av_num>=amount and av_num>0 and amount>0:
                            return 'sell',amount,price
                        else:
                            av_num=self.adjust_amount(stock,amount=av_num)
                            if av_num>0:
                                return 'sell',av_num,price
                            else:
                                return '','',''  
                    else:
                        return '','','' 
            else:
                if trader_type=='buy':
                    amount=value/price
                    amount=self.adjust_amount(stock,amount=amount)
                    limit_volume=limit_value/price
                    limit_volume=self.adjust_amount(amount=limit_volume)
                    if amount<=limit_volume and amount>0:
                        return 'buy',amount,price
                    else:
                        stock_type=self.select_data_type(stock=stock[:6])
                        if stock_type=='bond':
                            amount=10
                        else:
                            amount=100
                        return 'buy',amount,price 
                else:
                    return '','',''      
    
if __name__=='__main__':
    models=qmt_trader_ths()
    models.connect()
    print(models.query_stock_orders())
    models.buy()
    models1=qmt_trader_ths(account='55009680',session_id=123457)
    models1.connect()
    print(models1.query_stock_positions())
    

