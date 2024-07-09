from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from babel.dates import format_date
from babel.numbers import format_decimal, format_percent
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, BeforeValidator, Field

from indexes.settings import get_settings

env = Environment(loader=FileSystemLoader("indexes/templates"))

settings = get_settings()


class IpcaBCB(BaseModel):
	date_: Annotated[
		date,
		BeforeValidator(
			lambda v: datetime.strptime(v, settings.bcb_date_format).date(),
		),
	] = Field(validation_alias="data", serialization_alias="date")
	rate: Decimal = Field(validation_alias="valor")


class IpcaIBGELastTwo(BaseModel):
	id: int
	name: str
	current_date: date
	previous_date: date
	current_rate: Decimal
	previous_rate: Decimal


class IpcaCurrentView(BaseModel):
	name: str
	current_date: str
	current_rate: str
	previous_date: str
	previous_rate: str
	rate_percentage: str


def map_ibge_to_view(ipcas: list[IpcaIBGELastTwo]) -> list[IpcaCurrentView]:
	views = []
	for ipca in ipcas:
		current_date = format_date(
			ipca.current_date,
			"MMMM yyyy",
			locale="pt_BR",
		)
		current_rate = f"{format_decimal(ipca.current_rate, locale="pt_BR")}%"
		previous_date = format_date(
			ipca.previous_date,
			"MMMM yyyy",
			locale="pt_BR",
		)
		previous_rate = f"{format_decimal(ipca.previous_rate, locale="pt_BR")}%"

		percent = ipca.current_rate / ipca.previous_rate - 1

		if percent < 0:
			template = env.get_template(
				"ipca-rate-percentage-negative.html.jinja2",
			)
		elif percent > 0:
			template = env.get_template(
				"ipca-rate-percentage-positive.html.jinja2",
			)
		else:
			template = env.get_template("ipca-rate-percentage-zero.html.jinja2")

		view = IpcaCurrentView(
			name=ipca.name,
			current_date=current_date,
			current_rate=current_rate,
			previous_date=previous_date,
			previous_rate=previous_rate,
			rate_percentage=template.render(
				{"percentage": format_percent(abs(percent), locale="pt_BR")},
			),
		)
		views.append(view)

	return views
