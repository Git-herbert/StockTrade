from secedgar import filings, FilingType

# 10Q filings for Apple (ticker "aapl")
my_filings = filings(cik_lookup="TSLA",
                     filing_type=FilingType.FILING_10Q,
                     user_agent="herbertxu_chn@hotmail.com")
my_filings.save('/path/to/dir')


##https://github.com/sec-edgar/sec-edgar