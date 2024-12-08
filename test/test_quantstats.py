import quantstats as qs
import pandas as pd
import numpy as np

date_index = pd.date_range(start='2020-01-01 00:00', periods=1000)
stock_returns = pd.Series((np.random.random(size=1000) - 0.5) / 10, index=date_index)
print("type of stock_returns:", type(stock_returns), stock_returns)
# qs.reports.html(stock_returns.squeeze(), file="test_quantstats.html")
# qs.reports.html(pd.Series(stock_returns), file="test_quantstats.html")

qs.reports.html(stock_returns, output="test_quantstats.html")




