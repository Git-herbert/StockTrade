from ib_insync import IB, Stock
import ibkr_config

# Connect to TWS using config port
ib = IB()
ib.connect('127.0.0.1', IBKRConfig.PORT, clientId=1)

# Define the stock contract using config symbol
stock_contract = Stock(IBKRConfig.SYMBOL, 'SMART', 'USD')
ib.qualifyContracts(stock_contract)

# Request snapshot market data
ticker = ib.reqMktData(stock_contract, snapshot=True)

# Wait for data
ib.sleep(5)

# Print prices
print(f"Last Price: {ticker.last}")
print(f"Bid Price: {ticker.bid}") # 买价
print(f"Ask Price: {ticker.ask}") # 卖家
print(f"Close Price (Previous): {ticker.close}")
print(ticker)

ib.disconnect()