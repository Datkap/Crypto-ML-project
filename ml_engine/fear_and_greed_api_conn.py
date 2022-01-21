import requests as r
import pandas as pd

quotation_url = "https://api.alternative.me/v2/ticker/?limit=3&?convert=USD"
quotation_conn = r.get(quotation_url).json()

fear_and_greed_url = "https://api.alternative.me/fng/?limit=10&?format=csv"
fear_and_greed_conn = r.get(fear_and_greed_url).text

df = pd.read_json(fear_and_greed_conn)
df.head()
