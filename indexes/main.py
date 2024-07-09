from pathlib import Path

from litestar import Litestar, get
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from indexes.apis.ibge import get_last_two_ipca_variations
from indexes.models.ipca import map_ibge_to_view
from indexes.settings import get_settings

# TODO: Add context to open/close httpx connections


@get(path="/")
async def index() -> Template:
	ipcas = await get_last_two_ipca_variations()
	ipca_views = map_ibge_to_view(ipcas)
	return HTMXTemplate(
		template_name="index.html.jinja2",
		context={"ipcas": ipca_views},
	)


def build_app() -> Litestar:
	return Litestar(
		debug=get_settings().debug,
		request_class=HTMXRequest,
		route_handlers=[
			create_static_files_router(
				"/static",
				directories=["indexes/assets"],
			),
			index,
		],
		template_config=TemplateConfig(
			directory=Path("indexes/templates"),
			engine=JinjaTemplateEngine,
		),
	)


app = build_app()
