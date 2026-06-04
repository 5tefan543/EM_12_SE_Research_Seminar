import argparse
from pathlib import Path
from config import Config
from runner import Runner
import asyncio

from logger import set_global_log_level, get_logger, shutdown_logging
logger = get_logger("main")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the LLM security experiment."
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/config.json"),
        help="Path to the JSON config file.",
    )

    parser.add_argument(
        "--clean_output",
        action="store_true",
        help="Whether the output directory should be cleaned before running the experiment.",
    )

    return parser.parse_args()

def main() -> None:
    try:
        args = parse_args()
        config = Config.from_json_file(args.config)
        set_global_log_level(config.log_level)

        logger.info("Starting Code Generation")
        runner = Runner(config, clean_output=args.clean_output)
        asyncio.run(runner.run())
    except Exception as e:
        logger.error(f"An fatal error occurred: {e}")
    finally:
        shutdown_logging()

if __name__ == "__main__":
    main()
