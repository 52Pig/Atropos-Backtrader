from xgtrader_backtrader.user_def_data.user_def_data import user_def_data
from xgtrader_backtrader.trader_tool.tdx_trader_function import tdx_trader_function
tdx=tdx_trader_function()
models=user_def_data(start_date='20210105',end_date='20230101',data_type='D')
data=models.data
df=data.get_hist_data_em(stock='513300',data_type='D')
print(df)
signal,markers=tdx.six_pulse_excalibur_hist(df['close'])
print(signal)