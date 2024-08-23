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
    parser.add_argument("-r", help="Format is 1024x768")
    args = parser.parse_args()
    res = None
    if args.r is not None:
        sp = args.r.split("x")
        res = (int(sp[0]), int(sp[1]))
    run_game(args.debug, res)
