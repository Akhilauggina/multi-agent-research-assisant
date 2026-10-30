"""
Streamlit Web User Interface entrypoint.
Placed at the backend root to prevent Python module collision with package 'app'.
"""

from pathlib import Path
import sys

# Ensure backend root is on sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import and execute the UI
from app.app import *

