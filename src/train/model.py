import re
from time import sleep

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

def train_tables(vanna_ai: VannaAI, sleep_value: int = 15) -> None:
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

            # avoid rate limits
            logger.info(f"We sleep {sleep_value} seconds to avoid Gemini Rate Limits")
            sleep(sleep_value)
            vanna_ai.train(documentation=documentation)

        logger.info(f"Train Example Data For delta.gold.{table}")
        logger.info(f"We sleep {sleep_value} seconds to avoid Gemini Rate Limits")
        sleep(sleep_value)
        vanna_ai.train(sql=f"SELECT * FROM delta.gold.{table}")

    vanna_ai.train(sql="""
        SELECT
            f.play_id,
            f.play_timestamp,
            f.watch_duration_seconds,
            f.ingest_date AS play_ingest_date,
        
            -- Video info
            v.video_id,
            v.title AS video_title,
            v.description AS video_description,
            v.duration_seconds AS video_duration_seconds,
            v.upload_timestamp AS video_upload_timestamp,
            v.ingest_date AS video_ingest_date,
        
            -- Category info
            c.category_id,
            c.category_name,
            c.ingest_date AS category_ingest_date,
        
            -- Creator info
            cr.creator_id,
            cr.creator_name,
            cr.channel_name,
            cr.join_date AS creator_join_date,
            cr.ingest_date AS creator_ingest_date,
        
            -- User info
            u.user_id,
            u.user_name,
            u.subscription_type,
            u.registration_date AS user_registration_date,
            u.ingest_date AS user_ingest_date
        
        FROM delta.gold.fact_video_plays f
        LEFT JOIN delta.gold.dim_videos v ON f.video_id = v.video_id
        LEFT JOIN delta.gold.dim_categories c ON f.category_id = c.category_id
        LEFT JOIN delta.gold.dim_creators cr ON f.creator_id = cr.creator_id
        LEFT JOIN delta.gold.dim_users u ON f.user_id = u.user_id
    """)

    logger.info(f"Training Done")
