import yfinance as yf

sp500 = yf.Ticker('^GSPC')
print(type(sp500.history()))
print(type(sp500.history))
print(sp500.download())

