import os
import sys
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai

# Load environment variables
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

def get_tavily_client() -> TavilyClient:
    if not TAVILY_API_KEY or TAVILY_API_KEY == "set the api":
        print("\n❌ Error: TAVILY_API_KEY is not set in backend/.env")
        sys.exit(1)
    return TavilyClient(api_key=TAVILY_API_KEY)

def get_gemini_client() -> genai.Client:
    if not GEMINI_API_KEY:
        print("\n❌ Error: GEMINI_API_KEY is not set in backend/.env")
        sys.exit(1)
    return genai.Client(api_key=GEMINI_API_KEY)
