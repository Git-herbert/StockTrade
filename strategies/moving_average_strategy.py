from strategies.base import StrategyAbstract
import pandas as pd

class MovingAverageStrategy(StrategyAbstract):
    """具体策略：移动平均交叉（SMA Crossover）。"""

    def __init__(self, symbol, ib_client, short_window=20, long_window=50):
        super().__init__(symbol, ib_client)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, new_data):
        # 更新数据
        self.data = pd.concat([self.data, pd.DataFrame([new_data])], ignore_index=True)

        if len(self.data) < self.long_window:
            return None  # 数据不足

        # 计算 SMA
        self.data['SMA_short'] = self.data['close'].rolling(window=self.short_window).mean()
        self.data['SMA_long'] = self.data['close'].rolling(window=self.long_window).mean()

        # 生成信号
        if self.data['SMA_short'].iloc[-1] > self.data['SMA_long'].iloc[-1] and \
                self.data['SMA_short'].iloc[-2] <= self.data['SMA_long'].iloc[-2]:
            return 'BUY'
        elif self.data['SMA_short'].iloc[-1] < self.data['SMA_long'].iloc[-1] and \
                self.data['SMA_short'].iloc[-2] >= self.data['SMA_long'].iloc[-2]:
            return 'SELL'
        return None