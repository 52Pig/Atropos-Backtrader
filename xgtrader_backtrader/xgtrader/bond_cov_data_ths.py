import pandas as pd
import requests
import json
from .tdx_data import tdx_data
#可转债数据
class bond_cov_data_ths:
    def __init__(self):
        self.tdx_data=tdx_data()
        self.tdx_data.connect()
    def get_cov_bond_hist_data(self,stock='113016',start='20100101',end='20500101',limit='10000',
                                data_type='D',fqt='1',count=8000):
        '''
        可转债历史数据
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
        data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
        klt=data_dict[data_type]
        try:
            params={
                'secid':'1.{}'.format(stock),
                'klt':klt,
                'fqt':fqt,
                'lmt':limit,
                'start':start,
                'end':end,
                'iscca': '1',
                'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                'ut':'f057cbcbce2a86e2866ab8877db1d059',
                'forcect':'1'
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
            #data1['累计涨跌幅']=data1['涨跌幅'].cumsum()
            return data1
        except:
            try:
                params={
                    'secid':'0.{}'.format(stock),
                    'klt':klt,
                    'fqt':fqt,
                    'start':start,
                    'lmt':limit,
                    'end':end,
                    'iscca': '1',
                    'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                    'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                    'ut':'f057cbcbce2a86e2866ab8877db1d059',
                    'forcect':'1'
                }
                url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                res = requests.get(url=url, params=params)
                text = res.json()
                json_text =text
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
                data['volume']=data['vol']
                data['涨跌幅']=data['close'].pct_change()*100
                data['涨跌额']=data['close']-data['open']
                data['振幅']=(data['high']-data['low'])/data['low']*100
                return data
    def get_cov_bond_spot(self,stock='113016'):
        '''
        获取可转债实时数据
        '''
        try:
            params={
                'cb':'jQuery35107788691587529397_1680967733868',
                'secid':'1.{}'.format(stock),
                'forcect':'1',
                'invt': '2',
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f59,f60,f108,f152,f154,f161,f168,f169,f170,f262,f264,f265,f266,f267,f424,f426,f427,f428,f429,f432',
                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                '_': '1680967733870',
            }
            url='https://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text[41:len(res.text)-2]
            json_text=json.loads(text)['data']
            data_dict={}
            data_dict['最新价']=json_text['f43']/1000
            data_dict['最高价']=json_text['f44']/1000
            data_dict['最低价']=json_text['f45']/1000
            data_dict['今开']=json_text['f46']/1000 
            data_dict['总手']=json_text['f47']
            data_dict['金额']=json_text['f48']
            #data_dict['量比']=json_text['f50']/100
            data_dict['外盘']=json_text['f49']
            data_dict['涨停价']=json_text['f51']/1000
            data_dict['跌停价']=json_text['f52']/1000
            data_dict['涨停收盘价']=json_text['f60']/1000
            data_dict['涨跌幅']=json_text['f170']/100
            data_dict['证券代码']=json_text['f262']
            data_dict['名称']=json_text['f264']
            data_dict['溢价率']=json_text['f428']/100
            return data_dict
        except:
            try:
                params={
                    'cb':'jQuery35107788691587529397_1680967733868',
                    'secid':'0.{}'.format(stock),
                    'forcect':'1',
                    'invt': '2',
                    'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f59,f60,f108,f152,f154,f161,f168,f169,f170,f262,f264,f265,f266,f267,f424,f426,f427,f428,f429,f432',
                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                    '_': '1680967733870',
                }
                url='https://push2.eastmoney.com/api/qt/stock/get?'
                res=requests.get(url=url,params=params)
                text=res.text[41:len(res.text)-2]
                json_text=json.loads(text)['data']
                data_dict={}
                data_dict['最新价']=json_text['f43']/1000
                data_dict['最高价']=json_text['f44']/1000
                data_dict['最低价']=json_text['f45']/1000
                data_dict['今开']=json_text['f46']/1000 
                data_dict['总手']=json_text['f47']
                data_dict['金额']=json_text['f48']
                #data_dict['量比']=json_text['f50']/100
                data_dict['外盘']=json_text['f49']
                data_dict['涨停价']=json_text['f51']/1000
                data_dict['跌停价']=json_text['f52']/1000
                data_dict['涨停收盘价']=json_text['f60']/1000
                data_dict['涨跌幅']=json_text['f170']/100
                data_dict['证券代码']=json_text['f262']
                data_dict['名称']=json_text['f264']
                data_dict['溢价率']=json_text['f428']/100
                return data_dict
            except:
                json_text=self.tdx_data.get_security_quotes_none(stock=stock)
                data_dict={}
                data_dict['最新价']=json_text['price'].tolist()[-1]/100
                data_dict['最高价']=json_text['high'].tolist()[-1]/100
                data_dict['最低价']=json_text['low'].tolist()[-1]/100
                data_dict['今开']=json_text['open'].tolist()[-1]/100
                return data_dict
    def bank_cov_now(self):
        headers={'Cookie':'kbzw__Session=6onjptppfesqe36qi1dqh1a3b7; Hm_lvt_164fe01b1433a19b507595a43bf58262=1647848946; kbz_newcookie=1; Hm_lpvt_164fe01b1433a19b507595a43bf58262=1647849368',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        url='https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t=1647849403082'
        res=requests.get(url=url,headers=headers)
        rows=json.loads(res.text)['rows']
        df=pd.json_normalize(rows)
        df.rename(columns={'cell.list_date':'申购时间','id':'代码','cell.price':'正股价格','cell.increase_rt':'正股涨跌幅','cell.pma_rt':'正股最新价/转股价','cell.pb':'正股pb','cell.stock_id':'证券代码',
        'cell.stock_nm':'股票名称','cell.bond_nm':'可转债名称','cell.bond_id':'证券代码','cell.amount':'发行规模亿元','cell.cb_amount':'百元股票含权','cell.convert_price':'转股价',
        'cell.ration':'每股配售元','cell.online_amount':'网上发行规模','cell.lucky_draw_rt':'中签比例%','cell.underwriter_rt':'包销比例%','cell.rating_cd':'平级'},inplace=True)
        df1=df[['申购时间','代码','正股价格','正股涨跌幅','正股最新价/转股价','正股pb','证券代码','股票名称','可转债名称','证券代码','发行规模亿元','百元股票含权','转股价',
        '每股配售元','网上发行规模','中签比例%','包销比例%','平级']]
        return df1
    #可转债强制赎回
    def bank_cov_qz(self):
        headers={'Cookie':'kbzw__Session=6onjptppfesqe36qi1dqh1a3b7; Hm_lvt_164fe01b1433a19b507595a43bf58262=1647848946; kbz_newcookie=1; Hm_lpvt_164fe01b1433a19b507595a43bf58262=1647849368',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        url='https://www.jisilu.cn/data/cbnew/redeem_list/?___jsl=LST___t=1647864993962'
        res=requests.get(url=url,headers=headers)
        rows=json.loads(res.text)['rows']
        df=pd.json_normalize(rows)
        #df.rename(columns={'cell.bond_id':'证券代码','cell.bond_nm':'可转债名称','cell.stock_id':'证券代码','cell.orig_iss_amt':'规模亿元','cell.curr_iss_amt':'剩余规模亿元',
        #'cell.convert_dt':'转股开始日','cell.next_put_dt':'转股结束日','cell.convert_price':'转股价','cell.redeem_price_ratio':'强制赎回触发','cell.real_force_redeem_price':'强制赎回价格',
        #'cell.sprice':'正股价','cell.force_redeem_price':'触发价'},inplace=True)
        #df1=df[['证券代码','可转债名称','证券代码','规模亿元','剩余规模亿元','转股开始日','转股结束日','转股价','强制赎回触发','强制赎回价格','正股价','触发价']]
        return df
    #可转债回售
    def bank_cov_hs(self):
        headers={'Cookie':'kbzw__Session=6onjptppfesqe36qi1dqh1a3b7; Hm_lvt_164fe01b1433a19b507595a43bf58262=1647848946; kbz_newcookie=1; Hm_lpvt_164fe01b1433a19b507595a43bf58262=1647849368',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        url='https://www.jisilu.cn/data/cbnew/huishou_list/?___jsl=LST___t=1647866550798'
        res=requests.get(url=url,headers=headers)
        rows=json.loads(res.text)['rows']
        df=pd.json_normalize(rows)
        df.rename(columns={'cell.bond_id':'证券代码','cell.bond_nm':'可转债名称','cell.full_price':'最新价','cell.last_dt':'回售开始日','cell.stock_id':'证券代码',
        'cell.stock_nm':'股票名称','cell.orig_iss_amt':'规模亿元','cell.curr_iss_amt':'剩余规模亿元','cell.convert_price':'转股价','cell.put_convert_price_ratio':'回售触发比',
        'cell.put_price':'回售价','cell.put_tc':'回售条款','cell.sprice':'正股价','cell.put_convert_price':'回售触发价'},inplace=True)
        df1=df[['证券代码','可转债名称','最新价','回售开始日','证券代码','规模亿元','转股价','剩余规模亿元','股票名称','回售条款','正股价','回售触发价']]
        return df1
    #可转债退市
    def bank_cov_ts(self):
        headers={'Cookie':'kbzw__Session=6onjptppfesqe36qi1dqh1a3b7; Hm_lvt_164fe01b1433a19b507595a43bf58262=1647848946; kbz_newcookie=1; Hm_lpvt_164fe01b1433a19b507595a43bf58262=1647849368',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        url='https://www.jisilu.cn/data/cbnew/delisted/?___jsl=LST___t=1647867703115'
        res=requests.get(url=url,headers=headers)
        rows=json.loads(res.text)['rows']
        df=pd.json_normalize(rows)
        df.rename(columns={'cell.bond_id':'证券代码','cell.bond_nm':'可转债名称','cell.price':'最后交易价格','cell.stock_id':'证券代码','cell.stock_nm':'股票名称',
        'cell.orig_iss_amt':'发行规模亿元','cell.put_iss_amt':'回售规模','cell.curr_iss_amt':'剩余规模亿元','cell.issue_dt':'发行日期','cell.redeem_dt':'最后交易日期',
        'maturity_dt':'到期日','listed_years':'存续期限','delist_notes':'原因'},inplace=True)
        df1=df[['证券代码','可转债名称','最后交易价格','证券代码','股票名称','发行规模亿元','回售规模','剩余规模亿元','发行日期','最后交易日期']]
        return df1
    #东方财富可转债申购
    def bank_cov_new_em(self):
        url='https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112305407605488004101_1647870139241&sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=50&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=ALL&quoteColumns=f2~01~CONVERT_STOCK_CODE~CONVERT_STOCK_PRICE%2Cf235~10~SECURITY_CODE~TRANSFER_PRICE%2Cf236~10~SECURITY_CODE~TRANSFER_VALUE%2Cf2~10~SECURITY_CODE~CURRENT_BOND_PRICE%2Cf237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO%2Cf239~10~SECURITY_CODE~RESALE_TRIG_PRICE%2Cf240~10~SECURITY_CODE~REDEEM_TRIG_PRICE%2Cf23~01~CONVERT_STOCK_CODE~PBV_RATIO&source=WEB&client=WEB'
        res=requests.get(url=url)
        text=res.text
        df=text[42:len(text)-2]
        df1=json.loads(df)
        df2=pd.DataFrame(df1['result']['data'])
        df2.rename(columns={'SECURITY_CODE':'证券代码','SECURITY_NAME_ABBR':'可转债名称','CONVERT_STOCK_CODE':'证券代码','VALUE_DATE':'申购日期',
        'BOND_EXPIRE':'存续时间','CEASE_DATE':'结束时间','INTEREST_RATE_EXPLAIN':'各期的利率','REMARK':'公告'},inplace=True)
        df3=df2[['证券代码','可转债名称','证券代码','申购日期','存续时间','结束时间','各期的利率','公告']]
        return df3
    #东方财富可转债性价比
    #提前全部数据
    def bank_cov_em_xjb(self):
        url='https://40.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407202748379757598_1647871383940&pn=1&pz=450&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f243&fs=b:MK0354&fields=f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f26,f243&_=1647871383955'
        res=requests.get(url=url)
        text=res.text
        df=text[42:len(text)-2]
        df1=json.loads(df)
        df2=pd.DataFrame(df1['data']['diff'])
        df2.rename(columns={'f12':'证券代码','f14':'证券代码','f227':'纯可转债价值','f230':'涨跌幅','f229':'最新价','f232':'证券代码','f234':'股票名称',
        'f236':'转股价值','f239':'回售触发价','f240':'强制赎回触发价','f241':'到期赎回价','f242':'开始转股日期','f243':'申购日期'},inplace=True)
        df3=df2[['证券代码','证券代码','纯可转债价值','涨跌幅','最新价','证券代码','股票名称','转股价值',
        '回售触发价','强制赎回触发价','到期赎回价','开始转股日期','申购日期']]
        return df3
    #获取东方财富可转债一览表
    def get_cov_bond_all_data(self):
        url='https://datacenter-web.eastmoney.com/api/data/v1/get?'
        params={
            'callback': 'jQuery112308978339674558973_1654394381194',
            'sortColumns': 'PUBLIC_START_DATE',
            'sortTypes': '-1',
            'pageSize': '5000',
            'pageNumber': '1',
            'reportName': 'RPT_BOND_CB_LIST',
            'columns': 'ALL',
            'quoteColumns': 'f2~01~CONVERT_STOCK_CODE~CONVERT_STOCK_PRICE,f235~10~SECURITY_CODE~TRANSFER_PRICE,f236~10~SECURITY_CODE~TRANSFER_VALUE,f2~10~SECURITY_CODE~CURRENT_BOND_PRICE,f237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO,f239~10~SECURITY_CODE~RESALE_TRIG_PRICE,f240~10~SECURITY_CODE~REDEEM_TRIG_PRICE,f23~01~CONVERT_STOCK_CODE~PBV_RATIO',
            'source': 'WEB',
            'client': 'WEB'
        }
        header={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        res=requests.get(url=url,params=params,headers=header)
        text=res.text[42:len(res.text)-2]
        json_text=json.loads(text)
        df=pd.DataFrame(json_text['result']['data'])
        #书籍太多，选一些就可以了
        df.rename(columns={'SECURITY_CODE':'代码','SECURITY_NAME_ABBR':'名称','INTEREST_RATE_EXPLAIN':'每年利息',
        'ACTUAL_ISSUE_SCALE':'发现规模亿元','ISSUE_PRIC':'最新价','REMARK':'发行声明','PUBLIC_START_DATE':'股权登记',
        'SECURITY_SHORT_NAME':'股票名称','NE_GENERAL_LWR':'中签比例','INITIAL_TRANSFER_PRICE':'转股价',
        'TRANSFER_END_DATE':'到期日','TRANSFER_START_DATE':'可以开始转股','RESALE_CLAUSE':'详细信息',
        'CONVERT_STOCK_PRICE':'正股价','TRANSFER_VALUE':'价值'},inplace=True)
        df1=df[['代码','名称','发现规模亿元','发行声明','每年利息','股权登记','股票名称','转股价','到期日','可以开始转股','详细信息','正股价','价值']]
        return df1
    #获取可转债实时数据
    def bond_zh_hs_cov_min(self,symbol='',period=''):
        """
        东方财富网-可转债-分时行情
        https://quote.eastmoney.com/concept/sz128039.html
        :param symbol: 转债代码
        :type symbol: str
        :param period: choice of {'1', '5', '15', '30', '60'}
        :type period: str
        :param adjust: choice of {'', 'qfq', 'hfq'}
        :type adjust: str
        :param start_date: 开始日期
        :type start_date: str
        :param end_date: 结束日期
        :type end_date: str
        :return: 分时行情
        :rtype: pandas.DataFrame
        """
        symbol: str = "sh113570",
        period: str = "15",
        adjust: str = "0",
        start_date: str = "1979-09-01 09:32:00",
        end_date: str = "2222-01-01 09:32:00",
        market_type = {"sh": "1", "sz": "0"}
        if period == "1":
            url = "https://push2.eastmoney.com/api/qt/stock/trends2/get"
            params = {
                "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
                "ut": "fa5fd1943c7b386f172d6893dbfba10b",
                "ndays": "5",
                "iscr": "0",
                "iscca": "0",
                "secid": f"{market_type[symbol[:2]]}.{symbol[2:]}",
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
            temp_df["开盘"] = pd.to_numeric(temp_df["开盘"])
            temp_df["收盘"] = pd.to_numeric(temp_df["收盘"])
            temp_df["最高"] = pd.to_numeric(temp_df["最高"])
            temp_df["最低"] = pd.to_numeric(temp_df["最低"])
            temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
            temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
            temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
            temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)  # 带日期时间
            return temp_df
        else:
            adjust_map = {
                "": "0",
                "qfq": "1",
                "hfq": "2",
            }
            url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
            params = {
                "fields1": "f1,f2,f3,f4,f5,f6",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "klt": period,
                "fqt": adjust_map[adjust],
                "secid": f"{market_type[symbol[:2]]}.{symbol[2:]}",
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
            temp_df["开盘"] = pd.to_numeric(temp_df["开盘"])
            temp_df["收盘"] = pd.to_numeric(temp_df["收盘"])
            temp_df["最高"] = pd.to_numeric(temp_df["最高"])
            temp_df["最低"] = pd.to_numeric(temp_df["最低"])
            temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
            temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
            temp_df["振幅"] = pd.to_numeric(temp_df["振幅"])
            temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
            temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"])
            temp_df["换手率"] = pd.to_numeric(temp_df["换手率"])
            temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)  # 带日期时间
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
            df=temp_df
            df.to_excel(r'可转债数据.xlsx')
            print(df)
            return temp_df
    def bond_zh_cov_value_analysis(self,symbol='sh010107') -> pd.DataFrame:
        """
        https://data.eastmoney.com/kzz/detail/113527.html
        东方财富网-数据中心-新股数据-可转债数据-价值分析-溢价率分析
        :return: 可转债价值分析
        :rtype: pandas.DataFrame
        """
        url = "https://datacenter-web.eastmoney.com/api/data/get"
        params = {
            "sty": "ALL",
            "token": "894050c76af8597a853f5b408b759f5d",
            "st": "date",
            "sr": "1",
            "source": "WEB",
            "type": "RPTA_WEB_KZZ_LS",
            "filter": f'(zcode="{symbol}")',
            "p": "1",
            "ps": "8000",
            "_": "1648629088839",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        temp_df.columns = [
            "日期",
            "-",
            "-",
            "转股价值",
            "纯债价值",
            "纯债溢价率",
            "转股溢价率",
            "收盘价",
            "-",
            "-",
            "-",
            "-",
        ]
        temp_df = temp_df[
            [
                "日期",
                "收盘价",
                "纯债价值",
                "转股价值",
                "纯债溢价率",
                "转股溢价率",
            ]
        ]

        temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
        temp_df["收盘价"] = pd.to_numeric(temp_df["收盘价"])
        temp_df["纯债价值"] = pd.to_numeric(temp_df["纯债价值"])
        temp_df["转股价值"] = pd.to_numeric(temp_df["转股价值"])
        temp_df["纯债溢价率"] = pd.to_numeric(temp_df["纯债溢价率"])
        temp_df["转股溢价率"] = pd.to_numeric(temp_df["转股溢价率"])
        return temp_df
    #简表
    def simple_table(self):
        '''
        简表
        '''
        df=pd.read_html(r'https://www.ninwin.cn/index.php?m=cb&show_cb_only=Y&show_listed_only=Y')
        df1=df[0]
        return df1
    #全表
    def all_table(self):
        '''
        全表
        '''
        url=sg.popup_get_text('输入测试后的网站')
        df=pd.read_html(url)
        df1=df[0]
        return df1
    #发行中
    def bond_cov_ipo(self):
        '''
        发行中
        '''
        df=pd.read_html(r'https://www.ninwin.cn/index.php?m=cb&a=cb_to_list')
        df1=df[0] 
        return df1
    #申购
    def bond_cov_buy(self):
        '''
        申购
        '''
        df=pd.read_html(r'https://www.ninwin.cn/index.php?m=cb&a=cb_subs')
        df1=df[0]
        return df1
    #已经申购
    def bond_cov_end_buy():
        '''
        已经申购
        '''
        df=pd.read_html(r'https://www.ninwin.cn/index.php?m=cb&a=cb_hist_subs')
        df1=df[0]
        return df1
    #EB
    def bond_cov_eb(self):
        '''
        EB
        '''
        df=pd.read_html(r'https://www.ninwin.cn/index.php?m=cb&a=list_eb&show_eb=1&show_cb=0&show_eb_only=Y')
        df1=df[0]
        return df1
    #可转债交易指数数据
    def bond_cov_trader_index(self):
        '''
        可转债交易指数数据
        '''
        url='https://www.ninwin.cn/index.php?m=cb&c=idx&a=idxServer'
        header={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        res=requests.get(url=url,headers=header)
        df=pd.DataFrame(res.json()['data'])
        return df
    #统计
    def bond_cov_stats(self):
        url='https://www.ninwin.cn/index.php?m=cb&a=stats'
        df=pd.read_html(url)
        data=[]
        for i in range(1,len(df)):
            data.append(pd.DataFrame(df[i]))
        df1=pd.concat(data)
        return df1
    #强制赎回
    def bond_cov_qzsh(self):
        '''
        强制赎回
        '''
        url='https://www.ninwin.cn/index.php?m=cb&a=call'
        df=pd.read_html(url)
        df1=pd.DataFrame(df[0])
        return df1
    #回售
    def bond_cov_hs(self):
        '''
        回售
        '''
        url='https://www.ninwin.cn/index.php?m=cb&a=put'
        df=pd.read_html(url)
        df1=pd.DataFrame(df[0])
        return df1
    #下修价格
    def bond_cov_xx(self):
        '''
        下修价格
        '''
        url='https://www.ninwin.cn/index.php?m=cb&a=revise_down'
        df=pd.read_html(url)
        df1=pd.DataFrame(df[0])
        return df1
    #规模
    def bond_cov_size(self):
        '''
        规模
        '''
        url='https://www.ninwin.cn/index.php?m=cb&a=size'
        df=pd.read_html(url)
        df1=pd.DataFrame(df[0])
        return df1
    #退市
    def bond_cov_past(self):
        '''
        退市
        '''
        url='https://www.ninwin.cn/index.php?m=cb&a=past'
        df=pd.read_html(url)
        df1=pd.DataFrame(df[0])
        return df1
    #可转债公告
    def bond_cov_gg(self):
        url='https://www.ninwin.cn/index.php?m=cb&a=cb_gg_server'
        header={
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Connection':'keep-alive',
            'Content-Length':'276',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie':'P0s_cbQuestion=1; P0s_answerTime=1654601533; P0s_q_n=1; csrf_token=3dec268f9d160282; __51cke__=; PHPSESSID=lm85rick7od1fmjapu1tjl6a3g; P0s_visitor=jYhm8IvUoDplkanN%2BnfqZpx9bN0HUthzGpC5aarNuh9e9SGy%2BGX8jP5%2FEvM%3D; __tins__4771153=%7B%22sid%22%3A%201654653249466%2C%20%22vd%22%3A%205%2C%20%22expires%22%3A%201654655646416%7D; __51laig__=12; P0s_lastvisit=7709%091654654158%09%2Findex.php%3Fm%3Dcb%26a%3Dcb_gg_server',
            'Host':'www.ninwin.cn',
            'Origin':'https://www.ninwin.cn',
            'Referer':'https://www.ninwin.cn/index.php?m=cb&a=cb_gg',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        res=requests.get(url=url,headers=header)
        df=pd.DataFrame(res.json())
        return df
    def get_cov_bond_spot_trader_data(self,stock='123018'):
        '''
        控制住实时数据
        '''
        try:
            url='https://push2.eastmoney.com/api/qt/stock/details/get?'
            params={
                #'cb': 'jQuery3510784161408794853_1689866980183',
                'secid': '0.{}'.format(stock),
                'forcect': '1',
                'invt': '2',
                'pos': '-10000',
                'iscca': '1',
                'fields1': 'f1,f2,f3,f4,f5',
                'fields2': 'f51,f52,f53,f54,f55',
                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                '_': '1689866980185'
            }
            res=requests.get(url=url,params=params)
            text=res.json()
            df=pd.DataFrame(text['data']['details'])
            df.columns=['数据']
            all_df=[]
            for i in df['数据']:
                all_df.append(i.split(','))
            data=pd.DataFrame(all_df)
            data.columns=['时间','价格','成交量','单数','性质']
            def select_stock(x):
                if x=='2':
                    return '买盘'
                elif x=='1':
                    return '卖盘'
                else:
                    return x
            data['性质']=data['性质'].apply(select_stock)
            data['价格']=data['价格'].astype(float)
            data['时间']=data['时间'].apply(lambda x :int(str(x).replace(':','')))
            data=data[data['时间']>=92100]
            data['涨跌幅']=(data['价格'].pct_change()*100).cumsum()
            data['实时涨跌幅']=data['涨跌幅']-data['涨跌幅'].shift(1)
            return data
        except:
            try:
                url='https://push2.eastmoney.com/api/qt/stock/details/get?'
                params={
                    #'cb': 'jQuery3510784161408794853_1689866980183',
                    'secid': '1.{}'.format(stock),
                    'forcect': '1',
                    'invt': '2',
                    'pos': '-10000',
                    'iscca': '1',
                    'fields1': 'f1,f2,f3,f4,f5',
                    'fields2': 'f51,f52,f53,f54,f55',
                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                    '_': '1689866980185'
                }
                res=requests.get(url=url,params=params)
                text=res.json()
                df=pd.DataFrame(text['data']['details'])
                df.columns=['数据'] 
                all_df=[]
                for i in df['数据']:
                    all_df.append(i.split(','))
                data=pd.DataFrame(all_df)
                data.columns=['时间','价格','成交量','单数','性质']
                def select_stock(x):
                    if x=='2':
                        return '买盘'
                    elif x=='1':
                        return '卖盘'
                    else:
                        return x
                data['性质']=data['性质'].apply(select_stock)
                data['价格']=data['价格'].astype(float)
                data['时间']=data['时间'].apply(lambda x :int(str(x).replace(':','')))
                data=data[data['时间']>=92500]
                data['涨跌幅']=(data['价格'].pct_change()*100).cumsum()
                data['实时涨跌幅']=data['涨跌幅']-data['涨跌幅'].shift(1)
                return data
            except:
                data=self.tdx_data.get_trader_data(stock=stock,start=0,count=9000)
                data['价格']=data['price']/10
                data['涨跌幅']=(data['价格'].pct_change()*100).cumsum()
                data['实时涨跌幅']=data['涨跌幅']-data['涨跌幅'].shift(1)
                return data
    def get_cov_bond_dish_data(self,stock='111007'):
        '''
        获取可转债盘口数据
        '''
        try:
            url='https://push2.eastmoney.com/api/qt/stock/get?'
            data={}
            params={
                'invt': '2',
                'fltt': '1',
                #'cb': 'jQuery35106054114396324737_1690471800729',
                'fields': 'f58,f734,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f171,f47,f86,f292,f19,f39,f20,f40,f17,f531,f18,f15,f16,f13,f14,f11,f12,f37,f38,f35,f36,f33,f34,f31,f32,f48,f50,f161,f49,f191,f192,f71,f264,f263,f262,f267,f265,f268,f706,f700,f701,f703,f154,f704,f702,f705,f721,f51,f52,f301',
                'secid': '1.'+stock,
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'wbp2u': '|0|0|0|web',
            }
            res=requests.get(url=url,params=params)
            text=res.text
            text=res.json()['data']
            buy_5_price=text['f11']/1000
            data['buy_5_price']=buy_5_price
            buy_5_num=text['f12']
            data['buy_5_num']=buy_5_num
            buy_4_price=text['f13']/1000
            data['buy_4_price']=buy_4_price
            buy_4_num=text['f14']
            data['buy_4_num']=buy_4_num
            buy_3_price=text['f15']/1000
            data['buy_3_price']=buy_3_price
            buy_3_num=text['f16']
            data['buy_3_num']=buy_3_num
            buy_2_price=text['f17']/1000
            data['buy_2_price']=buy_2_price
            buy_2_num=text['f18']
            data['buy_2_num']=buy_2_num
            buy_1_price=text['f19']/1000
            data['buy_1_price']=buy_1_price
            buy_1_num=text['f20']
            data['buy_1_num']=buy_1_num
            sell_5_price=text['f31']/1000
            data['sell_5_price']=sell_5_price
            sell_5_num=text['f32']
            data['sell_5_num']=sell_5_num
            sell_4_price=text['f33']/1000
            data['sell_4_price']=sell_4_price
            sell_4_num=text['f34']
            data['sell_4_num']=sell_4_num
            sell_3_price=text['f35']/1000
            data['sell_3_price']=sell_3_price
            sell_3_num=text['f36']
            data['sell_3_num']=sell_3_num
            sell_2_price=text['f37']/100
            data['sell_2_price']=sell_2_price
            sell_2_num=text['f38']
            data['sell_2_num']=sell_2_num
            sell_1_price=text['f39']/1000
            data['sell_1_price']=sell_1_price
            sell_1_num=text['f40']
            data['sell_1_num']=sell_1_num
            data['最新价']=text['f43']/1000
            data['今开']=text['f46']/1000
            data['最高']=text['f44']/1000
            data['最低']=text['f45']/1000
            data['代码']=text['f57']
            data['名称']=text['f58']
            data['涨跌幅']=text['f169']/1000
            data['证券代码']=text['f262']
            data['股票名称']=text['f264']
            data['股票价格']=text['f267']/100
            data['股票涨跌幅']=text['f267']/100
            return data
        except:
            url='https://push2.eastmoney.com/api/qt/stock/get?'
            data={}
            params={
                'invt': '2',
                'fltt': '1',
                #'cb': 'jQuery35106054114396324737_1690471800729',
                'fields': 'f58,f734,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f171,f47,f86,f292,f19,f39,f20,f40,f17,f531,f18,f15,f16,f13,f14,f11,f12,f37,f38,f35,f36,f33,f34,f31,f32,f48,f50,f161,f49,f191,f192,f71,f264,f263,f262,f267,f265,f268,f706,f700,f701,f703,f154,f704,f702,f705,f721,f51,f52,f301',
                'secid': '0.'+stock,
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'wbp2u': '|0|0|0|web',
            }
            res=requests.get(url=url,params=params)
            text=res.text
            text=res.json()['data']
            buy_5_price=text['f11']/1000
            data['buy_5_price']=buy_5_price
            buy_5_num=text['f12']
            data['buy_5_num']=buy_5_num
            buy_4_price=text['f13']/1000
            data['buy_4_price']=buy_4_price
            buy_4_num=text['f14']
            data['buy_4_num']=buy_4_num
            buy_3_price=text['f15']/1000
            data['buy_3_price']=buy_3_price
            buy_3_num=text['f16']
            data['buy_3_num']=buy_3_num
            buy_2_price=text['f17']/1000
            data['buy_2_price']=buy_2_price
            buy_2_num=text['f18']
            data['buy_2_num']=buy_2_num
            buy_1_price=text['f19']/1000
            data['buy_1_price']=buy_1_price
            buy_1_num=text['f20']
            data['buy_1_num']=buy_1_num
            sell_5_price=text['f31']/1000
            data['sell_5_price']=sell_5_price
            sell_5_num=text['f32']
            data['sell_5_num']=sell_5_num
            sell_4_price=text['f33']/1000
            data['sell_4_price']=sell_4_price
            sell_4_num=text['f34']
            data['sell_4_num']=sell_4_num
            sell_3_price=text['f35']/1000
            data['sell_3_price']=sell_3_price
            sell_3_num=text['f36']
            data['sell_3_num']=sell_3_num
            sell_2_price=text['f37']/100
            data['sell_2_price']=sell_2_price
            sell_2_num=text['f38']
            data['sell_2_num']=sell_2_num
            sell_1_price=text['f39']/1000
            data['sell_1_price']=sell_1_price
            sell_1_num=text['f40']
            data['sell_1_num']=sell_1_num
            data['最新价']=text['f43']/1000
            data['今开']=text['f46']/1000
            data['最高']=text['f44']/1000
            data['最低']=text['f45']/1000
            data['代码']=text['f57']
            data['名称']=text['f58']
            data['涨跌幅']=text['f169']/1000
            data['证券代码']=text['f262']
            data['股票名称']=text['f264']
            data['股票价格']=text['f267']/100
            data['股票涨跌幅']=text['f267']/100
            return data