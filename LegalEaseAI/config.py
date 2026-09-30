import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME = os.getenv("APP_NAME", "LegalEase")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    FRONTEND_API_URL = os.getenv(
        "FRONTEND_API_URL",
        "http://127.0.0.1:8000"
    )

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    MAX_GENERATED_CHARS = int(
        os.getenv("MAX_GENERATED_CHARS", "50000")
    )


settings = Settings()
