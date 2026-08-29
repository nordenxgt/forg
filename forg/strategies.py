import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Callable
from forg.utils import file_ext, file_ctime, file_ord, file_size

def ofile(directory: Path) -> None:
    extensions_file = Path("extensions.json")
    if not extensions_file.exists(): raise FileNotFoundError(f"{extensions_file} json file is missing.\nRun: `python scrape_extensions.py`")
    with open("extensions.json", "r", encoding="utf-8") as f: 
        extensions = json.load(f)
    def _ofile(directory: Path, current_dir: Path, filename: str) -> None:
        return file_ext(filename, extensions)
    strategy(directory, _ofile)

def odate(directory: Path) -> None:
    def _odate(directory: Path, current_dir: Path, filename: str) -> None:
        return str(datetime.fromtimestamp(file_ctime(current_dir / filename)).date())
    strategy(directory, _odate)

def oname(directory: Path) -> None:
    def _oname(directory: Path, current_dir: Path, filename: str) -> None:
        return file_ord(filename)
    strategy(directory, _oname)

def osize(directory: Path) -> None:
    size = sum(f.stat().st_size for f in directory.rglob("*") if f.is_file())
    pt_size = size / 3
    def _osize(directory: Path, current_dir: Path, filename: str) -> None:
        return file_size(current_dir / filename, pt_size)
    strategy(directory, _osize)

def move_file(directory: Path, current_dir: Path, filename: str, dn: str | None) -> None:
    if not dn: return
    target_dir = directory / dn
    target_dir.mkdir(exist_ok=True)
    src, dst = current_dir / filename, target_dir / filename
    if src.parent == target_dir: return
    if dst.exists():
        stem, suffix = src.stem, src.suffix
        counter = 1
        while dst.exists():
            dst = target_dir/f"{stem}_{counter}{suffix}"
            counter += 1
    shutil.move(src, dst)

def strategy(directory: Path, callback: Callable[[Path, Path, str]]):
    if not directory.exists(): raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    if not directory.is_dir(): raise NotADirectoryError(f"'{directory}' is not a valid directory.")
    for dirpath, _, filenames in os.walk(directory):
        current_dir = Path(dirpath)
        for filename in filenames:
            dn = callback(directory, current_dir, filename)
            move_file(directory, current_dir, filename, dn)
