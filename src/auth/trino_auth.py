import contextlib
from typing import Generator
import trino
from trino.auth import BasicAuthentication
from trino.dbapi import Connection
from sqlalchemy import create_engine


@contextlib.contextmanager
def trino_connection(
    host: str,
    port: int,
    user: str,
    catalog: str,
    schema: str,
    password: str | None = None,
) -> Generator[Connection, None, None]:
    if not password:
        engine_url = f"{user}@{host}:{port}/{catalog}/{schema}"
    else:
        engine_url = f"{user}:{password}@{host}:{port}/{catalog}/{schema}"

    engine = create_engine(f"trino://{engine_url}")
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()
