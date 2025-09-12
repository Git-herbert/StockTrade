import psycopg2
from urllib.parse import urlparse
from custom_logger import CustomLogger
import ibkr_db_config as config
from abc import ABC, abstractmethod

class DatabaseAbstract(ABC):
    """数据库操作抽象类：定义所有数据库管理器必须实现的接口"""

    def __init__(self, db_url=config.DATABASE_URL):
        self.logger = CustomLogger(name="database_abstract", log_dir="../logs")
        # 解析 PostgreSQL URL
        parsed_url = urlparse(db_url)
        self.conn = psycopg2.connect(
            dbname=parsed_url.path.lstrip('/'),
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port
        )
        self.cursor = self.conn.cursor()
        self._create_table()

    @abstractmethod
    def _create_table(self):
        """创建表结构"""
        pass

    @abstractmethod
    def insert_data(self, symbol, data):
        """插入数据（通用接口，根据表不同实现）"""
        pass

    def close(self):
        """关闭数据库连接"""
        self.conn.close()
        self.logger.info("数据库连接已关闭")

if __name__ == '__main__':
    DatabaseAbstract()