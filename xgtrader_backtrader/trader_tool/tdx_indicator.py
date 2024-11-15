import pandas as pd
import numpy as np
def RD(N,D=3):   return np.round(N,D)        #四舍五入取3位小数 
def RET(S,N=1):  return np.array(S)[-N]      #返回序列倒数第N个值,默认返回最后一个
def ABS(S):      return np.abs(S)            #返回N的绝对值
def MAX(S1,S2):  return np.maximum(S1,S2)    #序列max
def MIN(S1,S2):  return np.minimum(S1,S2)    #序列min
def IF(S,A,B):   return np.where(S,A,B)      #序列布尔判断 return=A  if S==True  else  B


def REF(S, N=1):          #对序列整体下移动N,返回序列(shift后会产生NAN)    
    return pd.Series(S).shift(N).values  

def DIFF(S, N=1):         #前一个值减后一个值,前面会产生nan 
    return pd.Series(S).diff(N).values     #np.diff(S)直接删除nan，会少一行

def STD(S,N):             #求序列的N日标准差，返回序列    
    return  pd.Series(S).rolling(N).std(ddof=0).values     

def SUM(S, N):            #对序列求N天累计和，返回序列    N=0对序列所有依次求和         
    return pd.Series(S).rolling(N).sum().values if N>0 else pd.Series(S).cumsum().values  

def CONST(S):             #返回序列S最后的值组成常量序列
    return np.full(len(S),S[-1])
  
def HHV(S,N):             #HHV(C, 5) 最近5天收盘最高价        
    return pd.Series(S).rolling(N).max().values     

def LLV(S,N):             #LLV(C, 5) 最近5天收盘最低价     
    return pd.Series(S).rolling(N).min().values    
    
def HHVBARS(S,N):         #求N周期内S最高值到当前周期数, 返回序列
    return pd.Series(S).rolling(N).apply(lambda x: np.argmax(x[::-1]),raw=True).values 

def LLVBARS(S,N):         #求N周期内S最低值到当前周期数, 返回序列
    return pd.Series(S).rolling(N).apply(lambda x: np.argmin(x[::-1]),raw=True).values    
  
def MA(S,N):              #求序列的N日简单移动平均值，返回序列                    
    return pd.Series(S).rolling(N).mean().values  
  
def EMA(S,N):             #指数移动平均,为了精度 S>4*N  EMA至少需要120周期     alpha=2/(span+1)    
    return pd.Series(S).ewm(span=N, adjust=False).mean().values     

def SMA(S, N, M=1):       #中国式的SMA,至少需要120周期才精确 (雪球180周期)    alpha=1/(1+com)    
    return pd.Series(S).ewm(alpha=M/N,adjust=False).mean().values           #com=N-M/M

def DMA(S, A):            #求S的动态移动平均，A作平滑因子,必须 0<A<1  (此为核心函数，非指标）
    return pd.Series(S).ewm(alpha=A, adjust=True).mean().values

def WMA(S, N):            #通达信S序列的N日加权移动平均 Yn = (1*X1+2*X2+3*X3+...+n*Xn)/(1+2+3+...+Xn)
    return pd.Series(S).rolling(N).apply(lambda x:x[::-1].cumsum().sum()*2/N/(N+1),raw=True).values 
  
def AVEDEV(S, N):         #平均绝对偏差  (序列与其平均值的绝对差的平均值)   
    return pd.Series(S).rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean()).values 

def SLOPE(S, N):          #返S序列N周期回线性回归斜率            
    return pd.Series(S).rolling(N).apply(lambda x: np.polyfit(range(N),x,deg=1)[0],raw=True).values

def FORCAST(S, N):        #返回S序列N周期回线性回归后的预测值， jqz1226改进成序列出    
    return pd.Series(S).rolling(N).apply(lambda x:np.polyval(np.polyfit(range(N),x,deg=1),N-1),raw=True).values  

def LAST(S, A, B):        #从前A日到前B日一直满足S_BOOL条件, 要求A>B & A>0 & B>=0 
    return np.array(pd.Series(S).rolling(A+1).apply(lambda x:np.all(x[::-1][B:]),raw=True),dtype=bool)
  
#------------------   1级：应用层函数(通过0级核心函数实现） ----------------------------------
def COUNT(S, N):                       # COUNT(CLOSE>O, N):  最近N天满足S_BOO的天数  True的天数
    return SUM(S,N)    

def EVERY(S, N):                       # EVERY(CLOSE>O, 5)   最近N天是否都是True
    return  IF(SUM(S,N)==N,True,False)                    
  
def EXIST(S, N):                       # EXIST(CLOSE>3010, N=5)  n日内是否存在一天大于3000点  
    return IF(SUM(S,N)>0,True,False)

def FILTER(S, N):                      # FILTER函数，S满足条件后，将其后N周期内的数据置为0, FILTER(C==H,5)
    for i in range(len(S)): S[i+1:i+1+N]=0  if S[i] else S[i+1:i+1+N]        
    return S                           # 例：FILTER(C==H,5) 涨停后，后5天不再发出信号 
  
def BARSLAST(S):                       #上一次条件成立到当前的周期, BARSLAST(C/REF(C,1)>=1.1) 上一次涨停到今天的天数 
    M=np.concatenate(([0],np.where(S,1,0)))  
    for i in range(1, len(M)):  M[i]=0 if M[i] else M[i-1]+1    
    return M[1:]                       

def BARSLASTCOUNT(S):                  # 统计连续满足S条件的周期数        by jqz1226
    rt = np.zeros(len(S)+1)            # BARSLASTCOUNT(CLOSE>OPEN)表示统计连续收阳的周期数
    for i in range(len(S)): rt[i+1]=rt[i]+1  if S[i] else rt[i+1]
    return rt[1:]  
  
def BARSSINCEN(S, N):                  # N周期内第一次S条件成立到现在的周期数,N为常量  by jqz1226
    return pd.Series(S).rolling(N).apply(lambda x:N-1-np.argmax(x) if np.argmax(x) or x[0] else 0,raw=True).fillna(0).values.astype(int)

  
def CROSS(S1, S2):                     #判断向上金叉穿越 CROSS(MA(C,5),MA(C,10))  判断向下死叉穿越 CROSS(MA(C,10),MA(C,5))   
    return np.concatenate(([False], np.logical_not((S1>S2)[:-1]) & (S1>S2)[1:]))    # 不使用0级函数,移植方便  by jqz1226
def CROSS_UP(S1, S2):                     #判断向上金叉穿越 CROSS(MA(C,5),MA(C,10))  判断向下死叉穿越 CROSS(MA(C,10),MA(C,5))   
    return np.concatenate(([False], np.logical_not((S1>S2)[:-1]) & (S1>S2)[1:]))    # 不使用0级函数,移植方便  by jqz1226
def CROSS_DOWN(S1, S2):                     
    return np.concatenate(([False], np.logical_not((S1<S2)[:-1]) & (S1<S2)[1:]))    # 不使用0级函数,移植方便  by jqz1226

def LONGCROSS(S1,S2,N):                #两条线维持一定周期后交叉,S1在N周期内都小于S2,本周期从S1下方向上穿过S2时返回1,否则返回0         
    return  np.array(np.logical_and(LAST(S1<S2,N,1),(S1>S2)),dtype=bool)            # N=1时等同于CROSS(S1, S2)
    
def VALUEWHEN(S, X):                   #当S条件成立时,取X的当前值,否则取VALUEWHEN的上个成立时的X值   by jqz1226
    return pd.Series(np.where(S,X,np.nan)).ffill().values  
#df,DATE,CLOSE,OPEN,LOW,HIGH,VOL,CAPITAL,HSL,AMOUNT=set_start_data()
def params_data(test='test.txt',to_path='result.txt'):
    '''
    解析通达信公式
    test原来通达信公式文件
    to_path结果文件，python可以直接运行的文件
    '''
    test=open(r'{}'.format(test),'r',encoding='utf-8')
    result=test.readlines()
    columns=[]
    #挑选需要返回的数据
    for i in result:
        if ':' in i and ':=' not in i:
            name_list=i.split(':')
            columns.append(name_list[0])
    text=''.join(result)
    text1=text.replace(':=','=')
    text2=text1.replace(':','=')
    text4=text2.replace('&&',' and ')
    text5=text4.replace('||','or')
    text6=text5.replace('AND','and')
    text7=text6.replace('OR','or')
    text8=text7.replace('NOT','not')
    text9=text8.replace('DRAWNULL','None')
    text10=text9.replace(',NODRAW','')
    text11=text10.replace('MF0>MF1 and MF0>MF2','np.logical_and(MF0>MF1,MF0>MF2)')
    text12=text11.replace('MF0<MF1 and MF0<MF2','np.logical_and(MF0<MF1,MF0<MF2)')
    text3=text12.split(';')
    del text3[-1]
    fill=open(r'{}'.format(to_path),'w+',encoding='utf-8')
    fill.truncate()
    for i in text3:
        try:
            m=i.split('=')
            var=m[0]
            result=m[1]
            fill.write(var +'='+result)
        except:
           fill.write(var +'='+result)
    fill.write('\n')
    fill.write('return {}'.format(','.join(columns)))
    fill.close()
    print('公式分析成功')
def data_to_pandas(func=''):
    '''
    将函数的计算结果数据变成pandas数据,需要自动补充列名称
    func计算公式，例子data_to_pandas(CCI(CLOSE,HIGH,LOW)),CCI函数，也可以计算在返回
    print(data_to_pandas(CCI(CLOSE,HIGH,LOW)))
                   0       
    300          NaN       
    301          NaN       
    302          NaN       
    303          NaN       
    304          NaN       
    ...          ...       
    4634   10.314220       
    4635   68.462799       
    4636  106.677513       
    4637  116.201078       
    4638   85.026126  
    '''
    df=pd.DataFrame(func)
    #自己补充列明，列名称就是返回的参数
    columns=[]
    #df.columns=columns
    df1=df.T
    return df1
def CCI(CLOSE,HIGH,LOW,N=14):
    '''
    超卖超买类
    CCI商品路劲指标
    TYP赋值:(最高价+最低价+收盘价)/3
    输出CCI:(TYP-TYP的N日简单移动平均)*1000/(15*TYP的N日平均绝对偏差)
    '''
    TYP=(HIGH+LOW+CLOSE)/3
    result=(TYP-MA(TYP,N))*1000/(15*AVEDEV(TYP,N))
    return result
def KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3):
    '''
    超卖超买类
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出K:RSV的M1日[1日权重]移动平均
    输出D:K的M2日[1日权重]移动平均
    输出J:3*K-2*D
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M2,1)
    J=3*K-2*D
    return K,D,J
def MFI(CLOSE,HIGH,LOW,VOL,N=14):
    '''
    最近流量指标
    超卖超买类
    赋值: (最高价 + 最低价 + 收盘价)/3
    V1赋值:如果TYP>1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和/如果TYP<1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和
    输出资金流量指标:100-(100/(1+V1))
    '''
    TYP = (HIGH + LOW + CLOSE)/3
    V1=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N)  
    return 100-(100/(1+V1))  
def MTM(CLOSE,N=12,M=6):
    '''
    动量线指标
    超卖超买类
    输出动量线:收盘价-收盘价的有效数据周期数和N的较小值日前的收盘价
    输出MTMMA:MTM的M日简单移动平均
    '''
    MTM=CLOSE-REF(CLOSE,N)
    MTMMA=MA(MTM,M)
    return MTM,MTMMA
def EXPMEMA(data,N=20):
    '''
    data pandas.Series数据
    超卖超买类
    指数平滑移动平均
    '''
    result=data.ewm(com=N).mean()
    return result
def OSC(CLOSE,N=20,M=6):
    '''
    变动速度线
    超卖超买类
    输出变动速率线:100*(收盘价-收盘价的N日简单移动平均)
    输出MAOSC:OSC的M日指数平滑移动平均
    '''
    OSC=100*(CLOSE-MA(CLOSE,N))
    MAOSC=EXPMEMA(OSC,M)
    return OSC,MAOSC
def BARSCOUNT(CLOSE):
    df=pd.DataFrame()
    df['数据']=CLOSE
    df1=df['数据'].dropna()
    return len(df1.tolist())
def ROC(CLOSE,N=12,M=6):
    '''
    超卖超买类
    变动率指标
    NN赋值:收盘价的有效数据周期数和N的较小值
    输出ROC:100*(收盘价-NN日前的收盘价)/NN日前的收盘价
    输出MAROC:ROC的M日简单移动平均
    '''
    NN=MIN(BARSCOUNT(CLOSE),N)
    ROC=100*(CLOSE-REF(CLOSE,NN))/REF(CLOSE,NN)
    MAROC=MA(ROC,M)
    return ROC,MAROC
def RSI(CLOSE, N1=6,N2=12,N3=24):
    '''
    相对强弱指标
    LC赋值:1日前的收盘价
    输出RSI1:收盘价-LC和0的较大值的N1日[1日权重]移动平均/收盘价-LC的绝对值的N1日[1日权重]移动平均*100
    输出RSI2:收盘价-LC和0的较大值的N2日[1日权重]移动平均/收盘价-LC的绝对值的N2日[1日权重]移动平均*100
    输出RSI3:收盘价-LC和0的较大值的N3日[1日权重]移动平均/收盘价-LC的绝对值的N3日[1日权重]移动平均*100
    '''
    LC=REF(CLOSE,1)
    RSI1=SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100
    RSI2=SMA(MAX(CLOSE-LC,0),N2,1)/SMA(ABS(CLOSE-LC),N2,1)*100
    RSI3=SMA(MAX(CLOSE-LC,0),N3,1)/SMA(ABS(CLOSE-LC),N3,1)*100
    return RSI1,RSI2,RSI3
def KD(CLOSE,LOW,HIGH,N=9,M1=3,M2=3):
    '''
    相对强弱指标
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出K:RSV的M1日[1日权重]移动平均
    输出D:K的M2日[1日权重]移动平均
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M2,1)
    return K,D
def SKDJ(CLOSE,LOW,HIGH,N=9,M=3):
    '''
    慢速随机指标
    LOWV赋值:N日内最低价的最低值
    HIGHV赋值:N日内最高价的最高值
    RSV赋值:(收盘价-LOWV)/(HIGHV-LOWV)*100的M日指数移动平均
    输出K:RSV的M日指数移动平均
    输出D:K的M日简单移动平均
    '''
    LOWV=LLV(LOW,N)
    HIGHV=HHV(HIGH,N)
    RSV=EMA((CLOSE-LOWV)/(HIGHV-LOWV)*100,M)
    K=EMA(RSV,M)
    D=MA(K,M)
    return K,D
def UDL(CLOSE,N1=3,N2=5,N3=10,N4=20,M=6):
    '''
    引力线
    输出引力线:(收盘价的N1日简单移动平均+收盘价的N2日简单移动平均+收盘价的N3日简单移动平均+收盘价的N4日简单移动平均)/4
    输出MAUDL:UDL的M日简单移动平均
    '''
    UDL=(MA(CLOSE,N1)+MA(CLOSE,N2)+MA(CLOSE,N3)+MA(CLOSE,N4))/4
    MAUDL=MA(UDL,M)
    return UDL,MAUDL
def WR(CLOSE,LOW,HIGH,N=10,N1=6):
    '''
    威廉指标
    输出WR1:100*(N日内最高价的最高值-收盘价)/(N日内最高价的最高值-N日内最低价的最低值)
    输出WR2:100*(N1日内最高价的最高值-收盘价)/(N1日内最高价的最高值-N1日内最低价的最低值)
    '''
    WR1=100*(HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N))
    WR2=100*(HHV(HIGH,N1)-CLOSE)/(HHV(HIGH,N1)-LLV(LOW,N1))
    return WR1,WR2
def LWR(CLOSE,LOW,HIGH,N=9,M1=3,M2=3):
    '''
    LWR指标
    RSV赋值: (N日内最高价的最高值-收盘价)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出LWR1:RSV的M1日[1日权重]移动平均
    输出LWR2:LWR1的M2日[1日权重]移动平均
    '''
    RSV= (HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N))*100
    LWR1=SMA(RSV,M1,1)
    LWR2=SMA(LWR1,M2,1)
    return LWR1,LWR2
def MEMA(S,N,M=1):
    '''
    平滑移动平均
    '''
    return SMA(S,N,M)
def MARSI(CLOSE,M1=10,M2=6):
    '''
    相对强弱平均线
    DIF赋值:收盘价-1日前的收盘价
    VU赋值:如果DIF>=0,返回DIF,否则返回0
    VD赋值:如果DIF<0,返回-DIF,否则返回0
    MAU1赋值:VU的M1日平滑移动平均
    MAD1赋值:VD的M1日平滑移动平均
    MAU2赋值:VU的M2日平滑移动平均
    '''
    DIF=CLOSE-REF(CLOSE,1)
    VU=IF(DIF>=0,DIF,0)
    VD=IF(DIF<0,-DIF,0)
    MAU1=MEMA(VU,M1)
    MAD1=MEMA(VD,M1)
    MAU2=MEMA(VU,M2)
    MAD2=MEMA(VD,M2)
    RSI1=MA(100*MAU1/(MAU1+MAD1),M1)
    RSI2=MA(100*MAU2/(MAU2+MAD2),M2)
    return RSI1,RSI2
def BIAS_QL(CLOSE,N=6,M=6):
    '''
    乖离率-传统版
    输出乖离率 :(收盘价-收盘价的N日简单移动平均)/收盘价的N日简单移动平均*100
    输出BIASMA :乖离率的M日简单移动平均
    '''
    BIAS=(CLOSE-MA(CLOSE,N))/MA(CLOSE,N)*100
    BIASMA=MA(BIAS,M)
    return BIAS,BIASMA
def BIAS(CLOSE,N1=6,N2=12,N3=24):
    '''
    乖离率
    输出BIAS1 :(收盘价-收盘价的N1日简单移动平均)/收盘价的N1日简单移动平均*100
    输出BIAS2 :(收盘价-收盘价的N2日简单移动平均)/收盘价的N2日简单移动平均*100
    输出BIAS3 :(收盘价-收盘价的N3日简单移动平均)/收盘价的N3日简单移动平均*100
    '''
    BIAS1=(CLOSE-MA(CLOSE,N1))/MA(CLOSE,N1)*100
    BIAS2=(CLOSE-MA(CLOSE,N2))/MA(CLOSE,N2)*100
    BIAS3=(CLOSE-MA(CLOSE,N3))/MA(CLOSE,N3)*100
    return BIAS1,BIAS2,BIAS3
def BIAS36(CLOSE,M=6):
    '''
    三六乖离
    输出三六乖离:收盘价的3日简单移动平均-收盘价的6日简单移动平均
    输出BIAS612:收盘价的6日简单移动平均-收盘价的12日简单移动平均
    输出MABIAS:BIAS36的M日简单移动平均
    '''
    BIAS36=MA(CLOSE,3)-MA(CLOSE,6)
    BIAS612=MA(CLOSE,6)-MA(CLOSE,12)
    MABIAS=MA(BIAS36,M)
    return BIAS36,BIAS612,MABIAS
def ACCER(CLOSE,N=8):
    '''
    幅度涨速
    输出幅度涨速:收盘价的N日线性回归斜率/收盘价
    '''
    ACCER=SLOPE(CLOSE,N)/CLOSE
    return ACCER
#需要编写活力函数
def CYD(CLOSE,CAPITAL,N=21):
    '''
    承接因子
    输出CYDS:以收盘价计算的获利盘比例/(成交量(手)/当前流通股本(手))
    输出CYDN:以收盘价计算的获利盘比例/成交量(手)/当前流通股本(手)的N日简单移动平均
    '''
    CYDS=WINNER(CLOSE)/(VOL/CAPITAL)
    CYDN=WINNER(CLOSE)/MA(VOL/CAPITAL,N);   
    return CYDS,CYDN
def CYF(HSL,N=21):
    '''
    市场能量
    输出市场能量:100-100/(1+换手线的N日指数移动平均)
    '''
    CYF=100-100/(1+EMA(HSL,N))
    return CYF
def SFL(CLOSE):
    '''
    分水岭
    输出SWL:(收盘价的5日指数移动平均*7+收盘价的10日指数移动平均*3)/10
    输出SWS:以1和100*(成交量(手)的5日累和/(3*当前流通股本(手)))的较大值为权重收盘价的12日指数移动平均的动态移动平均
    '''
    SWL=(EMA(CLOSE,5)*7+EMA(CLOSE,10)*3)/10
    IF(100*(SUM(VOL,5)/(3*CAPITAL)>1),100*(SUM(VOL,5)/(3*CAPITAL)),1)
    SWS=DMA(EMA(CLOSE,12),MAX(1,1))
    return SWL,SWS
def ATR(CLOSE,HIGH,LOW,N=14):
    '''
    真实波幅
    输出MTR:(最高价-最低价)和1日前的收盘价-最高价的绝对值的较大值和1日前的收盘价-最低价的绝对值的较大值
    输出真实波幅:MTR的N日简单移动平均
    '''
    MTR=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW))
    ATR=MA(MTR,N)
    return MTR,ATR
def DKX(CLOSE,LOW,OPEN,HIGH,M=10):
    '''
    多空线
    MID赋值:(3*收盘价+最低价+开盘价+最高价)/6
    输出多空线:(20*MID+19*1日前的MID+18*2日前的MID+17*3日前的MID+16*4日前的MID+15*5日前的MID+14*6日前的MID+13*7日前的MID+12*8日前的MID+11*9日前的MID+10*10日前的MID+9*11日前的MID+8*12日前的MID+7*13日前的MID+6*14日前的MID+5*15日前的MID+4*16日前的MID+3*17日前的MID+2*18日前的MID+20日前的MID)/210
    输出MADKX:DKX的M日简单移动平均
    '''
    MID=(3*CLOSE+LOW+OPEN+HIGH)/6
    DKX=(20*MID+19*REF(MID,1)+18*REF(MID,2)+17*REF(MID,3)+
    16*REF(MID,4)+15*REF(MID,5)+14*REF(MID,6)+
    13*REF(MID,7)+12*REF(MID,8)+11*REF(MID,9)+
    10*REF(MID,10)+9*REF(MID,11)+8*REF(MID,12)+
    7*REF(MID,13)+6*REF(MID,14)+5*REF(MID,15)+
    4*REF(MID,16)+3*REF(MID,17)+2*REF(MID,18)+REF(MID,20))/210
    MADKX=MA(DKX,M)
    return DKX,MADKX
#*******************************************
#******************************************
#趋势类型
def ASI(OPEN,CLOSE,HIGH,LOW,M1=26,M2=10):   
    '''
     振动升降指标
    '''        
    LC=REF(CLOSE,1)
    AA=ABS(HIGH-LC)   
    BB=ABS(LOW-LC)
    CC=ABS(HIGH-REF(LOW,1))  
    DD=ABS(LC-REF(OPEN,1))
    R=IF( (AA>BB) & (AA>CC),AA+BB/2+DD/4,IF( (BB>CC) & (BB>AA),BB+AA/2+DD/4,CC+DD/4))
    X=(CLOSE-LC+(CLOSE-OPEN)/2+LC-REF(OPEN,1))
    SI=16*X/R*MAX(AA,BB)
    ASI=SUM(SI,M1)
    ASIT=MA(ASI,M2)
    return ASI,ASIT  
def CHO(CLOSE,OPEN,LOW,HIGH,VOL,N1=10,N2=20,M=6):
    '''
    佳庆指标
    MID赋值:成交量(手)*(2*收盘价-最高价-最低价)/(最高价+最低价)的历史累和
    输出佳庆指标:MID的N1日简单移动平均-MID的N2日简单移动平均
    输出MACHO:CHO的M日简单移动平均
    '''
    MID=SUM(VOL*(2*CLOSE-HIGH-LOW)/(HIGH+LOW),0)
    CHO=MA(MID,N1)-MA(MID,N2)
    MACHO=MA(CHO,M)
    return CHO,MACHO
def DMA_XT(CLOSE,N1=10,N2=50,M=10):
    '''
    平均差
    输出DIF:收盘价的N1日简单移动平均-收盘价的N2日简单移动平均
    输出DIFMA:DIF的M日简单移动平均
    '''
    DIF=MA(CLOSE,N1)-MA(CLOSE,N2)
    DIFMA=MA(DIF,M)
    return DIF,DIFMA
def DMI(CLOSE,HIGH,LOW,N=14,M=6):
    '''
    趋向指标
    MTR赋值:最高价-最低价和最高价-1日前的收盘价的绝对值的较大值和1日前的收盘价-最低价的绝对值的较大值的N日累和
    赋值:最高价-1日前的最高价
    赋值:1日前的最低价-最低价
    DMP赋值:如果HD>0并且HD>LD,返回HD,否则返回0的N日累和
    DMM赋值:如果LD>0并且LD>HD,返回LD,否则返回0的N日累和
    输出PDI: DMP*100/MTR
    输出MDI: DMM*100/MTR
    输出ADX: MDI-PDI的绝对值/(MDI+PDI)*100的M日简单移动平均
    输出ADXR:(ADX+M日前的ADX)/2
    '''
    MTR=SUM(MAX(MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1))),ABS(REF(CLOSE,1)-LOW)),N)
    HD =HIGH-REF(HIGH,1)
    LD =REF(LOW,1)-LOW
    list_A=[]
    list_B=[]
    for m,n in zip(LD>0,LD>HD):
        if m==n and m==True:
            list_A.append(True)
        else:
            list_A.append(False)
    for i,j in zip(LD>0,LD>HD):
        if i==j and i==True:
            list_B.append(True)
        else:
            list_B.append(False)
    DMP=SUM(IF(list_A,HD,0),N)
    DMM=SUM(IF(list_B,LD,0),N)
    PDI= DMP*100/MTR
    MDI=DMM*100/MTR
    ADX=MA(ABS(MDI-PDI)/(MDI+PDI)*100,M)
    ADXR=(ADX+REF(ADX,M))/2
    return PDI,MDI,ADX,ADXR
def DPO(CLOSE,N=21,M=6):
    '''
    区间震荡线
    输出区间震荡线:收盘价-N/2+1日前的收盘价的N日简单移动平均
    输出MADPO:DPO的M日简单移动平均
    '''
    #print(REF(MA(CLOSE,N),N/2))
    DPO=CLOSE-REF(MA(CLOSE,7),6)
    MADPO=MA(DPO,M)
    return DPO,MADPO
def EMV(HIGH,LOW,VOL,N=14,M=9):
    '''
    简易波动指标
    VOLUME赋值:成交量(手)的N日简单移动平均/成交量(手)
    MID赋值:100*(最高价+最低价-1日前的最高价+最低价)/(最高价+最低价)
    输出EMV:MID*VOLUME*(最高价-最低价)/最高价-最低价的N日简单移动平均的N日简单移动平均
    输出MAEMV:EMV的M日简单移动平均
    '''
    VOLUME=MA(VOL,N)/VOL
    MID=100*(HIGH+LOW-REF(HIGH+LOW,1))/(HIGH+LOW)
    EMV=MA(MID*VOLUME*(HIGH-LOW)/MA(HIGH-LOW,N),N)
    MAEMV=MA(EMV,M)
    return EMV,MAEMV
def MACD(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    平滑异同平均线
    输出DIF:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:(DIF-DEA)*2,COLORSTICK
    '''
    DIF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIF,MID)
    MACD=(DIF-DEA)*2
    return DIF,DEA,MACD
def VMACD(VOL,SHORT=12,LONG=26,MID=9):
    '''
    量平滑异同平均线
    输出DIF:成交量(手)的SHORT日指数移动平均-成交量(手)的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:DIF-DEA,COLORSTICK
    '''
    DIF=EMA(VOL,SHORT)-EMA(VOL,LONG)
    DEA=EMA(DIF,MID)
    MACD=DIF-DEA
    return DIF,DEA,MACD
def SMACD(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    单线平滑异同平均线
    DIF赋值:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:DIF,COLORSTICK
    '''
    DIF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIF,MID)
    MACD=DIF
    return DEA,MACD
def QACD(CLOSE,N1=12,N2=12,M=9):
    '''
    快速异同平均线
    输出DIF:收盘价的N1日指数移动平均-收盘价的N2日指数移动平均
    输出平滑异同平均线:DIF的M日指数移动平均
    输出DDIF:DIF-MACD
    '''
    DIF=EMA(CLOSE,N1)-EMA(CLOSE,N2)
    MACD=EMA(DIF,M)
    DDIF=DIF-MACD
    return DIF,MACD,DDIF
def TRIX(CLOSE,N=12,M=9):
    '''
    三重指数平均线
    MTR赋值:收盘价的N日指数移动平均的N日指数移动平均的N日指数移动平均
    输出三重指数平均线:(MTR-1日前的MTR)/1日前的MTR*100
    输出MATRIX:TRIX的M日简单移动平均 
    '''
    MTR=EMA(EMA(EMA(CLOSE,N),N),N)
    TRIX=(MTR-REF(MTR,1))/REF(MTR,1)*100
    MATRIX=MA(TRIX,M) 
    return TRIX,MATRIX
def UOS(CLOSE,HIGH,LOW,N1=7,N2=14,N3=28,M=6):
    '''
    终极指标
    TH赋值:最高价和1日前的收盘价的较大值
    TL赋值:最低价和1日前的收盘价的较小值
    ACC1赋值:收盘价-TL的N1日累和/TH-TL的N1日累和
    ACC2赋值:收盘价-TL的N2日累和/TH-TL的N2日累和
    ACC3赋值:收盘价-TL的N3日累和/TH-TL的N3日累和
    输出终极指标:(ACC1*N2*N3+ACC2*N1*N3+ACC3*N1*N2)*100/(N1*N2+N1*N3+N2*N3)
    输出MAUOS:UOS的M日指数平滑移动平均
    '''
    TH=MAX(HIGH,REF(CLOSE,1))
    TL=MIN(LOW,REF(CLOSE,1))
    ACC1=SUM(CLOSE-TL,N1)/SUM(TH-TL,N1)
    ACC2=SUM(CLOSE-TL,N2)/SUM(TH-TL,N2)
    ACC3=SUM(CLOSE-TL,N3)/SUM(TH-TL,N3)
    UOS=(ACC1*N2*N3+ACC2*N1*N3+ACC3*N1*N2)*100/(N1*N2+N1*N3+N2*N3)
    MAUOS=EXPMEMA(pd.Series(UOS),M)
    return UOS,np.array(MAUOS)
def VTP(CLOSE,VOL,N=51,M=6):
    '''
    量价曲线
    输出量价曲线:成交量(手)*(收盘价-1日前的收盘价)/1日前的收盘价的N日累和
    输出MAVPT:VPT的M日简单移动平均
    '''
    VPT=SUM(VOL*(CLOSE-REF(CLOSE,1))/REF(CLOSE,1),N)
    MAVP=MA(VPT,M)
    return VPT,MAVP
def WVAD(CLOSE,OPEN,HIGH,LOW,VOL,N=24,M=6):
    '''
    威廉变异离散量
    输出WVAD:(收盘价-开盘价)/(最高价-最低价)*成交量(手)的N日累和/10000
    输出MAWVAD:WVAD的M日简单移动平均
    '''
    WVAD=SUM((CLOSE-OPEN)/(HIGH-LOW)*VOL,N)/10000
    MAWVAD=MA(WVAD,M)
    return WVAD,MAWVAD
def DBQR(CLOSE,N=5,M1=10,M2=20,M3=60):
    '''
    对比强弱(需下载日线)
    输出ZS:(大盘的收盘价-N日前的大盘的收盘价)/N日前的大盘的收盘价
    输出GG:(收盘价-N日前的收盘价)/N日前的收盘价
    输出MADBQR1:GG的M1日简单移动平均
    输出MADBQR2:GG的M2日简单移动平均
    输出MADBQR3:GG的M3日简单移动平均
    '''
    ZS=(INDEXC-REF(INDEXC,N))/REF(INDEXC,N)
    GG=(CLOSE-REF(CLOSE,N))/REF(CLOSE,N)
    MADBQR1=MA(GG,M1)
    MADBQR2=MA(GG,M2)
    MADBQR3=MA(GG,M3)
    return ZS,GG,MADBQR1,MADBQR2,MADBQR3
def JS(CLOSE,N=5,M1=5,M2=10,M3=20):
    '''
    加数线
    输出加速线:100*(收盘价-N日前的收盘价)/(N*N日前的收盘价)
    输出MAJS1:JS的M1日简单移动平均
    输出MAJS2:JS的M2日简单移动平均
    输出MAJS3:JS的M3日简单移动平均
    '''
    JS=100*(CLOSE-REF(CLOSE,N))/(N*REF(CLOSE,N))
    MAJS1=MA(JS,M1)
    MAJS2=MA(JS,M2)
    MAJS3=MA(JS,M3)
    return JS,MAJS1,MAJS2,MAJS3
def CYE(CLOSE):
    '''
    市场趋势
    MAL赋值:收盘价的5日简单移动平均
    MAS赋值:收盘价的20日简单移动平均的5日简单移动平均
    输出CYEL:(MAL-1日前的MAL)/1日前的MAL*100
    输出CYES:(MAS-1日前的MAS)/1日前的MAS*100
    '''
    MAL=MA(CLOSE,5)
    MAS=MA(MA(CLOSE,20),5)
    CYEL=(MAL-REF(MAL,1))/REF(MAL,1)*100
    CYES=(MAS-REF(MAS,1))/REF(MAS,1)*100
    return CYEL,CYES
def QR(CLOSE,N=21):
    '''
    强弱指标(需下载日线)
    NN赋值:收盘价的有效数据周期数和N的较小值
    输出 个股: (收盘价-NN日前的收盘价)/NN日前的收盘价*100
    输出 大盘: (大盘的收盘价-NN日前的大盘的收盘价)/NN日前的大盘的收盘价*100
    输出 强弱值:个股-大盘的2日指数移动平均,COLORSTICK
    '''
    NN=MIN(BARSCOUNT(CLOSE),N)
    GG=(CLOSE-REF(CLOSE,NN))/REF(CLOSE,NN)*100
    DP=(INDEXC-REF(INDEXC,NN))/REF(INDEXC,NN)*100
    value=EMA(GG-DP,2)
    return GG,DP,value
def GDX(CLOSE,HIGH,LOW,N=30,M=9):
    '''
    轨道线
    AA赋值:(2*收盘价+最高价+最低价)/4-收盘价的N日简单移动平均的绝对值/收盘价的N日简单移动平均
    输出 轨道:以AA为权重收盘价的动态移动平均
    输出压力线:(1+M/100)*轨道
    输出 支撑线:(1-M/100)*轨道
    '''
    AA=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,N))/MA(CLOSE,N)
    轨道 =DMA(AA,0.5)
    压力线=(1+M/100)*轨道 
    支撑线=(1-M/100)*轨道
    return 轨道,压力线,支撑线
def JLHB(CLOSE,LOW,N=7,M=5):
    '''
    绝路航标
    VAR1赋值:(收盘价-60日内最低价的最低值)/(60日内最高价的最高值-60日内最低价的最低值)*80
    输出 B:VAR1的N日[1日权重]移动平均
    输出 VAR2:B的M日[1日权重]移动平均
    输出 绝路航标:如果B上穿VAR2ANDB<40,返回50,否则返回0
    '''
    VAR1=(CLOSE-LLV(LOW,60))/(HHV(HIGH,60)-LLV(LOW,60))*80
    B=SMA(VAR1,N,1)
    VAR2=SMA(B,M,1)
    绝路航标=IF(np.logical_and(B,VAR2),50,0)
    return B,VAR2,绝路航标
#********************************************
#********************************************
#能量类型
def BRAR(OPEN,HIGH,LOW,N=26):
    '''
    情绪指标
    输出BR:0和最高价-1日前的收盘价的较大值的N日累和/0和1日前的收盘价-最低价的较大值的N日累和*100
    输出AR:最高价-开盘价的N日累和/开盘价-最低价的N日累和*100
    '''
    BR=SUM(MAX(0,HIGH-REF(CLOSE,1)),N)/SUM(MAX(0,REF(CLOSE,1)-LOW),N)*100
    AR=SUM(HIGH-OPEN,N)/SUM(OPEN-LOW,N)*100
    return BR,AR
def CR(HIGH,LOW,N=26,M1=10,M2=20,M3=40,M4=60):
    '''
    带状能量线
    MID赋值:1日前的最高价+最低价/2
    输出带状能量线:0和最高价-MID的较大值的N日累和/0和MID-最低价的较大值的N日累和*100
    输出MA1:M1/2.5+1日前的CR的M1日简单移动平均
    输出均线:M2/2.5+1日前的CR的M2日简单移动平均
    输出MA3:M3/2.5+1日前的CR的M3日简单移动平均
    输出MA4:M4/2.5+1日前的CR的M4日简单移动平均
    '''
    MID=REF(HIGH+LOW,1)/2
    CR=SUM(MAX(0,HIGH-MID),N)/SUM(MAX(0,MID-LOW),N)*100
    MA1=pd.DataFrame(CR).shift(11).mean()
    MA2=pd.DataFrame(CR).shift(5).mean()
    MA3=pd.DataFrame(CR).shift(17).mean()
    MA4=pd.DataFrame(CR).shift(25).mean()
    return CR,MA1,MA2,MA3,MA4
def MASS(HIGH,LOW,N1=9,N2=25,M=6):
    '''
    梅斯线
    输出梅斯线:最高价-最低价的N1日简单移动平均/最高价-最低价的N1日简单移动平均的N1日简单移动平均的N2日累和
    输出MAMASS:MASS的M日简单移动平均
    '''
    MASS=SUM(MA(HIGH-LOW,N1)/MA(MA(HIGH-LOW,N1),N1),N2)
    MAMASS=MA(MASS,M)
    return MASS,MAMASS
def PSY(CLOSE,N=12,M=6):
    '''
    心理线
    输出PSY:统计N日中满足收盘价>1日前的收盘价的天数/N*100
    输出PSYMA:PSY的M日简单移动平均
    '''
    PSY=COUNT(CLOSE>REF(CLOSE,1),N)/N*100
    PSYMA=MA(PSY,M)
    return PSY,PSYMA
def VR(CLOSE,N=26,M=6):
    '''
    成交量变异率
    TH赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回0的N日累和
    TL赋值:如果收盘价<1日前的收盘价,返回成交量(手),否则返回0的N日累和
    TQ赋值:如果收盘价=1日前的收盘价,返回成交量(手),否则返回0的N日累和
    输出VR:100*(TH*2+TQ)/(TL*2+TQ)
    输出MAVR:VR的M日简单移动平均
    '''
    TH=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N)
    TL=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N)
    TQ=SUM(IF(CLOSE==REF(CLOSE,1),VOL,0),N)
    VR=100*(TH*2+TQ)/(TL*2+TQ)
    MAVR=MA(VR,M)
    return VR,MAVR
def WAD(CLOSE,LOW,M=30):
    '''
    威廉多空力度线
    MIDA赋值:收盘价-1日前的收盘价和最低价的较小值
    MIDB赋值:如果收盘价<1日前的收盘价,返回收盘价-1日前的收盘价和最高价的较大值,否则返回0
    输出威廉多空力度线:如果收盘价>1日前的收盘价,返回MIDA,否则返回MIDB的历史累和
    输出MAWAD:WAD的M日简单移动平均
    '''
    MIDA=CLOSE-MIN(REF(CLOSE,1),LOW)
    MIDB=IF(CLOSE<REF(CLOSE,1),CLOSE-MAX(REF(CLOSE,1),HIGH),0)
    WAD=SUM(IF(CLOSE>REF(CLOSE,1),MIDA,MIDB),0)
    MAWAD=MA(WAD,M)
    return WAD,MAWAD
def EXPMEMA(CLOSE,M=5):
    '''
    指数平滑
    '''
    return pd.Series(CLOSE).ewm(span=M, adjust=False).mean().values
def PCNT(CLOSE,M=5):
    '''
    输出幅度比:(收盘价-1日前的收盘价)/收盘价*100
    输出MAPCNT:PCNT的M日指数平滑移动平均
    '''
    PCNT=(CLOSE-REF(CLOSE,1))/CLOSE*100
    MAPCNT=EXPMEMA(PCNT,M)
    return PCNT,MAPCNT
def CYR(AMOUNT,N=13,M=5):
    '''
    市场强弱
    AMOUNT成交量=price*volume
    DIVE赋值:0.01*成交额(元)的N日指数移动平均/成交量(手)的N日指数移动平均
    输出市场强弱:(DIVE/1日前的DIVE-1)*100
    输出MACYR:CYR的M日简单移动平均
    '''
    DIVE=0.01*EMA(AMOUNT,N)/EMA(VOL,N)
    CYR=(DIVE/REF(DIVE,1)-1)*100
    MACYR=MA(CYR,M)
    return CYR,MACYR
#*********************************************
#*********************************************
#能量型
def AMO(AMOUNT,M1=5,M2=10):
    '''
    成交金额
    输出AMOW:成交额(元)/10000.0,VOLSTICK
    输出AMO1:AMOW的M1日简单移动平均
    输出AMO2:AMOW的M2日简单移动平均
    '''
    AMOW=AMOUNT/10000.0
    AMO1=MA(AMOW,M1)
    AMO2=MA(AMOW,M2)
    return AMOW,AMO1,AMO2
def OBV(VOL,CLOSE,M=30):
    '''
    累积能量线
    VA赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回-成交量(手)
    输出OBV:如果收盘价=1日前的收盘价,返回0,否则返回VA的历史累和
    输出MAOBV:OBV的M日简单移动平均
    '''
    VA=IF(CLOSE>REF(CLOSE,1),VOL,-VOL)
    OBV=SUM(IF(CLOSE==REF(CLOSE,1),0,VA),0)
    MAOBV=MA(OBV,M)
    return OBV,MAOBV
def VOL_XT(VOL,M1=5,M2=10):
    '''
    成交量
    输出VOLUME:成交量(手),VOLSTICK
    输出MAVOL1:VOLUME的M1日简单移动平均
    输出MAVOL2:VOLUME的M2日简单移动平均
    '''
    VOLUME=VOL
    MAVOL1=MA(VOLUME,M1)
    MAVOL2=MA(VOLUME,M2)
    return MAVOL1,MAVOL2
def VRSI(VOl,N1=6,N2=12,N3=24):
    '''
    相对强弱量
    LC赋值:1日前的成交量(手)
    输出RSI1:成交量(手)-LC和0的较大值的N1日[1日权重]移动平均/成交量(手)-LC的绝对值的N1日[1日权重]移动平均*100
    输出RSI2:成交量(手)-LC和0的较大值的N2日[1日权重]移动平均/成交量(手)-LC的绝对值的N2日[1日权重]移动平均*100
    输出RSI3:成交量(手)-LC和0的较大值的N3日[1日权重]移动平均/成交量(手)-LC的绝对值的N3日[1日权重]移动平均*100
    '''
    LC=REF(VOL,1)
    RSI1=SMA(MAX(VOL-LC,0),N1,1)/SMA(ABS(VOL-LC),N1,1)*100
    RSI2=SMA(MAX(VOL-LC,0),N2,1)/SMA(ABS(VOL-LC),N2,1)*100
    RSI3=SMA(MAX(VOL-LC,0),N3,1)/SMA(ABS(VOL-LC),N3,1)*100
    return RSI1,RSI2,RSI3
def HSL(HSL,N=5):
    '''
    换手线
    '''
    HSL=HSL
    MAHSL=MA(HSL,N)
    return HSL,MAHSL
#******************************************
#******************************************
#均线系统
def MA_XT(CLOSE,M1=5,M2=10,M3=20,M4=60):
    '''
    均线
    输出MA1:收盘价的M1日简单移动平均
    输出均线:收盘价的M2日简单移动平均
    输出MA3:收盘价的M3日简单移动平均
    输出MA4:收盘价的M4日简单移动平均
    输出MA5:收盘价的M5日简单移动平均
    输出MA6:收盘价的M6日简单移动平均
    输出MA7:收盘价的M7日简单移动平均
    输出MA8:收盘价的M8日简单移动平均
    '''
    MA1=MA(CLOSE,M1)
    MA2=MA(CLOSE,M2)
    MA3=MA(CLOSE,M3)
    MA4=MA(CLOSE,M4)
    return MA1,MA2,MA3,MA4
def MA2(CLOSE,M1=5,M2=10,M3=20,M4=60,M5=120,M6=240,M7=360,M8=420,M9=680,M10=720):
    '''
    均线2
    输出MA1:收盘价的M1日简单移动平均
    输出均线:收盘价的M2日简单移动平均
    输出MA3:收盘价的M3日简单移动平均
    输出MA4:收盘价的M4日简单移动平均
    输出MA5:收盘价的M5日简单移动平均
    输出MA6:收盘价的M6日简单移动平均
    输出MA7:收盘价的M7日简单移动平均
    输出MA8:收盘价的M8日简单移动平均
    输出MA9:收盘价的M9日简单移动平均
    输出MA10:收盘价的M10日简单移动平均
    '''
    MA1=MA(CLOSE,M1)
    MA2=MA(CLOSE,M2)
    MA3=MA(CLOSE,M3)
    MA4=MA(CLOSE,M4)
    MA5=MA(CLOSE,M5)
    MA6=MA(CLOSE,M6)
    MA7=MA(CLOSE,M7)
    MA8=MA(CLOSE,M8)
    MA9=MA(CLOSE,M9)
    MA10=MA(CLOSE,M10)
    return MA1,MA2,MA3,MA4,MA5,MA6,MA7,MA8,MA8,MA9,MA10
def ACD(CLOSE,HIGH,LOW,M=20):
    '''
    升降线
    LC赋值:1日前的收盘价
    DIF赋值:收盘价-如果收盘价>LC,返回最低价和LC的较小值,否则返回最高价和LC的较大值
    输出升降线:如果收盘价=LC,返回0,否则返回DIF的历史累和
    输出MAACD:ACD的M日指数平滑移动平均
    '''
    LC=REF(CLOSE,1)
    DIF=CLOSE-IF(CLOSE>LC,MIN(LOW,LC),MAX(HIGH,LC))
    ACD=SUM(IF(CLOSE==LC,0,DIF),0)
    MAACD=EXPMEMA(ACD,M)
    return ACD,MAACD
def BBI(CLOSE,M1=3,M2=6,M3=12,M4=24):
    '''
    多空均线
    输出多空均线:(收盘价的M1日简单移动平均+收盘价的M2日简单移动平均+收盘价的M3日简单移动平均+收盘价的M4日简单移动平均)/4
    '''
    BBI=(MA(CLOSE,M1)+MA(CLOSE,M2)+MA(CLOSE,M3)+MA(CLOSE,M4))/4
    return BBI
def EXPMA(CLOSE,M1=12,M2=50):
    '''
    指数平均线
    输出EXP1:收盘价的M1日指数移动平均
    输出EXP2:收盘价的M2日指数移动平均
    '''
    EXP1=EMA(CLOSE,M1)
    EXP2=EMA(CLOSE,M2)
    return EXP1,EXP2
def HMA(HIGH,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    高价平均线
    输出HMA1:最高价的M1日简单移动平均
    输出HMA2:最高价的M2日简单移动平均
    输出HMA3:最高价的M3日简单移动平均
    输出HMA4:最高价的M4日简单移动平均
    输出HMA5:最高价的M5日简单移动平均
    '''
    HMA1=MA(HIGH,M1)
    HMA2=MA(HIGH,M2)
    HMA3=MA(HIGH,M3)
    HMA4=MA(HIGH,M4)
    HMA5=MA(HIGH,M5)
    return HMA1,HMA2,HMA3,HMA4,HMA5
def LMA(LOW,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    低价平均线
    输出LMA1:最低价的M1日简单移动平均
    输出LMA2:最低价的M2日简单移动平均
    输出LMA3:最低价的M3日简单移动平均
    输出LMA4:最低价的M4日简单移动平均
    输出LMA5:最低价的M5日简单移动平均
    '''
    LMA1=MA(LOW,M1)
    LMA2=MA(LOW,M2)
    LMA3=MA(LOW,M3)
    LMA4=MA(LOW,M4)
    LMA5=MA(LOW,M5)
    return LMA1,LMA2,LMA3,LMA4,LMA5
def VMA(HIGH,OPEN,LOW,CLOSE,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    变异平均线
    VV赋值:(最高价+开盘价+最低价+收盘价)/4
    输出VMA1:VV的M1日简单移动平均
    输出VMA2:VV的M2日简单移动平均
    输出VMA3:VV的M3日简单移动平均
    输出VMA4:VV的M4日简单移动平均
    输出VMA5:VV的M5日简单移动平均
    '''
    VV=(HIGH+OPEN+LOW+CLOSE)/4
    VMA1=MA(VV,M1)
    VMA2=MA(VV,M2)
    VMA3=MA(VV,M3)
    VMA4=MA(VV,M4)
    VMA5=MA(VV,M5)
    return VMA1,VMA2,VMA3,VMA4,VMA5
def AMV(OPEN,CLOSE,VOL,M1=5,M2=13,M3=34,M4=60):
    '''
    成本均线
    AMOV赋值:成交量(手)*(开盘价+收盘价)/2
    输出AMV1:AMOV的M1日累和/成交量(手)的M1日累和
    输出AMV2:AMOV的M2日累和/成交量(手)的M2日累和
    输出AMV3:AMOV的M3日累和/成交量(手)的M3日累和
    输出AMV4:AMOV的M4日累和/成交量(手)的M4日累和
    '''
    AMOV=VOL*(OPEN+CLOSE)/2
    AMV1=SUM(AMOV,M1)/SUM(VOL,M1)
    AMV2=SUM(AMOV,M2)/SUM(VOL,M2)
    AMV3=SUM(AMOV,M3)/SUM(VOL,M3)
    AMV4=SUM(AMOV,M4)/SUM(VOL,M4)
    return AMV1,AMV2,AMV3,AMV4
def BBIBOLL(CLOSE,N=11,M=6):
    '''
    多空布林线
    CV赋值:收盘价
    输出多空布林线:(CV的3日简单移动平均+CV的6日简单移动平均+CV的12日简单移动平均+CV的24日简单移动平均)/4
    输出UPR:BBIBOLL+M*BBIBOLL的N日估算标准差
    输出DWN:BBIBOLL-M*BBIBOLL的N日估算标准差
    '''
    CV=CLOSE
    BBIBOLL=(MA(CV,3)+MA(CV,6)+MA(CV,12)+MA(CV,24))/4
    UPR=BBIBOLL+M*STD(BBIBOLL,N)
    DWN=BBIBOLL-M*STD(BBIBOLL,N)
    return BBIBOLL,UPR,DWN
def ALLIGAT(HIGH,LOW):
    '''
    鳄鱼线
    NN赋值:(最高价+最低价)/2
    输出上唇:3日前的NN的5日简单移动平均,COLOR40FF40
    输出牙齿:5日前的NN的8日简单移动平均,COLOR0000C0
    输出下颚:8日前的NN的13日简单移动平均,COLORFF4040
    '''
    H=HIGH
    L=LOW
    NN=(H+L)/2
    上唇=REF(MA(NN,5),3)
    牙齿=REF(MA(NN,8),5)
    下颚=REF(MA(NN,13),8)
    return 上唇,牙齿,下颚
def GMMA(CLOSE):
    '''
    顾比均线
    '''
    MA3=EMA(CLOSE,3)
    MA5=EMA(CLOSE,5)
    MA8=EMA(CLOSE,8)
    MA10=EMA(CLOSE,10)
    MA12=EMA(CLOSE,12)
    MA15=EMA(CLOSE,15)
    MA30=EMA(CLOSE,30)
    MA35=EMA(CLOSE,35)
    MA40=EMA(CLOSE,40)
    MA45=EMA(CLOSE,45)
    MA50=EMA(CLOSE,50)
    MA60=EMA(CLOSE,60)
    return MA3,MA5,MA8,MA10,MA12,MA15,MA30,MA35,MA40,MA45,MA50,MA60
#*******************************************
#*******************************************
#路径类
def BOLL(CLOSE,M=20):
    '''
    布林线
    输出BOLL:收盘价的M日简单移动平均
    输出UB:BOLL+2*收盘价的M日估算标准差
    输出LB:BOLL-2*收盘价的M日估算标准差
    '''
    BOLL=MA(CLOSE,M)
    UB=BOLL+2*STD(CLOSE,M)
    LB=BOLL-2*STD(CLOSE,M)
    return BOLL,UB,LB
def PBX(CLOSE,M1=4,M2=6,M3=9,M4=13,M5=18,M6=24):
    '''
    瀑布线
    输出PBX1:(收盘价的M1日指数移动平均+收盘价的M1*2日简单移动平均+收盘价的M1*4日简单移动平均)/3
    输出PBX2:(收盘价的M2日指数移动平均+收盘价的M2*2日简单移动平均+收盘价的M2*4日简单移动平均)/3
    输出PBX3:(收盘价的M3日指数移动平均+收盘价的M3*2日简单移动平均+收盘价的M3*4日简单移动平均)/3
    输出PBX4:(收盘价的M4日指数移动平均+收盘价的M4*2日简单移动平均+收盘价的M4*4日简单移动平均)/3
    输出PBX5:(收盘价的M5日指数移动平均+收盘价的M5*2日简单移动平均+收盘价的M5*4日简单移动平均)/3
    输出PBX6:(收盘价的M6日指数移动平均+收盘价的M6*2日简单移动平均+收盘价的M6*4日简单移动平均)/3
    '''
    PBX1=(EMA(CLOSE,M1)+MA(CLOSE,M1*2)+MA(CLOSE,M1*4))/3
    PBX2=(EMA(CLOSE,M2)+MA(CLOSE,M2*2)+MA(CLOSE,M2*4))/3
    PBX3=(EMA(CLOSE,M3)+MA(CLOSE,M3*2)+MA(CLOSE,M3*4))/3
    PBX4=(EMA(CLOSE,M4)+MA(CLOSE,M4*2)+MA(CLOSE,M4*4))/3
    PBX5=(EMA(CLOSE,M5)+MA(CLOSE,M5*2)+MA(CLOSE,M5*4))/3
    PBX6=(EMA(CLOSE,M6)+MA(CLOSE,M6*2)+MA(CLOSE,M6*4))/3
    return PBX1,PBX2,PBX3,PBX4,PBX5,PBX6
def ENE(CLOSE,N=25,M1=6,M2=6):
    '''
    轨道线
    输出UPPER:(1+M1/100)*收盘价的N日简单移动平均
    输出LOWER:(1-M2/100)*收盘价的N日简单移动平均
    输出轨道线:(UPPER+LOWER)/2
    '''
    UPPER=(1+M1/100)*MA(CLOSE,N)
    LOWER=(1-M2/100)*MA(CLOSE,N)
    ENE=(UPPER+LOWER)/2
    return UPPER,LOWER,ENE
def MIKE(HIGH,LOW,CLOSE,N=10):
    '''
    麦克支撑压力
    HLC赋值:1日前的(最高价+最低价+收盘价)/3的N日简单移动平均
    HV赋值:N日内最高价的最高值的3日指数移动平均
    LV赋值:N日内最低价的最低值的3日指数移动平均
    输出STOR:2*HV-LV的3日指数移动平均
    输出MIDR:HLC+HV-LV的3日指数移动平均
    输出WEKR:HLC*2-LV的3日指数移动平均
    '''
    HLC=REF(MA((HIGH+LOW+CLOSE)/3,N),1)
    HV=EMA(HHV(HIGH,N),3)
    LV=EMA(LLV(LOW,N),3)
    STOR=EMA(2*HV-LV,3)
    MIDR=EMA(HLC+HV-LV,3)
    WEKR=EMA(HLC*2-LV,3)
    WEKS=EMA(HLC*2-HV,3)
    MIDS=EMA(HLC-HV+LV,3)
    STOS=EMA(2*LV-HV,3)
    return STOR,MIDR,WEKR,WEKS,MIDS,STOS
def XS(CLOSE,VOL,N=13):
    '''
    薛斯通道
    VAR2赋值:收盘价*成交量(手)
    VAR3赋值:(VAR2的3日指数移动平均/成交量(手)的3日指数移动平均+VAR2的6日指数移动平均/成交量(手)的6日指数移动平均+VAR2的12日指数移动平均/成交量(手)的12日指数移动平均+VAR2的24日指数移动平均/成交量(手)的24日指数移动平均)/4的N日指数移动平均
    输出SUP:1.06*VAR3
    输出SDN:VAR3*0.94
    VAR4赋值:收盘价的9日指数移动平均
    输出LUP:VAR4*1.14的5日指数移动平均
    输出LDN:VAR4*0.86的5日指数移动平均
    '''
    VAR2=CLOSE*VOL
    VAR3=EMA((EMA(VAR2,3)/EMA(VOL,3)+EMA(VAR2,6)/EMA(VOL,6)+EMA(VAR2,12)/EMA(VOL,12)+EMA(VAR2,24)/EMA(VOL,24))/4,N)
    SUP=1.06*VAR3
    SDN=VAR3*0.94
    VAR4=EMA(CLOSE,9)
    LUP=EMA(VAR4*1.14,5)
    LDN=EMA(VAR4*0.86,5)
    return SUP,SDN,LUP,LDN
def XS2(CLOSE,HIGH,LOW,N=102,M=7):
    '''
    薛斯通道II
    AA赋值:(2*收盘价+最高价+最低价)/4的5日简单移动平均
    输出 通道1:AA*N/100
    输出 通道2:AA*(200-N)/100
    CC赋值:(2*收盘价+最高价+最低价)/4-收盘价的20日简单移动平均的绝对值/收盘价的20日简单移动平均
    DD赋值:以CC为权重收盘价的动态移动平均
    输出 通道3:(1+M/100)*DD
    '''
    AA=MA((2*CLOSE+HIGH+LOW)/4,5)
    通道1=AA*N/100
    通道2=AA*(200-N)/100
    CC=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,20))/MA(CLOSE,20)
    DD=DMA(CLOSE,0.5)
    通道3=(1+M/100)*DD
    通道4=(1-M/100)*DD
    return 通道1,通道2,通道3,通道4
def TQN(HIGH,LOW,X1=20,x2=20):
    '''
    唐奇安通道
    输出周期高点:1日前的X1日内最高价的最高值
    输出周期低点:1日前的X2日内最低价的最低值
    平空开多赋值:最高价>=周期高点
    平多开空赋值:最低价<=周期低点
    先平空仓再开多仓
    先平多仓再开空仓
    自动过滤交易信号
    '''
    H=HIGH
    L=LOW
    周期高点=REF(HHV(H,X1),1)
    周期低点=REF(LLV(L,X2),1)
    平空开多=HIGH>=周期高点
    平多开空=LOW<=周期低点
    return 周期高点,周期低点,平空开多,平多开空
#*******************************************
#*******************************************
#停损
def SAR(HIGH,LOW,M=10,af= 2, amax=20):
    '''
    抛物线指标
    '''
    af=af/100
    amax=amax/100
    data=pd.DataFrame()
    data['high']=HIGH
    data['low']=LOW
    data['high - low']=data['high']-data['low']
    high, low =data['high'].shift(M),data['low'].shift(M)

        # Starting values
    sig0, xpt0, af0 = True, high.tolist()[0], af
    _sar = [low.tolist()[0] - data['high - low'].std()]

    for i in range(1, len(LOW)):
        sig1, xpt1, af1 = sig0, xpt0, af0

        lmin = min(low.tolist()[i - 1], low.tolist()[i])
        lmax = max(high.tolist()[i - 1], high.tolist()[i])

        if sig1:
            sig0 = low.tolist()[i] > _sar[-1]
            xpt0 = max(lmax, xpt1)
        else:
            sig0 = high.tolist()[i] >= _sar[-1]
            xpt0 = min(lmin, xpt1)

        if sig0 == sig1:
            sari = _sar[-1] + (xpt1 - _sar[-1]) * af1
            af0 = min(amax, af1 + af)

            if sig0:
                af0 = af0 if xpt0 > xpt1 else af1
                sari = min(sari, lmin)
            else:
                af0 = af0 if xpt0 < xpt1 else af1
                sari = max(sari, lmax)
        else:
            af0 = af
            sari = xpt0

        _sar.append(sari)

    return _sar
#*******************************
#******************************
#交易类型
def MA_交易(CLOSE,SHORT=5,LONG=20):
    '''
    MA_交易
    MA1赋值:收盘价的SHORT日简单移动平均
    MA2赋值:收盘价的LONG日简单移动平均
    平空开多赋值:MA1上穿MA2
    平多开空赋值:MA2上穿MA1
    先平空仓再开多仓
    先平多仓再开空仓
    '''
    MA1=MA(CLOSE,SHORT)
    MA2=MA(CLOSE,LONG)
    平空开多=CROSS(MA1,MA2)
    平多开空=CROSS(MA2,MA1)
    return MA1,MA2,平空开多,平多开空
def MACD_交易(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    MACD交易
    DIFF赋值:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    DEA赋值:DIFF的MID日指数移动平均
    MACD赋值:2*(DIFF-DEA)
    平空开多赋值:MACD上穿0
    平多开空赋值:0上穿MACD
    先平空仓再开多仓
    '''
    DIFF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIFF,MID)
    MACD=2*(DIFF-DEA)
    平空开多=CROSS(MACD,0)
    平空开多=CROSS(0,MACD)
    return DIFF,DEA,MACD,平空开多,平空开多
def KDJ_交易(CLOSE,HIGH,LOW,N=9,M1=3):
    '''
    KDJ交易
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    K赋值:RSV的M1日[1日权重]移动平均
    D赋值:K的M1日[1日权重]移动平均
    J赋值:3*K-2*D
    平空开多赋值:J上穿0
    平多开空赋值:100上穿J
    先平空仓再开多仓
    先平多仓再开空仓
    自动过滤交易信号
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M1,1)
    J=3*K-2*D
    平空开多=CROSS(J,0)
    平多开空=CROSS(100,J)
    return K,D,J,平空开多,平多开空
#*****************************************
#*****************************************
#神系
def SG_XDT(CLOSE,INDEXC,P1=5,P2=10):
    '''
    心电图(需下载日线)
    输出强弱指标(需下载日线):收盘价/大盘的收盘价*1000
    输出MQR1:QR的5日简单移动平均
    输出MQR2:QR的10日简单移动平均
    ''' 
    QR=CLOSE/INDEXC*1000
    MQR1=MA(QR,5)
    MQR2=MA(QR,10)
    return QR,MQR1,MQR2
def SG_NDB(CLOSE,HIGH,LOW,P1=5,P2=10):
    '''
    脑电波(神系)
    HH赋值:如果收盘价/1日前的收盘价>1.093ANDL>1日前的最高价,返回2*收盘价-1日前的收盘价-最高价,否则返回2*收盘价-最高价-最低价
    V1赋值:收盘价的有效数据周期数
    V2赋值:2*V1日前的收盘价-V1日前的最高价-V1日前的最低价
    输出DK:HH的历史累和+V2
    输出MDK1:DK的P1日简单移动平均
    输出MDK2:DK的P2日简单移动平均
    '''
    C=CLOSE
    H=HIGH
    L=LOW
    HH=IF(np.logical_or(C/REF(C,1)>1.093 ,L>REF(H,1)),2*C-REF(C,1)-H,2*C-H-L)
    V1=1
    V2=2*REF(C,V1)-REF(H,V1)-REF(L,V1)
    DK=SUM(HH,0)+V2
    MDK1=MA(DK,P1)
    MDK2=MA(DK,P2)
    return DK,MDK1,MDK2
def SG_SMX(CLOSE,HIGH,LOW,INDEXH,INDEXL,INDEXC,N=50):
    '''
    生命线(需下载日线)
    INDEXH,INDEXL,INDEXC指数的高，低收盘价,可以通过akshare.stock_zh_a_daily(sybol='sh000001')获取
    H1赋值:N日内最高价的最高值
    L1赋值:N日内最低价的最低值
    H2赋值:N日内大盘的最高价的最高值
    L2赋值:N日内大盘的最低价的最低值
    ZY赋值:收盘价/大盘的收盘价*2000
    输出ZY1:ZY的3日指数移动平均
    输出ZY2:ZY的17日指数移动平均
    输出ZY3:ZY的34日指数移动平均
    '''
    H1=HHV(HIGH,N)
    L1=LLV(LOW,N)
    H2=HHV(INDEXH,N)
    L2=LLV(INDEXL,N)
    ZY=CLOSE/INDEXC*2000
    ZY1=EMA(ZY,3)
    ZY2=EMA(ZY,17)
    ZY3=EMA(ZY,34)
    return ZY1,ZY2,ZY3
def SG_LB(VOl,INDEXV):
    '''
    量比(需下载日线)
    VOl个股成交量，INDXEXV大盘成交量，可以通过ak.stock_zh_a_daily()获取
    ZY2赋值:成交量(手)/大盘的成交量*1000
    输出量比:ZY2
    输出MA5:ZY2的5日简单移动平均
    输出MA10:ZY2的10日简单移动平均
    '''
    ZY2=VOL/INDEXV*1000
    量比=ZY2
    MA5=MA(ZY2,5)
    MA10=MA(ZY2,10)
    return 量比,MA5,MA10
def SG_PF(CLOSE,INDEXV):
    '''
    强势股评分(需下载日线)
    ZY1赋值:收盘价/大盘的收盘价*1000
    A1赋值:如果ZY1>3日内ZY1的最高值,返回10,否则返回0
    A2赋值:如果ZY1>5日内ZY1的最高值,返回15,否则返回0
    A3赋值:如果ZY1>10日内ZY1的最高值,返回20,否则返回0
    A4赋值:如果ZY1>2日内ZY1的最高值,返回10,否则返回0
    A5赋值:统计9日中满足ZY1>1日前的ZY1的天数*5
    输出强势股评分:A1+A2+A3+A4+A5
    '''
    ZY1=CLOSE/INDEXC*1000
    A1=IF(ZY1>HHV(ZY1,3),10,0)
    A2=IF(ZY1>HHV(ZY1,5),15,0)
    A3=IF(ZY1>HHV(ZY1,10),20,0)
    A4=IF(ZY1>HHV(ZY1,2),10,0)
    A5=COUNT(ZY1>REF(ZY1,1) ,9)*5
    强势股评分=A1+A2+A3+A4+A5
    return 强势股评分
#*************************************************
#*************************************************
#龙系
def RAD(OPEN,HIGH,CLOSE,LOW,INDEXO,INDEXH,INDEXL,INDEXC,D=3,S=30,M=30):
    '''
    威力雷达(需下载日线)
    OPEN+HIGH+CLOSE+LOW个股
    INDEXO+INDEXH+INDEXL+INDEXC大盘数据，可以通过akshare获取
    SM赋值:(开盘价+最高价+收盘价+最低价)/4
    SMID赋值:SM的D日简单移动平均
    IM赋值:(大盘的开盘价+大盘的最高价+大盘的最低价+大盘的收盘价)/4
    IMID赋值:IM的D日简单移动平均
    SI1赋值:(SMID-1日前的SMID)/SMID
    II赋值:(IMID-1日前的IMID)/IMID
    输出RADER1:(SI1-II)*2的S日累和*1000
    输出RADERMA:RADER1的M日[1日权重]移动平均
    '''
    SM=(OPEN+HIGH+CLOSE+LOW)/4
    SMID=MA(SM,D)
    IM=(INDEXO+INDEXH+INDEXL+INDEXC)/4
    IMID=MA(IM,D)
    SI1=(SMID-REF(SMID,1))/SMID
    II=(IMID-REF(IMID,1))/IMID
    RADER1=SUM((SI1-II)*2,S)*1000
    RADERMA=SMA(RADER1,M,1)
    return RADER1,RADERMA
    return 
def LON(CLOSE,HIGH,LOW,VOL,N=10):
    '''
    龙系长线
    赋值: 1日前的收盘价
    赋值: 成交量(手)的2日累和/(((2日内最高价的最高值-2日内最低价的最低值))*100)
    赋值: (收盘价-LC)*VID
    赋值: RC的历史累和
    赋值: LONG的10日[1日权重]移动平均
    赋值: LONG的20日[1日权重]移动平均
    输出龙系长线 : DIFF-DEA
    输出LONMA : 龙系长线的N日简单移动平均
    输出LONT : 龙系长线, COLORSTICK
    '''
    LC = REF(CLOSE,1)
    VID = SUM(VOL,2)/(((HHV(HIGH,2)-LLV(LOW,2)))*100)
    RC = (CLOSE-LC)*VID
    LONG = SUM(RC,0)
    DIFF = SMA(LONG,10,1)
    DEA = SMA(LONG,20,1)
    LON = DIFF-DEA
    LONMA = MA(LON,N)
    LONT = LON
    return LON,LONMA,LONT
def SHT(CLOSE,VOL,N=5):
    '''
    龙系短线
    VAR1赋值:(成交量(手)-1日前的成交量(手))/1日前的成交量(手)的5日简单移动平均
    VAR2赋值:(收盘价-收盘价的24日简单移动平均)/收盘价的24日简单移动平均*100
    输出MY: VAR2*(1+VAR1)
    输出龙系短线: MY, COLORSTICK
    输出SHTMA: SHT的N日简单移动平均
    '''
    VAR1=MA((VOL-REF(VOL,1))/REF(VOL,1),5)
    VAR2=(CLOSE-MA(CLOSE,24))/MA(CLOSE,24)*100
    MY= VAR2*(1+VAR1)
    SHT= MY#COLORSTICK
    SHTMA= MA(SHT,N)
    return SHT,SHTMA
def ZLJC(CLOSE,LOW,HIGH):
    '''
    主力进出
    VAR1赋值:(收盘价+最低价+最高价)/3
    VAR2赋值:((VAR1-1日前的最低价)-(最高价-VAR1))*成交量(手)/100000/(最高价-最低价)的历史累和
    VAR3赋值:VAR2的1日指数移动平均
    输出 JCS:VAR3
    输出 JCM:VAR3的12日简单移动平均
    输出 JCL:VAR3的26日简单移动平均
    '''
    VAR1=(CLOSE+LOW+HIGH)/3
    VAR2=SUM(((VAR1-REF(LOW,1))-(HIGH-VAR1))*VOL/100000/(HIGH-LOW),0)
    VAR3=EMA(VAR2,1)
    JCS=VAR3
    JCM=MA(VAR3,12)
    JCL=MA(VAR3,26)
    return JCS,JCM,JCL
def ZLMM(CLOSE):
    '''
    赋值:1日前的收盘价
    RSI2赋值:收盘价-LC和0的较大值的12日[1日权重]移动平均/收盘价-LC的绝对值的12日[1日权重]移动平均*100
    RSI3赋值:收盘价-LC和0的较大值的18日[1日权重]移动平均/收盘价-LC的绝对值的18日[1日权重]移动平均*100
    输出MMS:3*RSI2-2*收盘价-LC和0的较大值的16日[1日权重]移动平均/收盘价-LC的绝对值的16日[1日权重]移动平均*100的3日简单移动平均
    输出MMM:MMS的8日指数移动平均
    输出MML:3*RSI3-2*收盘价-LC和0的较大值的12日[1日权重]移动平均/收盘价-LC的绝对值的12日[1日权重]移动平均*100的5日简单移动平均
    '''
    LC =REF(CLOSE,1)
    RSI2=SMA(MAX(CLOSE-LC,0),12,1)/SMA(ABS(CLOSE-LC),12,1)*100
    RSI3=SMA(MAX(CLOSE-LC,0),18,1)/SMA(ABS(CLOSE-LC),18,1)*100
    MMS=MA(3*RSI2-2*SMA(MAX(CLOSE-LC,0),16,1)/SMA(ABS(CLOSE-LC),16,1)*100,3)
    MMM=EMA(MMS,8)
    MML=MA(3*RSI3-2*SMA(MAX(CLOSE-LC,0),12,1)/SMA(ABS(CLOSE-LC),12,1)*100,5)
    return MMS,MMM,MML
def SLZT(CLOSE,LOW):
    '''
    神龙在天
    输出白龙: 收盘价的125日简单移动平均
    输出黄龙: 白龙+2*收盘价的170日估算标准差
    输出紫龙: 白龙-2*收盘价的145日估算标准差
    输出青龙: 步长为1极限值为7的125日抛物转向, LINESTICK
    VAR2赋值:70日内最高价的最高值
    VAR3赋值:20日内最高价的最高值
    输出红龙: VAR2*0.83
    输出蓝龙: VAR3*0.91
    '''
    白龙=MA(CLOSE,125)
    黄龙=白龙+2*STD(CLOSE,170)
    紫龙=白龙-2*STD(CLOSE,145)
    青龙=SAR(HIGH,LOW,125,1,7)# LINESTICK;
    VAR2=HHV(HIGH,70)
    VAR3=HHV(HIGH,20)
    红龙= VAR2*0.83
    蓝龙=VAR3*0.91
    return 白龙,黄龙,紫龙,青龙,红龙,蓝龙
def ADVOL(CLOSE,HIGH,LOW,VOL):
    '''
    龙系离散量
    A赋值:((收盘价-最低价)-(最高价-收盘价))*成交量(手)/10000/(最高价-最低价)的历史累和
    输出龙系离散量:A
    输出MA1:A的30日简单移动平均
    输出均线:MA1的100日简单移动平均
    '''
    A=SUM(((CLOSE-LOW)-(HIGH-CLOSE))*VOL/10000/(HIGH-LOW),0)
    ADVOL=A
    MA1=MA(A,30)
    MA2=MA(MA1,100)
    return ADVOL,MA1,MA2
#*********************************************
#*********************************************
#鬼系
def CYC(code='sh600031',start_date='20210101',end_date='20221022',P1=5,P2=13,P3=34):
    '''
    成本均线
    JJJ赋值:如果总量>0.01,简单理解流通股,返回0.01*总金额/总量,否则返回昨收盘价
    DDD赋值:(最高价<0.01 或者 最低价<0.01)
    JJJT赋值:如果DDD,返回1,否则返回(JJJ<(最高价+0.01)并且JJJ>(最低价-0.01))
    输出CYC1:如果JJJT,返回0.01*成交额(元)的P1日指数移动平均/成交量(手)的P1日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P1日指数移动平均
    输出CYC2:如果JJJT,返回0.01*成交额(元)的P2日指数移动平均/成交量(手)的P2日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P2日指数移动平均
    输出CYC3:如果JJJT,返回0.01*成交额(元)的P3日指数移动平均/成交量(手)的P3日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P3日指数移动平均
    输出CYC∞:如果JJJT,返回以100*成交量(手)/流通股本(股)为权重成交额(元)/(100*成交量(手))的动态移动平均,否则返回(最高价+最低价+收盘价)/3的120日指数移动平均
    '''
    pass
    def DYNAINFO_10(M=10):
        '''
        总金额=price*volume
        '''
        result=df['close']*df['volume']
        return result
    def DYNAINFO_3(M=3):
        '''
        昨日收盘价
        '''
        return df['close'].shift(1)
    def DYNAINFO_5(M=5):
        '''
        最高价
        '''
        return df['high']
    def DYNAINFO_6(M=6):
        '''
        最低价
        '''
        return df['low']
    AMOUNT=AMOUNT=df['close']*df['volume']
    VOL=df['volume']
    HIGH=df['high']
    LOW=df['low']
    CLOSE=df['close']
    def FINANCE_7(M=7):
        '''
        100*成交量
        '''
        return 100*df['volume']
    JJJ=IF(DYNAINFO_8(8)>0.01,0.01*DYNAINFO_10(10)/DYNAINFO_8(8),DYNAINFO_3(3))
    DDD=np.logical_or(DYNAINFO_5(5)<0.01,DYNAINFO_6(6)<0.01)
    JJJT=IF(DDD,False,np.logical_and(JJJ<(DYNAINFO_5(5)+0.01),JJJ>(DYNAINFO_6(6)-0.01)))
    CYC1=IF(JJJT,0.01*EMA(AMOUNT,P1)/EMA(VOL,P1),EMA((HIGH+LOW+CLOSE)/3,P1))
    CYC2=IF(JJJT,0.01*EMA(AMOUNT,P2)/EMA(VOL,P2),EMA((HIGH+LOW+CLOSE)/3,P2))
    CYC3=IF(JJJT,0.01*EMA(AMOUNT,P3)/EMA(VOL,P3),EMA((HIGH+LOW+CLOSE)/3,P3))
    #CYC_a=IF(JJJT,DMA(AMOUNT/(100*VOL),100*VOL/FINANCE_7(7)),EMA((HIGH+LOW+CLOSE)/3,120))
    return CYC1,CYC2,CYC3
def CYS(CLOSE,AMOUNT,VOL):
    '''
    市场盈亏
    AMOUNT成交额，VOL成交量
    CYC13赋值:0.01*成交额(元)的13日指数移动平均/成交量(手)的13日指数移动平均
    输出市场盈亏:(收盘价-CYC13)/CYC13*100
    '''
    CYC13=0.01*EMA(AMOUNT,13)/EMA(VOL,13)
    CYS=(CLOSE-CYC13)/CYC13*100
    return CYS
def CYQKL(CLOSE,OPEN):
    '''
    博弈K线长度
    输出KL:100*(以收盘价计算的获利盘比例-以开盘价计算的获利盘比例)
    '''
    KL=100*(WINNER(CLOSE)-WINNER(OPEN))
    return KL
def CYW(CLOSE,HIGH,LOW,VOL):
    '''
    主力控盘
    VAR1赋值:收盘价-最低价
    VAR2赋值:最高价-最低价
    VAR3赋值:收盘价-最高价
    VAR4赋值:如果最高价>最低价,返回(VAR1/VAR2+VAR3/VAR2)*成交量(手),否则返回0
    输出主力控盘: VAR4的10日累和/10000, COLORSTICK
    '''
    VAR1=CLOSE-LOW
    VAR2=HIGH-LOW
    VAR3=CLOSE-HIGH
    VAR4=IF(HIGH>LOW,(VAR1/VAR2+VAR3/VAR2)*VOL,0)
    CYW=SUM(VAR4,10)/10000 #COLORSTICK
    return CYW
#***************************************************
#***************************************************
#其他系
def PEAK(CLOSE,N,n=1):
    '''
    计算倾效
    np.polyfit(range(N),x,deg=1)
    '''
    pass
def TROUGH(CLOSE,N,n=1):
    '''
    箱底
    '''
    pass
def XT(CLOSE):
    '''
    箱体
    '''
    箱顶=PEAK(CLOSE,N,1)*0.98
    箱底=TROUGH(CLOSE,N,1)*1.02
    箱高=100*(箱顶-箱底)/箱底,#NODRAW
def  MOD(M,N):
    '''
    计算模
    M/N的余数
    '''
    return M//N
def SQJZ(CLSOE):
    '''
    N赋值:到最后交易的周期
    B赋值:收盘价<4日前的收盘价
    T1赋值: 条件连续成立次数
    A_B1赋值:(T1>9) AND T1关于9的模=1
    A_B2赋值:(T1>9) AND T1关于9的模=2
    A_B8赋值:(T1>9) AND T1关于9的模=8
    A_B9赋值:(T1>9) AND T1关于9的模=0
    B1赋值:(N=6 AND 5日后的(平滑处理)统计6日中满足B的天数=6) OR (N=7 AND 6日后的(平滑处理)统计7日中满足B的天数=7) OR (N=8 AND 7日后的(平滑处理)统计8日中满足B的天数=8) OR (N>=9 AND 8日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B1AND(1日前的B=0ORA_B1)时,在最低价位置书写数字,画洋红色
    B2赋值:(N=5 AND 4日后的(平滑处理)统计6日中满足B的天数=6) OR (N=6 AND 5日后的(平滑处理)统计7日中满足B的天数=7) OR (N=7 AND 6日后的(平滑处理)统计8日中满足B的天数=8) OR (N>=8 AND 7日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B2AND(2日前的B=0ORA_B2)时,在最低价位置书写数字,画洋红色
    B8赋值:(N=1 AND 统计8日中满足B的天数=8) OR (N>=2 AND 1日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B8AND(8日前的B=0ORA_B8)时,在最低价位置书写数字,画洋红色
    B9赋值:(N>=1 AND 统计9日中满足B的天数=9)
    当满足条件B9AND(9日前的B=0ORA_B9)时,在最低价位置书写数字,画红色
    S赋值:收盘价>4日前的收盘价
    T2赋值: 条件连续成立次数
    A_S1赋值:(T2>9) AND T2关于9的模=1
    A_S2赋值:(T2>9) AND T2关于9的模=2
    A_S8赋值:(T2>9) AND T2关于9的模=8
    A_S9赋值:(T2>9) AND T2关于9的模=0
    S1赋值:(N=6 AND 5日后的(平滑处理)统计6日中满足S的天数=6) OR (N=7 AND 6日后的(平滑处理)统计7日中满足S的天数=7) OR (N=8 AND 7日后的(平滑处理)统计8日中满足S的天数=8) OR (N>=9 AND 8日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S1AND(1日前的S=0ORA_S1)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S2赋值:(N=5 AND 4日后的(平滑处理)统计6日中满足S的天数=6) OR (N=6 AND 5日后的(平滑处理)统计7日中满足S的天数=7) OR (N=7 AND 6日后的(平滑处理)统计8日中满足S的天数=8) OR (N>=8 AND 7日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S2AND(2日前的S=0ORA_S2)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S8赋值:(N=1 AND 统计8日中满足S的天数=8) OR (N>=2 AND 1日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S8AND(8日前的S=0ORA_S8)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S9赋值:(N>=1 AND 统计9日中满足S的天数=9)
    当满足条件S9AND(9日前的S=0ORA_S9)时,在最高价位置书写数字,画绿色,显示在位置之上
    C=CLOSE
    N=CURRBARSCOUNT()
    B=C<REF(C,4)
    T1= BARSLASTCOUNT(B)
    A_B1=IF(T1>=9,1,None)
    A_B2=IF(T1>9,2,None)
    A_B8=IF(T1>9,8,None)
    A_B9=IF(T1>9,0,None)
    B1:=(N=6 AND REFXV(COUNT(B,6),5)=6) OR (N=7 AND REFXV(COUNT(B,7),6)=7) OR (N=8 AND REFXV(COUNT(B,8),7)=8) OR (N>=9 AND REFXV(COUNT(B,9),8)=9);
    DRAWNUMBER(B1 AND (REF(B,1)=0 OR A_B1),L,1),COLORMAGENTA;
    B2:=(N=5 AND REFXV(COUNT(B,6),4)=6) OR (N=6 AND REFXV(COUNT(B,7),5)=7) OR (N=7 AND REFXV(COUNT(B,8),6)=8) OR (N>=8 AND REFXV(COUNT(B,9),7)=9);
    DRAWNUMBER(B2 AND(REF(B,2)=0 OR A_B2),L,2),COLORMAGENTA;
    B8:=(N=1 AND COUNT(B,8)=8) OR (N>=2 AND REFXV(COUNT(B,9),1)=9);
    DRAWNUMBER(B8 AND (REF(B,8)=0 OR A_B8),L,8),COLORMAGENTA;
    B9:=(N>=1 AND COUNT(B,9)=9);
    DRAWNUMBER(B9 AND (REF(B,9)=0 OR A_B9),L,9),COLORRED;
    S:=C>REF(C,4);
    T2:= BARSLASTCOUNT(S);
    A_S1:=(T2>9) AND MOD(T2,9)=1;
    A_S2:=(T2>9) AND MOD(T2,9)=2;
    A_S8:=(T2>9) AND MOD(T2,9)=8;
    A_S9:=(T2>9) AND MOD(T2,9)=0;
    S1:=(N=6 AND REFXV(COUNT(S,6),5)=6) OR (N=7 AND REFXV(COUNT(S,7),6)=7) OR (N=8 AND REFXV(COUNT(S,8),7)=8) OR (N>=9 AND REFXV(COUNT(S,9),8)=9);
    DRAWNUMBER(S1 AND (REF(S,1)=0 OR A_S1),H,1),COLORMAGENTA,DRAWABOVE;
    S2:=(N=5 AND REFXV(COUNT(S,6),4)=6) OR (N=6 AND REFXV(COUNT(S,7),5)=7) OR (N=7 AND REFXV(COUNT(S,8),6)=8) OR (N>=8 AND REFXV(COUNT(S,9),7)=9);
    DRAWNUMBER(S2 AND (REF(S,2)=0 OR A_S2),H,2),COLORMAGENTA,DRAWABOVE;
    S8:=(N=1 AND COUNT(S,8)=8) OR (N>=2 AND REFXV(COUNT(S,9),1)=9);
    DRAWNUMBER(S8 AND (REF(S,8)=0 OR A_S8),H,8),COLORMAGENTA,DRAWABOVE;
    S9:=(N>=1 AND COUNT(S,9)=9);
    DRAWNUMBER(S9 AND (REF(S,9)=0 OR A_S9),H,9),COLORGREEN,DRAWABOVE;
    '''
    pass
def JAX(CLOSE,HIGH,LOW,N=30):
    '''
    济安线
    AA赋值:(2*收盘价+最高价+最低价)/4-收盘价的N日简单移动平均的绝对值/收盘价的N日简单移动平均
    输出济安线:以AA为权重(2*收盘价+最低价+最高价)/4的动态移动平均,线宽为3,画洋红色
    CC赋值:(收盘价/济安线)
    MA1赋值:CC*(2*收盘价+最高价+最低价)/4的3日简单移动平均
    MAAA赋值:((MA1-济安线)/济安线)/3
    TMP赋值:MA1-MAAA*MA1
    输出J:如果TMP<=济安线,返回济安线,否则返回无效数,线宽为3,画青色
    输出A:TMP,线宽为2,画棕色
    输出X:如果TMP<=济安线,返回TMP,否则返回无效数,线宽为2,画绿色
    '''
    AA=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,N))/MA(CLOSE,N)
    data=pd.DataFrame()
    data['数据']=(2*CLOSE+LOW+HIGH)/4
    #alpha中值0.5
    济安线=data['数据'].ewm(alpha=0.5, adjust=True).mean()#LINETHICK3,COLORMAGENTA
    CC=(CLOSE/济安线)
    MA1=MA(CC*(2*CLOSE+HIGH+LOW)/4,3)
    MAAA=((MA1-济安线)/济安线)/3
    TMP=MA1-MAAA*MA1
    J=IF(TMP<=济安线,济安线,None)#LINETHICK3,COLORCYAN
    A=TMP#LINETHICK2,COLORBROWN
    X=IF(TMP<=济安线,TMP,None)#LINETHICK2,COLORGREEN
    return J,A,X
def XJDX(CLOSE,HIGH,LOW):
    '''
    超级短线
    VAR1赋值:(2*收盘价+最高价+最低价)/4
    VAR2赋值:VAR1的4日指数移动平均的4日指数移动平均的4日指数移动平均
    输出J: (VAR2-1日前的VAR2)/1日前的VAR2*100, COLORSTICK
    输出D: J的3日简单移动平均
    输出K: J的1日简单移动平均
    '''
    VAR1=(2*CLOSE+HIGH+LOW)/4
    VAR2=EMA(EMA(EMA(VAR1,4),4),4)
    J=(VAR2-REF(VAR2,1))/REF(VAR2,1)*100# COLORSTICK
    D=MA(J,3)
    K= MA(J,1)
    return J,D,K
def ZJTJ(CLOSE):
    '''
    庄家抬轿
    获利盘，和成本函数需要写
    VAR1赋值:收盘价的9日指数移动平均的9日指数移动平均
    控盘赋值:(VAR1-1日前的VAR1)/1日前的VAR1*1000
    当满足条件控盘<0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,画白色
    A10赋值:控盘上穿0
    输出无庄控盘:如果控盘<0,返回控盘,否则返回0,画白色,NODRAW
    输出开始控盘:如果A10,返回5,否则返回0,线宽为1,画棕色
    当满足条件控盘>1日前的控盘AND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,画红色
    输出有庄控盘:如果控盘>1日前的控盘AND控盘>0,返回控盘,否则返回0,画红色,NODRAW
    VAR2赋值:100*以收盘价*0.95计算的获利盘比例
    当满足条件VAR2>50ANDCOST(85)<CLOSEAND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,COLORFF00FF
    输出高度控盘:如果VAR2>50ANDCOST(85)<CLOSEAND控盘>0,返回控盘,否则返回0,COLORFF00FF,NODRAW
    当满足条件控盘<1日前的控盘AND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,COLOR00FF00
    输出主力出货:如果控盘<1日前的控盘AND控盘>0,返回控盘,否则返回0,COLOR00FF00,NODRAW
    '''
    VAR1=EMA(EMA(CLOSE,9),9)
    控盘=(VAR1-REF(VAR1,1))/REF(VAR1,1)*1000
    #STICKLINE(控盘<0,控盘,0,1,0),COLORWHITE;
    A10=CROSS(控盘,0)
    无庄控盘=IF(控盘<0,控盘,0)#COLORWHITE,NODRAW;
    开始控盘=IF(A10,1,0)#LINETHICK1,COLORBROWN;
    #STICKLINE(控盘>REF(控盘,1) AND 控盘>0,控盘,0,1,0),COLORRED;
    有庄控盘=IF(np.logical_and(控盘>REF(控盘,1),控盘>0),控盘,0)#COLORRED,NODRAW;
    #VAR2=100*WINNER(CLOSE*0.95)
    #STICKLINE(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0,1,0),COLORFF00FF;
    #高度控盘:IF(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0),COLORFF00FF,NODRAW;
    #STICKLINE(控盘<REF(控盘,1) AND 控盘>0,控盘,0,1,0),COLOR00FF00;
    主力出货=IF(np.logical_and(控盘<REF(控盘,1),控盘>0),控盘,0)#COLOR00FF00,NODRAW;
    return 无庄控盘,开始控盘,有庄控盘,主力出货
def ZBCD(HIGH,LOW,OPEN,AMOUNT,VOL,N=10):
    '''
    准备抄底
    VAR1赋值:成交额(元)/成交量(手)/7
    VAR2赋值:(3*最高价+最低价+开盘价+2*收盘价)/7
    VAR3赋值:成交额(元)的N日累和/VAR1/7
    VAR4赋值:以成交量(手)/VAR3为权重VAR2的动态移动平均
    输出抄底:(收盘价-VAR4)/VAR4*100,画淡洋红色
    当满足条件-7.0上穿抄底时,在抄底位置画1号图标
    '''
    VAR1=AMOUNT/VOL/7
    VAR2=(3*HIGH+LOW+OPEN+2*CLOSE)/7
    VAR3=SUM(AMOUNT,N)/VAR1/7
    VAR4=DMA(VAR2,VOL/VAR3)
    抄底=(CLOSE-VAR4)/VAR4*100#COLORLIMAGENTA
    #DRAWICON(CROSS(-7.0,抄底),抄底,1)
    return 抄底
def BDZX(HIGH,LOW,CLOSE):
    '''
    波段之星
    VAR2赋值:(最高价+最低价+收盘价*2)/4
    VAR3赋值:VAR2的21日指数移动平均
    VAR4赋值:VAR2的21日估算标准差
    VAR5赋值:((VAR2-VAR3)/VAR4*100+200)/4
    VAR6赋值:(VAR5的5日指数移动平均-25)*1.56
    输出AK: VAR6的2日指数移动平均*1.22
    输出AD1: AK的2日指数移动平均
    输出AJ: 3*AK-2*AD1
    输出AA:100
    输出布林极限:0
    输出CC:80
    输出买进: 如果AK上穿AD1,返回58,否则返回20
    输出卖出: 如果AD1上穿AK,返回58,否则返回20
    '''
    VAR2=(HIGH+LOW+CLOSE*2)/4
    VAR3=EMA(VAR2,21)
    VAR4=STD(VAR2,21)
    VAR5=((VAR2-VAR3)/VAR4*100+200)/4
    VAR6=(EMA(VAR5,5)-25)*1.56
    AK= EMA(VAR6,2)*1.22
    AD1= EMA(AK,2)
    AJ= 3*AK-2*AD1
    AA=100
    BB=0
    CC=80
    买进= IF(CROSS(AK,AD1),58,20)
    卖出= IF(CROSS(AD1,AK),58,20)
    return AK,AD1,AJ,AA,BB,CC,买进,卖出
def LHXJ(HIGH,LOW,CLOSE):
    '''
    猎狐先觉
    VAR1赋值:(收盘价*2+最高价+最低价)/4
    VAR2赋值:VAR1的13日指数移动平均-VAR1的34日指数移动平均
    VAR3赋值:VAR2的5日指数移动平均
    输出主力弃盘: (-2)*(VAR2-VAR3)*3.8
    输出主力控盘: 2*(VAR2-VAR3)*3.8
    '''
    VAR1=(CLOSE*2+HIGH+LOW)/4
    VAR2=EMA(VAR1,13)-EMA(VAR1,34)
    VAR3=EMA(VAR2,5)
    主力弃盘=(-2)*(VAR2-VAR3)*3.8
    主力控盘=2*(VAR2-VAR3)*3.8
    return 主力弃盘,主力控盘
def LYJH(CLOSE,HIGH,LOW,M=80,M1=50):
    '''
    猎鹰歼狐
    VAR1赋值:(36日内最高价的最高值-收盘价)/(36日内最高价的最高值-36日内最低价的最低值)*100
    输出机构做空能量线: VAR1的2日[1日权重]移动平均
    VAR2赋值:(收盘价-9日内最低价的最低值)/(9日内最高价的最高值-9日内最低价的最低值)*100
    输出机构做多能量线: VAR2的5日[1日权重]移动平均-8
    输出LH: M
    输出LH1: M1
    '''
    VAR1=(HHV(HIGH,36)-CLOSE)/(HHV(HIGH,36)-LLV(LOW,36))*100
    机构做空能量线=SMA(VAR1,2,1)
    VAR2=(CLOSE-LLV(LOW,9))/(HHV(HIGH,9)-LLV(LOW,9))*100
    机构做多能量线=SMA(VAR2,5,1)-8
    LH=M
    LH1=M1
    return 机构做空能量线,机构做多能量线,LH,LH1
def JFZX(OPEN,CLOSE,VOL,N=30):
    '''
    飓风智能中线
    VAR2赋值:如果收阳线,返回成交量(手),否则返回0的N日累和/成交量(手)的N日累和*100
    VAR3赋值:100-如果收阳线,返回成交量(手),否则返回0的N日累和/成交量(手)的N日累和*100
    输出多头力量: VAR2
    输出空头力量: VAR3
    输出多空平衡: 50
    '''
    VAR2=SUM(IF(CLOSE>OPEN,VOL,0),N)/SUM(VOL,N)*100
    VAR3=100-SUM(IF(CLOSE>OPEN,VOL,0),N)/SUM(VOL,N)*100
    多头力量= VAR2
    空头力量= VAR3
    多空平衡= 50
    return 多头力量,空头力量,多空平衡
def CYHT(CLOSE,HIGH,LOW,OPEN):
    '''
    财运亨通
    VAR1赋值:(2*收盘价+最高价+最低价+开盘价)/5
    输出高抛: 80
    VAR2赋值:34日内最低价的最低值
    VAR3赋值:34日内最高价的最高值
    输出SK: (VAR1-VAR2)/(VAR3-VAR2)*100的13日指数移动平均
    输出SD: SK的3日指数移动平均
    输出低吸: 20
    输出强弱分界: 50
    VAR4赋值:如果SK上穿SD,返回40,否则返回22
    VAR5赋值:如果SD上穿SK,返回60,否则返回78
    输出卖出: VAR5
    输出买进: VAR4
    '''
    VAR1=(2*CLOSE+HIGH+LOW+OPEN)/5
    高抛= 80
    VAR2=LLV(LOW,34)
    VAR3=HHV(HIGH,34)
    SK= EMA((VAR1-VAR2)/(VAR3-VAR2)*100,13)
    SD= EMA(SK,3)
    低吸= 20
    强弱分界= 50
    VAR4=IF(CROSS(SK,SD),40,22)
    VAR5=IF(CROSS(SD,SK),60,78)
    卖出= VAR5
    买进= VAR4
    return 高抛,SK,SD,低吸,强弱分界,卖出,买进
def BSQJ(CLOSE):
    '''
    买卖区间
    买线赋值:收盘价的2日指数移动平均
    卖线赋值:收盘价的21日线性回归斜率*20+收盘价的42日指数移动平均
    当满足条件买线>=卖线时,在日期日0日内最高价的最高值和日期日0日内最低价的最低值位置之间画柱状线,宽度为6,0不为0则画空心柱.,COLOR001050
    当满足条件买线<卖线时,在日期日0日内最高价的最高值和日期日0日内最低价的最低值位置之间画柱状线,宽度为6,0不为0则画空心柱.,COLOR404050
    K线
    指导赋值:(收盘价的4日指数移动平均+收盘价的6日指数移动平均+收盘价的12日指数移动平均+收盘价的24日指数移动平均)/4的2日指数移动平均
    界赋值:收盘价的27日简单移动平均
    输出B买:如果指导上穿界ORCROSS(买线,卖线),返回收盘价,否则返回无效数,画洋红色,NODRAW
    输出持仓:如果买线>=卖线,返回收盘价,否则返回无效数,画红色,NODRAW
    输出S卖:如果界上穿指导ORCROSS(卖线,买线),返回收盘价,否则返回无效数,画淡灰色,NODRAW
    输出空仓:如果买线<卖线,返回收盘价,否则返回无效数,画绿色,NODRAW
    当满足条件买线上穿卖线时,在最低价位置画1号图标
    当满足条件卖线上穿买线时,在最高价位置画2号图标
    '''
    C=CLOSE
    买线=EMA(C,2)
    卖线=EMA(SLOPE(C,21)*20+C,42)
    #STICKLINE(买线>=卖线,REFDATE(HHV(H,0),DATE),REFDATE(LLV(L,0),DATE),6,0),COLOR001050
    #STICKLINE(买线<卖线,REFDATE(HHV(H,0),DATE),REFDATE(LLV(L,0),DATE),6,0),COLOR404050;
    #DRAWKLINE(H,O,L,C);
    指导=EMA((EMA(CLOSE,4)+EMA(CLOSE,6)+EMA(CLOSE,12)+EMA(CLOSE,24))/4,2)
    界=MA(CLOSE,27)
    B买=IF(np.logical_or(CROSS(指导,界),CROSS(买线,卖线)),C,None)#COLORMAGENTA,NODRAW;
    持仓=IF(买线>=卖线,C,None)#COLORRED,NODRAW
    S卖=IF(np.logical_or(CROSS(界,指导),CROSS(卖线,买线)),C,None)#COLORLIGRAY,NODRAW
    空仓=IF(买线<卖线,C,None)#COLORGREEN,NODRAW
    #DRAWICON(CROSS(买线,卖线),L,1);
    #DRAWICON(CROSS(卖线,买线),H,2);
    return B买,持仓,S卖,空仓
def CDP_STD(CLOSE,HIGH,LOW):
    '''
    逆势操作
    CH赋值:1日前的最高价
    CL赋值:1日前的最低价
    CC赋值:1日前的收盘价
    输出CDP:(CH+CL+CC)/3
    输出AH:2*CDP+CH-2*CL
    输出NH:CDP+CDP-CL
    输出NL:CDP+CDP-CH
    输出AL:2*CDP-2*CH+CL
    '''
    H=HIGH,
    L=LOW
    C=CLOSE
    CH=REF(H,1)
    CL=REF(L,1)
    CC=REF(C,1)
    CDP=(CH+CL+CC)/3
    AH=2*CDP+CH-2*CL
    NH=CDP+CDP-CL
    NL=CDP+CDP-CH
    AL=2*CDP-2*CH+CL
    return CDP,AH,NH,NL,AL
def TBP_STD(HIGH,LOW,CLOSE):
    '''
    趋势平衡点
    APX赋值:(最高价+最低价+收盘价)/3
    TR0赋值:最高价-最低价和最高价-1日前的收盘价的绝对值和最低价-1日前的收盘价的绝对值的较大值的较大值
    MF0赋值:收盘价-2日前的收盘价
    MF1赋值:1日前的MF0
    MF2赋值:2日前的MF0
    DIRECT1赋值:上次MF0>MF1ANDMF0>MF2距今天数
    DIRECT2赋值:上次MF0<MF1ANDMF0<MF2距今天数
    DIRECT0赋值:如果DIRECT1<DIRECT2,返回100,否则返回-100
    输出TBP:1日前的1日前的收盘价+如果DIRECT0>50,返回MF0和MF1的较小值,否则返回MF0和MF1的较大值
    输出多头获利:1日前的如果DIRECT0>50,返回APX*2-最低价,否则返回无效数,NODRAW
    输出多头停损:1日前的如果DIRECT0>50,返回APX-TR0,否则返回无效数,NODRAW
    输出空头回补:1日前的如果DIRECT0<-50,返回APX*2-最高价,否则返回无效数,NODRAW
    输出空头停损:1日前的如果DIRECT0<-50,返回APX+TR0,否则返回无效数,NODRAW
    '''
    H=HIGH
    L=LOW
    C=CLOSE
    APX=(H+L+C)/3
    TR0=MAX(H-L,MAX(ABS(H-REF(C,1)),ABS(L-REF(C,1))))
    MF0=C-REF(C,2)
    MF1=REF(MF0,1)
    MF2=REF(MF0,2)
    DIRECT1=BARSLAST(np.logical_and(MF0>MF1,MF0>MF2))
    DIRECT2=BARSLAST(np.logical_and(MF0<MF1,MF0<MF2))
    DIRECT0=IF(DIRECT1<DIRECT2,100,-100)
    TBP=REF(REF(C,1)+IF(DIRECT0>50,MIN(MF0,MF1),MAX(MF0,MF1)),1)
    多头获利=REF(IF(DIRECT0>50,APX*2-L,None),1)
    多头停损=REF(IF(DIRECT0>50,APX-TR0,None),1)
    空头回补=REF(IF(DIRECT0<-50,APX*2-H,None),1)
    空头停损=REF(IF(DIRECT0<-50,APX+TR0,None),1)
    return TBP,多头获利,多头停损,空头回补,空头停损
#***********************************************
#***********************************************
#****************有空写****************************










