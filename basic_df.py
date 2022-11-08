import pandas as pd

# import yfinance as yf

data = pd.read_csv('dataset/Kite.csv')
data['amm'] = data['Price'] * data['Qty']

sold = data.loc[data['Qty'] < 0]
bought = data.loc[data['Qty'] > 0]

sold_pivot = sold.drop(columns=['Price', 'amm']).pivot_table(index='Stock',
                                                             aggfunc='sum')
sold_pivot['avg_sold'] = sold_pivot['Amount'] / sold_pivot['Qty']

bought_pivot = bought.drop(columns=['Price', 'amm']).pivot_table(index='Stock',
                                                                 aggfunc='sum')
bought_pivot['avg'] = bought_pivot['Amount'] / bought_pivot['Qty']

sold_pivot['avg_buy'] = bought_pivot['avg']

sold_pivot['profit_per_stock'] = sold_pivot['avg_sold'] - sold_pivot['avg_buy']
sold_pivot['profit'] = sold_pivot['profit_per_stock'] * sold_pivot['Qty'] * -1

print(sold_pivot)
print(sum(sold_pivot['profit']))
# tickerSymbol = 'REL'
# tickerData = yf.Ticker(tickerSymbol)
#
# print(tickerData.history())
