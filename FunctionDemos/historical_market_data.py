from ib_insync import IB, Stock, util

ib = IB()
ib.connect('127.0.0.1', ibkrconfig.PORT, 1)

symbol_contract = Stock(ibkrconfig.SYMBOL, 'SMART', 'USD')
ib.qualifyContracts(symbol_contract)

# Request historical bars (e.g., 2 days of 15-min bars)
bars = ib.reqHistoricalData(
    symbol_contract,
    endDateTime='',  # Empty for now
    durationStr='2 D',  # 2 days
    barSizeSetting='15 mins',
    whatToShow='MIDPOINT',  # Or 'TRADES', 'BID', 'ASK'
    useRTH=True,  # Regular trading hours only
    formatDate=1  # YYYYMMDD format
)

# Convert to Pandas DataFrame
df = util.df(bars)
print(df.head())  # Displays OHLCV data

# Example: Calculate 20-period SMA
df['20_SMA'] = df['close'].rolling(window=20).mean()
print(f"Latest 20-SMA: {df['20_SMA'].iloc[-1]}")

ib.disconnect()