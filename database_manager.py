import sqlite3
from datetime import date
from custom_logger import CustomLogger
import ibkr_config as config

class DatabaseManager:
    """管理数据库操作：连接、建表、插入、查询"""

    def __init__(self, db_url=config.DATABASE_URL):
        self.logger = CustomLogger(name="database_manager", log_dir="logs")
        self.db_path = db_url.replace("sqlite:///", "")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)  # 允许多线程
        self.cursor = self.conn.cursor()
        self._create_table()

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
        self.logger.info("数据库表已创建或存在")

    def insert_bar(self, symbol, bar):
        """插入5秒K线数据"""
        try:
            timestamp = bar.date.strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
            INSERT OR REPLACE INTO stock_5s_kline 
            (stock_code, timestamp, open, high, low, close, volume, amount, adj_close, prev_close)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (symbol, timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume, None, None, None))
            self.conn.commit()
            self.logger.info(f"插入数据: {symbol} at {timestamp}")
        except Exception as e:
            self.logger.error(f"插入数据失败: {e}")

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
            self.logger.error(f"查询开盘价失败: {e}")
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
            self.logger.error(f"查询最新收盘价失败: {e}")
            return None

    def close(self):
        """关闭数据库连接"""
        self.conn.close()
        self.logger.info("数据库连接已关闭")