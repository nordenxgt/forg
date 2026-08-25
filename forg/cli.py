import argparse 
import sys
import os
import shutil
from pathlib import Path

def ofile(directory):
    directory = Path(directory)
    dir_contents = list(os.walk(directory))
    if directory.exists():
        for f in ["Documents", "Images", "Audios", "Videos"]:
            (directory/f).mkdir(exist_ok=True)
    for _, _, filenames in dir_contents:
        for filename in filenames:
            if filename.lower().endswith(".pdf"):
                shutil.move(filename, (directory/"Documents"))
            if filename.lower().endswith(".jpg"):
                shutil.move(filename, (directory/"Images"))
            elif filename.lower().endswith(".mp3"):
                shutil.move(filename, (directory/"Audios"))
            elif filename.lower().endswith(".mp4"):
                shutil.move(filename, (directory/"Videos"))
        

def main():
    parser = argparse.ArgumentParser(description="File organizer CLI tool", usage="forg command")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparser_run = subparsers.add_parser("run", help="Run the file organization")
    subparser_run.add_argument("folder", help="Path to the directory/directory")
    subparser_run.add_argument("-o", "--organize", type=str, choices=["file", "name", "date", "size"], default="file", help="Organization strategy of the files.")
    args = parser.parse_args()
    if args.command == "run":
        if args.organize == "file":
            ofile(args.folder)
        elif args.organize == "name":
            pass
        elif args.organize == "date":
            pass
        elif args.organize == "size":
            pass

if __name__ == "__main__":
    main()
