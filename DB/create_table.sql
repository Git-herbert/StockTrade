CREATE TABLE stock_daily_kline (
    stock_code VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(10, 4) NOT NULL,
    high NUMERIC(10, 4) NOT NULL,
    low NUMERIC(10, 4) NOT NULL,
    close NUMERIC(10, 4) NOT NULL,
    volume BIGINT NOT NULL,
    amount NUMERIC(15, 2),
    adj_close NUMERIC(10, 4),
    prev_close NUMERIC(10, 4),
    PRIMARY KEY (stock_code, date)
);

CREATE TABLE stock_5s_kline (
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