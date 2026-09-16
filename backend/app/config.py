from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./database/app.db"
    jwt_secret: str = "development-secret-change-me"
    otp_expiry_seconds: int = 600
    email_host: str | None = None
    email_port: int = 587
    email_username: str | None = None
    email_password: str | None = None
    ai_api_key: str | None = None
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()