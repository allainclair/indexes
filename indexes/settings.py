from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
	)

	debug: bool = False

	# Used only at the moment for "make" and "docker".
	port: int | None = None
	bcb_url_base: HttpUrl = HttpUrl("https://api.bcb.gov.br/dados/serie/")
	bcb_date_format: str = "%d/%m/%Y"


@lru_cache
def get_settings() -> Settings:
	return Settings()
