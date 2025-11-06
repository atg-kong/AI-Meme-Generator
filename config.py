"""
Configuration module for AI Meme Generator
Loads environment variables and provides configuration constants
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    PORT = int(os.getenv('PORT', 5000))

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

    # Imgflip API Configuration
    IMGFLIP_USERNAME = os.getenv('IMGFLIP_USERNAME', '')
    IMGFLIP_PASSWORD = os.getenv('IMGFLIP_PASSWORD', '')
    IMGFLIP_GET_MEMES_URL = 'https://api.imgflip.com/get_memes'
    IMGFLIP_CAPTION_URL = 'https://api.imgflip.com/caption_image'

    # LLM Provider Configuration
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4-turbo')

    # HuggingFace Configuration (optional)
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')

    # Dataset Configuration
    MEMES_DATASET_PATH = os.path.join(os.path.dirname(__file__), 'memes.json')

    # Generated Memes Storage
    GENERATED_MEMES_DIR = os.path.join(os.path.dirname(__file__), 'generated_memes')

    # Meme Generation Settings
    MAX_CAPTION_TOKENS = 50
    TEMPERATURE = 0.8  # Higher = more creative

    @staticmethod
    def validate():
        """Validate that required configuration is present"""
        errors = []

        if Config.LLM_PROVIDER == 'openai' and not Config.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")

        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")

    @staticmethod
    def ensure_directories():
        """Ensure required directories exist"""
        os.makedirs(Config.GENERATED_MEMES_DIR, exist_ok=True)


# Create configuration instance
config = Config()
