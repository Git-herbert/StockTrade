SYMBOLCONFIG = [
    {
        "symbol": "TSLA",
        "strategy": "PriceDropStrategy",
        "quantity": 1,
        # 可添加策略特定参数，例如："other_param": "value"
    },
    {
        "symbol": "AAPL",
        "strategy": "MovingAverageStrategy",
        "quantity": 10,
        "short_window": 20,  # 示例：MovingAverageStrategy 的参数
        "long_window": 50,
    },
    # 添加更多股票，例如：
    # {
    #     "symbol": "GOOG",
    #     "strategy": "PriceDropStrategy",
    #     "quantity": 5,
    # },
]