import IBKRConfig as config # Import your config file
from ib_insync import IB, Stock, util, MarketOrder
from custom_logger import CustomLogger

class TradingAgent():
    """
    主程序：管理连接、数据订阅和策略切换。
    """

    def __init__(self, host=config.LOCALHOST, port=config.PORT, client_id=1):
        self.logger = CustomLogger(name="trading_agent", log_dir="logs")
        self.logger.info(f"执行：TradingAgent：__init__")
        self.ib = IB()
        self.ib.connect(host, port, client_id)
        util.startLoop()  # 对于 Jupyter 或需要事件循环的环境
        self.strategy = None

    def set_strategy(self, strategy_class, symbol, **kwargs):
        """切换策略：传入策略类和参数。"""
        self.logger.info(f"执行：TradingAgent：set_strategy")
        self.strategy = strategy_class(symbol, self.ib, **kwargs)
        self.logger.info(f"切换到策略: {strategy_class.__name__}")


    def run_by_tick(self):
        """启动：订阅实时数据。"""
        self.logger.info(f"执行：TradingAgent：run")
        if not self.strategy:
            raise ValueError("请先设置策略")
        ticker = self.ib.reqMktData(self.strategy.contract)
        while True:
            self.ib.sleep(2)
            if ticker.last != float('nan'):
                self.logger.info(f"tick={ticker}")



    def on_bar_update(self, bars, has_new_bar):
        self.logger.info(f"执行：TradingAgent：on_bar_update")
        """实时数据回调：处理新 Bar 数据。"""
        if has_new_bar:
            new_data = {'date': bars[-1].date, 'close': bars[-1].close}  # 简化示例
            signal = self.strategy.generate_signal(new_data)
            if signal == 'BUY':
                # self.strategy.execute_order('BUY')
                pass
            elif signal == 'SELL':
                # self.strategy.execute_order('SELL')
                pass

    def run_by_bar(self):
        """启动：订阅实时数据。"""
        self.logger.info(f"执行：TradingAgent：run")
        if not self.strategy:
            raise ValueError("请先设置策略")
        # reqRealTimeBars: 这是一个异步方法，用于向 IB 请求实时 K 线数据（每 5 秒生成一根 K 线）。
        # new_bar 是一个 RealTimeBar 对象，包含时间戳、开盘价、最高价、最低价、收盘价、成交量等信息。
        bars = self.ib.reqRealTimeBars(self.strategy.contract, 5, 'MIDPOINT', False)
        # bars.updateEvent: RealTimeBarList 对象的 updateEvent 是一个事件（ib_insync 使用事件驱动模型）。每当新的 K 线数据到达时，IB 会触发这个事件。
        bars.updateEvent += self.on_bar_update
        # 启动 ib_insync 的事件循环，处理与 IB 的异步通信（如接收实时数据、处理回调等）。
        self.ib.run()  # 进入事件循环