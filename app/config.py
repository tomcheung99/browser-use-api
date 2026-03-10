from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM Provider — set at least one
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    kimi_api_key: str = ""

    # Default LLM model to use
    default_llm_provider: str = "openai"  # "openai" | "anthropic" | "kimi"
    default_model: str = "gpt-4o"

    # Browser settings
    headless: bool = True
    browser_timeout: int = 30000  # ms

    # API settings
    api_secret_key: str = ""  # Optional bearer token for protecting endpoints

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
