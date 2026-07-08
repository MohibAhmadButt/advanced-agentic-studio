import os

# Secure Token/Key retrieval from Cloud Settings
HF_TOKEN = os.environ.get("HF_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# File path registers
DB_FILE = "studio_vault.db"
OUTPUT_DIR = "outputs"

# Quick structural verification
if HF_TOKEN == "YOUR_HF_TOKEN_HERE" or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    print("⚠️ WARNING: Default API placeholder values detected. Replace with real keys or set environment variables before running.")