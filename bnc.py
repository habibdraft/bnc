import requests
import ray
import pandas as pd
import psycopg2
import psycopg2.extras
from psycopg2.extras import Json
import config

class BNCScraper:
    def __init__(self) -> None:
        self.asset_uuids = config.asset_uuids
        
        try:
            self.conn = psycopg2.connect(config.PGConnString)
        except:
            print ("Unable to connect to the database")
    
    def get_conn(self) -> psycopg2.extensions.connection: #change to decorator
        return self.conn
    
    def get_asset_uuids(self) -> list: #change to decorator
        return self.asset_uuids
    
    def execute_query(self, query: str) -> None:
        cur = self.conn.cursor()
        cur.execute(query)
        cur.close()
        self.conn.commit()
    
    def execute_query_and_return(self, query: str) -> list:
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        self.conn.commit()
        return res
    
    def close_connection(self) -> None:
        if self.conn is not None:
            self.conn.close()
            
    def get_access_token(self) -> str:
        url = config.bnc_access_token_url
        payload = """{
            \"audience\": \"%s\",
            \"client_id\": \"%s\",
            \"grant_type\": \"client_credentials\"
            }""" % (config.bnc_audience, config.bnc_client_id)
        headers = {
            'content-type': "application/json",
            'x-rapidapi-host': config.bnc_host,
            'x-rapidapi-key': config.bnc_api_key
            }
        response = requests.post(url, data=payload, headers=headers)
        res = response.json()
        return res['access_token']

    def get_all_assets(self) -> dict:
        url = config.bnc_asset_url
        querystring = {'status':'ACTIVE', 'type':'CRYPTO'}
        headers = {
            'x-rapidapi-host': config.bnc_host,
            'x-rapidapi-key': config.bnc_api_key
            }
        response = requests.get(url, headers=headers, params=querystring)
        res = response.json()
        return res['content']

    def get_asset_ticker(self, asset_uuids: list, access_token: str) -> dict:
        url = config.bnc_asset_ticker_url
        headers = {
            'authorization': "Bearer {}".format(access_token),
            'x-rapidapi-host': config.bnc_host,
            'x-rapidapi-key': config.bnc_api_key
            }
        
        ray.shutdown()
        ray.init()
        
        @ray.remote
        def f(uuid: str) -> dict:   
            querystring = {"assetId":"{}".format(uuid)}
            response = requests.get(url, headers=headers, params=querystring)
            res = response.json()
            if 'content' in res:
                return res['content'][0]

        futures = [f.remote(uuid) for uuid in asset_uuids]
        return ray.get(futures)

    def get_query_from_json(self, table: str, res: list) -> str:
        values = [list(x.values()) for x in res if x]
        columns = ','.join([list(x.keys()) for x in res if x][0])
        values_query = ''

        for record in values:
            val_list = []
            for val in record:
                if type(val) == str:
                    val = str(Json(val)).replace('"', '')
                val_list += [str(val)]
            values_query += "(" +', '.join(val_list) + "),\n"
        values_query = values_query[:-2] + ";"

        query = "INSERT INTO {} ({})\nVALUES {}".format(
            table,
            columns,
            values_query
            )
        return query
    
    def get_top_ten_currencies(self, df: pd.DataFrame) -> list:
        f = {'price': 'mean', 'volume': 'mean', 'date': 'max', 'assetid': 'first'}
        df_result = df.groupby(['name'], as_index=False).agg(f).sort_values(by=['price'], ascending=False)
        return list(df_result.head(10)['assetid'])
