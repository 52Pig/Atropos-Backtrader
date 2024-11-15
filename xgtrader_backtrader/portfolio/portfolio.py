import pandas as pd
class portfolio:
    def __init__(self,starting_cash=1000000,cash=100000):
        '''
        账户当前的资金，标的信息，即所有标的操作仓位的信息汇总。如未使用 SubPortfolioConfig 设置多仓位，默认只有subportfolios[0]一个仓位，Portfolio 指向该仓位。注意区分多仓和空仓。

        inout_cash: 累计出入金, 比如初始资金 1000, 后来转移出去 100, 则这个值是 1000 - 100
        available_cash: 可用资金, 可用来购买证券的资金
        transferable_cash: 可取资金, 即可以提现的资金, 不包括今日卖出证券所得资金
        locked_cash: 挂单锁住资金
        margin: 保证金，股票、基金保证金都为100%
        positions: 等同于 long_positions
        long_positions: 多单的仓位, 一个 dict, key 是证券代码, value 是 [Position]对象
        short_positions: 空单的仓位, 一个 dict, key 是证券代码, value 是 [Position]对象
        total_value: 总的权益, 包括现金, 保证金(期货)或者仓位(股票)的总价值, 可用来计算收益
        returns: 总权益的累计收益；（当前总资产 + 今日出入金 - 昨日总资产） / 昨日总资产；
        starting_cash: 初始资金, 现在等于 inout_cash
        positions_value: 持仓价值
        '''
        self.starting_cash=starting_cash
        cash=cash
        self.total_portfolio={'date':['2023-01-01'],
                              'stock_total_value':[0],
                              'available_cash':[cash],
                              'ups_downs_value':[0],
                              'reference_profit':[0],
                              'host_cost':[0],
                              'cumsum_host_cost':[0],
                              'total_value':[0],
                              'return_ratio':[0],
                              "cumsum_return_ratio":[0]}
    def adjust_portfolio_data(self,trader_type='buy',date='20230101',trader_value=0,ups_downs_value=0,host_cost=0):
        '''
        调整账户数据
        date交易时间
        stock股票代码
        price交易价格
        amount数量
        trader_type交易类型
        trader_value/stock_total_value/reference_profit/total_value外部输入
        '''
        if trader_type=='buy':  
            #时间
            date_list=self.total_portfolio['date']
            date_list.append(date)
            self.total_portfolio['date']=date_list
            #可用现金trader_value自带了方向
            available_cash_list=self.total_portfolio['available_cash']
            now_available_cash=available_cash_list[-1]
            available_cash=now_available_cash-trader_value-host_cost
            self.available_cash=available_cash
            available_cash_list.append(available_cash)
            self.total_portfolio['available_cash']=available_cash_list
            #股票市值trader_value
            stock_total_value_list=self.total_portfolio['stock_total_value']
            stock_value=stock_total_value_list[-1]
            now_stock_total_value=stock_total_value_list[-1]
            stock_total_value=now_stock_total_value+trader_value
            stock_total_value_list.append(stock_total_value)
            self.total_portfolio['stock_total_value']=stock_total_value_list
            #涨跌金额直接输入
            ups_downs_value_list=self.total_portfolio['ups_downs_value']
            ups_downs_value_list.append(ups_downs_value)
            self.total_portfolio['ups_downs_value']=ups_downs_value_list
            #浮动盈亏reference_profit
            reference_profit_list=self.total_portfolio['reference_profit']
            now_reference_profit=reference_profit_list[-1]
            reference_profit=now_reference_profit+ups_downs_value
            reference_profit_list.append(reference_profit)
            self.total_portfolio['reference_profit']=reference_profit_list
            #账户价值total_value
            total_value_list=self.total_portfolio['total_value']
            total_value=stock_total_value+available_cash
            total_value_list.append(total_value)
            self.total_portfolio['total_value']=total_value_list
            #浮动盈亏比例return_ratio
            return_ratio_list=self.total_portfolio['return_ratio']
            if stock_value<=0:
                return_ratio=0
            else:
                return_ratio=ups_downs_value/stock_value
            return_ratio_list.append(return_ratio)
            self.total_portfolio['return_ratio']=return_ratio_list
            #累计动盈亏比例cumsum_return_ratio
            cumsum_return_ratio_list=self.total_portfolio['cumsum_return_ratio']
            now_cumsum_return_ratio=cumsum_return_ratio_list[-1]
            cumsum_return_ratio=now_cumsum_return_ratio+return_ratio
            cumsum_return_ratio_list.append(cumsum_return_ratio)
            self.total_portfolio['cumsum_return_ratio']=cumsum_return_ratio_list
            #手续费
            host_cost_list=self.total_portfolio['host_cost']
            host_cost_list.append(host_cost)
            self.total_portfolio['host_cost']=host_cost_list
            #累计手续费
            cumsum_host_cost_list=self.total_portfolio['cumsum_host_cost']
            now_cumsum_host_cost=cumsum_host_cost_list[-1]
            cumsum_host_cost=now_cumsum_host_cost+host_cost
            cumsum_host_cost_list.append(cumsum_host_cost)
            self.total_portfolio['cumsum_host_cost']=cumsum_host_cost_list

        #卖出
        elif trader_type=='sell':
            #时间
            date_list=self.total_portfolio['date']
            date_list.append(date)
            self.total_portfolio['date']=date_list
            #可用现金trader_value自带了方向
            available_cash_list=self.total_portfolio['available_cash']
            now_available_cash=available_cash_list[-1]
            available_cash=now_available_cash-trader_value
            self.available_cash=available_cash
            available_cash_list.append(available_cash)
            self.total_portfolio['available_cash']=available_cash_list
            #股票市值trader_value
            stock_total_value_list=self.total_portfolio['stock_total_value']
            stock_value=stock_total_value_list[-1]
            now_stock_total_value=stock_total_value_list[-1]
            stock_total_value=now_stock_total_value+trader_value
            stock_total_value_list.append(stock_total_value)
            self.total_portfolio['stock_total_value']=stock_total_value_list
            #涨跌金额直接输入
            ups_downs_value_list=self.total_portfolio['ups_downs_value']
            ups_downs_value_list.append(ups_downs_value)
            self.total_portfolio['ups_downs_value']=ups_downs_value_list
            #浮动盈亏reference_profit
            reference_profit_list=self.total_portfolio['reference_profit']
            now_reference_profit=reference_profit_list[-1]
            reference_profit=now_reference_profit+ups_downs_value
            reference_profit_list.append(reference_profit)
            self.total_portfolio['reference_profit']=reference_profit_list
            #账户价值total_value
            total_value_list=self.total_portfolio['total_value']
            total_value=stock_total_value+available_cash
            total_value_list.append(total_value)
            self.total_portfolio['total_value']=total_value_list
            #浮动盈亏比例return_ratio
            return_ratio_list=self.total_portfolio['return_ratio']
            if stock_value<=0:
                return_ratio=0
            else:
                return_ratio=ups_downs_value/stock_value
            return_ratio_list.append(return_ratio)
            self.total_portfolio['return_ratio']=return_ratio_list
            #累计动盈亏比例cumsum_return_ratio
            cumsum_return_ratio_list=self.total_portfolio['cumsum_return_ratio']
            now_cumsum_return_ratio=cumsum_return_ratio_list[-1]
            cumsum_return_ratio=now_cumsum_return_ratio+return_ratio
            cumsum_return_ratio_list.append(cumsum_return_ratio)
            self.total_portfolio['cumsum_return_ratio']=cumsum_return_ratio_list
             #手续费
            host_cost_list=self.total_portfolio['host_cost']
            host_cost_list.append(host_cost)
            self.total_portfolio['host_cost']=host_cost_list
            #累计手续费
            cumsum_host_cost_list=self.total_portfolio['cumsum_host_cost']
            now_cumsum_host_cost=cumsum_host_cost_list[-1]
            cumsum_host_cost=now_cumsum_host_cost+0
            cumsum_host_cost_list.append(cumsum_host_cost)
            self.total_portfolio['cumsum_host_cost']=cumsum_host_cost_list
        #持股结算
        elif trader_type=='settle':
            #结算交易价值未0
            #时间
            date_list=self.total_portfolio['date']
            date_list.append(date)
            self.total_portfolio['date']=date_list
            #可用现金trader_value自带了方向数量不变
            available_cash_list=self.total_portfolio['available_cash']
            now_available_cash=available_cash_list[-1]
            #可用现金变化未0*****
            available_cash=now_available_cash-0
            available_cash_list.append(available_cash)
            self.total_portfolio['available_cash']=available_cash_list
            #股票市值trader_value，随涨跌金额变化
            stock_total_value_list=self.total_portfolio['stock_total_value']
            now_stock_total_value=stock_total_value_list[-1]
            #随涨跌金额变化
            stock_total_value=now_stock_total_value+ups_downs_value
            stock_total_value_list.append(stock_total_value)
            self.total_portfolio['stock_total_value']=stock_total_value_list
            #涨跌金额直接输入
            ups_downs_value_list=self.total_portfolio['ups_downs_value']
            ups_downs_value_list.append(ups_downs_value)
            self.total_portfolio['ups_downs_value']=ups_downs_value_list
            #浮动盈亏reference_profit
            reference_profit_list=self.total_portfolio['reference_profit']
            now_reference_profit=reference_profit_list[-1]
            reference_profit=now_reference_profit+ups_downs_value
            reference_profit_list.append(reference_profit)
            self.total_portfolio['reference_profit']=reference_profit_list
            #账户价值total_value
            total_value_list=self.total_portfolio['total_value']
            total_value=stock_total_value+available_cash
            total_value_list.append(total_value)
            self.total_portfolio['total_value']=total_value_list
            #浮动盈亏比例return_ratio
            return_ratio_list=self.total_portfolio['return_ratio']
            if now_stock_total_value<=0:
                return_ratio=0
            else:
                return_ratio=ups_downs_value/now_stock_total_value
                return_ratio=return_ratio
            return_ratio_list.append(return_ratio)
            self.total_portfolio['return_ratio']=return_ratio_list
            #累计动盈亏比例cumsum_return_ratio
            cumsum_return_ratio_list=self.total_portfolio['cumsum_return_ratio']
            now_cumsum_return_ratio=cumsum_return_ratio_list[-1]
            cumsum_return_ratio=now_cumsum_return_ratio+return_ratio
            cumsum_return_ratio_list.append(cumsum_return_ratio)
            self.total_portfolio['cumsum_return_ratio']=cumsum_return_ratio_list
            #手续费
            host_cost_list=self.total_portfolio['host_cost']
            host_cost_list.append(host_cost)
            self.total_portfolio['host_cost']=host_cost_list
            #累计手续费
            cumsum_host_cost_list=self.total_portfolio['cumsum_host_cost']
            now_cumsum_host_cost=cumsum_host_cost_list[-1]
            cumsum_host_cost=now_cumsum_host_cost+0
            cumsum_host_cost_list.append(cumsum_host_cost)
            self.total_portfolio['cumsum_host_cost']=cumsum_host_cost_list
        else:
            return '未知的交易状态'
        return self.total_portfolio
    def get_portfolio_data_to_pandas(self):
        '''
        获取账户数据转成pandas
        '''
        df=pd.DataFrame(self.total_portfolio)
        return df
    

        



    





