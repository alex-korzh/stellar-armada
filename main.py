import argparse
from app.run import run_game


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the game")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()
    run_game(args.debug)
