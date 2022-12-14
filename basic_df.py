import pandas as pd

# import yfinance as yf
zero = pd.read_csv('./dataset/ZeroTrade.csv')
n50 = pd.read_csv('./dataset/Nifty50_data.csv', thousands=',')

data = pd.DataFrame(index=zero.index)
data['Stock'] = zero.symbol
data['Price'] = zero.price
data['Qty'] = zero.trade_type.map({'buy': 1, 'sell': -1}) * zero.quantity
data['Amount'] = data['Price'] * data['Qty']

data['cum_qty'] = data.groupby('Stock')['Qty'].cumsum()
data['cum_Amt'] = data.groupby('Stock')['Amount'].cumsum()
data['cum_Avg'] = data.loc[data['cum_qty'] > 0]['cum_Amt'] / data.loc[data['cum_qty'] > 0]['cum_qty']
data['Profit'] = -1 * data.loc[data['cum_qty'] == 0]['cum_Amt']
data['Profit'] = data['Profit'].fillna(0)
data['%Profit'] = -100 * data['Profit'] / data['Amount']
data['%Profit'] = data.groupby('Stock')['%Profit'].cumsum()
data['cum_profit'] = data.groupby('Stock')['Profit'].cumsum()
data['Invested_amt'] = data['cum_Amt'] + data['cum_profit']
data['apparent_avg'] = data['Invested_amt'] / data['cum_qty']
data['apparent_amt'] = data['apparent_avg'] * data['cum_qty']
data = data.fillna(0)

stock_slice = []
for i in data['Stock'].drop_duplicates():
    stock_df = data.loc[data['Stock'] == i]
    ind_x = stock_df[stock_df['cum_qty'].map(lambda x: x == 0)].index
    stock_slice.append(stock_df.tail(1).index[0])

stock_slice = pd.Index(stock_slice)
foli0 = data.iloc[stock_slice]
foli0 = foli0.set_index('Stock')
foli0.loc['Total'] = foli0.sum(numeric_only=True)
foli0.loc['Total', ['apparent_avg', 'cum_Avg']] = pd.NA
foli0.loc['Total', ['%Profit']] = 100 * foli0.at['Total', 'cum_profit'] / foli0.at['Total', 'Invested_amt']
print(foli0[['Invested_amt', 'cum_profit', 'cum_qty', 'apparent_avg', 'cum_Avg', '%Profit']])


s50 = set(n50.Symbol)
s0 = set(foli0.index)

n50 = n50.set_index('Symbol')
n50 = n50.sort_index()
slice_bool_n50 = [x in s50.intersection(s0) for x in n50.index]
slice_bool_foli0 = [x in s50.intersection(s0) for x in foli0.index]
foli0['CMP'] = n50['Last Traded Price']

foli0['CMP_profit'] = foli0['CMP']*foli0['cum_qty']-foli0['apparent_amt']
foli0['CMP_diff'] = foli0['CMP']-foli0['apparent_avg']
print(foli0[['apparent_avg', 'CMP', 'CMP_diff', 'CMP_profit', 'cum_Avg']])
