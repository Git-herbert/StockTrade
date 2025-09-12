from strategies.base import StrategyAbstract
import ibkr_db_config as config


class PriceDropStrategy(StrategyAbstract):
    """
    价格跌幅策略：管理卖出/买回状态。
    """

    def __init__(self, symbol, ib_client, **kwargs):
        super().__init__(symbol, ib_client)
        self.sold = False  # 是否已卖出
        self.quantity = kwargs.get('quantity', 1)  # 默认1股

    def generate_signal(self, new_data):
        # 此策略不使用generate_signal（因为逻辑在线程中），但为兼容实现
        return None

    def check_and_trade(self, today_open, current_close):
        if today_open is None or current_close is None:
            return

        drop_pct = (current_close - today_open) / today_open * 100
        if drop_pct < -config.DROP_THRESHOLD and not self.sold:
            self.execute_order('SELL', self.quantity)
            self.sold = True
        elif drop_pct >= -config.DROP_THRESHOLD and self.sold:
            self.execute_order('BUY', self.quantity)
            self.sold = False