import re

from src.operators.vanna_ai import VannaAI
from src.process import execute
import logging

logger = logging.getLogger(__name__)

def get_model_training_data(ddl_string: str) -> tuple[str, str]:
    parts = re.split(r'\bCOMMENT\b', ddl_string, flags=re.IGNORECASE)
    ddl = parts[0].strip()

    documentation = ""
    if len(parts) > 1:
        comment_part = parts[1]
        match = re.match(r"\s*['\"](.*?)['\"]", comment_part, flags=re.DOTALL)
        if match:
            documentation = match.group(1).strip()

    return ddl, documentation

def train_tables(vanna_ai: VannaAI) -> None:
    df_tables = execute(
        sql="SHOW TABLES FROM delta.gold",
        catalog="delta",
    schema="gold")

    table_names = df_tables.iloc[:, 0].tolist()

    logger.info(f"Found {len(table_names)} table(s): {table_names}")

    for table in table_names:
        show_create_query = f"SHOW CREATE TABLE delta.gold.{table}"
        ddl_df = execute(sql=show_create_query)
        if ddl_df.empty:
            logger.warning(f"No CREATE TABLE output for: {table}")
            continue

        ddl_string = ddl_df.iloc[0, 0]
        ddl, documentation = get_model_training_data(ddl_string=ddl_string)

        vanna_ai.train(ddl=ddl)
        if documentation:
            logger.info(f"Train On Documentation For delta.gold.{table}")

            vanna_ai.train(documentation=documentation)

        logger.info(f"Train Example Data For delta.gold.{table}")
        vanna_ai.train(sql=f"SELECT * FROM delta.gold.{table}")

    logger.info(f"Training Done")
