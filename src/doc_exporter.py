"""
doc_exporter forwarding module for src package.
Re-exports all definitions from root doc_exporter.py.
"""
import sys
from pathlib import Path

_root_dir = str(Path(__file__).resolve().parent.parent)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from doc_exporter import *  # noqa: F401, F403
