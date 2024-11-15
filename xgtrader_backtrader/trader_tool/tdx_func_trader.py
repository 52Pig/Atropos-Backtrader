import pandas as pd
from xgtrader.unification_data_ths import unification_data_ths
import json
from xgtrader.etf_fund_data_ths import etf_fund_data_ths
from xgtrader.bond_cov_data_ths import bond_cov_data_ths
from xgtrader.stock_data_ths import stock_data_ths
from trader_tool.unification_data import unification_data
from trader_tool.tdx_indicator import *
tdx_func_1="""
M_A:=MA(C,144);
M_B:=MA(C,320);
妖:COUNT(CROSS(M5,M10),3)=1 AND COUNT(CROSS(M10,M20),5)=1 AND C>M_A AND CROSS(C,M_A) AND M_A<M_B;
"""
class tdx_func_trader:
    def __init__(self,trader_tool='ths',data_type='D',stock_list=['600031']):
        '''
        trader_tool交易系统ths/qmt
        data_type数据类型
        stock_list股票列表
        '''
        self.trader_tool=trader_tool
        self.data=unification_data(trader_tool=self.trader_tool)
        self.data=self.data.get_unification_data()
        self.etf_fund_data_ths=etf_fund_data_ths()
        self.bond_cov_data_ths=bond_cov_data_ths()
        self.stock_data_ths=stock_data_ths()
    
    def get_analysis_tdx_func(self):
        '''
        分析通达信函数
        '''
        
       
        params_data()

a=tdx_func_trader()
print(a.get_analysis_tdx_func())


        