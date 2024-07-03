from pathlib import Path

from litestar import Litestar, Router, get
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from indexes.settings import get_settings
from indexes.apis.bcb import get_last_ipca


@get(path="/")
async def index() -> Template:
	current_ipca = await get_last_ipca()
	return HTMXTemplate(template_name="index.html.jinja2", context={
		"current_ipca": current_ipca,
	})


def build_app() -> Litestar:
	return Litestar(
		debug=get_settings().debug,
		request_class=HTMXRequest,
		route_handlers=[
			create_static_files_router("/static", directories=["indexes/assets"]),
			index,
		],
		template_config=TemplateConfig(
			directory=Path("indexes/templates"),
			engine=JinjaTemplateEngine,
		),
	)


app = build_app()
