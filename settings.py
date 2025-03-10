from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl


class Settings(BaseSettings):
    TOKEN: str
    LOLZAPITOKEN: str
    CHAT_IDS: str

    @property
    def lolz_url(self) -> str:
        """URL для LOLZ API"""
        return f"https://api.lzt.market/"

    @property
    def lolz_api(self) -> str:
        """URL для LOLZ API"""
        return f"{self.LOLZAPITOKEN}"

    @property
    def headers_(self) -> list:
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.LOLZAPITOKEN}"
        }
        return headers
    
    @property
    def chat_ids(self) -> list:
        return [int(id) for id in self.CHAT_IDS.split(",")]

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True
    )


settings = Settings()