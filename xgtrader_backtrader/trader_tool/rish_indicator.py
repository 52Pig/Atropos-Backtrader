import ffn
import empyrical
import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import numpy as np
import empyrical
import tkinter
import akshare as ak
from finta import TA
import mplfinance as mpf
import matplotlib
matplotlib.use('TkAgg')
plt.rcParams['font.family']='SimHei'
plt.rcParams['axes.unicode_minus']=False
stock=sg.popup_get_file('输入要计算证券代码比如sh600031')
start_date=sg.popup_get_file('输入数据开始时间比如20210105')
root=tkinter.Tk()
root.geometry('600x500')
root.title('股票财务指标计算')
menumode=tkinter.Menu(root)
ffn_ananysis=tkinter.Menu(menumode)
#上证指数数据,最为参考
df1=ak.stock_zh_a_daily(symbol='sh000001',start_date=start_date)
menumode.add_cascade(label='ffn股票财务指标计算',menu=ffn_ananysis)
df=ak.stock_zh_a_daily(symbol=stock,start_date=start_date)
print(df)
#简单回报率
def stock_to_return():
    result=ffn.core.to_returns(df['close'])
    print('股票简单回报率',result)
#计算长期福利汇报
def log_to_return():
    result=ffn.core.to_log_returns(df['close'])
    sg.popup(result)
    print('回报',result)
#价格指数
def price_index():
    result=ffn.core.to_price_index(df['close'])
    sg.popup(result)
    print('结果',result)
#统计分析数据
def cal_pref_stats():
    result=ffn.core.calc_stats(df['close'])
    print(result)
#计算最大回测
def calc_max_down():
    result=ffn.core.calc_max_drawdown(df['close'])
    sg.popup(result)
    print('结果',result)
#风险回报率
def calc_risk_returns_ratio():
    result=ffn.core.calc_risk_return_ratio(df['close'].pct_change())
    sg.popup(result)
    print('结果',result)
#夏普比例
def calc_shappe():
    result=ffn.core.calc_sharpe(df['close'].pct_change())
    sg.popup(result)
    print('结果',result)
#计算信息比率
def calc_information_ratio():
    #第一个位置为股票回报率，比2个位置为参考股票回报率
    result=ffn.core.calc_information_ratio(df['close'].pct_change(),df['open'].pct_change())
    sg.popup(result)
    print('结果',result)
#概念趋势，参考其他股票
def calc_preb_mom():
    result=ffn.core.calc_prob_mom(df['close'].pct_change(),df['open'].pct_change())
    sg.popup(result)
    print('结果',result)
#总回报率
def calc_total_returns():
    result=ffn.core.calc_total_return(df['close'])
    sg.popup(result)
    print('结果',result)
#删除数据重复数据
def drop_qqruib():
    result=ffn.core.drop_duplicate_cols(df)
    print(result)
#计算投资组合波动率权重
def calc_inv_vol_wei():
    result=ffn.core.calc_inv_vol_weights(df['close'].pct_change())
    print(result)
#品军方式权重
def calc_mean_var_weight():
    result=ffn.core.calc_mean_var_weights(df)
    print(result)
#计算收益率Kmean
def calc_Kmean():
    ressult=ffn.core.calc_ftca(df['close'].pct_change().tolist())
    print(ressult)
#年回报率
def year_retuns_ratio():
    #第一个为收益率，第二个为持有的天数
    result=ffn.core.annualize(df['close'].pct_change(),60)
    sg.popup(result)
    print('结果',result)
#利用年度表示回报
def year_deannualize():
    #第一个为收益率，第二个为持有的天数
    result=ffn.core.annualize(df['close'].pct_change(),60)
    sg.popup(result)
    print('结果',result)
#短期收益率
def cacl_sortion_returns():
    #第一个为收益率，第二个为无风险收益率，第三为周期
    result=ffn.core.calc_sortino_ratio(df['close'].pct_change(),rf=0,nperiods=None)
    sg.popup(result)
    print('结果',result)
#计算超额收益率
def cacl_excess_returns():
    ##第一个为收益率，第二个为无风险收益率，第三为周期
    result=ffn.core.to_excess_returns(df['close'].pct_change,float(0))
    sg.popup(result)
    print('结果',result)
#计算calmar等于收益比如最大回撤绝对值
def calc_calmar_ratio():
    result=ffn.core.calc_calmar_ratio(df['close'])
    sg.popup(result)
    print('结果',result)
ffn_ananysis.add_command(label='股票简单回报',command=stock_to_return)
ffn_ananysis.add_command(label='股票福利回报率',command=log_to_return)
ffn_ananysis.add_command(label='股票价格指数',command=price_index)
ffn_ananysis.add_command(label='股票统计分析',command=cal_pref_stats)
ffn_ananysis.add_command(label='股票最大回撤',command=calc_max_down)
ffn_ananysis.add_command(label='股票夏普比率',command=calc_shappe)
ffn_ananysis.add_command(label='股票风险回报率',command=calc_risk_returns_ratio)
ffn_ananysis.add_command(label='股票信息比利',command=calc_information_ratio)
ffn_ananysis.add_command(label='股票概念趋势',command=calc_preb_mom)
ffn_ananysis.add_command(label='股票总回报率',command=calc_total_returns)
ffn_ananysis.add_command(label='股票删除重复数据',command=drop_qqruib)
ffn_ananysis.add_command(label='股票投资者波动率比重',command=calc_inv_vol_wei)
ffn_ananysis.add_command(label='股票平均风险比重',command=calc_mean_var_weight)
ffn_ananysis.add_command(label='股票年回报率',command=year_retuns_ratio)
ffn_ananysis.add_command(label='股票年回报率转换',command=year_deannualize)
ffn_ananysis.add_command(label='股票短期回报率',command=cacl_sortion_returns)
ffn_ananysis.add_command(label='股票超额收益率',command=cacl_excess_returns)
ffn_ananysis.add_command(label='股票收益率比最大回测绝对值',command=calc_calmar_ratio)
#简单回报
empyrical_analysis=tkinter.Menu(menumode)
menumode.add_cascade(label='empyrical计算股票财务指标1',menu=empyrical_analysis)
def simple_returns():
    result=empyrical.simple_returns(df['close'])
    sg.popup(result)
    print('结果',result)
#累计回报
def cum_returns():
    result=empyrical.cum_returns(df['close'].pct_change())
    sg.popup(result)
    print('结果',result)
#累计最终回报
def cum_returns_final():
    result=empyrical.cum_returns_final(df['close'].pct_change())
    sg.popup(result)
    print('结果',result)
#转换回报率，比如转成Can be 'weekly', 'monthly', or 'yearly'.
def agg_returns():
    result=empyrical.aggregate_returns(df['close'].pct_change(),'weekly')
    sg.popup(result)
    print('结果',result)
#最大回测
def max_drawdown():
    result=empyrical.max_drawdown(df['close'].pct_change())
    print(result)
#滚动最大回撤
def roll_max_drawdown():
    #第二个参数为周期
    result=empyrical.roll_max_drawdown(df['close'].pct_change(),window=5)
    print(result)
#年回报率
def anaun_returns():
    result=empyrical.annual_return(df['close'].pct_change())
    print(result)
#复合年增长率
def year_grath_ratio():
    result=empyrical.cagr(df['close'].pct_change())
    print(result)
#年波动率
def anaual_vol():
    result=empyrical.annual_volatility(df['close'].pct_change())
    print(result)
#滚动年波动率
def roll_annual_vol():
    result=empyrical.roll_annual_volatility(df['close'].pct_change(),window=5)
    print(result)
#omega比例
def omega_ratio():
    result=empyrical.omega_ratio(df['close'].pct_change())
    print(result)
#夏普比例
def sharpe_ratio():
    result=empyrical.sharpe_ratio(df['close'].pct_change())
    print(result)
#短期比例
def sortion_ratio():
    result=empyrical.sortino_ratio(df['close'].pct_change())
    print(result)
#下行风险
def downsode_risk():
    result=empyrical.downside_risk(df['close'].pct_change())
    print(result)
#超额夏普比率
def excess_sharpe():
    result=empyrical.excess_sharpe(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算股票a和b
def alpha_beta():
    #第一个为计算股票，第二个为参考股票
    result=empyrical.alpha_beta(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算滚动的a和b
def roll_alpha_bate():
    result=empyrical.roll_alpha_beta(df['close'].pct_change(),df1['close'].pct_change(),window=5)
    print(result)
#计算年华a和b
def alpha_bate_year():
    result=empyrical.alpha_beta_aligned(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算股票a
def alpha():
    result=empyrical.alpha(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#年华aipha
def aipha_year():
    result=empyrical.alpha_aligned(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算股票beta
def beta():
    result=empyrical.beta(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算图片年化b
def beta_year():
    result=empyrical.beta_aligned(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算滚动b
def roll_bate():
    result=empyrical.roll_beta(df['close'].pct_change(),df1['close'].pct_change(),window=5)
    print(result)
empyrical_analysis.add_command(label='股票简单回报率',command=simple_returns)
empyrical_analysis.add_command(label='股票累计回报率',command=cum_returns)
empyrical_analysis.add_command(label='股票累计最终回报率',command=cum_returns_final)
empyrical_analysis.add_command(label='股票回报率转换',command=agg_returns)
empyrical_analysis.add_command(label='股票最大回测',command=max_drawdown)
empyrical_analysis.add_command(label='股票滚动最大回测',command=roll_max_drawdown)
empyrical_analysis.add_command(label='股票年回报率',command=anaun_returns)
empyrical_analysis.add_command(label='股票年增长率',command=year_grath_ratio)
empyrical_analysis.add_command(label='股票年波动率',command=anaual_vol)
empyrical_analysis.add_command(label='股票年滚动波动率',command=roll_max_drawdown)
empyrical_analysis.add_command(label='股票omega比率',command=omega_ratio)
empyrical_analysis.add_command(label='股票夏普比例',command=sharpe_ratio)
empyrical_analysis.add_command(label='股票短期比例',command=sortion_ratio)
empyrical_analysis.add_command(label='股票下行风险',command=downsode_risk)
empyrical_analysis.add_command(label='股票超额夏普比率',command=excess_sharpe)
empyrical_analysis.add_command(label='计算股票a和b',command=alpha_beta)
empyrical_analysis.add_command(label='计算股票滚动a和b',command=roll_alpha_bate)
empyrical_analysis.add_command(label='计算股票年化a和b',command=alpha_bate_year)
empyrical_analysis.add_command(label='计算股票a',command=alpha)
empyrical_analysis.add_command(label='计算股票年化a',command=alpha)
empyrical_analysis.add_command(label='计算股票b',command=beta)
empyrical_analysis.add_command(label='计算股票滚动b',command=roll_bate)
liner_analysis=tkinter.Menu(menumode)
menumode.add_cascade(label='empyrical线性分析',menu=liner_analysis)
#收益率log可决系数
def log_liner_r():
    result=empyrical.stability_of_timeseries(df['close'].pct_change())
    print(result)
#计算股票95%在险价值
def var_in():
    result=empyrical.tail_ratio(df['close'].pct_change())
    print(result)
#计算股票吸引比例
def capturn_ratio():
    result=empyrical.capture(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#b下降脆弱性
def b_down_heuristic():
    result=empyrical.beta_fragility_heuristic(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#股票b年化下降脆弱性
def b_down_heuristic_year():
    result=empyrical.beta_fragility_heuristic_aligned(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算股票在险价值和es
def var_and_es_values():
    result=empyrical.gpd_risk_estimates(df['close'].pct_change())
    print(result)
#计算股票股票年化在险价值和es
def var_and_es_values_year():
    result=empyrical.gpd_risk_estimates_aligned(df['close'].pct_change())
    print(result)
#计算参考回报为正捕获比例
def up_capturn():
    reesult=empyrical.up_capture(df['close'].pct_change(),df1['close'].pct_change())
    print(reesult)
#计算参考回报为正滚动捕获比例
def roll_up_capturn():
    reesult=empyrical.roll_up_capture(df['close'].pct_change(),df1['close'].pct_change(),window=5)
    print(reesult)
#计算参考回报为负捕获回报率
def down_capturn():
    result=empyrical.down_capture(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算参考回报为负滚动捕获回报率
def roll_down_capturn():
    result=empyrical.roll_down_capture(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算a和b在参考为正捕获比例
def a_and_b_up_capturn():
    reesult=empyrical.up_alpha_beta(df['close'].pct_change(),df1['close'].pct_change())
    print(reesult)
#计算a和b在参考为负捕获比例
def a_and_b_down_capturn():
    result=empyrical.down_alpha_beta(df['close'].pct_change(),df1['close'].pct_change())
    print(result)
#计算股票条件在险价值
def condition_var():
    result=empyrical.conditional_value_at_risk(df['close'].pct_change())
    print(result)
liner_analysis.add_command(label='股票收益率可决系数',command=log_to_return)
liner_analysis.add_command(label='计算股票95%在险价值',command=var_in)
liner_analysis.add_command(label='计算股票吸引力',command=capturn_ratio)
liner_analysis.add_command(label='计算股票b下降脆弱性',command=b_down_heuristic)
liner_analysis.add_command(label='计算股票b年化下降脆弱性',command=b_down_heuristic)
liner_analysis.add_command(label='计算股票在险价值和es',command=var_and_es_values)
liner_analysis.add_command(label='计算股票年化在险价值和es',command=var_and_es_values_year)
liner_analysis.add_command(label='计算股票参考回报率为正滚动捕获比例',command=roll_up_capturn)
liner_analysis.add_command(label='计算股票参考回报率为负捕获比例',command=down_capturn)
liner_analysis.add_command(label='计算股票参考回报率为负滚动捕获比例',command=roll_down_capturn)
liner_analysis.add_command(label='计算股票参考回报率为正a和b捕获比例',command=a_and_b_up_capturn)
liner_analysis.add_command(label='计算股票参考回报率为负a和b捕获比例',command=a_and_b_down_capturn)
liner_analysis.add_command(label='股票的条件在险价值',command=condition_var)
kliner_plot=tkinter.Menu(menumode)
menumode.add_cascade(label='绘制股票图',menu=kliner_plot)
#绘制股票图
def K_plot():
    df1=df
    macd=TA.MACD(df1)
    boll=TA.BBANDS(df1)
    rsi=TA.RSI(df1)
    df1.rename(columns={'date':'Date','open':'Open','close':'Close','high':'High','low':'Low','volume':'Volume'},inplace=True)
        #时间格式转换
    plt.rcParams['font.family']='SimHei'
    plt.rcParams['axes.unicode_minus']=False
    df1['Date']=pd.to_datetime(df1['Date'])
    #出现设置索引
    df1.set_index(['Date'],inplace=True)
    #设置股票颜
    mc=mpf.make_marketcolors(up='g',down='r',edge='i')
        #设置系统
    s=mpf.make_mpf_style(marketcolors=mc)
    add_plot=[mpf.make_addplot(macd['MACD'],panel=1,title='{}MACD'.format('股票'),color='r'),mpf.make_addplot(macd['SIGNAL'],panel=1,color='y'),
    mpf.make_addplot(rsi,panel=2,title='RSI'),
    mpf.make_addplot(boll['BB_UPPER'],panel=0,color='r',title='BOLL'),mpf.make_addplot(boll['BB_MIDDLE'],panel=0,color='m'),mpf.make_addplot(boll['BB_LOWER'],panel=0,color='g')]
        #绘制股票图，5，10，20日均线
    mpf.plot(df1,type='candle',style=s,mav=(5,10,20),addplot=add_plot)
    plt.show()
kliner_plot.add_command(label='股票图绘制',command=K_plot)
root['menu']=menumode
root.mainloop()



