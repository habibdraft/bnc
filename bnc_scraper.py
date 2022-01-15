import bnc
import config

scraper = bnc.BNCScraper()
access_token = scraper.get_access_token()

select_query = 'select id from assets'
select_res = scraper.execute_query_and_return(select_query)

asset_uuids = [i[0] for i in select_res]
insert_res = scraper.get_asset_ticker(asset_uuids, access_token)
insert_query = scraper.get_query_from_json('asset_ticker', insert_res)

scraper.execute_query(insert_query)
scraper.close_connection()