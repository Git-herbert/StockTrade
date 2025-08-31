from abc import ABC, abstractmethod
from ib_insync import IB, Stock, util, MarketOrder
import pandas as pd
import logging
import IBKRConfig as config # Import your config file
from ib_insync import IB, Stock, util, MarketOrder

class TradingAgent():
    """
    主程序：管理连接、数据订阅和策略切换。
    """

    def __init__(self, host=config.LOCALHOST, port=config.PORT, client_id=1):
        self.ib = IB()
        self.ib.connect(host, port, client_id)
        util.startLoop()  # 对于 Jupyter 或需要事件循环的环境
        self.strategy = None

    def set_strategy(self, strategy_class, symbol, **kwargs):
        """切换策略：传入策略类和参数。"""
        self.strategy = strategy_class(symbol, self.ib, **kwargs)
        logging.info(f"切换到策略: {strategy_class.__name__}")

    def on_bar_update(self, bars, has_new_bar):
        """实时数据回调：处理新 Bar 数据。"""
        if has_new_bar:
            new_data = {'date': bars[-1].date, 'close': bars[-1].close}  # 简化示例
            signal = self.strategy.generate_signal(new_data)
            if signal == 'BUY':
                self.strategy.execute_order('BUY')
            elif signal == 'SELL':
                self.strategy.execute_order('SELL')

    def run(self, symbol):
        """启动：订阅实时数据。"""
        if not self.strategy:
            raise ValueError("请先设置策略")

        bars = self.ib.reqRealTimeBars(self.strategy.contract, 5, 'MIDPOINT', False)
        bars.updateEvent += self.on_bar_update
        print("run")
        self.ib.run()  # 进入事件循环