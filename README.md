# bnc
Data scraper for the Brave New Coin API https://rapidapi.com/BraveNewCoin/api/bravenewcoin/. This uses the code snippets for Python `requests`.

[Related Medium article](https://naziahabib.medium.com/create-a-data-scraper-in-python-67247e89e146)

Use the following definitions in your requests as defined in `bnc.py`:

`bnc_api_key` = <your_api_key_here>

`bnc_host` = 'bravenewcoin.p.rapidapi.com'

`bnc_audience` = 'https://api.bravenewcoin.com'

`bnc_client_id` = <client_id_here>

`bnc_access_token_url` = 'https://bravenewcoin.p.rapidapi.com/oauth/token'

`bnc_asset_url` = 'https://bravenewcoin.p.rapidapi.com/asset'

`bnc_asset_ticker_url` = 'https://bravenewcoin.p.rapidapi.com/market-cap'

## Getting data
Run the `bnc_create_tables.py` file to create the two tables `assets` and `asset_ticker` and populate the `assets` table.

Schedule the `bnc_scraper.py` file to scrape data from the API as often as every five minutes and write to the `asset_ticker` table.
