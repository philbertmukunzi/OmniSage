import os
from dotenv import load_dotenv

load_dotenv()

class ConfigError(Exception):
    pass

class Config:
    @staticmethod
    def get_env(key, default=None, required=True):
        value = os.getenv(key, default)
        if required and value is None:
            raise ConfigError(f"Environment variable '{key}' is not set")
        return value

    @staticmethod
    def parse_int_list(value):
        try:
            return set(map(int, filter(None, value.split(","))))
        except ValueError:
            raise ConfigError(f"Invalid format for integer list: {value}")

    # Discord Bot Configuration
    DISCORD_BOT_TOKEN = get_env("DISCORD_BOT_TOKEN")
    DISCORD_CLIENT_ID = get_env("DISCORD_CLIENT_ID")
    DISCORD_STATUS = get_env("DISCORD_STATUS_MESSAGE")
    
    # Channel and Role Restrictions
    ALLOWED_CHANNEL_IDS = parse_int_list(get_env("ALLOWED_CHANNEL_IDS", ""))
    ALLOWED_ROLE_IDS = parse_int_list(get_env("ALLOWED_ROLE_IDS", ""))
    
    # Message Limits
    MAX_TEXT = int(get_env("MAX_TEXT"))
    MAX_IMAGES = int(get_env("MAX_IMAGES"))
    MAX_MESSAGES = int(get_env("MAX_MESSAGES"))
    
    # LLM Configuration
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
    
    # TTS Configuration
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
    AWS_ACCESS_KEY_ID = get_env("AWS_ACCESS_KEY_ID", required=False)
    AWS_SECRET_ACCESS_KEY = get_env("AWS_SECRET_ACCESS_KEY", required=False)
    AWS_BUCKET_NAME = get_env("AWS_BUCKET_NAME", required=False)
    
    # Azure Configuration (for Azure Blob Storage grounding)
    AZURE_STORAGE_CONNECTION_STRING = get_env("AZURE_STORAGE_CONNECTION_STRING", required=False)
    AZURE_CONTAINER_NAME = get_env("AZURE_CONTAINER_NAME", required=False)