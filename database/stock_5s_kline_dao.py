from database.base import DatabaseAbstract
from datetime import date

class Kline5sDatabaseManager(DatabaseAbstract):
    """具体实现：针对 stock_5s_kline 表的操作"""
    # 如果子类没有定义__init__则会自动调用父类init

    def _create_table(self):
        """创建5秒K线表"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_5s_kline (
            stock_code VARCHAR(20) NOT NULL,
            timestamp DATETIME NOT NULL,
            open NUMERIC(10, 4) NOT NULL,
            high NUMERIC(10, 4) NOT NULL,
            low NUMERIC(10, 4) NOT NULL,
            close NUMERIC(10, 4) NOT NULL,
            volume BIGINT NOT NULL,
            amount NUMERIC(15, 2),
            adj_close NUMERIC(10, 4),
            prev_close NUMERIC(10, 4),
            PRIMARY KEY (stock_code, timestamp)
        );
        """)
        self.conn.commit()
        self.logger.info("stock_5s_kline 表已创建或存在")

    def insert_data(self, symbol, bar):
        """插入5秒K线数据"""
        try:
            timestamp = bar.date.strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
            INSERT OR REPLACE INTO stock_5s_kline 
            (stock_code, timestamp, open, high, low, close, volume, amount, adj_close, prev_close)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (symbol, timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume, None, None, None))
            self.conn.commit()
            self.logger.info(f"插入数据到 stock_5s_kline: {symbol} at {timestamp}")
        except Exception as e:
            self.logger.error(f"插入 stock_5s_kline 数据失败: {e}")

    def get_today_opening(self, symbol):
        """获取当日开盘价（最早的open）"""
        try:
            today = date.today().isoformat()
            self.cursor.execute("""
            SELECT open FROM stock_5s_kline
            WHERE stock_code = ? AND timestamp LIKE ? || '%'
            ORDER BY timestamp ASC LIMIT 1
            """, (symbol, today))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            self.logger.error(f"查询 stock_5s_kline 开盘价失败: {e}")
            return None

    def get_latest_close(self, symbol):
        """获取最新收盘价"""
        try:
            self.cursor.execute("""
            SELECT close FROM stock_5s_kline
            WHERE stock_code = ?
            ORDER BY timestamp DESC LIMIT 1
            """, (symbol,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            self.logger.error(f"查询 stock_5s_kline 最新收盘价失败: {e}")
            return None