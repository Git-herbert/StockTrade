import psycopg2
from urllib.parse import urlparse
import logging

# IBKR Config
LOCALHOST = '127.0.0.1'
PORT = 19994  # Default port for the server
sender_email = 'xuhaobin@wareorigin.com'  # 您的企业邮箱地址
password = '6eArdSvh9C3cxeHK'  # 步骤 1 中生成的客户端专用密码

# DataBase Config
# Replace with your actual PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:Xuhaobin101225@localhost:5432/postgres"
API_KEY = "your-secret-api-key"  # Example API key
DEBUG_MODE = True  # Enable/disable debug logging

# Set up logging
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        # 解析 PostgreSQL URL
        parsed_url = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            dbname=parsed_url.path.lstrip('/'),
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port
        )
        logger.info("Successfully connected to PostgreSQL database")

        # Create table
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_5s_kline (
                    stock_code VARCHAR(20) NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
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
            conn.commit()
            logger.info("Table 'stock_5s_kline' created or already exists")

        # Close connection
        conn.close()
        logger.info("Database connection closed")

    except psycopg2.Error as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise