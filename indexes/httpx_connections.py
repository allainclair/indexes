from httpx import AsyncClient
from enum import StrEnum, auto
from indexes.settings import get_settings

settings = get_settings()


class ConnectionName(StrEnum):
	BCB = auto()


bcb_connection: AsyncClient | None = None


def get_connection(name: ConnectionName) -> AsyncClient:
	match name:
		case ConnectionName.BCB:
			return get_bcb_connection()


def get_bcb_connection() -> AsyncClient:
	global bcb_connection
	if bcb_connection is None:
		bcb_connection = AsyncClient(base_url=str(settings.bcb_url_base))
		return bcb_connection

	return bcb_connection


async def close_bcb_connection() -> None:
	global bcb_connection
	if bcb_connection is not None:
		await bcb_connection.aclose()
		bcb_connection = None

	return bcb_connection
