import pandas as pd
import easyquotation
import requests
import json
import time
import yagmail
from ..xgtrader.tdx_data import tdx_data
class etf_fund_data_ths:
    def __init__(self):
        '''
        etf基金数据
        '''
        self.tdx_data=tdx_data()
        self.tdx_data.connect()
    def get_ETF_fund_hist_data(self,stock='159805',end='20500101',limit='1000000',
                                data_type='D',fqt='1',count=8000):
            '''
            获取ETF基金历史数据
            stock 证券代码
            end结束时间
            limit数据长度
            data_type数据类型：
            1 1分钟
            5 5分钟
            15 15分钟
            30 30分钟
            60 60分钟
            D 日线数据
            W 周线数据
            M 月线数据
            fqt 复权
            fq=0股票除权
            fq=1前复权
            fq=2后复权
            '''
            try:
                secid='{}.{}'.format(0,stock)
                data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
                klt=data_dict[data_type]
                params={
                    'secid':secid,
                    'klt':klt,
                    'fqt':fqt,
                    'lmt':limit,
                    'end':end,
                    'iscca': '1',
                    'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                    'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                    'forcect': '1',
                }
                url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                res = requests.get(url=url, params=params)
                text = res.text
                json_text = json.loads(text)
                df = pd.DataFrame(json_text['data']['klines'])
                df.columns = ['数据']
                data_list = []
                for i in df['数据']:
                    data_list.append(i.split(','))
                data = pd.DataFrame(data_list)
                columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                        '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
                data.columns = columns
                del data['_']
                for m in columns[1:-3]:
                    data[m] = pd.to_numeric(data[m])
                data1=data.sort_index(ascending=True,ignore_index=True)
                return data1
            except:
                try:
                    secid='{}.{}'.format(1,stock)
                    data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
                    klt=data_dict[data_type]
                    params={
                        'secid':secid,
                        'klt':klt,
                        'fqt':fqt,
                        'lmt':limit,
                        'end':end,
                        'iscca': '1',
                        'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                        'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                        'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                        'forcect': '1',
                    }
                    url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                    res = requests.get(url=url, params=params)
                    text = res.text
                    json_text = json.loads(text)
                    df = pd.DataFrame(json_text['data']['klines'])
                    df.columns = ['数据']
                    data_list = []
                    for i in df['数据']:
                        data_list.append(i.split(','))
                    data = pd.DataFrame(data_list)
                    columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                            '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
                    data.columns = columns
                    del data['_']
                    for m in columns[1:-3]:
                        data[m] = pd.to_numeric(data[m])
                    data1=data.sort_index(ascending=True,ignore_index=True)
                    return data1
                except:
                    '''
                    0 5分钟K线
                    1 15分钟K线 
                    2 30分钟K线 
                    3 1小时K线 
                    4 日K线
                    7 1分钟
                    8 1分钟K线
                    '''
                    data_dict = {'1': '8', '5': '0', '15': '1', '30': '2', '60': '3', 'D': '4', '7': '7',}
                    n=data_dict[data_type]
                    data=self.tdx_data.get_security_minute_data(stock=stock,n=n,count=count)
                    data['date']=data['datetime'].apply(lambda x:str(x)[:10])
                    data['volume']=data['vol']
                    data['涨跌幅']=data['close'].pct_change()*100
                    data['涨跌额']=data['close']-data['open']
                    data['振幅']=(data['high']-data['low'])/data['low']*100
                    return data
    def get_fund_etf_spot_em(self,fund='159755'):
        '''
        获取ETF基金实时行情
        :param fund:
        :return:
        '''
        quotation = easyquotation.use('jsl')
        df=quotation.etfindex()
        data=df[fund]
        return data
    def get_ETF_fund_hist_data_jsl(fund='159647'):
        '''
        历史数据,备用
        '''
        url='https://www.jisilu.cn/data/etf/detail_hists/'
        params={
            '___jsl':'LST___t=1679452650523'
        }
        data={
            'is_search':'0',
            'fund_id':fund,
            'rp':'50',
            'page':'1'
        }
        res=requests.post(url=url,params=params,data=data)
        text=res.json()
        df=pd.DataFrame(text['rows'])
        data=pd.DataFrame()
        for i in df['cell'].tolist():
            df1=pd.DataFrame(i,index=[0])
            data=pd.concat([data,df1],ignore_index=True)
        data['date']=pd.to_datetime(data['hist_dt'])
        data.index=data['date']
        data1=data.sort_index(ascending=True)
        return data1
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
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        if tm_hour==start_date and tm_min<30:
            is_tradre=False
        elif tm_hour==start_date and tm_min>30:
            is_tradre=True
        elif tm_hour>=start_date and tm_hour<=end_date:
            is_tradre=True
        else:
            is_tradre=False
        #利用通用时间，不考虑中午不交易
        wo=loc.tm_wday
        if wo<=trader_time:
            if (is_tradre) and (tm_hour<=end_date):
                return True
            else:
                return False
        else:
            print('周末')
            return False
    def seed_emial_qq(self,text='交易完成'):
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text1=json.loads(com)
        try:
            password=text1['qq掩码']
            yag = yagmail.SMTP(user='1752515969@qq.com', password=password, host='smtp.qq.com')
            m = self.qq
            text = text
            yag.send(to=m, contents=text, subject='邮件')
            print('邮箱发生成功')
        except:
            print('qq发送失败可能用的人多')
    def get_trader_date_list(self):
        '''
        获取交易日历
        :return:
        '''
        df=self.get_stock_hist_data_em()
        date_list=df['date'].tolist()
        return date_list
    def _fund_etf_code_id_map_em(self) -> dict:
        """
        东方财富-ETF代码和市场标识映射
        https://quote.eastmoney.com/center/gridlist.html#fund_etf
        :return: ETF 代码和市场标识映射
        :rtype: dict
        """
        url = "https://88.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "5000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "wbp2u": "|0|0|0|web",
            "fid": "f3",
            "fs": "b:MK0021,b:MK0022,b:MK0023,b:MK0024",
            "fields": "f12,f13",
            "_": "1672806290972",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_dict = dict(zip(temp_df["f12"], temp_df["f13"]))
        return temp_dict
    def fund_etf_spot_em(self) -> pd.DataFrame:
        """
        东方财富-ETF 实时行情
        https://quote.eastmoney.com/center/gridlist.html#fund_etf
        :return: ETF 实时行情
        :rtype: pandas.DataFrame
        """
        url = "https://88.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "5000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "wbp2u": "|0|0|0|web",
            "fid": "f3",
            "fs": "b:MK0021,b:MK0022,b:MK0023,b:MK0024",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
            "_": "1672806290972",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_df.rename(
            columns={
                "f12": "代码",
                "f14": "名称",
                "f2": "最新价",
                "f4": "涨跌额",
                "f3": "涨跌幅",
                "f5": "成交量",
                "f6": "成交额",
                "f17": "开盘价",
                "f15": "最高价",
                "f16": "最低价",
                "f18": "昨收",
                "f8": "换手率",
                "f21": "流通市值",
                "f20": "总市值",
            },
            inplace=True,
        )
        temp_df = temp_df[
            [
                "代码",
                "名称",
                "最新价",
                "涨跌额",
                "涨跌幅",
                "成交量",
                "成交额",
                "开盘价",
                "最高价",
                "最低价",
                "昨收",
                "换手率",
                "流通市值",
                "总市值",
            ]
        ]
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"], errors="coerce")
        temp_df["最高价"] = pd.to_numeric(temp_df["最高价"], errors="coerce")
        temp_df["最低价"] = pd.to_numeric(temp_df["最低价"], errors="coerce")
        temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
        return temp_df
    def fund_etf_hist_em(self,
        symbol: str = "159707",
        period: str = "daily",
        start_date: str = "19700101",
        end_date: str = "20500101",
        adjust: str = "",
    ) -> pd.DataFrame:
        """
        东方财富-ETF行情
        https://quote.eastmoney.com/sz159707.html
        :param symbol: ETF 代码
        :type symbol: str
        :param period: choice of {'daily', 'weekly', 'monthly'}
        :type period: str
        :param start_date: 开始日期
        :type start_date: str
        :param end_date: 结束日期
        :type end_date: str
        :param adjust: choice of {"qfq": "前复权", "hfq": "后复权", "": "不复权"}
        :type adjust: str
        :return: 每日行情
        :rtype: pandas.DataFrame
        """
        code_id_dict = self._fund_etf_code_id_map_em()
        adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
        period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "klt": period_dict[period],
            "fqt": adjust_dict[adjust],
            "beg": start_date,
            "end": end_date,
            "_": "1623766962675",
        }
        try:
            market_id = code_id_dict[symbol]
            params.update({"secid": f"{market_id}.{symbol}"})
            r = requests.get(url, params=params)
            data_json = r.json()
        except KeyError:
            market_id = 1
            params.update({"secid": f"{market_id}.{symbol}"})
            r = requests.get(url, params=params)
            data_json = r.json()
            if not data_json["data"]:
                market_id = 0
                params.update({"secid": f"{market_id}.{symbol}"})
                r = requests.get(url, params=params)
                data_json = r.json()
        if not (data_json["data"] and data_json["data"]["klines"]):
            return pd.DataFrame()
        temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
        temp_df.columns = [
            "日期",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        temp_df.index = pd.to_datetime(temp_df["日期"])
        temp_df.reset_index(inplace=True, drop=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        return temp_df

    def fund_etf_hist_min_em(self,
        symbol: str = "159707",
        start_date: str = "1979-09-01 09:32:00",
        end_date: str = "2222-01-01 09:32:00",
        period: str = "5",
        adjust: str = "",
    ) -> pd.DataFrame:
        """
        东方财富-ETF 行情
        https://quote.eastmoney.com/sz159707.html
        :param symbol: ETF 代码
        :type symbol: str
        :param start_date: 开始日期
        :type start_date: str
        :param end_date: 结束日期
        :type end_date: str
        :param period: choice of {"1", "5", "15", "30", "60"}
        :type period: str
        :param adjust: choice of {'', 'qfq', 'hfq'}
        :type adjust: str
        :return: 每日分时行情
        :rtype: pandas.DataFrame
        """
        code_id_dict = self._fund_etf_code_id_map_em()
        adjust_map = {
            "": "0",
            "qfq": "1",
            "hfq": "2",
        }
        if period == "1":
            url = "https://push2his.eastmoney.com/api/qt/stock/trends2/get"
            params = {
                "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "ndays": "5",
                "iscr": "0",
                "secid": f"{code_id_dict[symbol]}.{symbol}",
                "_": "1623766962675",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(
                [item.split(",") for item in data_json["data"]["trends"]]
            )
            temp_df.columns = [
                "时间",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "成交量",
                "成交额",
                "最新价",
            ]
            temp_df.index = pd.to_datetime(temp_df["时间"])
            temp_df = temp_df[start_date:end_date]
            temp_df.reset_index(drop=True, inplace=True)
            temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
            temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
            temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
            temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
            temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
            temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
            temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
            temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
            return temp_df
        else:
            url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
            params = {
                "fields1": "f1,f2,f3,f4,f5,f6",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "klt": period,
                "fqt": adjust_map[adjust],
                "secid": f"{code_id_dict[symbol]}.{symbol}",
                "beg": "0",
                "end": "20500000",
                "_": "1630930917857",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(
                [item.split(",") for item in data_json["data"]["klines"]]
            )
            temp_df.columns = [
                "时间",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "成交量",
                "成交额",
                "振幅",
                "涨跌幅",
                "涨跌额",
                "换手率",
            ]
            temp_df.index = pd.to_datetime(temp_df["时间"])
            temp_df = temp_df[start_date:end_date]
            temp_df.reset_index(drop=True, inplace=True)
            temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
            temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
            temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
            temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
            temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
            temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
            temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
            temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
            temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
            temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
            temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
            temp_df = temp_df[
                [
                    "时间",
                    "开盘",
                    "收盘",
                    "最高",
                    "最低",
                    "涨跌幅",
                    "涨跌额",
                    "成交量",
                    "成交额",
                    "振幅",
                    "换手率",
                ]
            ]
            return temp_df
    def fund_purchase_em(self) -> pd.DataFrame:
        """
        东方财富网站-天天基金网-基金数据-基金申购状态
        https://fund.eastmoney.com/Fund_sgzt_bzdm.html#fcode,asc_1
        :return: 基金申购状态
        :rtype: pandas.DataFrame
        """
        url = "http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        params = {
            "t": "8",
            "page": "1,50000",
            "js": "reData",
            "sort": "fcode,asc",
            "_": "1641528557742",
        }
        r = requests.get(url, params=params, headers=headers)
        data_text = r.text
        data_json = demjson.decode(data_text.strip("var reData="))
        temp_df = pd.DataFrame(data_json["datas"])
        temp_df.reset_index(inplace=True)
        temp_df["index"] = temp_df.index + 1
        temp_df.columns = [
            "序号",
            "基金代码",
            "基金简称",
            "基金类型",
            "最新净值/万份收益",
            "最新净值/万份收益-报告时间",
            "申购状态",
            "赎回状态",
            "下一开放日",
            "购买起点",
            "日累计限定金额",
            "-",
            "-",
            "手续费",
        ]
        temp_df = temp_df[
            [
                "序号",
                "基金代码",
                "基金简称",
                "基金类型",
                "最新净值/万份收益",
                "最新净值/万份收益-报告时间",
                "申购状态",
                "赎回状态",
                "下一开放日",
                "购买起点",
                "日累计限定金额",
                "手续费",
            ]
        ]
        temp_df["下一开放日"] = pd.to_datetime(temp_df["下一开放日"]).dt.date
        temp_df["最新净值/万份收益"] = pd.to_numeric(temp_df["最新净值/万份收益"])
        temp_df["购买起点"] = pd.to_numeric(temp_df["购买起点"])
        temp_df["日累计限定金额"] = pd.to_numeric(temp_df["日累计限定金额"])
        temp_df["手续费"] = temp_df["手续费"].str.strip("%")
        temp_df["手续费"] = pd.to_numeric(temp_df["手续费"])
        return temp_df


    def fund_name_em(self) -> pd.DataFrame:
        """
        东方财富网站-天天基金网-基金数据-所有基金的名称和类型
        https://fund.eastmoney.com/manager/default.html#dt14;mcreturnjson;ftall;pn20;pi1;scabbname;stasc
        :return: 所有基金的名称和类型
        :rtype: pandas.DataFrame
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        url = "http://fund.eastmoney.com/js/fundcode_search.js"
        res = requests.get(url, headers=headers)
        text_data = res.text
        data_json = demjson.decode(text_data.strip("var r = ")[:-1])
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["基金代码", "拼音缩写", "基金简称", "基金类型", "拼音全称"]
        return temp_df


    def fund_info_index_em(self,
        symbol: str = "沪深指数", indicator: str = "被动指数型"
    ) -> pd.DataFrame:
        """
        东方财富网站-天天基金网-基金数据-基金信息-指数型
        https://fund.eastmoney.com/trade/zs.html
        :param symbol: choice of {"全部", "沪深指数", "行业主题", "大盘指数", "中盘指数", "小盘指数", "股票指数", "债券指数"}
        :type symbol: str
        :param indicator: choice of {"全部", "被动指数型", "增强指数型"}
        :type indicator: str
        :return: pandas.DataFrame
        :rtype: 基金信息-指数型
        """
        symbol_map = {
            "全部": "",
            "沪深指数": "053",
            "行业主题": "054",
            "大盘指数": "01",
            "中盘指数": "02",
            "小盘指数": "03",
            "股票指数": "050|001",
            "债券指数": "050|003",
        }
        indicator_map = {
            "全部": "",
            "被动指数型": "051",
            "增强指数型": "052",
        }
        url = "http://api.fund.eastmoney.com/FundTradeRank/GetRankList"
        if symbol in {"股票指数", "债券指数"}:
            params = {
                "ft": "zs",
                "sc": "1n",
                "st": "desc",
                "pi": "1",
                "pn": "10000",
                "cp": "",
                "ct": "",
                "cd": "",
                "ms": "",
                "fr": symbol_map[symbol].split("|")[0],
                "plevel": "",
                "fst": "",
                "ftype": symbol_map[symbol].split("|")[1],
                "fr1": indicator_map[indicator],
                "fl": "0",
                "isab": "1",
                "_": "1658888335885",
            }
        else:
            params = {
                "ft": "zs",
                "sc": "1n",
                "st": "desc",
                "pi": "1",
                "pn": "10000",
                "cp": "",
                "ct": "",
                "cd": "",
                "ms": "",
                "fr": symbol_map[symbol].split("|")[0],
                "plevel": "",
                "fst": "",
                "ftype": "",
                "fr1": indicator_map[indicator],
                "fl": "0",
                "isab": "1",
                "_": "1658888335885",
            }
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "api.fund.eastmoney.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://fund.eastmoney.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        data_json = json.loads(data_json["Data"])
        temp_df = pd.DataFrame([item.split("|") for item in data_json["datas"]])
        temp_df.columns = [
            "基金代码",
            "基金名称",
            "-",
            "日期",
            "单位净值",
            "日增长率",
            "近1周",
            "近1月",
            "近3月",
            "近6月",
            "近1年",
            "近2年",
            "近3年",
            "今年来",
            "成立来",
            "-",
            "-",
            "-",
            "手续费",
            "-",
            "-",
            "-",
            "-",
            "-",
            "起购金额",
            "-",
            "-",
            "-",
            "-",
        ]
        temp_df = temp_df[
            [
                "基金代码",
                "基金名称",
                "单位净值",
                "日期",
                "日增长率",
                "近1周",
                "近1月",
                "近3月",
                "近6月",
                "近1年",
                "近2年",
                "近3年",
                "今年来",
                "成立来",
                "手续费",
                "起购金额",
            ]
        ]
        temp_df["跟踪标的"] = symbol
        temp_df["跟踪方式"] = indicator

        temp_df["单位净值"] = pd.to_numeric(temp_df["单位净值"])
        temp_df["日增长率"] = pd.to_numeric(temp_df["日增长率"])
        temp_df["近1周"] = pd.to_numeric(temp_df["近1周"])
        temp_df["近1月"] = pd.to_numeric(temp_df["近1月"])
        temp_df["近3月"] = pd.to_numeric(temp_df["近3月"])
        temp_df["近6月"] = pd.to_numeric(temp_df["近6月"])
        temp_df["近1年"] = pd.to_numeric(temp_df["近1年"])
        temp_df["近2年"] = pd.to_numeric(temp_df["近2年"])
        temp_df["近3年"] = pd.to_numeric(temp_df["近3年"])
        temp_df["今年来"] = pd.to_numeric(temp_df["今年来"])
        temp_df["成立来"] = pd.to_numeric(temp_df["成立来"])
        temp_df["手续费"] = pd.to_numeric(temp_df["手续费"])

        return temp_df


    def fund_open_fund_daily_em(self) -> pd.DataFrame:
        """
        东方财富网-天天基金网-基金数据-开放式基金净值
        https://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1
        :return: 当前交易日的所有开放式基金净值数据
        :rtype: pandas.DataFrame
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        url = "http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx"
        params = {
            "t": "1",
            "lx": "1",
            "letter": "",
            "gsid": "",
            "text": "",
            "sort": "zdf,desc",
            "page": "1,20000",
            "dt": "1580914040623",
            "atfc": "",
            "onlySale": "0",
        }
        res = requests.get(url, params=params, headers=headers)
        text_data = res.text
        data_json = demjson.decode(text_data.strip("var db="))
        temp_df = pd.DataFrame(data_json["datas"])
        show_day = data_json["showday"]
        temp_df.columns = [
            "基金代码",
            "基金简称",
            "-",
            f"{show_day[0]}-单位净值",
            f"{show_day[0]}-累计净值",
            f"{show_day[1]}-单位净值",
            f"{show_day[1]}-累计净值",
            "日增长值",
            "日增长率",
            "申购状态",
            "赎回状态",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "手续费",
            "-",
            "-",
            "-",
        ]
        data_df = temp_df[
            [
                "基金代码",
                "基金简称",
                f"{show_day[0]}-单位净值",
                f"{show_day[0]}-累计净值",
                f"{show_day[1]}-单位净值",
                f"{show_day[1]}-累计净值",
                "日增长值",
                "日增长率",
                "申购状态",
                "赎回状态",
                "手续费",
            ]
        ]
        return data_df


    def fund_open_fund_info_em(self,
        fund: str = "000002", indicator: str = "单位净值走势"
    ) -> pd.DataFrame:
        """
        东方财富网-天天基金网-基金数据-开放式基金净值
        https://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1
        :param fund: 基金代码; 可以通过调用 fund_open_fund_daily_em 获取所有开放式基金代码
        :type fund: str
        :param indicator: 需要获取的指标
        :type indicator: str
        :return: 指定基金指定指标的数据
        :rtype: pandas.DataFrame
        """
        # url = f"http://fundgz.1234567.com.cn/js/{fund}.js"  # 描述信息
        url = f"http://fund.eastmoney.com/pingzhongdata/{fund}.js"  # 各类数据都在里面
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        data_text = r.text

        # 单位净值走势
        if indicator == "单位净值走势":
            try:
                data_json = demjson.decode(
                    data_text[
                        data_text.find("Data_netWorthTrend")
                        + 21 : data_text.find("Data_ACWorthTrend")
                        - 15
                    ]
                )
            except:
                return pd.DataFrame()
            temp_df = pd.DataFrame(data_json)
            temp_df["x"] = pd.to_datetime(
                temp_df["x"], unit="ms", utc=True
            ).dt.tz_convert("Asia/Shanghai")
            temp_df["x"] = temp_df["x"].dt.date
            temp_df.columns = [
                "净值日期",
                "单位净值",
                "日增长率",
                "_",
            ]
            temp_df = temp_df[
                [
                    "净值日期",
                    "单位净值",
                    "日增长率",
                ]
            ]
            temp_df["净值日期"] = pd.to_datetime(temp_df["净值日期"]).dt.date
            temp_df["单位净值"] = pd.to_numeric(temp_df["单位净值"])
            temp_df["日增长率"] = pd.to_numeric(temp_df["日增长率"])
            return temp_df

        # 累计净值走势
        if indicator == "累计净值走势":
            try:
                data_json = demjson.decode(
                    data_text[
                        data_text.find("Data_ACWorthTrend")
                        + 20 : data_text.find("Data_grandTotal")
                        - 16
                    ]
                )
            except:
                return pd.DataFrame()
            temp_df = pd.DataFrame(data_json)
            if temp_df.empty:
                return pd.DataFrame()
            temp_df.columns = ["x", "y"]
            temp_df["x"] = pd.to_datetime(
                temp_df["x"], unit="ms", utc=True
            ).dt.tz_convert("Asia/Shanghai")
            temp_df["x"] = temp_df["x"].dt.date
            temp_df.columns = [
                "净值日期",
                "累计净值",
            ]
            temp_df = temp_df[
                [
                    "净值日期",
                    "累计净值",
                ]
            ]
            temp_df["净值日期"] = pd.to_datetime(temp_df["净值日期"]).dt.date
            temp_df["累计净值"] = pd.to_numeric(temp_df["累计净值"])
            return temp_df

        # 累计收益率走势
        if indicator == "累计收益率走势":
            data_json = demjson.decode(
                data_text[
                    data_text.find("Data_grandTotal")
                    + 18 : data_text.find("Data_rateInSimilarType")
                    - 15
                ]
            )
            temp_df_main = pd.DataFrame(data_json[0]["data"])  # 本产品
            # temp_df_mean = pd.DataFrame(data_json[1]["data"])  # 同类平均
            # temp_df_hs = pd.DataFrame(data_json[2]["data"])  # 沪深300
            temp_df_main.columns = ["x", "y"]
            temp_df_main["x"] = pd.to_datetime(
                temp_df_main["x"], unit="ms", utc=True
            ).dt.tz_convert("Asia/Shanghai")
            temp_df_main["x"] = temp_df_main["x"].dt.date
            temp_df_main.columns = [
                "净值日期",
                "累计收益率",
            ]
            temp_df_main = temp_df_main[
                [
                    "净值日期",
                    "累计收益率",
                ]
            ]
            temp_df_main["净值日期"] = pd.to_datetime(temp_df_main["净值日期"]).dt.date
            temp_df_main["累计收益率"] = pd.to_numeric(temp_df_main["累计收益率"])
            return temp_df_main

        # 同类排名走势
        if indicator == "同类排名走势":
            data_json = demjson.decode(
                data_text[
                    data_text.find("Data_rateInSimilarType")
                    + 25 : data_text.find("Data_rateInSimilarPersent")
                    - 16
                ]
            )
            temp_df = pd.DataFrame(data_json)
            temp_df["x"] = pd.to_datetime(
                temp_df["x"], unit="ms", utc=True
            ).dt.tz_convert("Asia/Shanghai")
            temp_df["x"] = temp_df["x"].dt.date
            temp_df.columns = [
                "报告日期",
                "同类型排名-每日近三月排名",
                "总排名-每日近三月排名",
            ]
            temp_df = temp_df[
                [
                    "报告日期",
                    "同类型排名-每日近三月排名",
                    "总排名-每日近三月排名",
                ]
            ]
            temp_df["报告日期"] = pd.to_datetime(temp_df["报告日期"]).dt.date
            temp_df["同类型排名-每日近三月排名"] = pd.to_numeric(temp_df["同类型排名-每日近三月排名"])
            temp_df["总排名-每日近三月排名"] = pd.to_numeric(temp_df["总排名-每日近三月排名"])
            return temp_df

        # 同类排名百分比
        if indicator == "同类排名百分比":
            data_json = demjson.decode(
                data_text[
                    data_text.find("Data_rateInSimilarPersent")
                    + 26 : data_text.find("Data_fluctuationScale")
                    - 23
                ]
            )
            temp_df = pd.DataFrame(data_json)
            temp_df.columns = ["x", "y"]
            temp_df["x"] = pd.to_datetime(
                temp_df["x"], unit="ms", utc=True
            ).dt.tz_convert("Asia/Shanghai")
            temp_df["x"] = temp_df["x"].dt.date
            temp_df.columns = [
                "报告日期",
                "同类型排名-每日近3月收益排名百分比",
            ]
            temp_df = temp_df[
                [
                    "报告日期",
                    "同类型排名-每日近3月收益排名百分比",
                ]
            ]
            temp_df["报告日期"] = pd.to_datetime(temp_df["报告日期"]).dt.date
            temp_df["同类型排名-每日近3月收益排名百分比"] = pd.to_numeric(
                temp_df["同类型排名-每日近3月收益排名百分比"]
            )
            return temp_df

        # 分红送配详情
        if indicator == "分红送配详情":
            url = f"http://fundf10.eastmoney.com/fhsp_{fund}.html"
            r = requests.get(url, headers=headers)
            temp_df = pd.read_html(r.text)[1]
            if temp_df.iloc[0, 1] == "暂无分红信息!":
                return None
            else:
                return temp_df

        # 拆分详情
        if indicator == "拆分详情":
            url = f"http://fundf10.eastmoney.com/fhsp_{fund}.html"
            r = requests.get(url, headers=headers)
            temp_df = pd.read_html(r.text)[2]
            if temp_df.iloc[0, 1] == "暂无拆分信息!":
                return None
            else:
                return temp_df


    def fund_money_fund_daily_em(self) -> pd.DataFrame:
        """
        东方财富网-天天基金网-基金数据-货币型基金收益
        http://fund.eastmoney.com/HBJJ_pjsyl.html
        :return: 当前交易日的所有货币型基金收益数据
        :rtype: pandas.DataFrame
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        url = "http://fund.eastmoney.com/HBJJ_pjsyl.html"
        r = requests.get(url, headers=headers)
        r.encoding = "gb2312"
        show_day = pd.read_html(r.text)[1].iloc[0, 5:11].tolist()
        temp_df = pd.read_html(r.text)[1].iloc[1:, 2:]
        temp_df_columns = temp_df.iloc[0, :].tolist()[1:]
        temp_df = temp_df.iloc[1:, 1:]
        temp_df.columns = temp_df_columns
        temp_df["基金简称"] = temp_df["基金简称"].str.strip("基金吧档案")
        temp_df.columns = [
            "基金代码",
            "基金简称",
            f"{show_day[0]}-万份收益",
            f"{show_day[1]}-7日年化%",
            f"{show_day[2]}-单位净值",
            f"{show_day[3]}-万份收益",
            f"{show_day[4]}-7日年化%",
            f"{show_day[5]}-单位净值",
            "日涨幅",
            "成立日期",
            "基金经理",
            "手续费",
            "可购全部",
        ]
        return temp_df


    def fund_money_fund_info_em(self,fund: str = "000009") -> pd.DataFrame:
        """
        东方财富网-天天基金网-基金数据-货币型基金收益-历史净值数据
        http://fundf10.eastmoney.com/jjjz_004186.html
        :param fund: 货币型基金代码, 可以通过 fund_money_fund_daily_em 来获取
        :type fund: str
        :return: 东方财富网站-天天基金网-基金数据-货币型基金收益-历史净值数据
        :rtype: pandas.DataFrame
        """
        url = "http://api.fund.eastmoney.com/f10/lsjz"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Referer": f"http://fundf10.eastmoney.com/jjjz_{fund}.html",
        }
        params = {
            "callback": "jQuery18306461675574671744_1588245122574",
            "fundCode": fund,
            "pageIndex": "1",
            "pageSize": "10000",
            "startDate": "",
            "endDate": "",
            "_": round(time.time() * 1000),
        }
        r = requests.get(url, params=params, headers=headers)
        text_data = r.text
        data_json = demjson.decode(text_data[text_data.find("{") : -1])
        temp_df = pd.DataFrame(data_json["Data"]["LSJZList"])
        temp_df.columns = [
            "净值日期",
            "每万份收益",
            "7日年化收益率",
            "_",
            "_",
            "_",
            "_",
            "申购状态",
            "赎回状态",
            "_",
            "_",
            "_",
            "_",
        ]
        temp_df = temp_df[["净值日期", "每万份收益", "7日年化收益率", "申购状态", "赎回状态"]]
        return temp_df


    def fund_financial_fund_daily_em(self,) -> pd.DataFrame:
        """
        东方财富网站-天天基金网-基金数据-理财型基金收益
        # 该接口暂无数据
        http://fund.eastmoney.com/lcjj.html#1_1__0__ljjz,desc_1_os1
        :return: 当前交易日的所有理财型基金收益
        :rtype: pandas.DataFrame
        """
        url = "http://api.fund.eastmoney.com/FundNetValue/GetLCJJJZ"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Referer": "http://fund.eastmoney.com/lcjj.html",
        }
        params = {
            "letter": "",
            "jjgsid": "0",
            "searchtext": "",
            "sort": "ljjz,desc",
            "page": "1,100",
            "AttentionCodes": "",
            "cycle": "",
            "OnlySale": "1",
            "_": "1588248310234",
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["Data"]["List"])
        if temp_df.empty:
            return
        show_day = data_json["Data"]["showday"]
        data_df = temp_df[
            [
                "Id",
                "actualsyi",
                "cycle",
                "fcode",
                "kfr",
                "mui",
                "shortname",
                "syi",
                "zrmui",
                "zrsyi",
            ]
        ]
        data_df.columns = [
            "序号",
            "上一期年化收益率",
            "封闭期",
            "基金代码",
            "申购状态",
            f"{show_day[0]}-万份收益",
            "基金简称",
            f"{show_day[0]}-7日年华",
            f"{show_day[1]}-万份收益",
            f"{show_day[1]}-7日年华",
        ]
        data_df = data_df[
            [
                "序号",
                "基金代码",
                "基金简称",
                "上一期年化收益率",
                f"{show_day[0]}-万份收益",
                f"{show_day[0]}-7日年华",
                f"{show_day[1]}-万份收益",
                f"{show_day[1]}-7日年华",
                "封闭期",
                "申购状态",
            ]
        ]
        return data_df


    def fund_financial_fund_info_em(self,symbol: str = "000134") -> pd.DataFrame:
        """
        东方财富网站-天天基金网-基金数据-理财型基金收益-历史净值明细
        https://fundf10.eastmoney.com/jjjz_000791.html
        :param symbol: 理财型基金代码, 可以通过 ak.fund_financial_fund_daily_em() 来获取
        :type symbol: str
        :return: 东方财富网站-天天基金网-基金数据-理财型基金收益-历史净值明细
        :rtype: pandas.DataFrame
        """
        url = "http://api.fund.eastmoney.com/f10/lsjz"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Referer": f"http://fundf10.eastmoney.com/jjjz_{symbol}.html",
        }
        params = {
            "callback": "jQuery18307915911837995662_1588249228826",
            "fundCode": symbol,
            "pageIndex": "1",
            "pageSize": "10000",
            "startDate": "",
            "endDate": "",
            "_": round(time.time() * 1000),
        }
        r = requests.get(url, params=params, headers=headers)
        text_data = r.text
        data_json = demjson.decode(text_data[text_data.find("{") : -1])
        temp_df = pd.DataFrame(data_json["Data"]["LSJZList"])
        temp_df.columns = [
            "净值日期",
            "单位净值",
            "累计净值",
            "_",
            "_",
            "_",
            "日增长率",
            "申购状态",
            "赎回状态",
            "_",
            "_",
            "_",
            "分红送配",
        ]
        temp_df = temp_df[["净值日期", "单位净值", "累计净值", "日增长率", "申购状态", "赎回状态", "分红送配"]]
        temp_df.sort_values(['净值日期'], inplace=True, ignore_index=True)
        temp_df['净值日期'] = pd.to_datetime(temp_df['净值日期']).dt.date
        temp_df['单位净值'] = pd.to_numeric(temp_df['单位净值'], errors="coerce")
        temp_df['累计净值'] = pd.to_numeric(temp_df['累计净值'], errors="coerce")
        temp_df['日增长率'] = pd.to_numeric(temp_df['日增长率'], errors="coerce")
        return temp_df


    def fund_graded_fund_daily_em(self,) -> pd.DataFrame:
        """
        东方财富网站-天天基金网-基金数据-分级基金净值
        http://fund.eastmoney.com/fjjj.html#1_1__0__zdf,desc_1
        :return: 当前交易日的所有分级基金净值
        :rtype: pandas.DataFrame
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Referer": "http://fund.eastmoney.com/fjjj.html",
        }
        url = "http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx"
        params = {
            "t": "1",
            "lx": "9",
            "letter": "",
            "gsid": "0",
            "text": "",
            "sort": "zdf,desc",
            "page": "1,10000",
            "dt": "1580914040623",
            "atfc": "",
        }
        res = requests.get(url, params=params, headers=headers)
        text_data = res.text
        data_json = demjson.decode(text_data.strip("var db="))
        temp_df = pd.DataFrame(data_json["datas"])
        show_day = data_json["showday"]
        temp_df.columns = [
            "基金代码",
            "基金简称",
            "-",
            f"{show_day[0]}-单位净值",
            f"{show_day[0]}-累计净值",
            f"{show_day[1]}--单位净值",
            f"{show_day[1]}--累计净值",
            "日增长值",
            "日增长率",
            "市价",
            "折价率",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "手续费",
        ]
        data_df = temp_df[
            [
                "基金代码",
                "基金简称",
                f"{show_day[0]}-单位净值",
                f"{show_day[0]}-累计净值",
                f"{show_day[1]}--单位净值",
                f"{show_day[1]}--累计净值",
                "日增长值",
                "日增长率",
                "市价",
                "折价率",
                "手续费",
            ]
        ]
        return data_df


    def fund_graded_fund_info_em(self,fund: str = "150232") -> pd.DataFrame:
        """
        东方财富网站-天天基金网-基金数据-分级基金净值-历史净值明细
        http://fundf10.eastmoney.com/jjjz_150232.html
        :param fund: 分级基金代码, 可以通过 fund_money_fund_daily_em 来获取
        :type fund: str
        :return: 东方财富网站-天天基金网-基金数据-分级基金净值-历史净值明细
        :rtype: pandas.DataFrame
        """
        url = "http://api.fund.eastmoney.com/f10/lsjz"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Referer": f"http://fundf10.eastmoney.com/jjjz_{fund}.html",
        }
        params = {
            "callback": "jQuery18309549480723031107_1588250168187",
            "fundCode": fund,
            "pageIndex": "1",
            "pageSize": "10000",
            "startDate": "",
            "endDate": "",
            "_": round(time.time() * 1000),
        }
        r = requests.get(url, params=params, headers=headers)
        text_data = r.text
        data_json = demjson.decode(text_data[text_data.find("{") : -1])
        temp_df = pd.DataFrame(data_json["Data"]["LSJZList"])
        temp_df.columns = [
            "净值日期",
            "单位净值",
            "累计净值",
            "_",
            "_",
            "_",
            "日增长率",
            "申购状态",
            "赎回状态",
            "_",
            "_",
            "_",
            "_",
        ]
        temp_df = temp_df[["净值日期", "单位净值", "累计净值", "日增长率", "申购状态", "赎回状态"]]
        return temp_df


    def fund_etf_fund_daily_em(self,) -> pd.DataFrame:
        """
        东方财富网-天天基金网-基金数据-场内交易基金
        http://fund.eastmoney.com/cnjy_dwjz.html
        :return: 当前交易日的所有场内交易基金数据
        :rtype: pandas.DataFrame
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        url = "http://fund.eastmoney.com/cnjy_dwjz.html"
        r = requests.get(url, headers=headers)
        r.encoding = "gb2312"
        show_day = pd.read_html(r.text)[1].iloc[0, 6:10].tolist()
        temp_df = pd.read_html(r.text)[1].iloc[1:, 2:]
        temp_df_columns = temp_df.iloc[0, :].tolist()[1:]
        temp_df = temp_df.iloc[1:, 1:]
        temp_df.columns = temp_df_columns
        temp_df["基金简称"] = temp_df["基金简称"].str.strip("基金吧档案")
        temp_df.reset_index(inplace=True, drop=True)
        temp_df.columns = [
            "基金代码",
            "基金简称",
            "类型",
            f"{show_day[0]}-单位净值",
            f"{show_day[0]}-累计净值",
            f"{show_day[2]}-单位净值",
            f"{show_day[2]}-累计净值",
            "增长值",
            "增长率",
            "市价",
            "折价率",
        ]
        return temp_df


    def fund_etf_fund_info_em(self,
        fund: str = "511280",
        start_date: str = "20000101",
        end_date: str = "20500101",
    ) -> pd.DataFrame:
        """
        东方财富网站-天天基金网-基金数据-场内交易基金-历史净值明细
        http://fundf10.eastmoney.com/jjjz_511280.html
        :param fund: 场内交易基金代码, 可以通过 fund_etf_fund_daily_em 来获取
        :type fund: str
        :param start_date: 开始统计时间
        :type start_date: str
        :param end_date: 结束统计时间
        :type end_date: str
        :return: 东方财富网站-天天基金网-基金数据-场内交易基金-历史净值明细
        :rtype: pandas.DataFrame
        """
        url = "http://api.fund.eastmoney.com/f10/lsjz"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Referer": f"http://fundf10.eastmoney.com/jjjz_{fund}.html",
        }
        params = {
            "fundCode": fund,
            "pageIndex": "1",
            "pageSize": "10000",
            "startDate": "-".join(
                [start_date[:4], start_date[4:6], start_date[6:]]
            ),
            "endDate": "-".join([end_date[:4], end_date[4:6], end_date[6:]]),
            "_": round(time.time() * 1000),
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["Data"]["LSJZList"])
        temp_df.columns = [
            "净值日期",
            "单位净值",
            "累计净值",
            "_",
            "_",
            "_",
            "日增长率",
            "申购状态",
            "赎回状态",
            "_",
            "_",
            "_",
            "_",
        ]
        temp_df = temp_df[["净值日期", "单位净值", "累计净值", "日增长率", "申购状态", "赎回状态"]]
        temp_df["净值日期"] = pd.to_datetime(temp_df["净值日期"]).dt.date
        temp_df["单位净值"] = pd.to_numeric(temp_df["单位净值"])
        temp_df["累计净值"] = pd.to_numeric(temp_df["累计净值"])
        temp_df["日增长率"] = pd.to_numeric(temp_df["日增长率"])
        temp_df.sort_values(['净值日期'], inplace=True, ignore_index=True)
        return temp_df


    def fund_value_estimation_em(self,symbol: str = "全部") -> pd.DataFrame:
        """
        东方财富网-数据中心-净值估算
        http://fund.eastmoney.com/fundguzhi.html
        :param symbol: choice of {'全部', '股票型', '混合型', '债券型', '指数型', 'QDII', 'ETF联接', 'LOF', '场内交易基金'}
        :type symbol: str
        :return: 近期净值估算数据
        :rtype: pandas.DataFrame
        """
        symbol_map = {
            "全部": 1,
            "股票型": 2,
            "混合型": 3,
            "债券型": 4,
            "指数型": 5,
            "QDII": 6,
            "ETF联接": 7,
            "LOF": 8,
            "场内交易基金": 9,
        }
        url = "http://api.fund.eastmoney.com/FundGuZhi/GetFundGZList"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Referer": "http://fund.eastmoney.com/",
        }
        params = {
            "type": symbol_map[symbol],
            "sort": "3",
            "orderType": "desc",
            "canbuy": "0",
            "pageIndex": "1",
            "pageSize": "20000",
            "_": int(time.time() * 1000),
        }
        r = requests.get(url, params=params, headers=headers)
        json_data = r.json()
        temp_df = pd.DataFrame(json_data["Data"]["list"])
        value_day = json_data["Data"]["gzrq"]
        cal_day = json_data["Data"]["gxrq"]
        temp_df.columns = [
            "基金代码",
            "-",
            "-",
            "-",
            "-",
            "-",
            "基金类型",
            "-",
            "-",
            "-",
            "-",
            "估算日期",
            "-",
            "-",
            "-",
            "-",
            "_",
            "-",
            "-",
            "估算偏差",
            f"{cal_day}-估算数据-估算值",
            f"{cal_day}-估算数据-估算增长率",
            f"{cal_day}-公布数据-日增长率",
            f"{value_day}-单位净值",
            f"{cal_day}-公布数据-单位净值",
            "-",
            "基金名称",
            "-",
            "-",
            "-",
        ]
        temp_df = temp_df[
            [
                "基金代码",
                "基金名称",
                f"{cal_day}-估算数据-估算值",
                f"{cal_day}-估算数据-估算增长率",
                f"{cal_day}-公布数据-单位净值",
                f"{cal_day}-公布数据-日增长率",
                "估算偏差",
                f"{value_day}-单位净值",
            ]
        ]
        temp_df.reset_index(inplace=True)
        temp_df["index"] = range(1, len(temp_df) + 1)
        temp_df.rename(columns={"index": "序号"}, inplace=True)
        return temp_df


    def fund_hk_fund_hist_em(self,
        code: str = "1002200683", symbol: str = "历史净值明细"
    ) -> pd.DataFrame:
        """
        东方财富网-天天基金网-基金数据-香港基金-历史净值明细(分红送配详情)
        https://overseas.1234567.com.cn/f10/FundJz/968092#FHPS
        :param code: 通过 ak.fund_em_hk_rank() 获取
        :type code: str
        :param symbol: choice of {"历史净值明细", "分红送配详情"}
        :type symbol: str
        :return: 香港基金-历史净值明细(分红送配详情)
        :rtype: pandas.DataFrame
        """
        url = "http://overseas.1234567.com.cn/overseasapi/OpenApiHander.ashx"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        if symbol == "历史净值明细":
            params = {
                "api": "HKFDApi",
                "m": "MethodJZ",
                "hkfcode": f"{code}",
                "action": "2",
                "pageindex": "0",
                "pagesize": "1000",
                "date1": "",
                "date2": "",
                "_": "1611131371333",
            }
            r = requests.get(url, params=params, headers=headers)
            data_json = r.json()
            temp_one_df = pd.DataFrame(data_json["Data"])
            temp_one_df.columns = [
                "_",
                "_",
                "_",
                "净值日期",
                "单位净值",
                "_",
                "日增长值",
                "日增长率",
                "_",
                "单位",
                "_",
            ]
            temp_one_df = temp_one_df[
                [
                    "净值日期",
                    "单位净值",
                    "日增长值",
                    "日增长率",
                    "单位",
                ]
            ]
        else:
            params = {
                "api": "HKFDApi",
                "m": "MethodJZ",
                "hkfcode": f"{code}",
                "action": "3",
                "pageindex": "0",
                "pagesize": "1000",
                "date1": "",
                "date2": "",
                "_": "1611131371333",
            }
            r = requests.get(url, params=params, headers=headers)
            data_json = r.json()
            temp_one_df = pd.DataFrame(data_json["Data"])
            temp_one_df.columns = [
                "_",
                "_",
                "_",
                "_",
                "_",
                "年份",
                "分红金额",
                "除息日",
                "权益登记日",
                "分红发放日",
                "_",
                "单位",
                "_",
                "_",
            ]
            temp_one_df = temp_one_df[
                [
                    "年份",
                    "权益登记日",
                    "除息日",
                    "分红发放日",
                    "分红金额",
                    "单位",
                ]
            ]
        return temp_one_df
    def get_etf_fund_spot_data(self,stock='159632'):
        '''
        ETF实时数据
        '''
        marker,stock=self.tdx_data.rename_stock_type_1(stock)
        secid='{}{}'.format(marker,stock)
        url='https://push2.eastmoney.com/api/qt/stock/get?'
        params={
            #cb: jQuery3510250885634607382_1693625754740
            'secid':secid,
            'forcect': '1',
            'invt': '2',
            'fields': 'f43,f44,f45,f46,f48,f49,f50,f51,f52,f59,f60,f108,f152,f161,f168,f169,f170',
            'ut': 'f057cbcbce2a86e2866ab8877db1d059',
            #_: 1693625754746
        }
        try:
            
            res=requests.get(url=url,params=params)
            text=res.json()['data']
            result={}
            if stock[:6]=='164824':
                result['最新价']=float(text['f43'])/10000
            else:
                result['最新价']=float(text['f43'])/1000
            result['最高价']=text['f44']/1000
            result['最低价']=text['f45']/1000
            result['今开']=text['f46']/1000
            result['金额']=text['f48']
            result['外盘']=text['f49']
            result['量比']=text['f50']/100
            result['涨停价']=text['f51']/1000
            result['跌停价']=text['f52']/1000
            result['昨收']=text['f60']/1000
            result['涨跌']=text['f169']/1000
            result['内盘']=text['f161']
            result['换手率']=text['f168']/100
            result['涨跌幅']=text['f170']/100
            print('东方财富数据')
            return result
        except:
            json_text=self.tdx_data.get_security_quotes_none(stock=stock)
            data_dict={}
            data_dict['最新价']=json_text['price'].tolist()[-1]/10
            data_dict['最高价']=json_text['high'].tolist()[-1]/10
            data_dict['最低价']=json_text['low'].tolist()[-1]/10
            data_dict['今开']=json_text['open'].tolist()[-1]/10
            data_dict['涨跌幅']=((data_dict['最新价']-data_dict['今开'])/data_dict['今开'])*100
            print('通达信数据')
            return data_dict
    def get_etf_spot_trader_data(self,stock='159632',limit=600000):
        '''
        ETF实时交易数据3秒一次
        '''
        marker,stock=self.tdx_data.rename_stock_type_1(stock)
        secid='{}{}'.format(marker,stock)
        try:
            url='https://push2.eastmoney.com/api/qt/stock/details/get?'
            params={
                #cb: jQuery3510250885634607382_1693625754742
                'secid':secid,
                'forcect': '1',
                'invt': '2',
                'pos':-limit,
                'iscca': '1',
                'fields1': 'f1,f2,f3,f4,f5',
                'fields2': 'f51,f52,f53,f54,f55',
                'ut': 'f057cbcbce2a86e2866ab8877db1d059'
                #_: 1693625754806
            }
            res=requests.get(url=url,params=params)
            text=res.json()['data']['details']
            data=[]
            for i in text:
                data.append(i.split(','))
            df=pd.DataFrame(data)
            df.columns=['时间','价格','成交量','未知','买卖盘']
            df['时间']=df['时间'].apply(lambda x:int(''.join(x.split(':'))))
            def select_data(x):
                if x=='1':
                    return '卖盘'
                elif x=='2':
                    return '买盘'
                else:
                    return x
            df['买卖盘']=df['买卖盘'].apply(select_data)
            df=df[df['时间']>=92400]
            df['价格']=pd.to_numeric(df['价格'])
            df['实时涨跌幅']=(df['价格'].pct_change())*100
            df['涨跌幅']=df['实时涨跌幅'].cumsum()
            return df
        except:
            data=self.tdx_data.get_trader_data(stock=stock,start=0,count=9000)
            data['价格']=data['price']/10
            data['涨跌幅']=(data['价格'].pct_change()*100).cumsum()
            data['实时涨跌幅']=data['涨跌幅']-data['涨跌幅'].shift(1)
            return data
    def _fund_lof_code_id_map_em(self) -> dict:
        """
        东方财富-LOF 代码和市场标识映射
        https://quote.eastmoney.com/center/gridlist.html#fund_lof
        :return: LOF 代码和市场标识映射
        :rtype: pandas.DataFrame
        """
        url = "https://2.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "5000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "wbp2u": "|0|0|0|web",
            "fid": "f3",
            "fs": "b:MK0404,b:MK0405,b:MK0406,b:MK0407",
            "fields": "f12,f13",
            "_": "1672806290972",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_dict = dict(zip(temp_df["f12"], temp_df["f13"]))
        return temp_dict


    def fund_lof_spot_em(self) -> pd.DataFrame:
        """
        东方财富-LOF 实时行情
        https://quote.eastmoney.com/center/gridlist.html#fund_lof
        :return: LOF 实时行情
        :rtype: pandas.DataFrame
        """
        url = "https://88.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "5000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "wbp2u": "|0|0|0|web",
            "fid": "f3",
            "fs": "b:MK0404,b:MK0405,b:MK0406,b:MK0407",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
            "_": "1672806290972",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_df.rename(
            columns={
                "f12": "代码",
                "f14": "名称",
                "f2": "最新价",
                "f4": "涨跌额",
                "f3": "涨跌幅",
                "f5": "成交量",
                "f6": "成交额",
                "f17": "开盘价",
                "f15": "最高价",
                "f16": "最低价",
                "f18": "昨收",
                "f8": "换手率",
                "f21": "流通市值",
                "f20": "总市值",
            },
            inplace=True,
        )
        temp_df = temp_df[
            [
                "代码",
                "名称",
                "最新价",
                "涨跌额",
                "涨跌幅",
                "成交量",
                "成交额",
                "开盘价",
                "最高价",
                "最低价",
                "昨收",
                "换手率",
                "流通市值",
                "总市值",
            ]
        ]
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"], errors="coerce")
        temp_df["最高价"] = pd.to_numeric(temp_df["最高价"], errors="coerce")
        temp_df["最低价"] = pd.to_numeric(temp_df["最低价"], errors="coerce")
        temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
        return temp_df


    def fund_lof_hist_em(self,
        symbol: str = "166009",
        period: str = "daily",
        start_date: str = "19700101",
        end_date: str = "20500101",
        adjust: str = "",
    ) -> pd.DataFrame:
        """
        东方财富-LOF 行情
        https://quote.eastmoney.com/sz166009.html
        :param symbol: LOF 代码
        :type symbol: str
        :param period: choice of {'daily', 'weekly', 'monthly'}
        :type period: str
        :param start_date: 开始日期
        :type start_date: str
        :param end_date: 结束日期
        :type end_date: str
        :param adjust: choice of {"qfq": "前复权", "hfq": "后复权", "": "不复权"}
        :type adjust: str
        :return: 每日行情
        :rtype: pandas.DataFrame
        """
        code_id_dict = self._fund_lof_code_id_map_em()
        adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
        period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "klt": period_dict[period],
            "fqt": adjust_dict[adjust],
            "secid": f"{code_id_dict[symbol]}.{symbol}",
            "beg": start_date,
            "end": end_date,
            "_": "1623766962675",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        if not (data_json["data"] and data_json["data"]["klines"]):
            return pd.DataFrame()
        temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
        temp_df.columns = [
            "日期",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        temp_df.index = pd.to_datetime(temp_df["日期"])
        temp_df.reset_index(inplace=True, drop=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        return temp_df


    def fund_lof_hist_min_em(self,
        symbol: str = "166009",
        start_date: str = "1979-09-01 09:32:00",
        end_date: str = "2222-01-01 09:32:00",
        period: str = "5",
        adjust: str = "",
    ) -> pd.DataFrame:
        """
        东方财富-LOF 分时行情
        https://quote.eastmoney.com/sz166009.html
        :param symbol: LOF 代码
        :type symbol: str
        :param start_date: 开始日期时间
        :type start_date: str
        :param end_date: 结束日期时间
        :type end_date: str
        :param period: choice of {"1", "5", "15", "30", "60"}
        :type period: str
        :param adjust: choice of {'', 'qfq', 'hfq'}
        :type adjust: str
        :return: 每日分时行情
        :rtype: pandas.DataFrame
        """
        code_id_dict = self._fund_lof_code_id_map_em()
        adjust_map = {
            "": "0",
            "qfq": "1",
            "hfq": "2",
        }
        if period == "1":
            url = "https://push2his.eastmoney.com/api/qt/stock/trends2/get"
            params = {
                "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "ndays": "5",
                "iscr": "0",
                "secid": f"{code_id_dict[symbol]}.{symbol}",
                "_": "1623766962675",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(
                [item.split(",") for item in data_json["data"]["trends"]]
            )
            temp_df.columns = [
                "时间",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "成交量",
                "成交额",
                "最新价",
            ]
            temp_df.index = pd.to_datetime(temp_df["时间"])
            temp_df = temp_df[start_date:end_date]
            temp_df.reset_index(drop=True, inplace=True)
            temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
            temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
            temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
            temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
            temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
            temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
            temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
            temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
            return temp_df
        else:
            url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
            params = {
                "fields1": "f1,f2,f3,f4,f5,f6",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "klt": period,
                "fqt": adjust_map[adjust],
                "secid": f"{code_id_dict[symbol]}.{symbol}",
                "beg": "0",
                "end": "20500000",
                "_": "1630930917857",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(
                [item.split(",") for item in data_json["data"]["klines"]]
            )
            temp_df.columns = [
                "时间",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "成交量",
                "成交额",
                "振幅",
                "涨跌幅",
                "涨跌额",
                "换手率",
            ]
            temp_df.index = pd.to_datetime(temp_df["时间"])
            temp_df = temp_df[start_date:end_date]
            temp_df.reset_index(drop=True, inplace=True)
            temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
            temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
            temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
            temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
            temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
            temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
            temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
            temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
            temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
            temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
            temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
            temp_df = temp_df[
                [
                    "时间",
                    "开盘",
                    "收盘",
                    "最高",
                    "最低",
                    "涨跌幅",
                    "涨跌额",
                    "成交量",
                    "成交额",
                    "振幅",
                    "换手率",
                ]
            ]
            return temp_df
