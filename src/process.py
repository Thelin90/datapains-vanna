from src.auth.trino_auth import trino_connection
from src.operators.trino_execution import run_sql
import pandas as pd

def execute(
    sql: str,
    host: str = "localhost",
    port: int = 30610,
    user: str = "datapains",
    catalog: str = "delta",
    schema: str = "gold"
) -> pd.DataFrame:
    with trino_connection(
        host=host,
        port=port,
        user=user,
        catalog=catalog,
        schema=schema
    ) as connection:
        return run_sql(sql=sql, connection=connection)
