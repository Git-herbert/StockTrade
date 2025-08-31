from ib_insync import IB, Stock
import ibkrconfig  # Import your config file

# Connect to TWS using config port
ib = IB()
ib.connect('127.0.0.1', ibkrconfig.PORT, clientId=1)

# Define the stock contract using config symbol
stock_contract = Stock(ibkrconfig.SYMBOL, 'SMART', 'USD')
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