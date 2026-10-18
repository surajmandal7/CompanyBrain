from __future__ import annotations

from .db import FalkorDB
from .seed_data import seed_graph


if __name__ == "__main__":
    result = seed_graph(FalkorDB())
    print({"status": "completed", **result})
