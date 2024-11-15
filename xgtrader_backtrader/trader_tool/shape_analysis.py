#形态分析
#形态分析
from xgtrader.bond_cov_data_ths import bond_cov_data_ths
import pandas as pd
class shape_analysis:
    def __init__(self,df=''):
        self.data=df
    def get_over_lining_sell(self,n=5,q=0.75):
        '''
        上影线卖出
        '''
        try:
            df=self.data
            #收盘价
            last_price=df['close'].tolist()[-1]
            #最大值
            max_price=df['high'].tolist()[-1]
            #最小价
            min_price=df['low'].tolist()[-1]
            #开盘价
            open_price=df['open'].tolist()[-1]
            #实体长度，形态可以是阴线
            entity=abs(last_price-open_price)
            zdf=df['涨跌幅'].tolist()[-1]
            #上影线长度
            over_line_lenth=max_price-last_price
            #最近N天的分位数
            q_value=df['close'][-n:].quantile(q)
            #上线线大于实体3备，价格位于最近5天0.75分位数上,涨跌幅大于1
            if over_line_lenth>=3*entity and last_price>=q_value and abs(zdf)>=1:
                return '是'
            else:
                return '不是'
        except:
            return '不是'
    def get_down_mean_line_sell(self,n=10):
        '''
        跌破5日均线卖出
        '''
        try:
            df=self.data
            open_price=df['open'].tolist()[-1]
            close_price=df['close'].tolist()[-1]
            #实体
            entity=abs(close_price-open_price)
            df['{}均线'.format(n)]=df['close'].rolling(n).mean()
            line=df['{}均线'.format(n)].tolist()[-1]
            #向下跌破的实体
            down_entity=abs(line-close_price)
            if close_price<line:
                return '是'
            else:
                return '不是'
        except:
            return '是'
    def get_del_qzsh_cov_bond(self,):
        '''
        删除强制赎回可转债
        '''
        try:
            df=pd.read_excel(r'非强制赎回\非强制赎回.xlsx',dtype='object')
            stock_list=df['cell.bond_id'].tolist()
            if self.stock in stock_list:
                return '不是'
            else:
                return '是'
        except:
            return '不是'
