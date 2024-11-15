import random
import json
import time
import math
import pandas as pd
import yagmail
class base_func:
    def __init__(self):
        pass
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
        elif stock[:3] in ['510','511','512','513','514','515','516','517','518','588','159','501','164'] or stock[:2] in ['16']:
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
    def adjust_amount(self,stock='',amount=''):
        '''
        调整数量
        '''           
        if stock[:3] in ['110','113','123','127','128','111']:
            amount=math.floor(amount/10)*10
        else:
            amount=math.floor(amount/100)*100
        return amount
    def check_stock_is_av_buy(self,stock='128036',price='156.700',amount=10,hold_limit=100):
        '''
        检查是否可以买入
        '''
        stock=self.adjust_stock(stock=stock)
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
        stock=self.adjust_stock(stock=stock)
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
    def adjust_hold_data(self,stock='603918',trader_type='sell',price=12,amount=100):
        '''
        模拟持股数据
        '''
        price=float(price)
        amount=float(amount)
        df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
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
                stock_balance-=float(amount)
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
        if trader_type=='buy':
            av_user_cash-=value
        elif trader_type=='sell':
            av_user_cash+=value
        else:
            av_user_cash=av_user_cash
        df['可用金额']=[av_user_cash]
        df.to_excel(r'账户数据\账户数据.xlsx')
        print('账户资金调整完成')
        return df
    def seed_dingding(self,msg='买卖交易成功,',access_token_list=['ab5d0a609429a786b9a849cefd5db60c0ef2f17f2ec877a60bea5f8480d86b1b']):
        import requests
        import json
        import random
        access_token=random.choice(access_token_list)
        url='https://oapi.dingtalk.com/robot/send?access_token={}'.format(access_token)
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "text",  # 发送消息类型为文本
            "at": {
                #"atMobiles": reminders,
                "isAtAll": False,  # 不@所有人
            },
            "text": {
                "content": msg,  # 消息正文
            }
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        text=r.json()
        errmsg=text['errmsg']
        if errmsg=='ok':
                print('钉钉发生成功')
                return text
        else:
            print(text)
            return text
    def seed_trader_info(self,text='交易完成'):
        with open(r'分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text1=json.loads(com)
        seed_type=text1['发送方式']
        if seed_type=='qq':
            try:
                password=text1['qq掩码']
                seed_qq=text1['发送qq']
                yag = yagmail.SMTP(user='{}'.format(seed_qq), password=password, host='smtp.qq.com')
                m = text1['接收qq']
                text = text
                yag.send(to=m, contents=text, subject='邮件')
                print('邮箱发生成功')
            except:
                print('qq发送失败可能用的人多')
        else:
            account_token_list=text1['钉钉account_token']
            text=text+','
            self.seed_dingding(msg=text,access_token_list=account_token_list)
    def get_seed_qq_test(self,text='交易完成',seed_qq='1752515969@qq.com',qq_paasword='jgyhavzupyglecaf',re_qq='1029762153@qq.com'):
        '''
        发送qq，可以自己给自己发
        text发送内容，支持表格文字
        see_qq发送QQ
        qq_pasword发送qq的掩码
        re_qq接收信息QQ
        '''
        try:
            yag = yagmail.SMTP(user=seed_qq, password=qq_paasword, host='smtp.qq.com')
            text = text
            yag.send(to=re_qq, contents=text, subject='邮件')
            print('qq发送完成')
        except:
            print('qq发送失败')
    
    def read_tdx_trader_stock_buy(path=r'D:\新建文件夹\T0002\blocknew\TRADER_STOCK.blk'):
        '''
        读取通达信自选股交易,买入模块
        '''
        try:
            stock_list=[]
            with open('{}'.format(path),'r+') as f:
                com=f.readlines()
            for i in com:
                i=i.strip()
                if len(i)>0:
                    stock_list.append(i)
            df=pd.DataFrame()
            df['证券代码']=stock_list
            df['证券代码']=df['证券代码'].apply(lambda x:str(x)[-6:])
            df['交易状态']='未买'
            return df
        except:
            print('路径有问题{}'.format(path))
            df=pd.DataFrame()
            df['证券代码']=None
            df['交易状态']=None
            return df
    def read_tdx_trader_stock_sell(path=r'D:\新建文件夹\T0002\blocknew\TRADER_STOCK.blk'):
        '''
        读取通达信自选股交易,卖出模块
        '''
        try:
            stock_list=[]
            with open('{}'.format(path),'r+') as f:
                com=f.readlines()
            for i in com:
                i=i.strip()
                if len(i)>0:
                    stock_list.append(i)
            df=pd.DataFrame()
            df['证券代码']=stock_list
            df['证券代码']=df['证券代码'].apply(lambda x:str(x)[-6:])
            df['交易状态']='未卖'
            return df
        except:
            print('路径有问题{}'.format(path))
            df=pd.DataFrame()
            df['证券代码']=None
            df['交易状态']=None
            return df



