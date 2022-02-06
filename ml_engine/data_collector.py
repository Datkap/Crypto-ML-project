import requests as r
import pandas as pd


def get_crypto(crypto_amount: int, fiat_currency: str):
    """Collects the data about details and current quotation of given amount of cryptocurrencies compared to given
    fiat currency. """
    quotation_url = f"https://api.alternative.me/v2/ticker/?limit={crypto_amount}&?convert={fiat_currency}"

    quotation_conn = r.get(quotation_url).json()['data']

    cryptocurrency_full_df = pd.DataFrame()

    for crypto_id in quotation_conn.keys():
        crypto = quotation_conn[crypto_id]
        params = quotation_conn[crypto_id]['quotes'][fiat_currency]
        crypto.update(params)
        del crypto['quotes']
        crypto_df = pd.DataFrame.from_dict([crypto])
        cryptocurrency_full_df = cryptocurrency_full_df.append(crypto_df, ignore_index=True)

    cryptocurrency_full_df.set_index('id', inplace=True)

    return cryptocurrency_full_df


def get_fear_and_greed():
    """Collects the data about current Fear and Greed Index score."""
    fear_and_greed_url = "https://api.alternative.me/fng/?limit=1&?format=csv"
    fear_and_greed_conn = r.get(fear_and_greed_url).json()['data']
    fear_and_greed_val = pd.DataFrame(fear_and_greed_conn)
    fear_and_greed_val.drop(['timestamp', 'time_until_update'], inplace=True, axis=1)

    return fear_and_greed_val


def combine_quotes_and_f_n_g(quotes, f_n_g):
    """Combines data of cryptocurrency collected by get_crypto function with Fear and Greed Index data collected with
    get_fear_and_greed. """
    quotes_df = quotes
    quotes_df['fear_and_greed_score'] = f_n_g['value'][0]
    quotes_df['fear_and_greed_classification'] = f_n_g['value_classification'][0]

    return quotes_df
