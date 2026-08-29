from pathlib import Path
from forg.strategies import ofile, odate, oname, osize

def run_organizer(directory: Path, strategy: str) -> None:
    strategies = {"file": ofile, "date": odate, "name": oname, "size": osize}
    if strategy not in strategies:
        raise ValueError(f"Unknown organization strategy: '{strategy}'.\nTry one of these '{', '.join(strategies.keys())}'")
    strategies[strategy](directory)
