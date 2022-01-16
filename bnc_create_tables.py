import bnc

queries =   ["""CREATE TABLE assets (
            id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            symbol VARCHAR(255) NOT NULL,
            slugName VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL
            )""",
             
            """CREATE TABLE asset_ticker (
            id UUID PRIMARY KEY,
            assetId UUID,
            timestamp TIMESTAMP,
            marketCapRank INT,
            volumeRank INT,
            price FLOAT,
            volume FLOAT,
            totalSupply BIGINT,
            freeFloatSupply BIGINT,
            marketCap FLOAT,
            totalMarketCap FLOAT
            )"""]

scraper = bnc.BNCScraper()
for query in queries:
    scraper.execute_query(query)
scraper.close_connection()
