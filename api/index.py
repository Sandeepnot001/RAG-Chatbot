import sys
import os
from pathlib import Path

# Add the root directory to sys.path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

# Import the FastAPI app
try:
    from main import app
    from mangum import Mangum
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    raise e

# Wrap the app for Vercel/Lambda environment
handler = Mangum(app)

# Export app as well for Vercel's direct FastAPI support
app = app
