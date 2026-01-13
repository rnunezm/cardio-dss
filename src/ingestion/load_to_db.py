python -m src.ingestion.load_to_db


def load_dataframe(df, table_name):
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="replace", index=False)