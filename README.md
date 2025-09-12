# StockTrade

策略1：
取出股票 及 股票使用的策略
查出股票当前价格，判断是否需要执行策略



请帮忙参考附件继续调整修改代码，使得代码可以实现以下功能：
1.调用1个线程，对股票代码进行轮询查询ibkr的实时5秒K线，然后插入数据v库
2.第2个个线程，则同样5秒对数据库的数据进行查询，如果当前价格跌幅在当日价格跌幅4个点以上，则卖出，但是如果跌穿4个点之后又返回4个点以内，则重新买回这部分股票



重新改一下整个流程，我现在先要把main.py的各个步骤先列出来，你帮忙列出TODO项的注释

1.先查询config文件夹下的ibkr_config获取ibkr的连接串信息，ibkr_config.py内没有股票的代码。
LOCALHOST='127.0.0.1'
PORT = 19994  # Default port for the server
sender_email = 'xuhaobin@wareorigin.com'  # 您的企业邮箱地址
password = '6eArdSv123xeHK'  # 步骤 1 中生成的客户端专用密码
DATABASE_URL = "sqlite:///mydatabase.db"  # Example database connection string
API_KEY = "your-secret-api-key"  # Example API key
DEBUG_MODE = True  # Enable/disable debug logging