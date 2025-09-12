from ib_insync import IB, Stock, util
from custom_logger import CustomLogger

class IbkrAgent:
    """管理IBKR实时数据采集"""

    def __init__(self, host, port, client_id, db_manager):
        self.logger = CustomLogger(name="data_collector", log_dir="logs")
        self.ib = IB()
        self.ib.connect(host, port, client_id)
        self.db_manager = db_manager
        util.startLoop()  # 事件循环
        self.logger.info("DataCollector 初始化完成")

    def on_bar_update(self, bars, has_new_bar, symbol):
        """处理新Bar数据，插入数据库"""
        if has_new_bar:
            self.db_manager.insert_5s_bar(symbol, bars[-1])

    def subscribe_realtime_bars(self, contract, symbol):
        """订阅实时5秒K线"""
        bars = self.ib.reqRealTimeBars(contract, 5, 'MIDPOINT', False)
        bars.updateEvent += lambda bars, has_new_bar: self.on_bar_update(bars, has_new_bar, symbol)
        self.logger.info(f"订阅 {symbol} 的5秒K线")
        return bars

    def run(self):
        """运行事件循环"""
        self.ib.run()