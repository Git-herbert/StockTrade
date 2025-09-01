import strategies
from trading_agent.trading_agent import TradingAgent
from strategies.moving_average_strategy import MovingAverageStrategy
import IBKRConfig as config
from custom_logger import CustomLogger

if __name__ == '__main__':

    logger = CustomLogger(name="main", log_dir="logs")

    agent = TradingAgent()

    # 切换到移动平均策略
    agent.set_strategy(MovingAverageStrategy, symbol=config.SYMBOL, short_window=20, long_window=50)

    agent.run_by_tick()