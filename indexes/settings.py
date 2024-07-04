from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
	)

	bcb_base: HttpUrl = HttpUrl("https://api.bcb.gov.br/dados/serie/")
	bcb_date_format: str = "%d/%m/%Y"
	debug: bool = False

	# https://servicodados.ibge.gov.br/api/docs/agregados?versao=3
	# Use Query Builder for a faster understanding.
	ibge_url_ipca_base: HttpUrl = HttpUrl("https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/")

	# Used only at the moment for "make" and "docker".
	port: int | None = None


@lru_cache
def get_settings() -> Settings:
	return Settings()
