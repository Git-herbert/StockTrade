import threading
import time
from custom_logger import CustomLogger
import ibkr_config as config
from data_collector import DataCollector
from database_manager import DatabaseManager

class TradingAgent:
    """协调数据采集、数据库操作和交易策略"""

    def __init__(self, host=config.LOCALHOST, port=config.PORT, client_id=1):
        self.logger = CustomLogger(name="trading_agent", log_dir="logs")
        self.db_manager = DatabaseManager()
        self.data_collector = DataCollector(host, port, client_id, self.db_manager)
        self.strategy = None
        self.logger.info("TradingAgent 初始化完成")

    def set_strategy(self, strategy_class, symbol, **kwargs):
        """切换策略"""
        kwargs['logger'] = self.logger  # 传递logger给策略
        self.strategy = strategy_class(symbol, self.data_collector.ib, **kwargs)
        self.logger.info(f"切换到策略: {strategy_class.__name__} for {symbol}")

    def data_collection_thread(self):
        """线程1：数据采集"""
        self.data_collector.subscribe_realtime_bars(self.strategy.contract, self.strategy.symbol)
        self.data_collector.run()

    def trading_logic_thread(self):
        """线程2：交易逻辑"""
        while True:
            try:
                today_open = self.db_manager.get_today_opening(self.strategy.symbol)
                current_close = self.db_manager.get_latest_close(self.strategy.symbol)
                self.strategy.check_and_trade(today_open, current_close)
            except Exception as e:
                self.logger.error(f"交易逻辑错误: {e}")
            time.sleep(5)