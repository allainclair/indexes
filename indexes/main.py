from asyncio import create_task
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import logfire
from litestar import Litestar, get
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.contrib.opentelemetry import OpenTelemetryConfig
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from indexes.apis.ibge import (
	get_last_ipcas,
	task_to_get_last_two_ipca_variations_hourly,
)
from indexes.httpx_connections import close_ibge_connection
from indexes.models.ipca import map_ibge_to_view
from indexes.settings import get_settings

logfire.configure()
logfire.instrument_httpx()


@asynccontextmanager
async def _lifespan(_: Litestar) -> AsyncGenerator[None, None]:
	task = create_task(task_to_get_last_two_ipca_variations_hourly())
	yield
	task.cancel()
	await close_ibge_connection()


@get(path="/")
async def index() -> Template:
	ipca_views = map_ibge_to_view(get_last_ipcas())
	return HTMXTemplate(
		template_name="index.html.jinja2", context={"ipcas": ipca_views}
	)


def build_app() -> Litestar:
	open_telemetry_config = OpenTelemetryConfig()
	return Litestar(
		debug=get_settings().debug,
		lifespan=[_lifespan],
		middleware=[open_telemetry_config.middleware],
		request_class=HTMXRequest,
		route_handlers=[
			create_static_files_router(
				"/static", directories=["indexes/assets"]
			),
			index,
		],
		template_config=TemplateConfig(
			directory=Path("indexes/templates"), engine=JinjaTemplateEngine
		),
	)


app = build_app()
