"""
Backwards-compatibility shim for src.gdrive_exporter.
All document styling, table generation, metadata pill formatting,
and Google Drive upload logic is now modularized in doc_exporter.py.
"""
import sys
from pathlib import Path

_root_dir = str(Path(__file__).resolve().parent.parent)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from doc_exporter import *  # noqa: F401, F403
