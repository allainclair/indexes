from indexes.settings import get_settings
from indexes.httpx_connections import get_bcb_connection
from indexes.models.ipca import IpcaBCB
from rich import print

settings = get_settings()

CODE_IGPM = 189
CODE_INCC = 192
CODE_IPCA = 433
CODE_IPCA_15 = 7478


async def get_last_two_ipca() -> tuple[IpcaBCB, IpcaBCB]:
	last_two_ipcas = await _get_last_two_ipca_from_bcb(CODE_IPCA)
	last_ipca = last_two_ipcas[-1]
	before_last_ipca = last_two_ipcas[-2]
	return IpcaBCB.model_validate(last_ipca), IpcaBCB.model_validate(before_last_ipca)


async def _get_last_two_ipca_from_bcb(code):
	client = get_bcb_connection()
	response = await client.get(
		f"bcdata.sgs.{code}/dados/ultimos/2", params={"formato": "json"},
	)
	response.raise_for_status()
	return response.json()
