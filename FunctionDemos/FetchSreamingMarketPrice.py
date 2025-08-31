from ib_insync import IB, Stock, util
import ibkrconfig

# For Jupyter or interactive: util.startLoop()

ib = IB()
ib.connect('127.0.0.1', ibkrconfig.PORT, 1)

stock_contract = Stock(ibkrconfig.SYMBOL, 'SMART', 'USD')
ib.qualifyContracts(stock_contract)

# Request streaming market data
ticker = ib.reqMktData(stock_contract)

# Simple loop to print updates for 30 seconds
for _ in range(30):
    ib.sleep(1)
    if ticker.last != float('nan'):
        print(ticker)

# Cancel and disconnect
ib.cancelMktData(stock_contract)
ib.disconnect()