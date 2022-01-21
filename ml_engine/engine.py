import pandas as pd
from fear_and_greed_api_conn import fear_and_greed_conn

fear_and_greed_df = pd.read_csv(fear_and_greed_conn)

fear_and_greed_df.head()
