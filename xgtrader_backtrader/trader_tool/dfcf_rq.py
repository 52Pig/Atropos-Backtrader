import pandas as pd
import requests
import json
#from stock_change import stock_em
class popularity:
    '''
    股票人气
    '''
    def __init__(self,data_type='人气',market='A',globalId='786e4c21-70dc-435a-93bb-38'):
        '''
        输入默认参数
        data_type=人气/飙升
        maker市场=A/HK/US/ETF
        :param maker:
        :param globalId:
        '''
        self.globalId=globalId
        self.data_type=data_type
        self.market=market
        if self.market == 'A':
            self.marketType = ""
        elif self.market == 'HK':
            self.marketType = '000003'
        elif self.market == 'US':
            self.marketType = '000004'
        elif self.market == 'ETF':
            self.marketType = 'etf'
        else:
            self.marketType = ""
    def get_all_stock_rank_code(self):
        '''
        获取全部证券代码
        :return:
        '''
        if self.data_type=='人气':
            if self.market=='A':
                marketType=""
                url = 'https://emappdata.eastmoney.com/stockrank/getAllCurrentList'
                def select_data(x):
                    if x[:2] == 'SH':
                        return '1.' + x[2:]
                    else:
                        return '0.' + x[2:]
            elif self.market=='HK':
                marketType='000003'
                url='https://emappdata.eastmoney.com/stockrank/getAllCurrHkUsList'
                def select_data(x):
                    return '116.'+x.split('|')[1]
            elif self.market=='US':
                marketType ='000004'
                url='https://emappdata.eastmoney.com/stockrank/getAllCurrHkUsList'
                def select_data(x):
                    X=x.split('|')
                    if X[0]=='NASDAQ':
                        return '105.'+X[1]
                    else:
                        return '106.' + X[1]
            elif self.market=='ETF':
                marketType='etf'
                url='https://emappdata.eastmoney.com/fundrank/getAllCurrentETFList'
                def select_data(x):
                    if x[:2] == 'SH':
                        return '1.' + x[2:]
                    else:
                        return '0.' + x[2:]
            else:
                marketType=""
                url = 'https://emappdata.eastmoney.com/stockrank/getAllCurrentList'
        elif self.data_type=='飙升':
            if self.market=='A':
                marketType=""
                url = 'https://emappdata.eastmoney.com/stockrank/getAllHisRcList'
                def select_data(x):
                    if x[:2] == 'SH':
                        return '1.' + x[2:]
                    else:
                        return '0.' + x[2:]
            elif self=='HK':
                marketType='000003'
                url='https://emappdata.eastmoney.com/stockrank/getAllHisRcHkUsList'
                def select_data(x):
                    return '116.'+x.split('|')[1]
            elif self.market=='US':
                marketType ='000004'
                url='https://emappdata.eastmoney.com/stockrank/getAllHisRcHkUsList'
                def select_data(x):
                    X=x.split('|')
                    if X[0]=='NASDAQ':
                        return '105.'+X[1]
                    else:
                        return '106.' + X[1]
            elif self.market=='ETF':
                marketType='etf'
                url='https://emappdata.eastmoney.com/fundrank/getAllHisRcETFList'
                def select_data(x):
                    if x[:2] == 'SH':
                        return '1.' + x[2:]
                    else:
                        return '0.' + x[2:]
            else:
                marketType=""
                url = 'https://emappdata.eastmoney.com/stockrank/getAllHisRcList'
                def select_data(x):
                    if x[:2] == 'SH':
                        return '1.' + x[2:]
                    else:
                        return '0.' + x[2:]
        data={"appId": "appId01", "globalId": self.globalId, "marketType": marketType, "pageNo": 1, "pageSize": 100}
        url=url
        headers={
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '101',
            'content-type': 'application/json',
            'origin': 'https://vipmoney.eastmoney.com',
            'referer': 'https://vipmoney.eastmoney.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
        }
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['data'])
        try:
            df.columns=['证券代码','排名','rc']
        except:
            df.columns = ['证券代码', '排名','历史排名', 'rc']
        df['证券代码1']=df['证券代码']
        df['证券代码']=df['证券代码'].apply(select_data)
        return df
    def get_stock_popularity_rank_data(self):
        '''
        人气排行数据
        :return:
        '''
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '101',
            'content-type': 'application/json',
            'origin': 'https://vipmoney.eastmoney.com',
            'referer': 'https://vipmoney.eastmoney.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
        }
        url='https://push2.eastmoney.com/api/qt/ulist.np/get?'
        secids=','.join(self.get_all_stock_rank_code()['证券代码'].tolist())
        params={
            'ut': 'f057cbcbce2a86e2866ab8877db1d059',
            'fltt': '2',
            'invt': '2',
            'fields':'f14,f148,f3,f12,f2,f13,f29',
            'secids':secids,
            'v':'03661423047380299'
        }
        res=requests.get(url=url,params=params)
        text=res.json()
        df=pd.DataFrame(text['data']['diff'])
        df.columns=['最新价','涨跌幅','代码','市场','股票名称','f29','f148']
        return df
    def get_stock_hist_rank(self,stock='SZ300075'):
        '''
        获取股票历史排名
        香港市场/美股带有标识符HK|00700
        基金ETF待遇市场标识符SH,SZ SH512480
        :param stock:
        :return:
        '''
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '104',
            'content-type': 'application/json',
            'origin': 'https://vipmoney.eastmoney.com',
            'referer': 'https://vipmoney.eastmoney.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
        }
        data={"appId":"appId01","globalId":self.globalId,"marketType":self.marketType,"srcSecurityCode":stock}
        url='https://emappdata.eastmoney.com/stockrank/getHisList'
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['data'])
        df.columns=['日期','排名']
        df['排名变化']=df['排名'].shift(1)-df['排名']
        return df
    def get_stock_spot_rank_data(self,stock='SZ300075'):
        '''
        获取实时排名数据
        香港市场/美股带有标识符HK|00700
        基金ETF待遇市场标识符SH,SZ SH512480
        :param stock:
        :return:
        '''
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '104',
            'content-type': 'application/json',
            'origin': 'https://vipmoney.eastmoney.com',
            'referer': 'https://vipmoney.eastmoney.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
        }
        url='https://emappdata.eastmoney.com/stockrank/getCurrentList'
        data={"appId":"appId01","globalId":self.globalId,"marketType":self.marketType,"srcSecurityCode":stock}
        res=requests.post(url=url,headers=headers,data=json.dumps(data))
        text=res.json()
        df = pd.DataFrame(text['data'])
        df.columns = ['日期', '排名']
        df['排名变化'] = df['排名'].shift(1) - df['排名']
        return df
    def get_stock_vermicelli_characteristics(self,stock='SZ300075'):
        '''
        获取股票粉丝特征
        香港市场/美股带有标识符HK|00700
        基金ETF待遇市场标识符SH,SZ SH512480
        :param stock:
        :return:
        '''
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '104',
            'content-type': 'application/json',
            'origin': 'https://vipmoney.eastmoney.com',
            'referer': 'https://vipmoney.eastmoney.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
        }
        url='https://emappdata.eastmoney.com/stockrank/getHisProfileList'
        data = {"appId": "appId01", "globalId": self.globalId, "marketType": self.marketType, "srcSecurityCode": stock}
        res = requests.post(url=url, headers=headers, data=json.dumps(data))
        text = res.json()
        df = pd.DataFrame(text['data'])
        df.columns=['时间','标志','证券代码','新排名变化','新晋粉丝',
                    '老排名变化','铁杆粉丝','市场代码','单元统计'
        ]
        return df
    def get_stock_cov_key_word_rank(self,stock="SZ300075"):
        '''
        获取股票相关性最热的关键字排行
        香港市场/美股带有标识符HK|00700
        基金ETF待遇市场标识符SH,SZ SH512480
        :return:
        '''
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '104',
            'content-type': 'application/json',
            'origin': 'https://vipmoney.eastmoney.com',
            'referer': 'https://vipmoney.eastmoney.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
        }
        data={"appId":"appId01","globalId":self.globalId,"srcSecurityCode":stock}
        url='https://emappdata.eastmoney.com/stockrank/getHotStockRankList'
        res = requests.post(url=url, headers=headers, data=json.dumps(data))
        text = res.json()
        df = pd.DataFrame(text['data'])
        df.columns=['时间','证券代码','概念名称','概念代码','热度统计','标志']
        return df
#if __name__=='__main__':
    '''
    市场人气
    输入默认参数,进行选择配置
    data_type=人气/飙升
    maker市场=A/HK/US/ETF
    globalId如果我的不能获取配置自己的网站
    https://vipmoney.eastmoney.com/collect/stockranking/pages/ranking9_3/list.html
    models=popularity(data_type='人气',market='A',globalId='786e4c21-70dc-435a-93bb-38')
    #查询人气股票码代码
    df1=models.get_all_stock_rank_code()
    print(df1)
    #全部的人气排行
    df2=models.get_all_stock_rank_code()
    print(df2)
    #获取个股的人气历史排行
  
    香港市场/美股带有标识符HK|00700
    基金ETF待遇市场标识符SH,SZ SH512480
    通过models.get_all_stock_rank_code()查询代码

    df3=models.get_stock_hist_rank(stock='SZ300075')
    print(df3)
    #人气排名数据
    df4=models.get_stock_popularity_rank_data()
    print(df4)
    #实时人气排行

    香港市场/美股带有标识符HK|00700
    基金ETF待遇市场标识符SH,SZ SH512480
    通过models.get_all_stock_rank_code()查询代码

    df5=models.get_stock_spot_rank_data(stock='SZ300075')
    print(df5)
    #股票粉丝特征
    df6=models.get_stock_vermicelli_characteristics(stock='SZ300075')
    print(df6)
    #股票最相关的概念热度

    香港市场/美股带有标识符HK|00700
    基金ETF待遇市场标识符SH,SZ SH512480
    通过models.get_all_stock_rank_code()查询代码

    df7=models.get_stock_cov_key_word_rank(stock='SZ300075')
    print(df7)
    #把人气排行100的添加到东方财富自选股
    #自己配置cookie,appkey
    models1=stock_em(Cookie='qgqp_b_id=0f8580ebcfbfccffc09b509b666f135f; ad_tc_221000003614433342=true; HAList=a-sh-600031-%u4E09%u4E00%u91CD%u5DE5%2Cty-1-600031-%u4E09%u4E00%u91CD%u5DE5%2Cty-0-300059-%u4E1C%u65B9%u8D22%u5BCC; em-quote-version=topspeed; mtp=1; ct=WNoSWFRASxKIV2btfIFOEi-98E4Rz1wjWUjPLnDjBZu1Mrv8j9A1J82XYDeBxPMc1cXYpCWe6WqGXO-xma2kLtifhEJA5xGqIVl3so6sN7k7cV11llgC4vOgvR5ToXLNHjOF_fkXSgcGoGVWUXUnux0imF9BULmDLvoY1CfTxlM; ut=FobyicMgeV4NKY1cLeahQ8ytBB1IiqgoaAxQ8l--liBk1S_lSXGHKlR_abCpUEVZ-Z5Qrud4JDLAM8SD89FvzNgFiX0U0FNCHcFPbzbpiP-Qq-JX9qNYu2OhclCrvEoMikggR-SylPjtR9QPNXhk8ZKDuuZ3rc5oEFTcEMgSkEBDuqsea2H5bIJEWSxbcK8hfC8eEwIugnjfOA7h_awakbsLtdsN-COPCkTADtN48bRiSoSe1A-jponBR4jI3vC0gS0A8WmqTpcM8oVK3gfWQ4DtX_fN4UDe; pi=1452376043169950%3bs1452376043169950%3b%e7%bb%8f%e7%ae%a1%e8%8f%9c%e9%b8%9f%3bfqid1d6R7ESSRmKUPKtUERDq5fIHbFeT3Lbw30X2wG1SYtmC72vCnnB4JeVtpDjK44MKca5fohx2yCzOUhalwm2yokwOYUFneTH8tayK2g0jMxkCAnuT4J3a%2f1Qnfyr9eUYwL0O436cCaOq9A9%2bRJzrZwPMgfBl6CZ7OPSL7BVK%2f7HTf1Rk8dE9yBRuUi6DeO2brKD2n%3bLlueSUexj2Xw4qrNmM2LajTh7hu%2binRMplbD2x98U42bj7OmhltqUcaxbsw6L5dsuNygu%2fuxLD%2fkFa8umVukOX9Bt57LLD1Hfwl2O7f7MlaS5T7%2fBnuz3dxAg3NFexELpDuH7cJVaIm%2fqgqhmpliCLdssYSeog%3d%3d; uidal=1452376043169950%e7%bb%8f%e7%ae%a1%e8%8f%9c%e9%b8%9f; sid=152853388; vtpst=|; st_si=55602655935179; st_pvi=89500947722457; st_sp=2022-09-09%2011%3A42%3A17; st_inirUrl=https%3A%2F%2Fwww.so.com%2Flink; st_sn=3; st_psi=20220928152615948-113200302281-3355896367; st_asi=delete',appkey='d41d8cd98f00b204e9800998ecf8427e')
    #替代组合，删除
    models1.del_stock_zh_name(name='东方财富人气')
    #建立
    models1.create_stock_zh(name='东方财富人气')
    #加入
    for stock in df4['代码'].tolist():
        models1.add_stock_to_account(name='东方财富人气',stock=stock)
    models2=popularity(data_type='飙升',market='A')
    df8=models2.get_stock_popularity_rank_data()
    print(df8)
    models1.del_stock_zh_name(name='东方财富飙升')
    #建立
    models1.create_stock_zh(name='东方财富飙升')
    #加入
    for stock in df8['代码'].tolist():
        models1.add_stock_to_account(name='东方财富飙升',stock=stock)
    import akshare as ak
    from datetime import datetime
    now_date=''.join(str(datetime.now())[:10].split('-'))
    df=ak.stock_zt_pool_em(date=now_date)
    stock_list=df['证券代码'].tolist()
    models1.del_stock_zh_name(name='涨停')
    #建立
    models1.create_stock_zh(name='涨停')
    for stock in stock_list:
        models1.add_stock_to_account(name='涨停',stock=stock)
    '''


