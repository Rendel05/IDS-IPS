import sys
from pathlib import Path


def resource_path(relative_path: str | Path) -> str:

    relative = Path(relative_path)
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    path = base_path / relative

    if hasattr(sys, "_MEIPASS") and not path.exists() and relative.parts[:1] == ("src",):
        return str(base_path / Path(*relative.parts[1:]))

    return str(path)
