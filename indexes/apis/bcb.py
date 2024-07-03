from indexes.settings import get_settings
from indexes.httpx_connections import get_bcb_connection
from indexes.models.ipca import BCBIpca

settings = get_settings()

CODE_IGPM = 189
CODE_INCC = 192
CODE_IPCA = 433
CODE_IPCA_15 = 7478


async def get_last_ipca() -> BCBIpca:
	last_ipca = (await _get_from_bcb(CODE_IPCA))[-1]
	return BCBIpca.model_validate(last_ipca)


async def _get_from_bcb(code):
	client = get_bcb_connection()
	response = await client.get(
		f"bcdata.sgs.{code}/dados/ultimos/1", params={"formato": "json"},
	)
	response.raise_for_status()
	return response.json()
