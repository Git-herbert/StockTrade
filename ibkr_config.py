from datetime import date, datetime

LOCALHOST='127.0.0.1'
PORT = 19994  # Default port for the server
sender_email = 'xuhaobin@wareorigin.com'  # 您的企业邮箱地址
password = '6eArdSvh9C3cxeHK'  # 步骤 1 中生成的客户端专用密码
DATABASE_URL = "sqlite:///mydatabase.db"  # Example database connection string
API_KEY = "your-secret-api-key"  # Example API key
DEBUG_MODE = True  # Enable/disable debug logging

SYMBOLLIST = [
    {"symbol": "TSLA", "quantity": 1, "strategy": "PriceDropStrategy"}
]
DROP_THRESHOLD = 4.0  # 跌幅阈值，单位：%

CURRENT_DATE = date.today().isoformat()
CURRENT_TIME = datetime.now()
CURRENT_TIME_STR = CURRENT_TIME.strftime('%Y-%m-%d %H:%M:%S')  # Format: Year-Month-Day Hour:Minute:Second

if __name__ == '__main__':
    print(CURRENT_DATE)
    print(type(CURRENT_DATE))
    print(CURRENT_TIME)
    print(CURRENT_TIME_STR)
    print("aaa" + "bbb")
    pass