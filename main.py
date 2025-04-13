import argparse
import logging

from src.models.google_gemini_chat_config import GoogleGeminiChatConfig
from src.operators.vanna_ai import VannaAI
from src.train.model import train_tables
from vanna.flask import VannaFlaskApp
from src.process import execute

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


def main(train: bool):
    google_gemini_chat_config = GoogleGeminiChatConfig()
    vanna_ai = VannaAI(google_gemini_chat_config=google_gemini_chat_config)

    vanna_ai.run_sql = execute
    vanna_ai.run_sql_is_set = True

    if train:
        logging.info("Training enabled. Running train_tables...")
        train_tables(vanna_ai=vanna_ai)
    else:
        logging.info("Training flag not set. Skipping training.")

    app = VannaFlaskApp(vanna_ai, allow_llm_to_see_data=True)

    app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the main script with optional training.")
    parser.add_argument(
        "--train",
        action="store_true",
        help="If set, run training on tables using train_tables function."
    )

    args = parser.parse_args()
    main(train=args.train)
