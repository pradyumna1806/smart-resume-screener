from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongodb_url : str
    database_name : str
    gemini_api_key : str
    gemini_model : str = "gemini-3.5-flash"

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore",
    )

settings = Settings()
