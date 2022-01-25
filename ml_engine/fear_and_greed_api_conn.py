import requests as r
import pandas as pd

fiat_currency = 'USD'
crypto_amount = 5

quotation_url = f"https://api.alternative.me/v2/ticker/?limit={crypto_amount}&?convert={fiat_currency}"

quotation_conn = r.get(quotation_url).json()['data']

cryptocurrency_full_df = pd.DataFrame()

for crypto_id in quotation_conn.keys():
    crypto = quotation_conn[crypto_id]
    params = quotation_conn[crypto_id]['quotes'][fiat_currency]
    crypto.update(params)
    del crypto['quotes']
    crypto_df = pd.DataFrame.from_dict([crypto])
    cryptocurrency_full_df.append(crypto_df, ignore_index=True)




fear_and_greed_url = "https://api.alternative.me/fng/?limit=10&?format=csv"
fear_and_greed_conn = r.get(fear_and_greed_url).text

df = pd.read_json(fear_and_greed_conn)
df.head()
