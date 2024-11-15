import pandas as pd
from tqdm import tqdm
import numpy as np
import json
from .unification_data import unification_data
import os
import pandas as pd
from datetime import datetime
from .tdx_indicator import *
class tdx_trader_function:
    '''
    通达信交易函数
    '''
    def __init__(self,trader_tool='ths'):
        self.trader_tool=trader_tool
        self.data=unification_data(trader_tool=self.trader_tool)
        #self.data=self.data.get_unification_data()
    def six_pulse_excalibur(self,df):
        '''
        六脉神剑
        DIFF赋值:收盘价的8日指数移动平均-收盘价的13日指数移动平均
        DEA赋值:DIFF的5日指数移动平均
        当满足条件DIFF>DEA时,在1位置画1号图标
        当满足条件DIFF<DEA时,在1位置画2号图标
        当满足条件是否最后一个周期=1时,在1位置书写文字,COLORFFFFFF
        ABC1赋值:DIFF>DEA
        尊重市场1赋值:(收盘价-8日内最低价的最低值)/(8日内最高价的最高值-8日内最低价的最低值)*100
        K赋值:尊重市场1的3日[1日权重]移动平均
        D赋值:K的3日[1日权重]移动平均
        当满足条件K>D时,在2位置画1号图标
        当满足条件K<D时,在2位置画2号图标
        当满足条件是否最后一个周期=1时,在2位置书写文字,COLORFFFFFF
        ABC2赋值:K>D
        指标营地赋值:1日前的收盘价
        RSI1赋值:(收盘价-指标营地和0的较大值的5日[1日权重]移动平均)/(收盘价-指标营地的绝对值的5日[1日权重]移动平均)*100
        RSI2赋值:(收盘价-指标营地和0的较大值的13日[1日权重]移动平均)/(收盘价-指标营地的绝对值的13日[1日权重]移动平均)*100
        当满足条件RSI1>RSI2时,在3位置画1号图标
        当满足条件RSI1<RSI2时,在3位置画2号图标
        当满足条件是否最后一个周期=1时,在3位置书写文字,COLORFFFFFF
        ABC3赋值:RSI1>RSI2
        尊重市场赋值:-(13日内最高价的最高值-收盘价)/(13日内最高价的最高值-13日内最低价的最低值)*100
        LWR1赋值:尊重市场的3日[1日权重]移动平均
        LWR2赋值:LWR1的3日[1日权重]移动平均
        当满足条件LWR1>LWR2时,在4位置画1号图标
        当满足条件LWR1<LWR2时,在4位置画2号图标
        当满足条件是否最后一个周期=1时,在4位置书写文字,COLORFFFFFF
        ABC4赋值:LWR1>LWR2
        BBI赋值:(收盘价的3日简单移动平均+收盘价的5日简单移动平均+收盘价的8日简单移动平均+收盘价的13日简单移动平均)/4
        当满足条件收盘价>BBI时,在5位置画1号图标
        当满足条件收盘价<BBI时,在5位置画2号图标
        当满足条件是否最后一个周期=1时,在5位置书写文字,COLORFFFFFF
        ABC10赋值:7
        ABC5赋值:收盘价>BBI
        MTM赋值:收盘价-1日前的收盘价
        MMS赋值:100*MTM的5日指数移动平均的3日指数移动平均/MTM的绝对值的5日指数移动平均的3日指数移动平均
        MMM赋值:100*MTM的13日指数移动平均的8日指数移动平均/MTM的绝对值的13日指数移动平均的8日指数移动平均
        当满足条件MMS>MMM时,在6位置画1号图标
        当满足条件MMS<MMM时,在6位置画2号图标
        当满足条件是否最后一个周期=1时,在6位置书写文字,COLORFFFFFF
        ABC6赋值:MMS>MMM
        输出买入:如果ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6=1ANDREF(ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6,1)=0,返回6,否则返回0,画黄色,线宽为2
        输出持有:如果ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6,返回6,否则返回0,画洋红色,线宽为2
        共振赋值:ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6 
        当满足条件共振时,在0和6位置之间画柱状线,宽度为0.6,1不为0则画空心柱.,画洋红色
        当满足条件买入时,在0和6位置之间画柱状线,宽度为0.6,0不为0则画空心柱.,画黄色
        当满足条件DIFF>DEA时,在1位置画1号图标
        当满足条件DIFF<DEA时,在1位置画2号图标
        当满足条件K>D时,在2位置画1号图标
        当满足条件K<D时,在2位置画2号图标
        当满足条件RSI1>RSI2时,在3位置画1号图标
        当满足条件RSI1<RSI2时,在3位置画2号图标
        当满足条件LWR1>LWR2时,在4位置画1号图标
        当满足条件LWR1<LWR2时,在4位置画2号图标
        当满足条件收盘价>BBI时,在5位置画1号图标
        当满足条件收盘价<BBI时,在5位置画2号图标
        当满足条件MMS>MMM时,在6位置画1号图标
        当满足条件MMS<MMM时,在6位置画2号图标
        当满足条件买入时,在6.6位置画9号图标
        '''
        markers=0
        signal=0
        #df=self.data.get_hist_data_em(stock=stock)
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        DIFF=EMA(CLOSE,8)-EMA(CLOSE,13)
        DEA=EMA(DIFF,5)
        #如果满足DIFF>DEA 在1的位置标记1的图标
        #DRAWICON(DIFF>DEA,1,1);
        markers+=IF(DIFF>DEA,1,0)[-1]
        #如果满足DIFF<DEA 在1的位置标记2的图标
        #DRAWICON(DIFF<DEA,1,2);
        markers+=IF(DIFF<DEA,1,0)[-1]
        #DRAWTEXT(ISLASTBAR=1,1,'. MACD'),COLORFFFFFF;{微信公众号:尊重市场}
        ABC1=DIFF>DEA
        signal+=IF(ABC1,1,0)[-1]
        尊重市场1=(CLOSE-LLV(LOW,8))/(HHV(HIGH,8)-LLV(LOW,8))*100
        K=SMA(尊重市场1,3,1)
        D=SMA(K,3,1)
        #如果满足k>d 在2的位置标记1的图标
        markers+=IF(K>D,1,0)[-1]
        #DRAWICON(K>D,2,1);
        markers+=IF(K<D,1,0)[-1]
        #DRAWICON(K<D,2,2);
        #DRAWTEXT(ISLASTBAR=1,2,'. KDJ'),COLORFFFFFF;
        ABC2=K>D
        signal+=IF(ABC2,1,0)[-1]
        指标营地=REF(CLOSE,1)
        RSI1=(SMA(MAX(CLOSE-指标营地,0),5,1))/(SMA(ABS(CLOSE-指标营地),5,1))*100
        RSI2=(SMA(MAX(CLOSE-指标营地,0),13,1))/(SMA(ABS(CLOSE-指标营地),13,1))*100
        markers+=IF(RSI1>RSI2,1,0)[-1]
        #DRAWICON(RSI1>RSI2,3,1);
        markers+=IF(RSI1<RSI2,1,0)[-1]
        #DRAWICON(RSI1<RSI2,3,2);
        #DRAWTEXT(ISLASTBAR=1,3,'. RSI'),COLORFFFFFF;
        ABC3=RSI1>RSI2
        signal+=IF(ABC3,1,0)[-1]
        尊重市场=-(HHV(HIGH,13)-CLOSE)/(HHV(HIGH,13)-LLV(LOW,13))*100
        LWR1=SMA(尊重市场,3,1)
        LWR2=SMA(LWR1,3,1)
        #DRAWICON(LWR1>LWR2,4,1);
        markers+=IF(LWR1>LWR2,1,0)[-1]
        #DRAWICON(LWR1<LWR2,4,2);
        markers+=IF(LWR1<LWR2,1,0)[-1]
        #DRAWTEXT(ISLASTBAR=1,4,'. LWR'),COLORFFFFFF;
        ABC4=LWR1>LWR2
        signal+=IF(ABC4,1,0)[-1]
        BBI=(MA(CLOSE,3)+MA(CLOSE,5)+MA(CLOSE,8)+MA(CLOSE,13))/4
        #DRAWICON(CLOSE>BBI,5,1);
        markers+=IF(CLOSE>BBI,1,0)[-1]
        #DRAWICON(CLOSE<BBI,5,2);
        markers+=IF(CLOSE<BBI,1,0)[-1]
        #DRAWTEXT(ISLASTBAR=1,5,'. BBI'),COLORFFFFFF;
        ABC10=7
        ABC5=CLOSE>BBI
        signal+=IF(ABC5,1,0)[-1]
        MTM=CLOSE-REF(CLOSE,1)
        MMS=100*EMA(EMA(MTM,5),3)/EMA(EMA(ABS(MTM),5),3)
        MMM=100*EMA(EMA(MTM,13),8)/EMA(EMA(ABS(MTM),13),8)
        markers+=IF(MMS>MMM,1,0)[-1]
        #DRAWICON(MMS>MMM,6,1);
        markers+=IF(MMS<MMM,1,0)[-1]
        #DRAWICON(MMS<MMM,6,2);
        #DRAWTEXT(ISLASTBAR=1,6,'. ZLMM'),COLORFFFFFF;
        ABC6=MMS>MMM
        signal+=IF(ABC6,1,0)[-1]
        '''
        买入:IF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6=1  
        AND REF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6,1)=0,6,0),COLORYELLOW,LINETHICK2;
        持有:IF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6,6,0),COLORMAGENTA,LINETHICK2;
        共振:=ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6 ;
        STICKLINE(共振,0,6,0.6,1),COLORMAGENTA;
        STICKLINE(买入,0,6,0.6,0),COLORYELLOW;
        DRAWICON(DIFF>DEA,1,1);
        DRAWICON(DIFF<DEA,1,2);
        DRAWICON(K>D,2,1);
        DRAWICON(K<D,2,2);
        DRAWICON(RSI1>RSI2,3,1);
        DRAWICON(RSI1<RSI2,3,2);
        DRAWICON(LWR1>LWR2,4,1);
        DRAWICON(LWR1<LWR2,4,2);
        DRAWICON(CLOSE>BBI,5,1);
        DRAWICON(CLOSE<BBI,5,2);
        DRAWICON(MMS>MMM,6,1);{微信公众号:尊重市场}
        DRAWICON(MMS<MMM,6,2);
        DRAWICON(买入,6.6,9);
        '''
        return signal,markers
    def six_pulse_excalibur_hist(self,df):
        '''
        六脉神剑
        DIFF赋值:收盘价的8日指数移动平均-收盘价的13日指数移动平均
        DEA赋值:DIFF的5日指数移动平均
        当满足条件DIFF>DEA时,在1位置画1号图标
        当满足条件DIFF<DEA时,在1位置画2号图标
        当满足条件是否最后一个周期=1时,在1位置书写文字,COLORFFFFFF
        ABC1赋值:DIFF>DEA
        尊重市场1赋值:(收盘价-8日内最低价的最低值)/(8日内最高价的最高值-8日内最低价的最低值)*100
        K赋值:尊重市场1的3日[1日权重]移动平均
        D赋值:K的3日[1日权重]移动平均
        当满足条件K>D时,在2位置画1号图标
        当满足条件K<D时,在2位置画2号图标
        当满足条件是否最后一个周期=1时,在2位置书写文字,COLORFFFFFF
        ABC2赋值:K>D
        指标营地赋值:1日前的收盘价
        RSI1赋值:(收盘价-指标营地和0的较大值的5日[1日权重]移动平均)/(收盘价-指标营地的绝对值的5日[1日权重]移动平均)*100
        RSI2赋值:(收盘价-指标营地和0的较大值的13日[1日权重]移动平均)/(收盘价-指标营地的绝对值的13日[1日权重]移动平均)*100
        当满足条件RSI1>RSI2时,在3位置画1号图标
        当满足条件RSI1<RSI2时,在3位置画2号图标
        当满足条件是否最后一个周期=1时,在3位置书写文字,COLORFFFFFF
        ABC3赋值:RSI1>RSI2
        尊重市场赋值:-(13日内最高价的最高值-收盘价)/(13日内最高价的最高值-13日内最低价的最低值)*100
        LWR1赋值:尊重市场的3日[1日权重]移动平均
        LWR2赋值:LWR1的3日[1日权重]移动平均
        当满足条件LWR1>LWR2时,在4位置画1号图标
        当满足条件LWR1<LWR2时,在4位置画2号图标
        当满足条件是否最后一个周期=1时,在4位置书写文字,COLORFFFFFF
        ABC4赋值:LWR1>LWR2
        BBI赋值:(收盘价的3日简单移动平均+收盘价的5日简单移动平均+收盘价的8日简单移动平均+收盘价的13日简单移动平均)/4
        当满足条件收盘价>BBI时,在5位置画1号图标
        当满足条件收盘价<BBI时,在5位置画2号图标
        当满足条件是否最后一个周期=1时,在5位置书写文字,COLORFFFFFF
        ABC10赋值:7
        ABC5赋值:收盘价>BBI
        MTM赋值:收盘价-1日前的收盘价
        MMS赋值:100*MTM的5日指数移动平均的3日指数移动平均/MTM的绝对值的5日指数移动平均的3日指数移动平均
        MMM赋值:100*MTM的13日指数移动平均的8日指数移动平均/MTM的绝对值的13日指数移动平均的8日指数移动平均
        当满足条件MMS>MMM时,在6位置画1号图标
        当满足条件MMS<MMM时,在6位置画2号图标
        当满足条件是否最后一个周期=1时,在6位置书写文字,COLORFFFFFF
        ABC6赋值:MMS>MMM
        输出买入:如果ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6=1ANDREF(ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6,1)=0,返回6,否则返回0,画黄色,线宽为2
        输出持有:如果ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6,返回6,否则返回0,画洋红色,线宽为2
        共振赋值:ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6 
        当满足条件共振时,在0和6位置之间画柱状线,宽度为0.6,1不为0则画空心柱.,画洋红色
        当满足条件买入时,在0和6位置之间画柱状线,宽度为0.6,0不为0则画空心柱.,画黄色
        当满足条件DIFF>DEA时,在1位置画1号图标
        当满足条件DIFF<DEA时,在1位置画2号图标
        当满足条件K>D时,在2位置画1号图标
        当满足条件K<D时,在2位置画2号图标
        当满足条件RSI1>RSI2时,在3位置画1号图标
        当满足条件RSI1<RSI2时,在3位置画2号图标
        当满足条件LWR1>LWR2时,在4位置画1号图标
        当满足条件LWR1<LWR2时,在4位置画2号图标
        当满足条件收盘价>BBI时,在5位置画1号图标
        当满足条件收盘价<BBI时,在5位置画2号图标
        当满足条件MMS>MMM时,在6位置画1号图标
        当满足条件MMS<MMM时,在6位置画2号图标
        当满足条件买入时,在6.6位置画9号图标
        '''
        markers=0
        signal=0
        #df=self.data.get_hist_data_em(stock=stock)
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        DIFF=EMA(CLOSE,8)-EMA(CLOSE,13)
        DEA=EMA(DIFF,5)
        #如果满足DIFF>DEA 在1的位置标记1的图标
        #DRAWICON(DIFF>DEA,1,1);
        markers+=IF(DIFF>DEA,1,0)
        #如果满足DIFF<DEA 在1的位置标记2的图标
        #DRAWICON(DIFF<DEA,1,2);
        markers+=IF(DIFF<DEA,1,0)
        #DRAWTEXT(ISLASTBAR=1,1,'. MACD'),COLORFFFFFF;{微信公众号:尊重市场}
        ABC1=DIFF>DEA
        signal+=IF(ABC1,1,0)
        尊重市场1=(CLOSE-LLV(LOW,8))/(HHV(HIGH,8)-LLV(LOW,8))*100
        K=SMA(尊重市场1,3,1)
        D=SMA(K,3,1)
        #如果满足k>d 在2的位置标记1的图标
        markers+=IF(K>D,1,0)
        #DRAWICON(K>D,2,1);
        markers+=IF(K<D,1,0)
        #DRAWICON(K<D,2,2);
        #DRAWTEXT(ISLASTBAR=1,2,'. KDJ'),COLORFFFFFF;
        ABC2=K>D
        signal+=IF(ABC2,1,0)
        指标营地=REF(CLOSE,1)
        RSI1=(SMA(MAX(CLOSE-指标营地,0),5,1))/(SMA(ABS(CLOSE-指标营地),5,1))*100
        RSI2=(SMA(MAX(CLOSE-指标营地,0),13,1))/(SMA(ABS(CLOSE-指标营地),13,1))*100
        markers+=IF(RSI1>RSI2,1,0)
        #DRAWICON(RSI1>RSI2,3,1);
        markers+=IF(RSI1<RSI2,1,0)
        #DRAWICON(RSI1<RSI2,3,2);
        #DRAWTEXT(ISLASTBAR=1,3,'. RSI'),COLORFFFFFF;
        ABC3=RSI1>RSI2
        signal+=IF(ABC3,1,0)
        尊重市场=-(HHV(HIGH,13)-CLOSE)/(HHV(HIGH,13)-LLV(LOW,13))*100
        LWR1=SMA(尊重市场,3,1)
        LWR2=SMA(LWR1,3,1)
        #DRAWICON(LWR1>LWR2,4,1);
        markers+=IF(LWR1>LWR2,1,0)
        #DRAWICON(LWR1<LWR2,4,2);
        markers+=IF(LWR1<LWR2,1,0)
        #DRAWTEXT(ISLASTBAR=1,4,'. LWR'),COLORFFFFFF;
        ABC4=LWR1>LWR2
        signal+=IF(ABC4,1,0)
        BBI=(MA(CLOSE,3)+MA(CLOSE,5)+MA(CLOSE,8)+MA(CLOSE,13))/4
        #DRAWICON(CLOSE>BBI,5,1);
        markers+=IF(CLOSE>BBI,1,0)
        #DRAWICON(CLOSE<BBI,5,2);
        markers+=IF(CLOSE<BBI,1,0)
        #DRAWTEXT(ISLASTBAR=1,5,'. BBI'),COLORFFFFFF;
        ABC10=7
        ABC5=CLOSE>BBI
        signal+=IF(ABC5,1,0)
        MTM=CLOSE-REF(CLOSE,1)
        MMS=100*EMA(EMA(MTM,5),3)/EMA(EMA(ABS(MTM),5),3)
        MMM=100*EMA(EMA(MTM,13),8)/EMA(EMA(ABS(MTM),13),8)
        markers+=IF(MMS>MMM,1,0)
        #DRAWICON(MMS>MMM,6,1);
        markers+=IF(MMS<MMM,1,0)
        #DRAWICON(MMS<MMM,6,2);
        #DRAWTEXT(ISLASTBAR=1,6,'. ZLMM'),COLORFFFFFF;
        ABC6=MMS>MMM
        signal+=IF(ABC6,1,0)
        '''
        买入:IF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6=1  
        AND REF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6,1)=0,6,0),COLORYELLOW,LINETHICK2;
        持有:IF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6,6,0),COLORMAGENTA,LINETHICK2;
        共振:=ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6 ;
        STICKLINE(共振,0,6,0.6,1),COLORMAGENTA;
        STICKLINE(买入,0,6,0.6,0),COLORYELLOW;
        DRAWICON(DIFF>DEA,1,1);
        DRAWICON(DIFF<DEA,1,2);
        DRAWICON(K>D,2,1);
        DRAWICON(K<D,2,2);
        DRAWICON(RSI1>RSI2,3,1);
        DRAWICON(RSI1<RSI2,3,2);
        DRAWICON(LWR1>LWR2,4,1);
        DRAWICON(LWR1<LWR2,4,2);
        DRAWICON(CLOSE>BBI,5,1);
        DRAWICON(CLOSE<BBI,5,2);
        DRAWICON(MMS>MMM,6,1);{微信公众号:尊重市场}
        DRAWICON(MMS<MMM,6,2);
        DRAWICON(买入,6.6,9);
        '''
        return signal,markers
    def every_inch_perfect(self,stock='600031'):
        '''
        十全十美
        填充背景
        DIFF赋值:收盘价的8日指数移动平均-收盘价的13日指数移动平均
        DEA赋值:DIFF的5日指数移动平均
        输出A1:当满足条件DIFF>DEA时,在5和10位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件DIFF<DEA时,在5和10位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        尊重市场1赋值:(收盘价-8日内最低价的最低值)/(8日内最高价的最高值-8日内最低价的最低值)*100
        K赋值:尊重市场1的3日[1日权重]移动平均
        D赋值:K的3日[1日权重]移动平均
        输出A2:当满足条件K>D时,在10和15位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件K<D时,在10和15位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        LC赋值:1日前的收盘价
        CBA1赋值:(收盘价-LC和0的较大值的5日[1日权重]移动平均)/(收盘价-LC的绝对值的5日[1日权重]移动平均)*100
        CBA2赋值:(收盘价-LC和0的较大值的13日[1日权重]移动平均)/(收盘价-LC的绝对值的13日[1日权重]移动平均)*100
        输出A3:当满足条件CBA1>CBA2时,在15和20位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件CBA1<CBA2时,在15和20位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        尊重市场赋值:-(13日内最高价的最高值-收盘价)/(13日内最高价的最高值-13日内最低价的最低值)*100
        指标营地1赋值:尊重市场的3日[1日权重]移动平均
        指标营地2赋值:指标营地1的3日[1日权重]移动平均
        输出A4:当满足条件指标营地1>指标营地2时,在20和25位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件指标营地1<指标营地2时,在20和25位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        BBI赋值:(收盘价的3日简单移动平均+收盘价的6日简单移动平均+收盘价的12日简单移动平均+收盘价的24日简单移动平均)/4
        输出A5:当满足条件收盘价>BBI时,在25和30位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件收盘价<BBI时,在25和30位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        MTM赋值:收盘价-1日前的收盘价
        MMS赋值:100*MTM的5日指数移动平均的3日指数移动平均/MTM的绝对值的5日指数移动平均的3日指数移动平均
        MMM赋值:100*MTM的13日指数移动平均的8日指数移动平均/MTM的绝对值的13日指数移动平均的8日指数移动平均
        输出A6:当满足条件MMS>MMM时,在30和35位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件MMS<MMM时,在30和35位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        MAV赋值:(收盘价*2+最高价+最低价)/4
        SK赋值:MAV的13日指数移动平均-MAV的34日指数移动平均
        SD赋值:SK的5日指数移动平均
        空方主力赋值:(-2*(SK-SD))*3.8,画绿色
        多方主力赋值:(2*(SK-SD))*3.8,画红色
        输出A7:当满足条件多方主力>空方主力时,在37和42位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        当满足条件多方主力<空方主力时,在37和42位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        MA11赋值:收盘价的5日简单移动平均
        MA22赋值:1日前的收盘价的5日简单移动平均
        当满足条件MA22>MA11时,在43和48位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        输出A8:当满足条件MA22<=MA11时,在43和48位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        XYZ2赋值:如果月份<12,返回1,否则返回1
        XYZ3赋值:(2*收盘价+最高价+最低价)/4
        XYZ4赋值:34日内最低价的最低值
        XYZ5赋值:34日内最高价的最高值
        主力赋值:(XYZ3-XYZ4)/(XYZ5-XYZ4)*100的13日指数移动平均*XYZ2
        散户赋值:0.667*1日前的主力+0.333*主力的2日指数移动平均
        当满足条件主力<散户时,在49和54位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        输出A9:当满足条件主力>散户时,在49和54位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        输出A10:当满足条件(多方主力>空方主力)AND(MA22<=MA11)AND(主力>散户)时,在56和61位置之间画柱状线,宽度为3,0不为0则画空心柱.,画黄色
        当满足条件(多方主力<空方主力)AND(MA22>MA11)AND(主力<散户)时,在56和61位置之间画柱状线,宽度为3,0不为0则画空心柱.,画青色
        输出A11:当满足条件(多方主力>空方主力)AND(MA22<=MA11)AND(主力>散户)AND(DIFF>DEA)AND(K>D)AND(CBA1>CBA2)AND(指标营地1>指标营地2)AND(收盘价>BBI)AND(MMS>MMM)时,在63和68位置之间画柱状线,宽度为3,0不为0则画空心柱.,画洋红色
        ABC1赋值:收盘价的10日简单移动平均
        ABC2赋值:收盘价的55日简单移动平均
        ABC3赋值:(3日前的收盘价-收盘价)/3日前的收盘价*100>5
        ABC4赋值:ABC3的10日过滤
        ABC5赋值:上次ABC4距今天数
        ABC6赋值:ABC5+2日前的最高价
        ABC7赋值:ABC5+1日前的最高价
        ABC8赋值:ABC5日前的最高价
        ABC9赋值:ABC6和ABC7的较大值
        ABC10赋值:ABC9和ABC8的较大值
        ABC11赋值:(收盘价-1日前的收盘价)/1日前的收盘价*100>5
        ABC12赋值:ABC5<150
        ABC13赋值:(开盘价-ABC10)/ABC10*100<30
        ABC14赋值:(收盘价-ABC5日内最低价的最低值)/ABC5日内最低价的最低值*100<50
        ABC15赋值:(收盘价-5日前的开盘价)/5日前的开盘价*100<30
        ABC16赋值:成交量(手)/成交量(手)的5日简单移动平均<3.5
        ABC17赋值:(收盘价-89日前的收盘价)/89日前的收盘价*100<80
        ABC18赋值:ABC11 AND ABC12 AND ABC13 AND ABC14 AND ABC15 AND ABC16 AND ABC17
        ABC19赋值:ABC18的15日过滤
        ABC20赋值:(收盘价-ABC2)/ABC2<0.1
        ABC21赋值:(收盘价-ABC1)/ABC1<0.3
        ABC22赋值:(ABC20=1 AND ABC21=1)*0.2
        ABC23赋值:(ABC22=0 AND 1日前的ABC22=0.2 AND 1日前的统计10日中满足ABC22=0.2的天数=10=1)*(-0.1)
        ABC24赋值:ABC23=(-0.1)
        ABC25赋值:ABC19 OR ABC24
        ABC27赋值:成交量(手)/1日前的成交量(手)>1.2 AND 收阳线OROSE (最低价>1日前的最高价 AND 收阴线ANDN 成交量(手)/1日前的成交量(手)>1.2)
        ABC28赋值:如果模糊匹配品种代码OR(模糊匹配品种代码ANDDATE>=1200824),返回收盘价>=计算涨停价ANDCLOSE=最高价,否则返回收盘价>=计算涨停价ANDCLOSE=最高价
        共振赋值:ABC25 AND ABC27 AND ABC28 AND 1日前的取反 AND (多方主力>空方主力) AND (MA22<= MA11) AND (主力>散户) AND (DIFF>DEA) AND (K>D) AND (CBA1>CBA2) AND (指标营地1>指标营地2) AND (收盘价>BBI) AND (MMS>MMM)
        当满足条件共振时,在75位置画9号图标
        '''
        markers=0
        signal=0
        df=self.data.get_hist_data_em(stock=stock)
        CLOSE=df['close']
        C=df['close']
        LOW=df['low']
        L=df['low']
        HIGH=df['high']
        H=df['high']
        #DRAWGBK(C>1,RGB(0,0,0),RGB(1,1,1),1,0,0)
        DIFF=EMA(CLOSE,8)-EMA(CLOSE,13)
        DEA=EMA(DIFF,5)
        #A1:STICKLINE(DIFF>DEA,5,10,2,1),COLORRED
        markers+=IF(DIFF>DEA,1,0)[-1]
        #STICKLINE(DIFF<DEA,5,10,2,1),COLORGREEN
        markers+=IF(DIFF<DEA,1,0)[-1]
        尊重市场1=(CLOSE-LLV(LOW,8))/(HHV(HIGH,8)-LLV(LOW,8))*100
        K=SMA(尊重市场1,3,1)
        D=SMA(K,3,1)
        #A2:STICKLINE(K>D,10,15,2,1),COLORRED
        markers+=IF(K>D,1,0)[-1]
        #STICKLINE(K<D,10,15,2,1),COLORGREEN
        markers+=IF(K<D,1,0)[-1]
        LC=REF(CLOSE,1)
        CBA1=(SMA(MAX(CLOSE-LC,0),5,1))/(SMA(ABS(CLOSE-LC),5,1))*100
        CBA2=(SMA(MAX(CLOSE-LC,0),13,1))/(SMA(ABS(CLOSE-LC),13,1))*100
        #A3:STICKLINE(CBA1>CBA2,15,20,2,1),COLORRED
        markers+=IF(CBA1>CBA2,1,0)[-1]
        #STICKLINE(CBA1<CBA2,15,20,2,1),COLORGREEN
        markers+=IF(CBA1<CBA2,1,0)[-1]
        尊重市场=-(HHV(HIGH,13)-CLOSE)/(HHV(HIGH,13)-LLV(LOW,13))*100
        指标营地1=SMA(尊重市场,3,1)
        指标营地2=SMA(指标营地1,3,1)
        #A4:STICKLINE(指标营地1>指标营地2,20,25,2,1),COLORRED
        markers+=IF(指标营地1>指标营地2,1,0)[-1]
        #STICKLINE(指标营地1<指标营地2,20,25,2,1),COLORGREEN
        markers+=IF(指标营地1<指标营地2,1,0)[-1]
        BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
        #A5:STICKLINE(CLOSE>BBI,25,30,2,1),COLORRED
        markers+=IF(CLOSE>BBI,1,0)[-1]
        #STICKLINE(CLOSE<BBI,25,30,2,1),COLORGREEN
        markers+=IF(CLOSE<BBI,1,0)[-1]
        MTM=CLOSE-REF(CLOSE,1)
        MMS=100*EMA(EMA(MTM,5),3)/EMA(EMA(ABS(MTM),5),3)
        MMM=100*EMA(EMA(MTM,13),8)/EMA(EMA(ABS(MTM),13),8)
        #A6:STICKLINE(MMS>MMM,30,35,2,1),COLORRED
        markers+=IF(MMS>MMM,1,0)[-1]
        #STICKLINE(MMS<MMM,30,35,2,1),COLORGREEN
        markers+=IF(MMS<MMM,1,0)[-1]
        MAV=(C*2+H+L)/4
        SK=EMA(MAV,13)-EMA(MAV,34)
        SD=EMA(SK,5)
        空方主力=(-2*(SK-SD))*3.8
        多方主力=(2*(SK-SD))*3.8
        #A7:STICKLINE(多方主力>空方主力,37,42,2,0),COLORRED
        markers+=IF(多方主力>空方主力,1,0)[-1]
        #STICKLINE(多方主力<空方主力,37,42,2,0),
        markers+=IF(多方主力<空方主力,1,0)[-1]
        MA11=MA(CLOSE,5)
        MA22=REF(MA(CLOSE,5),1)
        #STICKLINE(MA22>MA11,43,48,2,0),COLORGREEN;
        #A8:STICKLINE(MA22<= MA11,43,48,2,0),COLORRED;
        markers+=IF(MA22>MA11,1,0)[-1]
        markers+=IF(MA22<MA11,1,0)[-1]
        XYZ2=1
        XYZ3=(2*CLOSE+HIGH+LOW)/4
        XYZ4=LLV(LOW,34)
        XYZ5=HHV(HIGH,34)
        主力=EMA((XYZ3-XYZ4)/(XYZ5-XYZ4)*100,13)*XYZ2
        散户=EMA(0.667*REF(主力,1)+0.333*主力,2)
        '''
        STICKLINE(主力<散户,49,54,2,0),COLORGREEN
        A9:STICKLINE(主力>散户,49,54,2,0),COLORRED;
        A10:STICKLINE((多方主力>空方主力) AND(MA22<= MA11) AND (主力>散户) ,56,61,3,0),COLORYELLOW;
        STICKLINE((多方主力<空方主力) AND(MA22>MA11) AND (主力<散户) ,56,61,3,0),COLORCYAN;
        A11:STICKLINE((多方主力>空方主力) AND (MA22<= MA11) AND (主力>散户) AND (DIFF>DEA) AND (K>D) AND (CBA1>CBA2) AND (指标营地1>指标营地2) AND (CLOSE>BBI) AND (MMS>MMM),63,68,3,0),COLORMAGENTA
        {微信公众号:尊重市场}
        ABC1:=MA(CLOSE,10);
        ABC2:=MA(CLOSE,55);
        ABC3:=(REF(CLOSE,3)-CLOSE)/REF(CLOSE,3)*100>5;
        ABC4:=FILTER(ABC3,10);
        ABC5:=BARSLAST(ABC4);
        ABC6:=REF(HIGH,ABC5+2);
        ABC7:=REF(HIGH,ABC5+1);
        ABC8:=REF(HIGH,ABC5);
        ABC9:=MAX(ABC6,ABC7);
        ABC10:=MAX(ABC9,ABC8);
        ABC11:=(CLOSE-REF(CLOSE,1))/REF(CLOSE,1)*100>5;
        ABC12:=ABC5<150;
        ABC13:=(OPEN-ABC10)/ABC10*100<30;
        ABC14:=(CLOSE-LLV(LOW,ABC5))/LLV(LOW,ABC5)*100<50;
        ABC15:=(CLOSE-REF(OPEN,5))/REF(OPEN,5)*100<30;
        ABC16:=VOL/MA(VOL,5)<3.5;
        ABC17:=(CLOSE-REF(CLOSE,89))/REF(CLOSE,89)*100<80;
        ABC18:=ABC11 AND ABC12 AND ABC13 AND ABC14 AND ABC15 AND ABC16 AND ABC17;
        ABC19:=FILTER(ABC18,15);
        ABC20:=(CLOSE-ABC2)/ABC2<0.1;
        ABC21:=(CLOSE-ABC1)/ABC1<0.3;
        ABC22:=(ABC20=1 AND ABC21=1)*0.2;
        ABC23:=(ABC22=0 AND REF(ABC22,1)=0.2 AND REF(COUNT(ABC22=0.2,10)=10,1)=1)*(-0.1);
        ABC24:=ABC23=(-0.1);
        ABC25:=ABC19 OR ABC24;
        ABC27:=VOL/REF(VOL,1)>1.2 AND CLOSE>OPEN OR (LOW>REF(HIGH,1) AND OPEN>CLOSE AND VOL/REF(VOL,1)>1.2);
        {微信公众号:尊重市场}
        ABC28:=IF(CODELIKE(3) OR (CODELIKE(4) AND DATE>=1200824),CLOSE>=ZTPRICE(REF(CLOSE,1),0.2) AND CLOSE=HIGH,CLOSE>=ZTPRICE(REF(CLOSE,1),0.1) AND CLOSE=HIGH);
        共振:=ABC25 AND ABC27 AND ABC28 AND REF(NOT(ABC28),1) AND (多方主力>空方主力) AND (MA22<= MA11) AND (主力>散户) AND (DIFF>DEA) AND (K>D) AND (CBA1>CBA2) AND (指标营地1>指标营地2) AND (CLOSE>BBI) AND (MMS>MMM);
        DRAWICON(共振,75,9);
        '''

    

            


            
            

