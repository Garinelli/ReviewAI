import sys
from pathlib import Path

sys.path.extend(
    [
        str(p)
        for p in Path(".").resolve().rglob("bot/**")
        if p.is_dir() and not p.name.startswith((".", "__"))
    ]
    + [str(p) for p in Path(__file__).resolve().parents[:4]]
)