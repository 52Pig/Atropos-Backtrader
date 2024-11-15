# -*- coding: utf-8 -*-
# @File : login.py

import datetime
import time
import pandas as pd
import execjs
import os
import requests
from ..trader_tool.dfcf_cov_data import dfcf_bond_cov_data
filename = 'encode_jsl.txt'

path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(path, filename)

headers = {
    'Host': 'www.jisilu.cn', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
    'Cache-Control': 'no-cache', 'Accept': 'application/json,text/javascript,*/*;q=0.01',
    'Origin': 'https://www.jisilu.cn', 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Referer': 'https://www.jisilu.cn/login/',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8'
}


def decoder(text): # 加密用户名和密码
    with open(full_path, 'r', encoding='utf8') as f:
        source = f.read()

    ctx = execjs.compile(source)
    key = '397151C04723421F'
    return ctx.call('jslencode', text, key)


def get_bond_info(session): # 获取行情数据
    ts = int(time.time() * 1000)
    url = 'https://www.jisilu.cn/data/cbnew/cb_list_new/?___jsl=LST___t={}'.format(ts)
    data={
        'fprice':'' ,
        'tprice':'' ,
        'curr_iss_amt':'' ,
        'volume': '',
        'svolume':'' ,
        'premium_rt': '',
        'ytm_rt':'', 
        'rating_cd':'' ,
        'is_search': 'N',
        'market_cd[]': 'shmb',
        'market_cd[]': 'shkc',
        'market_cd[]': 'szmb',
        'market_cd[]': 'szcy',
        'btype':'' ,
        'listed': 'Y',
        'qflag': 'N',
        'sw_cd': '',
        'bond_ids':'' ,
        'rp': '50',
        'page': '0'
    }
    import json
    r = session.post(
        url=url,
        headers=headers,
        data=json.dumps(data)
    )
    ret = r.json()
    result = []
    for item in ret['rows']:
        result.append(item['cell'])
    return result


def login(user, password): # 登录
    session = requests.Session()
    url = 'https://www.jisilu.cn/account/ajax/login_process/'
    username = decoder(user)
    jsl_password = decoder(password)
    data = {
        'return_url': 'https://www.jisilu.cn/',
        'user_name': username,
        'password': jsl_password,
        'net_auto_login': '1',
        '_post_type': 'ajax',
    }

    js = session.post(
        url=url,
        headers=headers,
        data=data,
    )

    ret = js.json()

    if ret.get('errno') == 1:
        print('集思录登录成功 账户 {} 密码{}'.format(user,password))
        return session
    else:
        print('集思录登录失败 账户 {} 密码{}'.format(user,password))
        raise ValueError('登录失败')


def get_all_cov_bond_data(jsl_user='150079',jsl_password='35790'): # 主函数
    '''
    jsl_user账户名称
    jsl_password账户密码
    '''
    try:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        session = login(jsl_user, jsl_password)
        ret = get_bond_info(session)
        df = pd.DataFrame(ret)
        df = df.reset_index()
        columns=['index','证券代码','可转债名称','_','价格','涨跌幅','正股代码','正股名称','_',
        '正股价','正股涨跌','正股PB','转股价','转股价值','_','转股溢价率','双低','申万','市场',	'_',
        '上市时间','_','_','持有','_','债券评级','期权价值','回售触发价','强赎触发价','转债占比',
        '基金持仓','到期时间','剩余年限','剩余规模','成交额','svolume','换手率','到期税前收益',
        '_','_','_','_','_','_','融资融券','_','_','_',	'_','_','_','_','_','_','_','_',
        '_','_','_','_','_','_']
        df.columns=columns
        del df['_']
        return df
    except:
        '''
        [
                "序号",
                "转债代码",
                "转债名称",
                "转债最新价",
                "转债涨跌幅",
                "正股代码",
                "正股名称",
                "正股最新价",
                "正股涨跌幅",
                "转股价",
                "转股价值",
                "转股溢价率",
                "纯债溢价率",
                "回售触发价",
                "强赎触发价",
                "到期赎回价",
                "纯债价值",
                "开始转股日",
                "上市日期",
                "申购日期",
            ]
        '''
        print('东方财富可转债数据')
        models=dfcf_bond_cov_data()
        df=models.bond_cov_comparison()
        df.rename(columns={'转债代码':'证券代码','转债名称':'可转债名称','转债最新价':'价格',
                              '转债涨跌幅':'涨跌幅','正股最新价':"正股价","正股涨跌幅":"正股涨跌"},inplace=True)
        df['选择']=df['上市日期'].apply(lambda x:'是' if x=='-' else '不是')
        df=df[df['选择']=='不是']
        df['价格']=df['价格'].replace('-',None)
        df['涨跌幅']=df['涨跌幅'].replace('-',None)
        return df
        