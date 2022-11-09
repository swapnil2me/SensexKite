import pandas as pd

# import yfinance as yf

data = pd.read_csv('dataset/Kite.csv')
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
