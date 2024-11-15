from trader_tool.unification_data import unification_data
from trader_tool.shape_analysis import shape_analysis
import pandas as pd
from tqdm import tqdm
class analysis_models:
    def __init__(self,trader_tool='qmt'):
        '''
        分析模型
        涨停板交易
        '''
        self.trader_tool=trader_tool
        data_models=unification_data(trader_tool=self.trader_tool)
        self.data=data_models.get_unification_data()
        self.shape_analysis=shape_analysis()
        self.fix_grid_log={} 
        self.dt_grid_log={}
    def select_bond_cov(self,x):
        '''
        选择证券代码
        '''
        if x[:3] in ['110','113','123','127','128','111'] or x[:2] in ['11','12']:
            return '是'
        else:
            return '不是'
    def mean_line_models(self,df):
        '''
        均线模型
        趋势模型
        5，10，20，30，60
        '''
        df=df
        #df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,start=start_date,end=end_date,limit=1000000000)
        df1=pd.DataFrame()
        df1['date']=df['date']
        df1['5']=df['close'].rolling(window=5).mean()
        df1['10']=df['close'].rolling(window=10).mean()
        df1['20']=df['close'].rolling(window=20).mean()
        df1['30']=df['close'].rolling(window=30).mean()
        df1['60']=df['close'].rolling(window=60).mean()
        score=0
        #加分的情况
        mean_5=df1['5'].tolist()[-1]
        mean_10=df1['10'].tolist()[-1]
        mean_20=df1['20'].tolist()[-1]
        mean_30=df1['30'].tolist()[-1]
        mean_60=df1['60'].tolist()[-1]
        #相邻2个均线进行比较
        if mean_5>mean_10:
            score+=25
        if mean_10>mean_20:
            score+=25
        if mean_20>mean_30:
            score+=25
        if mean_30>mean_60:
            score+=25
        return score
    def get_return_ananlysis(self,df='',n=5):
        '''
        收益率分析
        '''
        #涨跌幅
        df1=df
        prices=df1[-n:]['close']
        zdf= ((prices.iloc[-1] / prices.iloc[0]) - 1)*100
        #最大回撤
        max_down_result=((prices / prices.expanding(min_periods=1).max()).min() - 1)*100
        #累计收益】
        return zdf,max_down_result
    def cacal_zig_data(self,stock='123018',x=0.005):
        '''
        计算之字转向
        x=5%之子转向
        :return:
        '''
        ZIG_STATE_START = 0
        ZIG_STATE_RISE = 1
        ZIG_STATE_FALL = 2
        df=self.data.get_spot_data(stock=stock)
        df['价格']=df['价格'].astype(float)
        # print(list(df["close"]))
        df = df[::-1]
        df = df.reset_index(drop=True)
        # df = df.iloc[-100:]
        x = x
        k = df["价格"]
        d = df["时间"]
        peer_i = 0
        candidate_i = None
        scan_i = 0
        peers = [0]
        z = np.zeros(len(k))
        state = ZIG_STATE_START
        while True:
            scan_i += 1
            if scan_i == len(k) - 1:
                # 扫描到尾部
                if candidate_i is None:
                    peer_i = scan_i
                    peers.append(peer_i)
                else:
                    if state == ZIG_STATE_RISE:
                        if k[scan_i] >= k[candidate_i]:
                            peer_i = scan_i
                            peers.append(peer_i)
                        else:
                            peer_i = candidate_i
                            peers.append(peer_i)
                            peer_i = scan_i
                            peers.append(peer_i)
                    elif state == ZIG_STATE_FALL:
                        if k[scan_i] <= k[candidate_i]:
                            peer_i = scan_i
                            peers.append(peer_i)
                        else:
                            peer_i = candidate_i
                            peers.append(peer_i)
                            peer_i = scan_i
                            peers.append(peer_i)
                break
            if state == ZIG_STATE_START:
                if k[scan_i] >= k[peer_i] * (1 + x):
                    candidate_i = scan_i
                    state = ZIG_STATE_RISE
                elif k[scan_i] <= k[peer_i] * (1 - x):
                    candidate_i = scan_i
                    state = ZIG_STATE_FALL
            elif state == ZIG_STATE_RISE:
                if k[scan_i] >= k[candidate_i]:
                    candidate_i = scan_i
                elif k[scan_i] <= k[candidate_i] * (1 - x):
                    peer_i = candidate_i
                    peers.append(peer_i)
                    state = ZIG_STATE_FALL
                    candidate_i = scan_i
            elif state == ZIG_STATE_FALL:
                if k[scan_i] <= k[candidate_i]:
                    candidate_i = scan_i
                elif k[scan_i] >= k[candidate_i] * (1 + x):
                    peer_i = candidate_i
                    peers.append(peer_i)
                    state = ZIG_STATE_RISE
                    candidate_i = scan_i
        for i in range(len(peers) - 1):
            peer_start_i = peers[i]
            peer_end_i = peers[i + 1]
            start_value = k[peer_start_i]
            end_value = k[peer_end_i]
            a = (end_value - start_value) / (peer_end_i - peer_start_i)  # 斜率
            for j in range(peer_end_i - peer_start_i + 1):
                z[j + peer_start_i] = start_value + a * j
        df['结果']=z
        #前天
        line_1=df['结果'].shift(2)
        #昨天
        line_2=df['结果'].shift(1)
        #今天
        line_3=df['结果'].shift(0)
        result=[]
        for x,y,z in zip(line_1,line_2,line_3):
            if x<y and y>z:
                result.append('sell')
            elif x>y and y<z:
                result.append('buy')
            else:
                result.append(None)
        df['买卖点']=result
        df1=df.sort_index(ascending=False,ignore_index=True)
        return df1
    def get_mean_line_trader_analysis(self,stock='128036',window=30):
        '''
        均线交易分析模型，
        数据为3秒一次
        60 3分钟
        '''
        import numpy as np
        df=self.data.get_hist_data_em(stock=stock,data_type='1')
        df['close']=df['close'].astype(float)
        df['mean_5']=df['close'].rolling(5).mean()
        x1=df['mean_1'].shift(2)
        x2=df['mean_1'].shift(1)
        x3=df['mean_1'].shift(0)
        df['买点']=np.logical_and(x1<x2,x3>x2)
        df['卖点']=np.logical_and(x1>x2,x3<x2)
        print(df[df['买点']==True])
        buy_spot=df['买点'].tolist()[-1]
        sell_spot=df['卖点'].tolist()[-1]
        if buy_spot==True:
            return 'buy'
        elif sell_spot==True:
            return 'sell'
        else:
            return False
    def get_macd_trader_analysis(self,stock='111007'):
        '''
        macd
        '''
        pass
    def get_mi_pulse_trader_analysis(self,n=10,x1=1,x2=-2,stock='111007',select='是',h='9',mi='3300',num=1.5):
        '''
        分钟脉冲分析     
        '''
        df=self.data.get_spot_trader_data(stock=stock)
        n=20*n
        zdf_list=df['涨跌幅'].tolist()[-n:]
        zdf=zdf_list[-1]-zdf_list[1]
        print(stock,zdf)
        if zdf>=x1:
            return 'sell'
        elif zdf<=x2:
            return 'buy'
        else:
            return False
    def get_dynamic_trader_analysis(self,daily=5,mi=10,x=0.3,x1=-0.3,stock='128041'):
        '''
        动态分钟脉冲
        '''
        df=self.data.get_hist_data_em(stock=stock,data_type='D')
        df['平均振幅']=df['振幅'].rolling(daily).mean()
        zdf=df['平均振幅'].tolist()[-1]
        zdf=abs(zdf)
        #实时交易数据
        df1=self.data.get_spot_trader_data(stock=stock)
        n=20*mi
        zdf_list=df1['涨跌幅'].tolist()[-n:]
        spot_zdf=zdf_list[-1]-zdf_list[0]
        if spot_zdf>=0:
            sell_zdf=zdf*x
            if spot_zdf>sell_zdf:
                return 'sell'
            else:
                return False
        elif spot_zdf<0:
            buy_zdf=zdf*x1
            if spot_zdf<=buy_zdf:
                return 'buy'
            else:
                return False
        else:
            return False
    def get_hour_pulse_trader_analysis(self,hour=1,x1=5,x2=-3,stock=''):
        '''
        小时趋势
        '''
        df=self.data.get_hist_data_em(stock=stock,data_type='1')
        df['累计涨跌幅']=df['涨跌幅'].cumsum()
        zdf_list=df['累计涨跌幅'].tolist()[-hour:]
        zdf=zdf_list[-1]-zdf_list[0]
        if zdf>=x1:
            return 'sell'
        elif zdf<=x2:
            return 'buy'
        else:
            return False
    def surge_and_fall_overfall_rebound(self,stock='123018',min_return=7,max_down=-1,max_df=-5,ft_return=3):
        '''
        冲高回落--超跌反弹
        min_return冲高的涨跌幅
        max_down最大的回撤
        #超跌反弹
        max_df最大跌幅
        ft_return反弹收益
        '''
        df=self.data.get_spot_trader_data(stock=stock)
        #最大涨跌幅
        max_return_ratio=max(df['涨跌幅'].tolist())
        #现在的涨跌幅
        now_return_ratio=df['涨跌幅'].tolist()[-1]
        #目前的收益回撤
        max_down_ratio=now_return_ratio-max_return_ratio
        if max_return_ratio>min_return and max_down_ratio<=max_down:
            text='冲高回落，股票{} 最大涨跌幅{} 现在的涨跌幅{} 收益回撤{}'.format(stock,max_return_ratio,now_return_ratio,max_down_ratio)
            return '冲高回落',True,text
        #最小涨跌幅
        min_return_ratio=min(df['涨跌幅'].tolist())
        #反弹收益
        ft_return_ratio=now_return_ratio-min_return_ratio
        if min_return_ratio<max_df and ft_return_ratio >ft_return:
            text='超跌反弹，股票{} 最大跌幅{} 现在的涨跌幅{} 收益反弹{}'.format(stock, min_return_ratio,now_return_ratio,ft_return_ratio)
            return '超跌反弹',True,text
        else:
            text='不符合超跌反弹，股票{} 最大跌幅{} 现在的涨跌幅{} 收益反弹{}'.format(stock, min_return_ratio,now_return_ratio,ft_return_ratio)
            return "超跌反弹",False,text
    def get_trader_mean_line_analysis(self,stock='128041',n=5,mean_line=20):
        '''
        盘中参考均线分析
        '''
        df=self.data.get_hist_data_em(stock=stock,data_type='5',limit=100000000)
        df['mean_line']=df['close'].rolling(mean_line).mean()
        open_price=df['open'].tolist()[-1]
        close_price=df['close'].tolist()[-1]
        mean_price=df['mean_line'].tolist()[-1]
        if open_price <mean_price and close_price>mean_price:
            return 'buy'
        elif open_price>mean_price and close_price<mean_price:
            return 'sell'
        else:
            return False
    def get_rising_speed_analysis(self,n=5,stock='110070'):
        '''
        涨速分析
        '''
        df=self.data.get_spot_trader_data(stock=stock)
        df['实时涨跌幅'][-200:].plot()
    def get_creat_fix_grid(self,stock='600031',open_price=16,now_pice=17,n=8,entiy=0.01,auto_adjust=True):
        '''
        生成网格交易 固定网格利用价格来计算
        从上到下一次为1，2，3，4，5网格
        中间开盘价未中间0分界线
        open_pric开盘价
        now_price现在价
        n网格数量
        entiy单元格大小，涨跌幅
        auto_adjust 自动调整 价格突破最大网格边界自动添加一个格子
        '''
        #df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock)
        all_stock=list(self.fix_grid_log.keys())
        if stock in all_stock:
            data_dict=self.fix_grid_log[stock]
            for i in range(1,int(n/2)+1):
                data_dict['{}'.format(i)]=open_price+open_price*entiy*(abs((i-1)-int(n/2)))
            for i in range(int(n/2)+1,n+1):
                data_dict['{}'.format(i)]=open_price-open_price*entiy*(abs((i-1)-int(n/2)))
            value_list=[]
            keys_list=[str(i) for i in range(1,n+1)]
            if now_pice>data_dict['1']:
                if auto_adjust==True:
                    entiy=((now_pice-open_price)/n)*2
                    for i in range(1,n+1):
                        values=now_pice-entiy*i
                        value_list.append(values)
                        data_dict=dict(zip(keys_list,value_list))
                        index='1'
                        self.fix_grid_log[stock]=data_dict
                else:
                    index='up'
            elif now_pice<data_dict[str(n)]:
                if auto_adjust==True:
                    entiy=((now_pice-open_price)/n)*2
                    for i in range(1,n+1):
                        values=now_pice-entiy*i
                        value_list.append(values)
                        data_dict=dict(zip(keys_list,value_list[::-1]))
                        index=str(n)
                        self.grid_log[stock]=data_dict
                else:
                    index='down'
            else:
                for j in range(1,n):
                    if now_pice<=data_dict[str(j)] and now_pice>=data_dict[str(j+1)]:
                        index=j
                        break
                    else:
                        index=0
        else:
            data_dict={}
            for i in range(1,int(n/2)+1):
                data_dict['{}'.format(i)]=open_price+open_price*entiy*(abs((i-1)-int(n/2)))
            for i in range(int(n/2)+1,n+1):
                data_dict['{}'.format(i)]=open_price-open_price*entiy*(abs((i-1)-int(n/2)))
            value_list=[]
            keys_list=[str(i) for i in range(1,n+1)]
            if now_pice>data_dict['1']:
                if auto_adjust==True:
                    entiy=((now_pice-open_price)/n)*2
                    for i in range(1,n+1):
                        values=now_pice-entiy*i
                        value_list.append(values)
                        data_dict=dict(zip(keys_list,value_list))
                        index='1'
                        self.fix_grid_log[stock]=data_dict
                else:
                    index='up'
            elif now_pice<data_dict[str(n)]:
                if auto_adjust==True:
                    entiy=((now_pice-open_price)/n)*2
                    for i in range(1,n+1):
                        values=now_pice-entiy*i
                        value_list.append(values)
                        data_dict=dict(zip(keys_list,value_list[::-1]))
                        index=str(n)
                        self.fix_grid_loggrid_log[stock]=data_dict
                else:
                    index='down'
            else:
                for j in range(1,n):
                    if now_pice<=data_dict[str(j)] and now_pice>=data_dict[str(j+1)]:
                        index=j
                        break
                    else:
                        index=0
        return data_dict,entiy,index
    def get_fix_grid_analysis(self,stock='110074',n=8,entiy=0.01,time_size=600,buy_sell_dot=0.75,
        stop=True,stop_line=-0.03,auto_adjust=True):
        '''
        固定网格分析
        '''
        from datetime import datetime
        now_time=datetime.now()
        open_price=self.data.get_spot_data(stock=stock)['昨收']
        df=self.data.get_spot_trader_data(stock=stock)
        price_list=df['价格'].tolist()[-time_size:]
        pre_price=price_list[0]
        now_price=price_list[-1]
        if now_price<=open_price*(1+stop_line) and stop==True:
            text='{} {} 现在的涨跌幅 {}达到止损线全部卖出'.format(now_time,stock,now_price)
            return 'sell',text
        else:
            #前面涨跌幅在的格子
            pre_dict,entiy,pre_index=self.get_creat_fix_grid(stock=stock,open_price=open_price,now_pice=pre_price,n=n,entiy=entiy,auto_adjust=auto_adjust)
            now_dict,entiy,now_index=self.get_creat_fix_grid(stock=stock,open_price=open_price,now_pice=now_price,n=n,entiy=entiy,auto_adjust=auto_adjust)
            if now_index in ['up'] and now_price>=pre_dict[str(1)]+pre_price*(entiy*buy_sell_dot):
                text='固定网格卖出 时间{} 可转债{} 突破上边线而且达到{}分位数'.format(now_time,stock,buy_sell_dot)
                return 'sell',text
            elif now_index=='down' or pre_index=='down':
                text='固定网格卖出 时间{} {}跌破下边线'.format(now_time,stock)
                return 'sell',text
            elif now_index in ['up'] or pre_index=='up':
                text='固定网格卖出 时间{} {}突破上边线'.format(now_time,stock)
                return 'sell',text
            #向上多单元格跳动，比如从3单元格直接跳动到1 单元格
            elif (int(pre_index)-int(now_index))>=2:
                text='固定网格卖出 向上多单元格跳动 {} {} 从{}单元格跳到{}单元格'.format(now_time,stock,pre_index,now_index)
                return 'sell',text
            #向下多单元格跳动，比如从1单元格直接跳动到3 单元格
            elif (int(pre_index)-int(now_index))<=-2:
                text='固定网格买入 向下多单元格跳动 {} {} 从{}单元格跳到{}单元格'.format(now_time,stock,pre_index,now_index)
                return 'buy',text
            #一个一个单元格跳动
            #在同一个单元格不操作
            elif int(now_index)==int(pre_index):
                text='{} 可转债{} 现在的价格{} 在同一个网格布交易 目前的网格{}'.format(now_time,stock,now_price,now_index)
                return False,text
            else:
                #买入的操作
                #可转债从上一个格子进入下一个格子同时现在的涨跌幅在新格子的1-buy_sell_dot的分位数位置
                if int(pre_index) <int(now_index):
                    if now_price<=pre_dict[str(now_index)]-pre_price*(entiy*buy_sell_dot):
                        text='固定网格买入 {} {} 从{}单元格跌到{}单元格 达到{}单元格的{}位置'.format(now_time,
                        stock,pre_index,now_index,now_index,buy_sell_dot)
                        return 'buy',text
                    else:
                        text='{} {} 从{}单元格跌到{}单元格目前没有达到{}买入点'.format(now_time,
                        stock,pre_index,now_index,buy_sell_dot)
                        return False,text
                #卖出操作
                elif int(pre_index) >int(now_index):
                    if now_price>=pre_dict[str(pre_index)]+pre_price*(entiy*buy_sell_dot):
                        text='固定网格卖出 {} {} 从{}单元格上涨{}单元格 达到{}单元格 的{}位置'.format(now_time,
                        stock,pre_index,now_index,now_index,buy_sell_dot)
                        return 'sell',text
                    else:
                        text='固定网格{} {} 从{}单元格上涨{}单元格目前没有达到{}卖出点'.format(now_time,
                        stock,pre_index,now_index,buy_sell_dot)
                        return False,text 
                else:
                    return False,0   
    def get_creat_cov_bond_grid(self,stock='',df='',daily=5,n=6,entiy_select=0.5,bs=2,spot_zdf=2,auto_adjust=True):
        '''
        生成动态网格交易利用涨跌幅
        从上到下一次为1，2，3，4，5网格
        daily最近5天
        entiy_select单元格大小涨跌幅
        bs单元格增强倍数
        spot_zdf止损涨跌幅
        auto_adjust 自动调整 价格突破最大网格边界自动添加一个格子
        '''
        #df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock)
        all_stock=list(self.dt_grid_log.keys())
        if stock in all_stock:
            data_dict=self.fix_grid_log[stock]
            df=df
            #因为数据是实时数据，剔除今天的数据
            df1=df[-daily+1:-1]
            mean_zf=df1['振幅'].mean()
            #单元格
            entiy=mean_zf/n
            if float(entiy)<=float(entiy_select):
                entiy=entiy*bs
            else:
                entiy=entiy
            data_dict={}
            for i in range(1,int(n/2)+1):
                data_dict['{}'.format(i)]=entiy*(abs((i-1)-int(n/2)))
            for i in range(int(n/2)+1,n+1):
                data_dict['{}'.format(i)]=entiy*(int(n/2)-i)
            value_list=[]
            keys_list=[str(i) for i in range(1,n+1)]
            if spot_zdf>data_dict['1']:
                if auto_adjust==True:
                    df1=df[-daily:]
                    mean_zf=df1['振幅'].mean()
                    if float(entiy)<=float(entiy_select):
                        entiy=entiy*bs
                    else:
                        entiy=entiy
                    #单元格
                    entiy=mean_zf/n
                    for i in range(1,n+1):
                        values=spot_zdf-entiy*i
                        value_list.append(values)
                        data_dict=dict(zip(keys_list,value_list))
                        index='1'
                        self.dt_grid_log[stock]=data_dict
                else:
                    index='up'
            elif spot_zdf<data_dict[str(n)]:
                if auto_adjust==True:
                    df1=df[-daily:]
                    mean_zf=df1['振幅'].mean()
                    if float(entiy)<=float(entiy_select):
                        entiy=entiy*bs
                    else:
                        entiy=entiy
                    #单元格
                    entiy=mean_zf/n
                    for i in range(1,n+1):
                        values=spot_zdf+entiy*i
                        value_list.append(values)
                        data_dict=dict(zip(keys_list,value_list[::-1]))
                        index=str(n)
                        self.dt_grid_log[stock]=data_dict
                else:
                    index='down'
            else: 
                for j in range(1,n):
                    if spot_zdf<=data_dict[str(j)] and spot_zdf>=data_dict[str(j+1)]:
                        index=j
                        break
                    else:
                        index=0
            return data_dict,entiy,index
        else:
            df=df
            #因为数据是实时数据，剔除今天的数据
            df1=df[-daily+1:-1]
            mean_zf=df1['振幅'].mean()
            #单元格
            entiy=mean_zf/n
            if float(entiy)<=float(entiy_select):
                entiy=entiy*bs
            else:
                entiy=entiy
            data_dict={}
            for i in range(1,int(n/2)+1):
                data_dict['{}'.format(i)]=entiy*(abs((i-1)-int(n/2)))
            for i in range(int(n/2)+1,n+1):
                data_dict['{}'.format(i)]=entiy*(int(n/2)-i)
            value_list=[]
            keys_list=[str(i) for i in range(1,n+1)]
            if spot_zdf>data_dict['1']:
                if auto_adjust==True:
                    df1=df[-daily:]
                    mean_zf=df1['振幅'].mean()
                    if float(entiy)<=float(entiy_select):
                        entiy=entiy*bs
                    else:
                        entiy=entiy
                    #单元格
                    entiy=mean_zf/n
                    for i in range(1,n+1):
                        values=spot_zdf-entiy*i
                        value_list.append(values)
                        data_dict=dict(zip(keys_list,value_list))
                        index='1'
                        self.dt_grid_log[stock]=data_dict
                else:
                    index='up'
            elif spot_zdf<data_dict[str(n)]:
                if auto_adjust==True:
                    df1=df[-daily:]
                    mean_zf=df1['振幅'].mean()
                    if float(entiy)<=float(entiy_select):
                        entiy=entiy*bs
                    else:
                        entiy=entiy
                    #单元格
                    entiy=mean_zf/n
                    for i in range(1,n+1):
                        values=spot_zdf+entiy*i
                        value_list.append(values)
                        data_dict=dict(zip(keys_list,value_list[::-1]))
                        index=str(n)
                        self.dt_grid_log[stock]=data_dict
                else:
                    index='down'
            else: 
                for j in range(1,n):
                    if spot_zdf<=data_dict[str(j)] and spot_zdf>=data_dict[str(j+1)]:
                        index=j
                        break
                    else:
                        index=0
            return data_dict,entiy,index
    def get_grid_analysis(self,stock='110074',daily=5,n=6,time_size=600,buy_sell_dot=0.75,
    stop=True,stop_line=-3,entiy_select='0.5',bs=2,auto_adjust=True):
        '''
        网格分析数据3秒一次数据
        daily最近N天，振幅为平均值为上下网格
        n网格线多少
        time_size时间窗口 20是一分钟
        buy_sell_dot 到到目标网格的分位数
        stop开启网格止损
        stop_line=-3止损线
        '''
        from datetime import datetime
        now_time=datetime.now()
        hist_df=self.data.get_hist_data_em(stock=stock)
        df=self.data.get_spot_trader_data(stock=stock)
        #print(df)
        zdf_list=df['涨跌幅'].tolist()[-time_size:]
        #前N分钟的涨跌幅
        pre_zdf=zdf_list[0]
        #现在的涨跌幅
        now_zdf=zdf_list[-1]
        if now_zdf<=stop_line and stop==True:
            text='{} {} 现在的涨跌幅 {}达到止损线全部卖出'.format(now_time,stock,now_zdf)
            return 'sell',text
        else:
            #前面涨跌幅在的格子
            pre_dict,entiy,pre_index=self.get_creat_cov_bond_grid(stock=stock,daily=daily,n=n,df=hist_df,spot_zdf=pre_zdf,entiy_select=entiy_select,bs=bs,auto_adjust=auto_adjust)
            #现在涨跌幅在的格子
            now_dict,entiy,now_index=self.get_creat_cov_bond_grid(stock=stock,daily=daily,n=n,df=hist_df,spot_zdf=now_zdf,entiy_select=entiy_select,bs=bs,auto_adjust=auto_adjust)
            print(pre_dict,entiy,pre_index)
            print(now_dict,entiy,now_index)
            #现在的可转债涨跌幅大于上边线自动添加一个卖出网格
            if now_index in ['up'] and now_zdf>=pre_dict[str(1)]+(entiy*buy_sell_dot):
                text='卖出 时间{} 可转债{} 突破上边线而且达到{}分位数'.format(now_time,stock,buy_sell_dot)
                return 'sell',text
            elif now_index=='down' or pre_index=='down':
                text='卖出 时间{} 控制住{}跌破下边线'.format(now_time,stock)
                return 'sell',text
            elif now_index in ['up'] or pre_index=='up':
                text='卖出 时间{} 可转债{}突破上边线'.format(now_time,stock)
                return 'sell',text
            #向上多单元格跳动，比如从3单元格直接跳动到1 单元格
            elif (int(pre_index)-int(now_index))>=2:
                text='卖出 向上多单元格跳动 {} {} 从{}单元格跳到{}单元格'.format(now_time,stock,pre_index,now_index)
                return 'sell',text
            #向下多单元格跳动，比如从1单元格直接跳动到3 单元格
            elif (int(pre_index)-int(now_index))<=-2:
                text='买入 向下多单元格跳动 {} {} 从{}单元格跳到{}单元格'.format(now_time,stock,pre_index,now_index)
                return 'buy',text
            #一个一个单元格跳动
            #在同一个单元格不操作
            elif int(now_index)==int(pre_index):
                text='{} {} 现在的涨跌幅{} 在同一个网格布交易 目前的网格{}'.format(now_time,stock,now_zdf,now_index)
                return False,text
            else:
                #买入的操作
                #可转债从上一个格子进入下一个格子同时现在的涨跌幅在新格子的1-buy_sell_dot的分位数位置
                if int(pre_index) <int(now_index):
                    if now_zdf<=pre_dict[str(now_index)]-(entiy*buy_sell_dot):
                        text='买入 {} {} 从{}单元格跌到{}单元格 达到{}单元格的{}位置'.format(now_time,
                        stock,pre_index,now_index,now_index,buy_sell_dot)
                        return 'buy',text
                    else:
                        text='{} {} 从{}单元格跌到{}单元格目前没有达到{}买入点'.format(now_time,
                        stock,pre_index,now_index,buy_sell_dot)
                        return False,text
                #卖出操作
                elif int(pre_index) >int(now_index):
                    if now_zdf>=pre_dict[str(pre_index)]+(entiy*buy_sell_dot):
                        text='卖出 {} {} 从{}单元格上涨{}单元格 达到{}单元格 的{}位置'.format(now_time,
                        stock,pre_index,now_index,now_index,buy_sell_dot)
                        return 'sell',text
                    else:
                        text='{} {} 从{}单元格上涨{}单元格目前没有达到{}卖出点'.format(now_time,
                        stock,pre_index,now_index,buy_sell_dot)
                        return False,text 
                else:
                    return False,0   
    def get_return_ananlysis(self,df='',n=5):
        '''
        收益率分析
        '''
        #涨跌幅
        df1=df
        prices=df1[-n:]['close']
        zdf= ((prices.iloc[-1] / prices.iloc[0]) - 1)*100
        #最大回撤
        max_down_result=((prices / prices.expanding(min_periods=1).max()).min() - 1)*100
        #累计收益】
        return zdf,max_down_result
    def get_shape_analysis(self,df=''):
        '''
        形态分析
        df分析的表格
        stock_list
        '''
        print('可转债形态分析')
        df=df
        try:
            del df['Unnamed: 0']
        except:
            pass
        stock_list=df['证券代码'].tolist()
        over_lining=[]
        mean_line=[]
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            try:
                hist_df=self.data.get_hist_data_em(stock=stock)
                models=shape_analysis(df=hist_df)
                over=models.get_over_lining_sell()
                over_lining.append(over)
                #均线分析
                line=models.get_down_mean_line_sell()
                mean_line.append(line)
            except:
                over_lining.append(None)
                mean_line.append(None)
        df['上影线']=over_lining
        df['跌破均线']=mean_line
        df1=df[df['上影线']=='不是']
        df1=df1[df1['跌破均线']=='不是']
        return df1
    def get_stock_mean_line_retuen_analysis(self,df='',n=5,max_retuen=5,min_return=1,max_down=8):
        '''
        收益分析
        n=最近N天
        max_retuen=最近N天最大收益率
        min_return最近N天最小收益率
        max_down 最近N天最大回撤
        '''
        print('收益分析')
        n=n
        max_retuen=max_retuen
        min_return=min_return
        max_down=max_down
        zdf_list=[]
        max_down_list=[]
        df=df
        try:
            df['Unnamed: 0']
        except:
            pass
        stock_list=df['证券代码'].tolist()
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            try:
                df1=self.data.get_hist_data_em(stock=stock,start_date='19990101',end_date='20500101',limit=1000000)
                sorce=self.mean_line_models(df=df1)
                zdf,down=self.get_return_ananlysis(df=df1,n=n)
                zdf_list.append(zdf)
                max_down_list.append(down)
            except:
                print('收益分析{}计算失败'.format(stock))
                zdf_list.append(None)
                max_down_list.append(None)
        df['最近{}天收益'.format(n)]=zdf_list
        df['最近天{}最大回撤'.format(n)]=max_down_list
        df1=df
        #df.to_excel(r'分析原始数据\分析原始数据.xlsx')
        df2=df1[df1['最近{}天收益'.format(n)]>=min_return]
        df3=df2[df2['最近{}天收益'.format(n)]<=max_retuen]
        df4=df3[df3['最近天{}最大回撤'.format(n)]>=max_down]
        return df4
    