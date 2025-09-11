import threading
from trading_agent import TradingAgent
from strategies.price_drop_strategy import PriceDropStrategy
import ibkr_config as config
from custom_logger import CustomLogger

if __name__ == '__main__':
    logger = CustomLogger(name="main", log_dir="logs")

    agent = TradingAgent()

    # 切换到价格跌幅策略
    symbol_info = config.SYMBOLLIST[0]
    agent.set_strategy(PriceDropStrategy, symbol=symbol_info["symbol"], quantity=symbol_info["quantity"])

    # 启动线程
    thread1 = threading.Thread(target=agent.data_collection_thread)
    thread2 = threading.Thread(target=agent.trading_logic_thread)
    thread1.start()
    thread2.start()

    # 等待线程
    thread1.join()
    thread2.join()