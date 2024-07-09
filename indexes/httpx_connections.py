from httpx import AsyncClient

from indexes.settings import get_settings

settings = get_settings()
ibge_connection: AsyncClient | None = None


def get_ibge_connection() -> AsyncClient:
	global ibge_connection
	if ibge_connection is None:
		ibge_connection = AsyncClient(base_url=str(settings.ibge_url_ipca_base))
		return ibge_connection

	return ibge_connection


async def close_ibge_connection() -> None:
	global ibge_connection
	if ibge_connection is not None:
		await ibge_connection.aclose()
		ibge_connection = None

	return ibge_connection
