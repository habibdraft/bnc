import psycopg2
import config

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

try:
    self.conn = psycopg2.connect(config.PGConnString)
except:
    print ("Unable to connect to the database")
    
cur = conn.cursor()
for query in queries:
    cur.execute(queries)
cur.close()
conn.commit()

if conn is not None:
    conn.close()