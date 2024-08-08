from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    bot_token: SecretStr
    yoomoney_secret_key: SecretStr
    yoomoney_wallet_id: SecretStr
    sqlite_database_path: Path
    admin_id: int

    class Config:
        env_file = '.env'

config = Config()
