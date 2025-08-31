from ib_insync import IB, Stock, MarketOrder, LimitOrder
import ibkrconfig

ib = IB()
ib.connect('127.0.0.1', ibkrconfig.PORT, 1)

contract = Stock(ibkrconfig.SYMBOL, 'SMART', 'USD')
ib.qualifyContracts(contract)

# Create a market order to sell 1 share (use caution!)
order = MarketOrder(
    action='SELL',  # Or 'BUY'
    totalQuantity=1,
    outsideRth=True,  # Allows after-hours/overnight execution
    tif='GTC'  # Persists overnight until canceled or filled
)

# order = LimitOrder(
#     action='BUY',          # Or 'SELL'
#     totalQuantity=1,
#     lmtPrice=150.00,       # Limit price; set based on pre-market quotes
#     outsideRth=True,       # Key: Allows execution outside regular hours (pre-market/after-hours)
#     tif='GTC'              # Time in Force: Good Til Canceled (spans sessions if needed)
# )

trade = ib.placeOrder(contract, order)

ib.sleep(1)
print(f"Order ID: {trade.order.orderId}, Status: {trade.orderStatus.status}")

ib.disconnect()
