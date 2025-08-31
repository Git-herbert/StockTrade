import threading
from abc import ABC, abstractmethod
from ib_insync import IB, Stock, util, MarketOrder
import pandas as pd
import logging


class StrategyAbstract(ABC):
    """
    抽象策略类：定义所有策略必须实现的接口。
    可以根据需要添加更多方法，如 on_init, on_finish 等。
    """

    def __init__(self, symbol, ib_client):
        self.symbol = symbol
        self.ib = ib_client
        self.contract = Stock(symbol, 'SMART', 'USD')  # 示例：股票合约
        self.ib.qualifyContracts(self.contract)
        self.data = pd.DataFrame()  # 存储历史或实时数据

    @abstractmethod
    def generate_signal(self, new_data):
        """
        生成信号：返回 'BUY', 'SELL' 或 None。
        new_data: 最新的市场数据（如 Bar 或 Tick）。
        """
        pass

    def execute_order(self, action, quantity=100):
        """执行订单：市场单示例。"""
        order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(self.contract, order)
        logging.info(f"执行订单: {action} {quantity} 股 {self.symbol}")
        return trade
