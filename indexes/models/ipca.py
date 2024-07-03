from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from indexes.settings import get_settings

settings = get_settings()


class BCBIpca(BaseModel):
	date_: date = Field(validation_alias="data", serialization_alias="date")
	rate: Decimal = Field(validation_alias="valor")

	@field_validator("date_", mode="plain")
	@classmethod
	def validate_date(cls, value: str) -> date:
		return datetime.strptime(value, settings.bcb_date_format).date()
