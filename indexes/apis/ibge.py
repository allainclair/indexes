from collections.abc import Callable, Coroutine
from datetime import UTC, date, datetime, timedelta
from typing import Any

from indexes.httpx_connections import get_ibge_connection
from indexes.models.ipca import IpcaIBGELastTwo

ID_MONTHLY_VARIATION = "63"
ID_THREE_MONTHS_ACCUMULATION = "2263"
ID_SIX_MONTHS_ACCUMULATION = "2264"
ID_THIS_YEAR_ACCUMULATION = "69"
ID_YEARLY_ACCUMULATION = "2265"
IDS = [
	ID_MONTHLY_VARIATION,
	ID_THREE_MONTHS_ACCUMULATION,
	ID_SIX_MONTHS_ACCUMULATION,
	ID_THIS_YEAR_ACCUMULATION,
	ID_YEARLY_ACCUMULATION,
]

_last_datetime: datetime | None = None
_last_ipcas: list[IpcaIBGELastTwo] | None = None


async def get_last_two_ipca_variations() -> list[IpcaIBGELastTwo]:
	return await cache_ttl(_get_last_two_ipca_variations)


async def _get_last_two_ipca_variations() -> list[IpcaIBGELastTwo]:
	client = get_ibge_connection()
	last_two = -2
	response = await client.get(
		f"{last_two}/variaveis/2266|63|2263|2264|69|2265?localidades=N1[all]",
	)
	json = response.json()
	ipca_variations = []
	for ipca_variation in json:
		id_ = ipca_variation.get("id")
		if id_ in IDS:
			for variation in ipca_variation.get("resultados"):
				series = variation.get("series")[0].get("serie")
				dates = sorted(series.keys())
				last_date_str, previous_date_str = dates[-1], dates[-2]
				last_date = date(
					year=int(last_date_str[:4]),
					month=int(last_date_str[4:6]),
					day=1,
				)
				previous_date = date(
					year=int(previous_date_str[:4]),
					month=int(previous_date_str[4:6]),
					day=1,
				)
				last_result = series.get(last_date_str)
				previous_result = series.get(previous_date_str)

				ipca_last_two = IpcaIBGELastTwo(
					id=id_,
					name=ipca_variation.get("variavel").strip("IPCA - "),
					current_date=last_date,
					previous_date=previous_date,
					current_rate=last_result,
					previous_rate=previous_result,
				)
				ipca_variations.append(ipca_last_two)

	# Switch 69 (variation this year) and 2265 (12 months accumulation).
	ipca_variations[-1], ipca_variations[-2] = (
		ipca_variations[-2],
		ipca_variations[-1],
	)
	return ipca_variations


async def cache_ttl(
	func: Callable[[], Coroutine[Any, Any, list[IpcaIBGELastTwo]]],
	ttl: int = 3600,
) -> list[IpcaIBGELastTwo]:
	global _last_datetime
	global _last_ipcas
	now = datetime.now(UTC)

	if not _last_datetime or now - _last_datetime > timedelta(seconds=ttl):
		_last_ipcas = await func()
		_last_datetime = now

	assert _last_ipcas
	return _last_ipcas
