"""
配置文件
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    IMAP_SERVER: str
    SMTP_PORT: int=465
    EMAIL_ACCOUNT: str
    PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

