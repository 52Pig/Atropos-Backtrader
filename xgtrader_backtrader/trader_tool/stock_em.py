import requests
import pandas as pd
import json
import time
import os
'''
函数名称       函数
获取全部组合代码 get_all_zh_code()
登录操作自选股  login()
建立自选股模块   create_stock_zh(name='涨停板')
删除自选股模块   del_stock_zh_name(name='涨停板')
获取全部的自选股  get_all_account_stock()
添加股票         add_stock_to_account(name='涨停板',stock='600031')
删除股票         del_stock_from_account(name='涨停板',stock='600009')
获取涨停数据      get_zt_data_em()
将全部的涨停股票加入东方财富自选股     all_zt_stock_add_to_account(name='涨停板')
将昨天涨停今日没有涨停的股票踢出自选股 del_not_zt_stock_from_account()
获取股票组合全部股票  get_stock_zh_all_stock(name='涨停板')
'''
class stock_em:
    def __init__(self,Cookie='qgqp_b_id=c4fe92d6c0206867bc4f6dda1b26a14b; mtp=1; ct=tKskCXGfPKuQ5QDKMU2CPkLgFb5rD_T0LgmR43Gvtb-N5Cm2b8KwkJHFGr8tYcLn8raccDaEAXqiQJ-KWSnlvsnsGx4SG6Cic6nuyPkycMPImR5TBujiCDWp9xuF97I54nVrDLj7ZNm2cqIBi1HP1W7ItAi382XMs6kHvXkGzYA; ut=FobyicMgeV6Hb_DbDix6-Ocg0eztXx9lKcjRgmne9MNM7bEii9I76_02_-60R62gBRMEtnsuGwj-jZ_qkADMSH_-o-gue9_zfemLnHVY16ysRmOHureIqLGi4UucQV0d0RYVOrXZbwVfkm6WqU02sgOFcKnsXup6o4sQAIgIOmWCXnounqBbJ_agpZdnHEZjTVA8B5eytbgOANTztopcmXPmYR8eEPZJ4oJkA8pb7o_L5mRXMIkLAeNd5pFJCoSiXpD5b5trLKgmZnkNNT60wWPGcLCL3THJ; pi=1452376043169950%3Bs1452376043169950%3B%E7%BB%8F%E7%AE%A1%E8%8F%9C%E9%B8%9F%3B8mgnKlaj7AvbEFdQy2bdb63SYdEvdEXIvs2GPYnsSPvldwfQSQsij7nTAVL4XwUEPsk5rvS0qRgUZiRsqtMDinmMlRSl5pYeRDZgyv4BMahOrdOduBvVK2L2x3WgceUSiKz125smIvItmzlxo1PuPCfz5FbRyaz4Hl4U%2B15MUYgLeI9yRsBuC%2F68MQLhiQZyK%2FKkIoQr%3B4rm7BIdF5pM%2B6Y9Uycgup5Vv%2BtadzuAz3ony2617OlaZAY24%2BW8FUJzCojv41RS8n2FB%2Bo2%2FejDsM9v%2BjDM09zQBU49WltuvOOQN5OK3PbMhIFhbyPrYXMkCmmInhWbYg7lS%2BBI3pyjHkEyWpQhA7zX46m8gPQ%3D%3D; uidal=1452376043169950%e7%bb%8f%e7%ae%a1%e8%8f%9c%e9%b8%9f; sid=152853388; vtpst=|; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; HAList=ty-0-123223-%u4E5D%u5178%u8F6C02%2Cty-0-127092-%u8FD0%u673A%u8F6C%u503A%2Cty-1-603123-%u7FE0%u5FAE%u80A1%u4EFD%2Cty-1-600355-%u7CBE%u4F26%u7535%u5B50%2Cty-0-000996-*ST%u4E2D%u671F%2Cty-0-300331-%u82CF%u5927%u7EF4%u683C%2Cty-1-603607-%u4EAC%u534E%u6FC0%u5149%2Cty-1-600895-%u5F20%u6C5F%u9AD8%u79D1%2Cty-0-000564-ST%u5927%u96C6%2Cty-0-301191-%u83F2%u83F1%u79D1%u601D; websitepoptg_api_time=1697383224641; st_si=46642354424048; st_asi=delete; st_pvi=38509843414622; st_sp=2023-07-22%2008%3A46%3A44; st_inirUrl=https%3A%2F%2Fcn.bing.com%2F; st_sn=2; st_psi=20231016231454761-113200301712-8122359889',appkey='d41d8cd98f00b204e9800998ecf8427e'):
        self.cookie=Cookie
        self.appkey=appkey
    def get_headers(self):
        headers=headers={
            'Cookie':self.cookie,
            'Host':'myfavor.eastmoney.com',
            'Referer':'http://quote.eastmoney.com/zixuan/?from=home',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
        }
        return headers
    def get_all_zh_code(self):
        '''
        获取全部组合代码，名称
        '''
        url='http://myfavor.eastmoney.com/v4/webouter/ggdefstkindexinfos?'
        headers=self.get_headers()
        params={
            'appkey': 'd41d8cd98f00b204e9800998ecf8427e',
        }
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        df=pd.DataFrame(text['data']['ginfolist'])
        return df
    #建立自选股模块
    def create_stock_zh(self,name='涨停板'):
        '''
        建立自选股模块
        '''
        all_name=self.get_all_zh_code()
        name_dict=dict(zip(all_name['gname'],all_name['gid']))
        name_list=list(name_dict.keys())
        if name in name_list:
            print('{}自选股已经存在'.format(name))
            print('存在的自选股')
            print(all_name)
            return '存在'
        else:
            header=self.get_headers()
            params={
                'appkey':self.appkey,
                'gn':name

            }
            url="http://myfavor.eastmoney.com/v4/webouter/ag?"
            res=requests.get(url=url,params=params,headers=header)
            text=res.json()
            message=text['message']
            if message=='成功':
                print('{}自选股建立成功'.format(name))
                return message
            else:
                print(message)
                return message
            
    #删除自选股模块
    def del_stock_zh_name(self,name='卖出股票'):
        '''
        name=自选股默认的是自选股
        '''
        all_name=self.get_all_zh_code()
        name_dict=dict(zip(all_name['gname'],all_name['gid']))
        name_list=list(name_dict.keys())
        if name in name_list:
            headers=self.get_headers()
            g=name_dict[name]
            params={
                'appkey':self.appkey,
                'g':g,
            }
            url='http://myfavor.eastmoney.com/v4/webouter/dg?'
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            message=text['message']
            if message=='成功':
                print('{}自选股删除成功'.format(name))
                return message
        else:
            print('{}自选股不存在'.format(name))
            print('存在的自选股')
            print(all_name)
            return '不存在'
    def add_stock_to_account(self,name='涨停板',stock='600031'):
        '''
        添加股票
        stock证券代码
        name=自选股默认的是自选股
        '''
        headers=self.get_headers()
        all_name=self.get_all_zh_code()
        name_dict=dict(zip(all_name['gname'],all_name['gid']))
        name_list=list(name_dict.keys())
        if name not in name_list:
            print('{}自选股不存在建立{}自选股'.format(name,name)) 
            stats=self.create_stock_zh(name=name)
            if stats=='超过分组上限':
                name='自选股'
                print('超过分组上限{}自动添加到自选股'.format(stock))
                gid=name_dict[name]
                if stock[0]=='6' or stock[:1]=='68':
                    code='1$'+stock
                elif stock[0]=='0' or stock[0]=='3':
                    code='0$'+stock
                elif stock[0]=='1':
                    code='0$'+stock
                elif stock[0]=='5':
                    code='1$'+stock
                else:
                    code=stock
                params={
                    'appkey': self.appkey,
                    'g':gid,
                    'sc':code
                }
                url='http://myfavor.eastmoney.com/v4/webouter/as?'
                res=requests.get(url=url,params=params,headers=headers)
                text=res.json()
                message=text['message']
                if message=='成功':
                    print('{}添加到{}自选股成功'.format(stock,name))
                else:
                    print('{}在{}自选股已经存在'.format(stock,name))
                    return message
        else:
            gid=name_dict[name]
            if stock[0]=='6' or stock[:1]=='68':
                code='1$'+stock
            elif stock[0]=='0' or stock[0]=='3':
                code='0$'+stock
            elif stock[0]=='1':
                code='0$'+stock
            elif stock[0]=='5':
                code='1$'+stock
            else:
                code=stock
            params={
                'appkey': self.appkey,
                'g':gid,
                'sc':code,
                }

            url='http://myfavor1.eastmoney.com/v4/webouter/as?'
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            message=text['message']
            if message=='成功':
                print('{}添加到{}自选股成功'.format(stock,name))
            else:
                print(message)
                print('{}在{}自选股已经存在'.format(stock,name))
                return message
    def del_stock_from_account(self,name='涨停板',stock='600009'):
        '''
        删除股票
        stock证券代码
        name=自选股默认的是自选股
        '''
        headers=self.get_headers()
        all_name=self.get_all_zh_code()
        name_dict=dict(zip(all_name['gname'],all_name['gid']))
        name_list=list(name_dict.keys())
        if name in name_list:
            g=name_dict[name]
            if stock[0]=='6' or stock[:1]=='68':
                code='1$'+stock
            elif stock[0]=='0' or stock[0]=='3':
                code='0$'+stock
            elif stock[0] == '1':
                code = '0$' + stock
            elif stock[0] == '5':
                code = '1$' + stock
            else:
                code=stock
            params={
                'appkey':self.appkey,
                'g':g,
                'sc':code

            }
            url='http://myfavor.eastmoney.com/v4/webouter/ds?'
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            message=text['message']
            if message=='成功':
                print('{}从{}自选股删除成功'.format(stock,name))
            else:
                print('{}在{}自选股不存在'.format(stock,name))
                return message
        else:
            print('没有{}自选股'.format(name))
        
    def get_stock_zh_all_stock(self,name='自选股'):
        '''
        获取股票组合全部股票
        name=自选股默认的是自选股
        '''
        headers=self.get_headers()
        all_name=self.get_all_zh_code()
        name_dict=dict(zip(all_name['gname'],all_name['gid']))
        name_list=list(name_dict.keys())
        if name in name_list:
            g=name_dict[name]
            params={
                'appkey':self.appkey,
                'g':g
            }
            url='http://myfavor.eastmoney.com/v4/webouter/gstkinfos?'
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            message=text['message']
            if message=='成功':
                df=pd.DataFrame(text['data']['stkinfolist'])
                if df.shape[0]>0:
                    df=df[['security','updatetime','price']]
                    df['security']=df['security'].apply(lambda x:str(x)[2:8])
                else:
                    print('{}自选股没有持股'.format(name))
                    df['security']=None
                    df['updatetime']=None
                    df['price']=None
                return df
            else:
                print(message)
                return message
        else:
            print('{}自选股不存在'.format(name))

    
    