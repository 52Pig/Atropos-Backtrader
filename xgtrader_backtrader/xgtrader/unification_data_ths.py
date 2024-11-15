#统一数据源

from .stock_data_ths import stock_data_ths
from .bond_cov_data_ths import bond_cov_data_ths
from .etf_fund_data_ths import etf_fund_data_ths
import yagmail
import json
class unification_data_ths:
    def __init__(self):
        '''
        统一数据源
        '''
        self.stock_data=stock_data_ths()
        self.bond_cov_data=bond_cov_data_ths()
        self.etf_fund_data=etf_fund_data_ths()
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
        if stock[-2:]=='SH' or stock[-2:]=='SZ':
            stock=stock
        else:
            if stock[:3] in ['600','601','603','688','510','511',
                             '512','513','515','113','110','128','123','127']:
                stock=stock+'.SH'
            else:
                stock=stock+'.SZ'
        return stock
    def get_hist_data_em(self,stock='600031.SH',start_date='20210105',end_date='20500101',data_type='D',limit=10000000):
        '''
        获取历史数据
         获取股票数据
        start_date=''默认上市时间
        - ``1`` : 分钟
            - ``5`` : 5 分钟
            - ``15`` : 15 分钟
            - ``30`` : 30 分钟
            - ``60`` : 60 分钟
            - ``101`` : 日
            - ``102`` : 周
            - ``103`` : 月
        fq=0股票除权
        fq=1前复权
        fq=2后复权
        '''
        stock=stock[:6]
        code_type=self.select_data_type(stock=stock)
        if code_type=='stock':
            df=self.stock_data.get_stock_hist_data_em(stock=stock,start_date=start_date,
                                                          end_date=end_date,data_type=data_type)
        elif code_type=='fund':
            df=self.etf_fund_data.get_ETF_fund_hist_data(stock=stock,end=end_date,
                                                             limit=limit,data_type=data_type)
        else:
            df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,end=end_date,
                                                             data_type=data_type,limit=1000000)
        return df
    def get_spot_data(self,stock='600031.SH'):
        '''
        获取实时数据
        '''
        stock=stock[:6]
        code_type=self.select_data_type(stock=stock)
        if code_type=='stock':
            df=self.stock_data.get_stock_spot_data(stock=stock)
        elif code_type=='fund':
            df=self.etf_fund_data.get_etf_fund_spot_data(stock=stock)
        else:
            df=self.bond_cov_data.get_cov_bond_spot(stock=stock)
        return df
    def get_spot_trader_data(self,stock='600031.SH'):
        '''
        获取实时交易数据3秒一次
        '''
        stock=stock[:6]
        code_type=self.select_data_type(stock=stock)
        if code_type=='stock':
            df=self.stock_data.get_stock_all_trader_data(stock=stock)
        elif code_type=='fund':
            df=self.etf_fund_data.get_etf_spot_trader_data(stock=stock)
        else:
            df=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        return df
    def seed_emial_qq(self,text='交易完成'):
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text1=json.loads(com)
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



        

        