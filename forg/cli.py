import argparse 
import sys
from pathlib import Path
from forg.service import run_organizer

def main():
    parser = argparse.ArgumentParser(description="File organizer CLI tool", usage="forg command")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparser_run = subparsers.add_parser("run", help="Run the file organization")
    subparser_run.add_argument("directory", help="Path to the directory")
    subparser_run.add_argument(
        "-o", 
        "--organize",
        type=str,
        choices=["file", "name", "date", "size"],
        default="file",
        help="Organization strategy of the files."
    )
    args = parser.parse_args()
    if args.command == "run":
        try:
            run_organizer(Path(args.directory), args.organize)
            print(f"Sucessfully organized '{args.directory}' by '{args.organize}' strategy")
        except (FileNotFoundError, NotADirectoryError, ValueError) as e: 
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(2)

if __name__ == "__main__":
    main()
