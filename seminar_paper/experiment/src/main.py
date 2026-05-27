import argparse
from pathlib import Path
from config import Config
from runner import Runner
import asyncio


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

    return parser.parse_args()

def main() -> None:
    args = parse_args()
    config = Config.from_json_file(args.config)
    runner = Runner(config)
    asyncio.run(runner.run())

if __name__ == "__main__":
    main()
