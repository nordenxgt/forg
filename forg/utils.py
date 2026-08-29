import subprocess
import platform
from pathlib import Path

def st_ltime(filepath: Path) -> float:
    result = subprocess.run(["stat", "-c", "%W", str(filepath)], capture_output=True, text=True, check=True).stdout.strip()
    if result in ["0", "-"]: raise ValueError("Birth time/Creation date not supported by this filesystem.")
    return float(result)

def file_ext(filename: str, extensions: dict) -> str:
    return extensions.get(Path(filename.lower()).suffix)

def file_ctime(filepath: Path) -> float:
    if platform.system() == "Windows":  return filepath.stat().st_ctime 
    if platform.system() == "Darwin":   return filepath.stat().st_birthtime
    if platform.system() == "Linux":    return st_ltime(filepath)
    return filepath.stat().st_mtime

def file_ord(filename: str) -> str:
    fo = ord(filename[0].upper())
    if 65 <= fo <= 75:  return f"{chr(65)}-{chr(75)}" # A-K
    if 76 <= fo <= 85:  return f"{chr(76)}-{chr(85)}" # M-U
    if 86 <= fo <= 90:  return f"{chr(86)}-{chr(90)}" # V-Z
    return "Others"

def file_size(filename: Path, pt_size: float) -> str:
    f_size = filename.stat().st_size 
    if f_size <= pt_size:       return "Small"
    elif f_size <= 2*pt_size:   return "Medium"
    else:                       return "Large"
