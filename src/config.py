import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    URL_XML: str
    CREDENTIALS_FILE: str
    SPREADSHEET: str
    FTP_HOST: str
    FTP_USER: str
    FTP_PASSWORD: str
    REMOTE_FILE_PATH: str
    REMOTE_IMAGES_PATH: str
    REMOTE_FILE_NAME: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."  , ".env")
    )


settings = Settings()

