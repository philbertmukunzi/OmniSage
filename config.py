import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ConfigError(Exception):
    """Custom exception for configuration errors"""
    pass

class Config:
    @staticmethod
    def get_env(key, default=None, required=True):
        """
        Get an environment variable, optionally with a default value.
        Strips comments from the value.
        """
        value = os.getenv(key, default)
        if required and value is None:
            raise ConfigError(f"Environment variable '{key}' is not set")
        return value.split('#')[0].strip() if isinstance(value, str) else value

    @staticmethod
    def parse_int_list(value):
        """Parse a comma-separated string into a set of integers"""
        if not value.strip():
            return set()
        try:
            return set(map(int, filter(None, value.split(','))))
        except ValueError:
            raise ConfigError(f"Invalid format for integer list: {value}")

    # Discord Bot Configuration
    DISCORD_BOT_TOKEN = get_env("DISCORD_BOT_TOKEN")
    DISCORD_CLIENT_ID = get_env("DISCORD_CLIENT_ID")
    DISCORD_STATUS = get_env("DISCORD_STATUS_MESSAGE")
    ALLOWED_CHANNEL_IDS = parse_int_list(get_env("ALLOWED_CHANNEL_IDS", ""))
    ALLOWED_ROLE_IDS = parse_int_list(get_env("ALLOWED_ROLE_IDS", ""))
    
    # Message Limits
    MAX_TEXT = int(get_env("MAX_TEXT"))
    MAX_IMAGES = int(get_env("MAX_IMAGES"))
    MAX_MESSAGES = int(get_env("MAX_MESSAGES"))
    
    # LLM (Language Learning Model) Configuration
    LLM = get_env("LLM")
    LLM_TYPE, LLM_MODEL = LLM.split("/")
    LOCAL_LLM_URL = get_env("LOCAL_LLM_URL")
    SYSTEM_PROMPT = get_env("LLM_SYSTEM_PROMPT")
    
    # API Keys
    OPENAI_API_KEY = get_env("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = get_env("ANTHROPIC_API_KEY")
    
    # LLM Settings
    LLM_SETTINGS = {
        k.strip(): (
            int(float(v.strip())) if k == "max_tokens"
            else float(v.strip()) if v.replace(".", "").isdigit()
            else v.strip()
        )
        for k, v in (item.split("=") for item in get_env("LLM_SETTINGS").split(",") if "=" in item)
    }
    
    # Bot Configuration
    BOT_PREFIX = get_env("BOT_PREFIX")
    COOLDOWN_RATE = int(get_env("COOLDOWN_RATE"))
    COOLDOWN_PER = int(get_env("COOLDOWN_PER"))
    
    # Text-to-Speech (TTS) Configuration
    TTS_ENABLED = get_env("TTS_ENABLED").lower() == "true"
    TTS_MODEL = get_env("TTS_MODEL")
    TTS_VOICE = get_env("TTS_VOICE")
    TTS_FILENAME = get_env("TTS_FILENAME")
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = int(get_env("MAX_REQUESTS_PER_MINUTE"))
    REQUEST_WINDOW = int(get_env("REQUEST_WINDOW"))
    
    # Grounding Configuration
    USE_GROUNDING = get_env("USE_GROUNDING").lower() == "true"
    GROUNDING_SOURCE = get_env("GROUNDING_SOURCE")
    GROUNDING_PATH = get_env("GROUNDING_PATH")
    
    # AWS Configuration (for S3 grounding)
    AWS_ACCESS_KEY_ID = get_env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = get_env("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = get_env("AWS_BUCKET_NAME")
    
    # Azure Configuration (for Azure Blob Storage grounding)
    AZURE_STORAGE_CONNECTION_STRING = get_env("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_CONTAINER_NAME = get_env("AZURE_CONTAINER_NAME")

    @classmethod
    def validate(cls):
        """
        Validate the configuration.
        Add any configuration checks here.
        """
        if cls.USE_GROUNDING and cls.GROUNDING_SOURCE not in ['local', 's3', 'azure']:
            raise ConfigError(f"Invalid GROUNDING_SOURCE: {cls.GROUNDING_SOURCE}")
        
        # Add more validation checks as needed

# Run validation when the config is imported
Config.validate()