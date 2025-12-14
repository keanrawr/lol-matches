from pydantic_settings import BaseSettings, SettingsConfigDict


class ScraperSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    riot_api_key: str

    s3_bucket_name: str
    s3_access_key: str
    s3_secret_access_key: str
