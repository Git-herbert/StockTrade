from base import StrategyAbstract
import pandas as pd

class RSIStrategyAgent(StrategyAbstract):
    """具体策略：RSI 超买超卖。"""

    def __init__(self, symbol, ib_client, rsi_period=14, overbought=70, oversold=30):
        super().__init__(symbol, ib_client)
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold

    def calculate_rsi(self):
        delta = self.data['close'].diff(1)
        gain = delta.where(delta > 0, 0).rolling(window=self.rsi_period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signal(self, new_data):
        # 更新数据
        self.data = pd.concat([self.data, pd.DataFrame([new_data])], ignore_index=True)

        if len(self.data) < self.rsi_period:
            return None

        rsi = self.calculate_rsi().iloc[-1]

        if rsi < self.oversold:
            return 'BUY'
        elif rsi > self.overbought:
            return 'SELL'
        return None