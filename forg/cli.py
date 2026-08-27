import argparse 
import sys
import os
import shutil
import json
import platform
import subprocess
from pathlib import Path
from datetime import datetime

def ofile(directory: Path) -> None:
    if not directory.exists(): raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    if not directory.is_dir(): raise NotADirectoryError(f"'{directory}' is not a valid directory.")

    with open("extensions.json", "r", encoding="utf-8") as f: 
        extensions = json.load(f)

    for dirpath, _, filenames in os.walk(directory):
        current_dir = Path(dirpath)
        for filename in filenames:
            ext = Path(filename.lower()).suffix
            if extensions.get(ext):
                (directory/extensions[ext]).mkdir(exist_ok=True)
                shutil.move(current_dir/filename, directory/extensions[ext])

def get_linux_creation_date(filepath):
    result = subprocess.run(["stat", "-c", "%W", filepath], capture_output=True, text=True, check=True)
    result = result.stdout.strip()
    if result in ["0", "-"]:
        raise ValueError("Birth time/Creation date not supported by this filesystem.")
    result = float(result)
    return result

def odate(directory: Path) -> None:
    for dirpath, _, filenames in os.walk(directory):
        current_dir = Path(dirpath)
        for filename in filenames:
            created_time = None
            if platform.system() == "Windows":
                created_time = (current_dir/filename).stat().st_ctime
            if platform.system() == "Darwin":
                created_time = (current_dir/filename).stat().st_birthtime
            if platform.system() == "Linux":
                created_time = get_linux_creation_date(Path(current_dir/filename))
            created_date = datetime.fromtimestamp(created_time).date()
            (directory/str(created_date)).mkdir(exist_ok=True)
            shutil.move(current_dir/filename, directory/str(created_date))

def oname(directory: Path) -> None:
    for dirpath, _, filenames in os.walk(directory):
        current_dir = Path(dirpath)
        for filename in filenames:
            file_ord = ord(filename[0].upper())
            if 65 <= file_ord <= 75:
                d = f"{chr(65)}-{chr(75)}"
                d.mkdir(exist_ok=True)
                shutil.move(current_dir/filename, directory/d)
            elif 76 <= file_ord <= 85:
                d = f"{chr(76)}-{chr(85)}"
                d.mkdir(exist_ok=True)
                shutil.move(current_dir/filename, directory/d)
            elif 86 <= file_ord <= 90:
                d = f"{chr(86)}-{chr(90)}"
                d.mkdir(exist_ok=True)
                shutil.move(current_dir/filename, directory/d)

def osize(directory: Path) -> None:
    size = 0
    for dirpath, _, filenames in os.walk(directory):
        current_dir = Path(dirpath)
        for filename in filenames:
            size += Path(current_dir/filename).stat().st_size
    parts = size/3
    for dirpath, _, filenames in os.walk(directory):
        current_dir = Path(dirpath)
        for filename in filenames:
            if 0 <= (current_dir/filename).stat().st_size <= parts:
                Path(directory/"Small").mkdir(exist_ok=True)
                shutil.move(current_dir/filename, directory/"Small")
            elif parts+1 <= (current_dir/filename).stat().st_size <= 2*parts:
                Path(directory/"Medium").mkdir(exist_ok=True)
                shutil.move(current_dir/filename, directory/"Medium")
            elif 2*parts+1 <= (current_dir/filename).stat().st_size <= 3*parts:
                Path(directory/"Large").mkdir(exist_ok=True)
                shutil.move(current_dir/filename, directory/"Large")

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
        elif args.organize == "date":
            odate(Path(args.directory))
        elif args.organize == "name":
            oname(Path(args.directory))
        elif args.organize == "size":
            osize(Path(args.directory))

if __name__ == "__main__":
    main()
