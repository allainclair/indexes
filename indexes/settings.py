from functools import lru_cache

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
	)
	debug: bool = False

	# https://servicodados.ibge.gov.br/api/docs/agregados?versao=3
	# Use Query Builder for a faster understanding.
	ibge_url_ipca_base: HttpUrl = HttpUrl(
		"https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/",
	)

	# Used only at the moment for "make" and "docker".
	host: str = "127.0.0.1"
	port: int | None = None

	http_timeout: int = 5


@lru_cache
def get_settings() -> Settings:
	return Settings()
