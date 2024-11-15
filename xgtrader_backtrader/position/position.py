import pandas as pd
from ..data.data import data
from ..portfolio.portfolio import portfolio
class position:
    def __init__(self,start_date='20210105',end_date='20230101',data_type='D',starting_cash=100000,cash=100000,commission=0.001):
        '''
        持股
        security: 标的代码
        price: 最新行情价格
        acc_avg_cost 是累计的持仓成本，在清仓/减仓时也会更新，该持仓累积的收益都会用于计算成本（一开始acc_avg_cost为0，amount也为0），加仓：new_acc_avg_cost = (acc_avg_cost * amount + trade_value + commission) / (amount + trade_amount)；减仓：new_acc_avg_cost = (acc_avg_cost * amount - trade_value + commission) / (amount - trade_amount) 说明：commission是本次买入或者卖出的手续费
        avg_cost 是当前持仓成本，只有在开仓/加仓时会更新： new_avg_cost = (position_value + trade_value + commission) / (position_amount + trade_amount)
        每次买入后会调整avg_cost, 卖出时avg_cost不变. 这个值也会被用来计算浮动盈亏.
        cumsum_hold_cost: 当日持仓成本，计算方法：当日无收益：cumsum_hold_cost = 前收价 （清算后），加仓：cumsum_hold_cost = (cumsum_hold_cost * amount + trade_value)/(amount + trade_amount)，减仓：cumsum_hold_cost = (cumsum_hold_cost * amount - trade_value)/(amount - trade_amount)；trade_value = trade_price * trade_amount
        init_time: 建仓时间，格式为 datetime.datetime
        transact_time: 最后交易时间，格式为 datetime.datetime
        locked_amount: 挂单冻结仓位
        total_amount: 总仓位, 但不包括挂单冻结仓位( 如果要获取当前持仓的仓位,需要将locked_amount和total_amount相加)
        closeable_amount: 可卖出的仓位
        today_amount: 今天开的仓位
        value: 标的价值，计算方法是: price * total_amount * multiplier, 其中股票、基金的multiplier为1，期货为相应的合约乘数
        side: 多/空，'long' or 'short'
        pindex: 仓位索引，subportfolio index
        '''
        self.position=dict()
        self.total_position=pd.DataFrame()
        self.commission=commission
        self.data_type=data_type
        self.start_date=start_date
        self.end_date=end_date
        self.data=data(start_date=self.start_date,end_date=self.end_date,data_type=self.data_type)
        self.portfolio=portfolio(starting_cash=starting_cash,cash=cash)
    def creat_position(self,stock='600031',multiplier=1,price=10,start_date='20230101',
                       amount=0,trader_type=''):
        '''
        建立持股
        date必须有的
        Reference profit参考盈亏
        profit_ratio=盈亏比率
        '''
        if stock in list(self.position.keys()):
            print('{}持股已经建立'.format(stock))
            return dict()
        else:
            data_dict={'stock':[stock],'price':[price],'date':[start_date],
            'host_cost':[0],
            'cumsum_hold_cost':[amount*price*self.commission],'amount':[amount],
            'trader_value':[amount*price],
            "trader_amount":[amount],
            'value':[amount*price],
            "price_limit":[0],
            "ups_downs_value":[0],
            'return':[0],
            "cumsum_return":[0],
            "trader_type":[trader_type]}
            self.position[stock]=data_dict
            self.data.get_add_data(stock=stock)
            return self.position
    def adjust_position_data(self,trader_type='buy',stock='60031',date='2023-01-01',price=1,amount=100):
        '''
        date交易时间
        stock股票代码
        price交易价格
        amount数量
        trader_type交易类型
        '''
        if trader_type=='buy':
            data_dict={}
            buy_amount=amount
            #代码
            stock_list=self.position[stock]['stock']
            stock_list.append(stock)
            data_dict['stock']=stock_list
            #价格
            price_list=self.position[stock]['price']
            price_list.append(price)
            data_dict['price']=price_list
            #时间
            date_list=self.position[stock]['date']
            date_list.append(date)
            data_dict['date']=date_list
            #host_cost
            host_cost_list=self.position[stock]['host_cost']
            cost=buy_amount*price*self.commission
            host_cost_list.append(cost)
            data_dict['host_cost']=host_cost_list
            #cumsum_hold_cost成本，买入才有手续费
            cumsum_hold_cost_list=self.position[stock]['cumsum_hold_cost']
            cost=cumsum_hold_cost_list[-1]
            cost=cost+amount*price*self.commission
            cumsum_hold_cost_list.append(round(cost,2))
            data_dict['cumsum_hold_cost']=cumsum_hold_cost_list
            #持有数量
            amount_list=self.position[stock]['amount']
            #今天买入的不参加收益计算
            pre_amount=amount_list[-1]
            hold_amount=amount_list[-1]
            hold_amount=hold_amount+amount
            amount_list.append(hold_amount)
            data_dict['amount']=amount_list
            #交易数量
            trader_amount_list=self.position[stock]['trader_amount']
            trader_amount_list.append(buy_amount)
            data_dict['trader_amount']=trader_amount_list
            #持有价值value
            value_list=self.position[stock]['value']
            
            #交易价值trader_value
            trader_value_list=self.position[stock]['trader_value']
            trader_value=buy_amount*price
            trader_value_list.append(trader_value)
            data_dict['trader_value']=trader_value_list
            #今天买入的不参加收益计算
            pre_value=value_list[-1]
            hold_value=value_list[-1]
            value=hold_value+amount*price
            value_list.append(value)
            data_dict['value']=value_list
            #涨跌幅额price_limit
            price_limit_list=self.position[stock]['price_limit']
            price_limit=self.data.hist_return[stock][date]
            price_limit_list.append(price_limit)
            data_dict['price_limit']=price_limit_list
            #涨跌额ups_downs_value
            ups_downs_value_list=self.position[stock]['ups_downs_value']
            ups_downs_value=pre_value*price_limit
            ups_downs_value_list.append(ups_downs_value)
            data_dict['ups_downs_value']=ups_downs_value_list
            #收益比例
            return_list=self.position[stock]['return']
            if pre_value>0:
                return_ratio=ups_downs_value/pre_value
            else:
                return_ratio=0
            return_list.append(return_ratio)
            data_dict['return']=return_list
            #累计收益cumsum_return
            cumsum_return_list=self.position[stock]['cumsum_return']
            pre_cumsum_return=cumsum_return_list[-1]
            cumsum_return=return_ratio+pre_cumsum_return
            cumsum_return_list.append(cumsum_return)
            data_dict['cumsum_return']=cumsum_return_list
            #交易类型trader_type
            trader_type_list=self.position[stock]['trader_type']
            trader_type_list.append(trader_type)
            data_dict['trader_type']=trader_type_list
            self.position[stock]=data_dict
            #结算账户
            portfolio_log=self.get_cacla_portfolio_dict()
            host_cost=portfolio_log['host_cost'].get(date,0)
            trader_value=portfolio_log['trader_value'].get(date,0)
            ups_downs_value=portfolio_log['ups_downs_value'].get(date,0)
            self.portfolio.adjust_portfolio_data(trader_type=trader_type,date=date,trader_value=trader_value,
                                                 ups_downs_value=ups_downs_value,host_cost=host_cost)
            
            return self.position
        #卖出
        elif trader_type=='sell':
            sell_amount=amount
            data_dict={}
            #代码
            stock_list=self.position[stock]['stock']
            stock_list.append(stock)
            data_dict['stock']=stock_list
            #价格
            price_list=self.position[stock]['price']
            price_list.append(price)
            data_dict['price']=price_list
            #时间
            date_list=self.position[stock]['date']
            date_list.append(date)
            data_dict['date']=date_list
            #host_cost
            host_cost_list=self.position[stock]['host_cost']
            cost=0
            host_cost_list.append(cost)
            data_dict['host_cost']=host_cost_list
            #cumsum_hold_cost成本，买入才有手续费
            cumsum_hold_cost_list=self.position[stock]['cumsum_hold_cost']
            cost=cumsum_hold_cost_list[-1]
            cumsum_hold_cost_list.append(round(cost,2))
            data_dict['cumsum_hold_cost']=cumsum_hold_cost_list
            #持有数量减少
            amount_list=self.position[stock]['amount']
            hold_amount=amount_list[-1]
            amount=hold_amount-amount
            if amount<=0:
                amount=0
            else:
                amount=amount
            amount_list.append(amount)
            data_dict['amount']=amount_list
            #交易数量
            trader_amount_list=self.position[stock]['trader_amount']
            trader_amount_list.append(-sell_amount)
            data_dict['trader_amount']=trader_amount_list
            
            #交易价值trader_value
            trader_value_list=self.position[stock]['trader_value']
            trader_value=sell_amount*price
            trader_value_list.append(-trader_value)
            data_dict['trader_value']=trader_value_list
            

            #持有价值value
            value_list=self.position[stock]['value']
            pre_value=value_list[-1]
            hold_value=value_list[-1]
            #持有价值减少
            value=hold_value-sell_amount*price
            if value>=0:
                value=value
            else:
                value=0
            value_list.append(value)
            data_dict['value']=value_list
            #涨跌幅额price_limit
            price_limit_list=self.position[stock]['price_limit']
            price_limit=self.data.hist_return[stock][date]
            price_limit_list.append(price_limit)
            data_dict['price_limit']=price_limit_list
            #涨跌额ups_downs_value
            ups_downs_value_list=self.position[stock]['ups_downs_value']
            if pre_value<=0:
                ups_downs_value=0
            else:
                ups_downs_value=pre_value*price_limit
            ups_downs_value_list.append(ups_downs_value)
            data_dict['ups_downs_value']=ups_downs_value_list
            #收益比例
            return_list=self.position[stock]['return']
            if pre_value<=0:
                return_ratio=0
            else:
                return_ratio=ups_downs_value/pre_value
            return_list.append(return_ratio)
            data_dict['return']=return_list
            #累计收益cumsum_return
            cumsum_return_list=self.position[stock]['cumsum_return']
            pre_cumsum_return=cumsum_return_list[-1]
            cumsum_return=return_ratio+pre_cumsum_return
            cumsum_return_list.append(cumsum_return)
            data_dict['cumsum_return']=cumsum_return_list
            #交易类型trader_type
            trader_type_list=self.position[stock]['trader_type']
            trader_type_list.append(trader_type)
            data_dict['trader_type']=trader_type_list
            self.position[stock]=data_dict
            #结算账户
            portfolio_log=self.get_cacla_portfolio_dict()
            host_cost=portfolio_log['host_cost'].get(date,0)
            trader_value=portfolio_log['trader_value'].get(date,0)
            ups_downs_value=portfolio_log['ups_downs_value'].get(date,0)
            self.portfolio.adjust_portfolio_data(trader_type=trader_type,date=date,trader_value=trader_value,
                                                 ups_downs_value=ups_downs_value,host_cost=host_cost)
            return self.position
        #结算，需要时间价格发生变化，结束只持有的价值发生变化
        elif trader_type=='settle':
            data_dict={}
            #代码
            stock_list=self.position[stock]['stock']
            stock_list.append(stock)
            data_dict['stock']=stock_list
            #价格
            price_list=self.position[stock]['price']
            price_list.append(price)
            data_dict['price']=price_list
            #时间
            date_list=self.position[stock]['date']
            date_list.append(date)
            data_dict['date']=date_list
            #host_cost
            host_cost_list=self.position[stock]['host_cost']
            cost=0
            host_cost_list.append(cost)
            data_dict['host_cost']=host_cost_list
            #cumsum_hold_cost成本，买入才有手续费
            cumsum_hold_cost_list=self.position[stock]['cumsum_hold_cost']
            cost=cumsum_hold_cost_list[-1]
            cumsum_hold_cost_list.append(round(cost,2))
            data_dict['cumsum_hold_cost']=cumsum_hold_cost_list
            #持有数量不变
            amount_list=self.position[stock]['amount']
            hold_amount=amount_list[-1]
            hold_amount=hold_amount
            amount_list.append(hold_amount)
            data_dict['amount']=amount_list
            #交易数量
            trader_amount_list=self.position[stock]['trader_amount']
            trader_amount_list.append(0)
            data_dict['trader_amount']=trader_amount_list
            
            #交易价值trader_value
            trader_value_list=self.position[stock]['trader_value']
            trader_value=0
            trader_value_list.append(trader_value)
            data_dict['trader_value']=trader_value_list
            

            #持有价值value变化
            value_list=self.position[stock]['value']
            hold_value=value_list[-1]
            value=hold_amount*price
            value_list.append(value)
            data_dict['value']=value_list

            #涨跌幅额price_limit
            price_limit_list=self.position[stock]['price_limit']
            price_limit=self.data.hist_return[stock][date]
            price_limit_list.append(price_limit)
            data_dict['price_limit']=price_limit_list
            #涨跌额ups_downs_value
            #持有的价值需要参与结算pre_value
            pre_value=value
            pre_value=hold_amount
            ups_downs_value_list=self.position[stock]['ups_downs_value']
            ups_downs_value=pre_value*price_limit
            ups_downs_value_list.append(ups_downs_value)
            data_dict['ups_downs_value']=ups_downs_value_list
            #收益比例
            return_list=self.position[stock]['return']
            if pre_value<=0:
                return_ratio=0
            else:
                return_ratio=ups_downs_value/pre_value
            return_list.append(return_ratio)
            data_dict['return']=return_list
            #累计收益cumsum_return
            cumsum_return_list=self.position[stock]['cumsum_return']
            pre_cumsum_return=cumsum_return_list[-1]
            cumsum_return=return_ratio+pre_cumsum_return
            cumsum_return_list.append(cumsum_return)
            data_dict['cumsum_return']=cumsum_return_list


            #交易类型trader_type
            trader_type_list=self.position[stock]['trader_type']
            trader_type_list.append(trader_type)
            data_dict['trader_type']=trader_type_list
            self.position[stock]=data_dict
            #结算账户
            portfolio_log=self.get_cacla_portfolio_dict()
            host_cost=portfolio_log['host_cost'].get(date,0)
            trader_value=portfolio_log['trader_value'].get(date,0)
            ups_downs_value=portfolio_log['ups_downs_value'].get(date,0)
            self.portfolio.adjust_portfolio_data(trader_type=trader_type,date=date,trader_value=trader_value,
                                                 ups_downs_value=ups_downs_value,host_cost=host_cost)
            return self.position

        else:
            return '未知的交易状态'
    def del_isition(self,stock='600031'):
        '''
        删除持股
        '''
        del self.position[stock]
        return self.position
    def get_total_position(self):
        '''
        获取总数据
        pandas格式
        '''
        stock_list=list(self.position.keys())
        result=pd.DataFrame()
        for stock in stock_list:
            df=pd.DataFrame(self.position[stock])
            try:
                del df['stock']
                del df['price']
            except:
                pass
            result=pd.concat([result,df],ignore_index=True)
        self.total_position=result.groupby(by=['date']).sum()
        return self.total_position 
    def get_cacla_portfolio(self):
        '''
        获取需要输入账户的数据
        '''
        stock_list=list(self.position.keys())
        result=pd.DataFrame()
        for stock in stock_list:
            df=pd.DataFrame(self.position[stock])
            result=pd.concat([result,df],ignore_index=True)
        result=result[['date','host_cost','trader_value','ups_downs_value']]
        data=result.groupby(by=['date']).sum()
        return data
    def get_cacla_portfolio_dict(self):
        '''
        获取需要输入账户的数据
        '''
        stock_list=list(self.position.keys())
        result=pd.DataFrame()
        for stock in stock_list:
            df=pd.DataFrame(self.position[stock])
            result=pd.concat([result,df],ignore_index=True)
        result=result[['date','host_cost','trader_value','ups_downs_value']]
        data=result.groupby(by=['date']).mean()
        portfolio_dict=dict()
        portfolio_dict['host_cost']=dict(zip(data.index,data['host_cost']))
        portfolio_dict['trader_value']=dict(zip(data.index,data['trader_value']))
        portfolio_dict['ups_downs_value']=dict(zip(data.index,data['ups_downs_value']))
        return portfolio_dict
    def get_total_position_trader(self):
        '''
        获取总数据交易数据
        '''
        stock_list=list(self.position.keys())
        result=pd.DataFrame()
        for stock in stock_list:
            df=pd.DataFrame(self.position[stock])
            result=pd.concat([result,df],ignore_index=True)
        return result
    
    def get_position_by_stock(self,stock='600031'):
        '''
        通过股票代码来获取持股
        '''
        stock_list=list(self.position.keys())
        for stock in stock_list:
            return self.position[stock]
        else:
            print('{}没有持股'.format(stock))
            result={}
            return result
    def get_position_df_by_stock(self,stock='600031'):
        '''
        通过股票代码来获取持股
        获取表格数据
        '''
        stock_list=list(self.position.keys())
        for stock in stock_list:
            df=pd.DataFrame(self.position[stock])
            return df
        else:
            print('{}没有持股'.format(stock))
            result={}
            return result






