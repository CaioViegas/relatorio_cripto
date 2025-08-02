import requests
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Table, Column, String, Float, Integer, MetaData, DateTime

load_dotenv()

# ========== 1. Coleta de dados da API ==========
def fetch_coin_data(coin_ids):
    """
    Fetches data from CoinGecko API for the given list of coin IDs.

    Parameters
    ----------
    coin_ids : list of str
        List of coin IDs to fetch data for.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the fetched data. The columns are:
            id : str
                CoinGecko ID of the coin.
            symbol : str
                Symbol of the coin (e.g. BTC, ETH, etc.).
            name : str
                Name of the coin.
            price_usd : float
                Current price of the coin in USD.
            market_cap_usd : float
                Market capitalization of the coin in USD.
            volume_24h_usd : float
                24 hour trading volume of the coin in USD.
            change_24h_pct : float
                Percentage change in the coin's price over the past 24 hours.
            change_7d_pct : float
                Percentage change in the coin's price over the past 7 days.
            rank : int
                Market capitalization rank of the coin.
            circulating_supply : float
                Number of coins in circulation.
            total_supply : float
                Total supply of coins.
            sentiment_votes_up_percentage : float
                Percentage of users who have voted positively on the coin.
            last_updated : pd.Timestamp
                Last time the coin's data was updated on CoinGecko.

    """
    url_base = "https://api.coingecko.com/api/v3/coins/{}"
    coin_data = []

    for coin_id in coin_ids:
        response = requests.get(url_base.format(coin_id), params={'localization': 'false'})
        if response.status_code == 200:
            data = response.json()
            market = data.get('market_data', {})
            coin_data.append({
                'id': data.get('id'),
                'symbol': data.get('symbol'),
                'name': data.get('name'),
                'price_usd': market.get('current_price', {}).get('usd'),
                'market_cap_usd': market.get('market_cap', {}).get('usd'),
                'volume_24h_usd': market.get('total_volume', {}).get('usd'),
                'change_24h_pct': market.get('price_change_percentage_24h'),
                'change_7d_pct': market.get('price_change_percentage_7d'),
                'rank': data.get('market_cap_rank'),
                'circulating_supply': market.get('circulating_supply'),
                'total_supply': market.get('total_supply'),
                'sentiment_votes_up_percentage': data.get('sentiment_votes_up_percentage'),
                'last_updated': pd.to_datetime(data.get('last_updated'))
            })
    return pd.DataFrame(coin_data)


# ========== 2. Criação da conexão e estrutura do banco ==========
def create_database_and_table():
    """
    Creates a PostgreSQL database and the 'cryptos' table if it does not exist yet.

    The database is named 'cryptoproject' and the table is named 'cryptos'. The
    columns of the table are:

        id : str
            CoinGecko ID of the coin.
        symbol : str
            Symbol of the coin (e.g. BTC, ETH, etc.).
        name : str
            Name of the coin.
        price_usd : float
            Current price of the coin in USD.
        market_cap_usd : float
            Market capitalization of the coin in USD.
        volume_24h_usd : float
            24 hour trading volume of the coin in USD.
        change_24h_pct : float
            Percentage change in the coin's price over the past 24 hours.
        change_7d_pct : float
            Percentage change in the coin's price over the past 7 days.
        rank : int
            Market capitalization rank of the coin.
        circulating_supply : float
            Number of coins in circulation.
        total_supply : float
            Total supply of coins.
        sentiment_votes_up_percentage : float
            Percentage of users who have voted positively on the coin.
        last_updated : pd.Timestamp
            Last time the coin's data was updated on CoinGecko.

    Returns
    -------
    sqlalchemy.engine.Engine
        The Engine object that can be used to connect to the database.

    """
    SENHA = os.getenv("SENHA")

    db_path=f"postgresql://postgres:{SENHA}@localhost:5432/cryptoproject"
    print("DB PATH:", db_path)
    engine = create_engine(db_path)
    metadata = MetaData()

    cryptos_table = Table("cryptos", metadata,
        Column("id", String, primary_key=True),
        Column("symbol", String),
        Column("name", String),
        Column("price_usd", Float),
        Column("market_cap_usd", Float),
        Column("volume_24h_usd", Float),
        Column("change_24h_pct", Float),
        Column("change_7d_pct", Float),
        Column("rank", Integer),
        Column("circulating_supply", Float),
        Column("total_supply", Float),
        Column("sentiment_votes_up_percentage", Float),
        Column("last_updated", DateTime)
    )

    metadata.create_all(engine)
    return engine


# ========== 3. Inserção dos dados no banco ==========
def insert_data_to_db(df, engine, table_name="cryptos"):
    """
    Inserts the given DataFrame into the given database table.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be inserted.
    engine : sqlalchemy.engine.Engine
        The Engine object that can be used to connect to the database.
    table_name : str, optional
        The name of the table to insert the data into. Defaults to "cryptos".
    """
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    print("Data inserted successfully into the database.")


# ========== 4. Função principal para orquestrar tudo ==========
def run_pipeline():
    """
    Main function to run the entire pipeline.

    This function fetches data from CoinGecko for the given list of coin IDs,
    creates the database and tables, and inserts the data into the database.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    coin_ids = ['bitcoin', 'ethereum', 'ripple', 'solana', 'cardano']
    print("Collecting CoinGecko data...")
    df = fetch_coin_data(coin_ids)
    print("Creating the database and tables...")
    engine = create_database_and_table()
    print("Inserting data into the database...")
    insert_data_to_db(df, engine)
    print("Pipeline completed. Ready for Power BI.")
    print(df)


# ========== Execução ==========
if __name__ == "__main__":
    run_pipeline()
