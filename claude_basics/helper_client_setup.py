
import os
from pathlib import Path
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

print("Python:", sys.executable)
print("API key loaded:", bool(os.getenv("ANTHROPIC_API_KEY")))

client = Anthropic()
model = "claude-haiku-4-5"