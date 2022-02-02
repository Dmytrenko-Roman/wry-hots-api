from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_name: str

    class Config:
        env_file = "../.env"


database_settings = DatabaseSettings()


class TokenSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = "../.env"


token_settings = TokenSettings()
