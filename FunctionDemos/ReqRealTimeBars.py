from ib_insync import IB, Stock

# For Jupyter or interactive: util.startLoop()

ib = IB()
ib.connect('127.0.0.1', IBKRConfig.PORT, 1)

stock_contract = Stock(IBKRConfig.SYMBOL, 'SMART', 'USD')
ib.qualifyContracts(stock_contract)

# Request streaming market data
bars = ib.reqRealTimeBars(stock_contract, 5, 'MIDPOINT', False)

ib.run()
ib.disconnect()


