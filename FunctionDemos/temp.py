import asyncio
from ib_insync import IB, Contract

class TradingApp:
    def __init__(self):
        self.ib = IB()
        self.strategy = Strategy()

    async def connect(self):
        await self.ib.connectAsync('127.0.0.1', 7497, clientId=1)

    async def request_market_data(self):
        self.strategy.contract = Contract(symbol='AAPL', secType='STK', currency='USD', exchange='SMART')
        ticker = await self.ib.reqMktDataAsync(self.strategy.contract)
        print(f"Requested market data for {self.strategy.contract.symbol}")
        return ticker

class Strategy:
    def __init__(self):
        self.contract = None

async def main():
    app = TradingApp()
    await app.connect()
    await app.request_market_data()
    # Keep the event loop running to receive market data
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())