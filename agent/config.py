import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    project_id: str = os.getenv("PROJECT_ID")
    project_location: str = os.getenv("PROJECT_LOCATION")

    bot_name: str = os.getenv("BOT_NAME")
    system_prompt: str = os.getenv("SYSTEM_PROMPT")

    gemini_voice: str = os.getenv("GEMINI_VOICE")
    gemini_model: str = os.getenv("GEMINI_MODEL")

    sample_rate: int = 16000
    output_sample_rate: int = 24000

    host: str = os.getenv("HOST")


config = Config()