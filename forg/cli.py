import argparse 
import sys
import os
import shutil
import json
from pathlib import Path

def ofile(directory: Path) -> None:
    if not directory.exists(): raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    if not directory.is_dir(): raise NotADirectoryError(f"'{directory}' is not a valid directory.")

    with open("extensions.json", "r", encoding="utf-8") as f: 
        extensions = json.load(f)

    for dirpath, _, filenames in os.walk(directory):
        current_dir = Path(dirpath)
        for filename in filenames:
            ext = Path(filename.lower()).suffix
            if extensions[ext]:
                (directory/extensions[ext]).mkdir(exist_ok=True)
                shutil.move(current_dir/filename, directory/extensions[ext])

def main():
    parser = argparse.ArgumentParser(description="File organizer CLI tool", usage="forg command")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparser_run = subparsers.add_parser("run", help="Run the file organization")
    subparser_run.add_argument("directory", help="Path to the directory")
    subparser_run.add_argument("-o", "--organize", type=str, choices=["file", "name", "date", "size"], default="file", help="Organization strategy of the files.")

    args = parser.parse_args()
    if args.command == "run":
        if args.organize == "file":
            try: 
                ofile(Path(args.directory))
            except (FileNotFoundError, NotADirectoryError) as e: 
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(2)
        elif args.organize == "name":
            pass
        elif args.organize == "date":
            pass
        elif args.organize == "size":
            pass

if __name__ == "__main__":
    main()
