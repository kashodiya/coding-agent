
#!/usr/bin/env python3

"""
Entry point script to run the AI coding agent.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import and run the main function
from src.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
