from xgtrader import easytrader
from pywinauto.application import Application
import pyautogui
import time
import pandas as pd
import warnings
from xgtrader import pytesseract
import math
import json
warnings.filterwarnings(action='ignore')
class xgtrader:
    def __init__(self,exe=r'C:\同花顺软件\同花顺\xiadan.exe',
    tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract',
    is_slippage=True,slippage=0.01,
    data_soure='本地',
    open_set='是'):
        '''
        exe同花顺客户端，不是下单程序
        tesseract_cmd识别软件安装位置
        同花顺历史版本下载，我用的是最新版
        http://activity.10jqka.com.cn/acmake/cache/486.html#download
        slippage滑点
        data_sour=本地/默认
        '''
        self.exe=exe
        self.user=''
        pytesseract.tesseract_cmd=tesseract_cmd
        if is_slippage==True:
            self.slippage=slippage
        else:
            self.slippage=0
        self.data_soure=data_soure
        self.open_set=open_set
    def select_slippage(self,stock='600031',price=15.01,trader_type='buy'):
        '''
        选择滑点
        安价格来滑点，比如0.01就是一块
        etf3位数可转债,股票可转债2位数
        '''
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

    def select_data_type(self,stock='600031'):
        '''
        选择数据类型
        '''
        if stock[:3] in ['110','113','123','127','128','111','118']:
            return 'bond'
        elif stock[:3] in ['510','511','512','513','514','515','516','517','518','588','159','501','164']:
            return 'fund'
        else:
            return 'stock'
    def login(self):
        '''
        登录
        '''
        app = Application(backend="uia").start(self.exe,timeout=20)
        time.sleep(3)
        pyautogui.press('10')
        time.sleep(3)
        pyautogui.press('f12')
        pyautogui.press('f10')
        time.sleep(3)
        pyautogui.press('f12')
        time.sleep(10)
    def exit_procedure(self):
        '''
        退出程序
        '''
        #退出交易交易程序
        pyautogui.hotkey('alt','f4')
        time.sleep(3)
        #退出同花顺
        pyautogui.hotkey('alt','f4')
        time.sleep(3)
        pyautogui.press('enter')
    def connect(self,client='universal_client'):
        print('链接同花顺')
        user=easytrader.use(client)
        #path=self.exe[:-9]+'xiadan.exe'
        user.connect('{}'.format(self.exe))
        #不使用这个可能无法输入数据
        user.enable_type_keys_for_editor()
        self.user=user
        #return self.user
    def buy_chi_bond(self,security='GC001', price=2.61, amount=1000):
        self.user.repo(security=security, price=price, amount=amount)
    def balance(self):
        '''
        获取资金状况
        '''
        try:
            balance=self.user.balance
            df=pd.DataFrame()
            for key,value in balance.items():
                df[key]=[value]
            return df
        except:
            try:
                self.user.refresh()
                balance=self.user.balance
                df=pd.DataFrame()
                for key,value in balance.items():
                    df[key]=[value]
                return df
            except:
                print('获取账户失败读取上次数据，谨慎使用')
                df=pd.read_excel(r'账户数据\账户数据.xlsx',dtype='object')
                try:
                    del df['Unnamed: 0']
                except:
                    pass
                return df
    def position(self):
        '''
        获取持股
        '''
        try:
            position=self.user.position
            df=pd.DataFrame(position)
            if self.open_set=='是':
                df['股票余额']=df['股票余额']
                df['可用余额']=df['可用余额']
            else:
                pass
            return df
        except:
            try:
                self.user.refresh()
                position=self.user.position
                df=pd.DataFrame(position)
                if self.open_set=='是':
                    df['股票余额']=df['股票余额']
                    df['可用余额']=df['可用余额']
                else:
                    pass
                return df
            except:
                print('获取持股失败读取上次数据，谨慎使用')
                df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
                try:
                    df['Unnamed: 0']
                except:
                    pass
                return df
    def buy(self,security='600031', price=16.5, amount=100):
        '''
        买入不调整数据兼容以前的框架
        '''
        if self.open_set=='是':
            amount=amount/10
        else:
            pass
        price=self.select_slippage(stock=security,price=price,trader_type='buy')
        try:
            self.user.buy(security=security,price=price,amount=amount)
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('enter')
            return True
        except:
            try:
                self.user.refresh()
                self.user.buy(security=security,price=price,amount=amount)
                pyautogui.press('enter')
                pyautogui.press('enter')
                pyautogui.press('enter')
                pyautogui.press('enter')
                pyautogui.press('enter')
                pyautogui.press('enter')
                return True
            except:
                print('买入失败')
                return False
    def sell(self,security='300780', price=14, amount=100):
        '''
        卖出调整数据兼容以前的框架
        '''
        if self.open_set=='是':
            amount=amount/10
        else:
            pass
        price=self.select_slippage(stock=security,price=price,trader_type='sell')
        try:
            self.user.sell(security=security,price=price,amount=amount)
            pyautogui.press('enter')
            return True
        except:
            try:
                self.user.refresh()
                self.user.sell(security=security,price=price,amount=amount)
                pyautogui.press('enter')
                return True
            except:
                print('卖出失败')
                return False
    def market_buy(self, security, amount, ttype=None, limit_price=None, **kwargs):
        """
        市价买入
        :param security: 六位证券代码
        :param amount: 交易数量
        :param ttype: 市价委托类型，默认客户端默认选择，
                     深市可选 ['对手方最优价格', '本方最优价格', '即时成交剩余撤销', '最优五档即时成交剩余 '全额成交或撤销']
                     沪市可选 ['最优五档成交剩余撤销', '最优五档成交剩余转限价']
        :param limit_price: 科创板 限价

        :return: {'entrust_no': '委托单号'}
        """
        if self.open_set=='是':
            amount=amount/10
        else:
            pass
        price=self.select_slippage(stock=security,price=price,trader_type='buy')
        self.user.market_buy(security, amount, ttype=None, limit_price=None, **kwargs)
    def market_sell(self, security, amount, ttype=None, limit_price=None, **kwargs):
        """
        市价卖出
        :param security: 六位证券代码
        :param amount: 交易数量
        :param ttype: 市价委托类型，默认客户端默认选择，
                     深市可选 ['对手方最优价格', '本方最优价格', '即时成交剩余撤销', '最优五档即时成交剩余 '全额成交或撤销']
                     沪市可选 ['最优五档成交剩余撤销', '最优五档成交剩余转限价']
        :param limit_price: 科创板 限价
        :return: {'entrust_no': '委托单号'}
        """
        if self.open_set=='是':
            amount=amount/10
        else:
            pass
        price=self.select_slippage(stock=security,price=price,trader_type='sell')
        self.user.market_sell(security, amount, ttype=None, limit_price=None, **kwargs)

    def market_trade(self, security, amount, ttype=None, limit_price=None, **kwargs):
        """
        市价交易
        :param security: 六位证券代码
        :param amount: 交易数量
        :param ttype: 市价委托类型，默认客户端默认选择，
                     深市可选 ['对手方最优价格', '本方最优价格', '即时成交剩余撤销', '最优五档即时成交剩余 '全额成交或撤销']
                     沪市可选 ['最优五档成交剩余撤销', '最优五档成交剩余转限价']

        :return: {'entrust_no': '委托单号'}
        """
        if self.open_set=='是':
            amount=amount/10
        else:
            pass
        self.user.market_trade(security, amount, ttype=None, limit_price=None, **kwargs)
    def auto_ipo(self):
        '''
        打新
        '''
        try:
            self.user.auto_ipo()
        except:
           self.user.refresh()
           self.user.auto_ipo()
    def cancel_entrust(self,tarder_type='全撤'):
        '''
        撤单buy/sell 获取的 entrust_no
        '''
        try:
            if tarder_type=='全撤':
                self.user.cancel_all_entrusts()
            else:
                self.user.cancel_entrusts()
        except:
            self.user.refresh()
            if tarder_type=='全撤':
                self.user.cancel_all_entrusts()
            else:
                self.user.cancel_entrusts()
    def today_trades(self):
        '''
        当日成交
        '''
        try:
            df=self.user.today_trades
            df=pd.DataFrame(df)
            if df.shape[0]==0 or df is None:
                print('今日没有成交')
                return False
            else:
                return df
        except:
            try:
                self.user.refresh()
                df=self.user.today_trades
                df=pd.DataFrame(df)
                if df.shape[0]==0 or df is None:
                    print('今日没有成交')
                    return False
                else:
                    return df
            except:
                print('当日成交获取失败')
                return False
    def today_entrusts(self):
        '''
        当日委托
        '''
        try:
            df=self.user.today_entrusts
            df=pd.DataFrame(df)
            if df.shape[0]==0 or df is None:
                print('当日没有委托')
                return False
            else:
                return df
            return df
        except:
            try:
                self.user.refresh()
                df=self.user.today_entrusts
                df=pd.DataFrame(df)
                if df.shape[0]==0 or df is None:
                    print('当日没有委托')
                    return False
                else:
                    return df
            except:
                print('当日委托失败')
                return False
    def refresh(self):
        '''
        刷新
        '''
        try:
            self.user.refresh()
        except:
            self.refresh()
    def exit(self):
        '''
        退出
        '''
        self.user.exit()
    def save_balance(self):
        '''
        保持账户数据
        '''
        df=self.balance()
        df.to_excel(r'账户数据\账户数据.xlsx')
        return df
    def save_position(self):
        '''
        保存持股数据
        1兼容以前老的债券公司可转债
        '''
        df=self.position()
        if df.shape[0]>0:
            df1=df[df['可用余额']>=1]
            df1.to_excel(r'持股数据\持股数据.xlsx')
            return df1
        else:
            print('没有持股')
    def save_all_data(self):
        '''
        保持全部数据
        '''
        self.save_balance()
        self.save_position()
    def adjust_hold_data(self,stock='603918',trader_type='sell',price=12,amount=100):
        '''
        模拟持股数据
        '''
        price=float(price)
        amount=float(amount)
        if self.data_soure=='本地':
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        else:
            df=self.position()
        del df['Unnamed: 0']
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
                if stock_balance<=0:
                    stock_balance=0
            else:
                pass
            df1['可用余额']=[available_balance]
            df1['股票余额']=[stock_balance]
            data=df.drop(stock,axis=0)
            data=pd.concat([data,df1],ignore_index=True)
            data.to_excel(r'持股数据\持股数据.xlsx')
            print('持股数据调整成功')
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
            data.to_excel(r'持股数据\持股数据.xlsx')
            print('持股数据调整成功')													
            print('{}没有持股'.format(stock))
    def adjust_account_cash(self,stock='128036',trader_type='buy',price=123,amount=10):
        '''
        调整账户资金
        '''
        price=float(price)
        amount=float(amount)
        df=pd.read_excel(r'账户数据\账户数据.xlsx',dtype='object')
        try:
            del df['Unnamed: 0']
        except:
            pass
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
        df.to_excel(r'账户数据\账户数据.xlsx')
        print('账户资金调整完成')
        return df
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
    def check_stock_is_av_buy(self,stock='128036',price='156.700',amount=10,hold_limit=100):
        '''
        检查是否可以买入
        '''
        price=float(price)
        buy_value=price*amount
        cash_df=pd.read_excel(r'账户数据\账户数据.xlsx',dtype='object')
        try:
            del cash_df['Unnamed: 0'] 
        except:
            pass
        hold_data=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        try:
            del hold_data['Unnamed: 0'] 
        except:
            pass
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
        hold_data=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        try:
            del hold_data['Unnamed: 0'] 
        except:
            pass
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
    def order_target_volume(self,stock='501018',amount=1000,price=12,trader_type='buy'):
        '''
        目标数量下单
        stock: 标的代码
        amount: 期望的最终数量
        price:价格
        trader_type针对买入账户没有持股的股票，一般不改动
        '''
        stats=''
        if self.data_soure=='本地':
            hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        else:
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
                    if self.open_set=='是':
                        buy_sell_num=buy_sell_num/10
                    else:
                        pass
                    self.buy(security=stock,amount=int(buy_sell_num),price=price)
                    stats='buy'
                #存在卖出空间：
                elif buy_sell_num <0:
                    #可以卖出的数量多
                    if av_num>=buy_sell_num:
                        buy_sell_num=abs(buy_sell_num)
                        if self.open_set=='是':
                            buy_sell_num=buy_sell_num/10
                        else:
                            pass
                        self.sell(security=stock,amount=int(buy_sell_num),price=price)
                        stats='sell'
                    else:
                        #可以卖出的不足卖出全部可以卖出的
                        if self.open_set=='是':
                            av_num=av_num/10
                        else:
                            pass
                        stats=self.sell(stock=stock,amount=int(av_num),price=price)
                        stats='sell'
                else:
                    print('目标交易{}不存在交易差额'.format(stock))
                    stats=''
            else:
                print('{}没有持股,启动默认交易'.format(stock))
                if trader_type=='buy':
                    if self.open_set=='是':
                        amount=amount/10
                    else:
                        pass
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
        
        if self.data_soure=='本地':
            hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        else:
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
                if stock[:3] in ['110','113','123','127','128','111'] or stock[:2] in ['12','11']:
                    amount=math.floor(amount/10)*10
                else:
                    amount=math.floor(amount/100)*100
                if amount==0:
                    print('交易数量为0不交易')
                else:
                    if amount>0:
                        if self.open_set=='是':
                            amount=amount/10
                        else:
                            pass
                        self.buy(security=stock,amount=int(amount),price=price)
                        stats='buy'
                    else:
                        amount=abs(amount)
                        if self.open_set=='是':
                            amount=amount/10
                        else:
                            pass
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
        
        if self.data_soure=='本地':
            hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        else:
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
        if self.data_soure=='本地':
            hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        else:
            hold_stock=self.position()
        try:
            del hold_stock['Unnamed: 0']
        except:
            pass
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
    a=xgtrader()
    a.connect()
    #保持最新数据
    a.save_all_data()
    a.buy()
    a.order_target_value()
