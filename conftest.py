import sys
from pathlib import Path


# Get the root directory of the ComicCraft project.
# __file__ = tests/conftest.py
# .parent = tests/
# .parents[1] = ComicCraft/
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# Add the project root to Python's import path.
# This allows tests to import:
# from app.main import app
# from app.schemas import PromptRequest
# etc.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))