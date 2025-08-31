import logging
import os

if __name__ == '__main__':
    logging.basicConfig(filename='stocktrade.log', filemode='w', level=logging.DEBUG)
    # 确保日志目录存在
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建 logger
    logger = logging.getLogger('TradingBot')
    logger.setLevel(logging.INFO)

    # 创建文件处理器
    file_handler = logging.FileHandler('logs/trading.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 添加处理器到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# 测试日志
logger.info('程序启动')
logger.error('发生错误')