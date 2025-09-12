from ib_insync import IB, Stock

# For Jupyter or interactive: util.startLoop()

ib = IB()
ib.connect('127.0.0.1', IBKRConfig.PORT, 1)

stock_contract = Stock(IBKRConfig.SYMBOL, 'SMART', 'USD')
ib.qualifyContracts(stock_contract)

# Request streaming market data
ticker = ib.reqMktData(stock_contract)

# Simple loop to print updates for 30 seconds
for _ in range(30):
    ib.sleep(1)
    if ticker.last != float('nan'):
        print(ticker)
        print(ticker.close)

# Cancel and disconnect
ib.cancelMktData(stock_contract)
ib.disconnect()


