import requests as r
import pandas as pd
import os


def get_crypto(crypto_amount: int, fiat_currency: str):
    """Collects the data about details and current quotation of given amount of cryptocurrencies compared to given
    fiat currency."""
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

    return cryptocurrency_full_df


def get_fear_and_greed():
    """Collects the data about current Fear and Greed Index score."""
    fear_and_greed_url = "https://api.alternative.me/fng/?limit=1&?format=csv"
    fear_and_greed_conn = r.get(fear_and_greed_url).json()['data']
    fear_and_greed_val = pd.DataFrame(fear_and_greed_conn)
    fear_and_greed_val.drop(['timestamp', 'time_until_update'], inplace=True, axis=1)

    return fear_and_greed_val


def combine_quotes_and_fng(quotes, fng):
    """Combines data of cryptocurrency collected by get_crypto function with Fear and Greed Index data collected with
    get_fear_and_greed."""
    quotes['fear_and_greed_score'] = fng['value'][0]
    quotes['fear_and_greed_classification'] = fng['value_classification'][0]

    return quotes


def save_data(quotes, path='Quotes'):
    """Splits data collected with combine_quotes_and_fng into separate cryptos and saves them in desired destination
    as csv files. """
    if not os.path.exists(path):
        os.mkdir(path)

    for crypto_id in quotes['id']:
        full_path = path + f"/{crypto_id}_{quotes['name'].loc[quotes['id'] == crypto_id].iloc[0]}".replace(" ", "_") + \
                    ".csv"
        if os.path.exists(full_path):
            current_df = pd.read_csv(full_path)
            updated_df = current_df.append(quotes.loc[quotes['id'] == crypto_id], ignore_index=True)
            updated_df.to_csv(full_path, index=False)
        else:
            new_df = quotes.loc[quotes['id'] == crypto_id]
            new_df.to_csv(full_path, index=False)