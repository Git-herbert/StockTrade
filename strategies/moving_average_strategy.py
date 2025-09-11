from strategies.base import StrategyAbstract
import pandas as pd

class MovingAverageStrategy(StrategyAbstract):
    """实现简单移动平均线（SMA）交叉交易策略。

    该策略基于短期和长期移动平均线的交叉生成买入/卖出信号：
    当短期SMA从下方或平等于长期SMA的位置穿越到上方时，生成买入信号；
    当短期SMA从上方或平等于长期SMA的位置穿越到下方时，生成卖出信号。
    """

    def __init__(self, symbol, ib_client, short_window=20, long_window=50):
        """初始化移动平均线交叉策略。

        参数：
            symbol (str): 交易品种（例如，股票或资产代码）。
            ib_client (object): Interactive Brokers 客户端，用于交易操作。
            short_window (int, 可选): 短期SMA的窗口大小，默认为20。
            long_window (int, 可选): 长期SMA的窗口大小，默认为50。
        """
        super().__init__(symbol, ib_client)  # 调用父类（StrategyAbstract）的初始化方法
        self.short_window = short_window  # 存储短期SMA窗口大小
        self.long_window = long_window    # 存储长期SMA窗口大小

    def generate_signal(self, new_data):
        """根据SMA交叉策略生成交易信号。

        该方法会追加新的价格数据，计算短期和长期SMA，并检查交叉事件以生成“买入”或“卖出”信号。

        参数：
            new_data (dict): 包含新价格数据的字典（例如，{'close': 价格}）。

        返回：
            str 或 None: 如果是买入信号，返回“BUY”；如果是卖出信号，返回“SELL”；如果无信号，返回None。
        """
        # 将新数据追加到现有DataFrame，忽略索引以确保数据连续性
        self.data = pd.concat([self.data, pd.DataFrame([new_data])], ignore_index=True)

        # 检查数据是否足够计算长期SMA
        if len(self.data) < self.long_window:
            return None  # 如果数据不足以计算SMA，则返回None

        # 计算短期和长期简单移动平均线
        self.data['SMA_short'] = self.data['close'].rolling(window=self.short_window).mean()
        self.data['SMA_long'] = self.data['close'].rolling(window=self.long_window).mean()

        # 根据SMA交叉生成交易信号
        # 买入信号：短期SMA从下方或平等于长期SMA的位置穿越到上方
        if self.data['SMA_short'].iloc[-1] > self.data['SMA_long'].iloc[-1] and \
                self.data['SMA_short'].iloc[-2] <= self.data['SMA_long'].iloc[-2]:
            return 'BUY'
        # 卖出信号：短期SMA从上方或平等于长期SMA的位置穿越到下方
        elif self.data['SMA_short'].iloc[-1] < self.data['SMA_long'].iloc[-1] and \
                self.data['SMA_short'].iloc[-2] >= self.data['SMA_long'].iloc[-2]:
            return 'SELL'
        # 如果没有发生交叉，则不生成信号
        return None