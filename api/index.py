import sys
import os
from pathlib import Path

# Add the root directory to sys.path so we can import 'backend' and 'main'
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

# Import the FastAPI app from main.py
try:
    from main import app
except ImportError as e:
    print(f"Error importing app: {e}")
    raise e

# Vercel needs the app object to be named 'app'
# Since main.py already has 'app = FastAPI(...)', we just need it in this scope
