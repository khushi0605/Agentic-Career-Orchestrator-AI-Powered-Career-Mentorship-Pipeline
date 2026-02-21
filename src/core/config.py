import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# API Key Retrieval
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Safety Check: Stop the app if keys are missing
if not all([GOOGLE_API_KEY, SERP_API_KEY, RAPIDAPI_KEY]):
    missing = [k for k, v in {
        "GOOGLE_API_KEY": GOOGLE_API_KEY,
        "SERP_API_KEY": SERP_API_KEY,
        "RAPIDAPI_KEY": RAPIDAPI_KEY
    }.items() if not v]
    raise ValueError(f"Missing environment variables: {', '.join(missing)}. Please check your .env file.")