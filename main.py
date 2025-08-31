import strategies
from trading_agent.trading_agent import TradingAgent
from strategies.moving_average_strategy import MovingAverageStrategy
import IBKRConfig as config

if __name__ == '__main__':

    agent = TradingAgent()

    for one in config.SYMBOLLIST:

        # 切换到移动平均策略
        agent.set_strategy(MovingAverageStrategy, symbol=one['symbol'], short_window=20, long_window=50)

        agent.run(one)