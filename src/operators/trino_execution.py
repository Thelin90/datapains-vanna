import pandas as pd
from trino.dbapi import Connection

def run_sql(sql: str, connection: Connection | None) -> pd.DataFrame:
    return pd.read_sql_query(sql, connection)
