import argparse 
import sys
import os
import shutil
from pathlib import Path

FILE_ORGANIZATION = ("Documents", "Images", "Audios", "Videos")

def ofile(directory):
    directory = Path(directory)

    if not directory.exists(): raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    if not directory.is_dir(): raise NotADirectoryError(f"'{directory}' is not a valid directory.")

    dir_contents = list(os.walk(directory))

    for f in FILE_ORGANIZATION: 
        (directory/f).mkdir(exist_ok=True)

    for dirpath, _, filenames in dir_contents:
        current_dir = Path(dirpath)
        for filename in filenames:
            source_file = current_dir / filename
            if filename.lower().endswith(".txt"):
                shutil.move(source_file, (directory/FILE_ORGANIZATION[0]))
            elif filename.lower().endswith(".jpg"):
                shutil.move(source_file, (directory/FILE_ORGANIZATION[1]))
            elif filename.lower().endswith(".mp3"):
                shutil.move(source_file, (directory/FILE_ORGANIZATION[2]))
            elif filename.lower().endswith(".mp4"):
                shutil.move(source_file, (directory/FILE_ORGANIZATION[3]))

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
                ofile(args.directory)
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
