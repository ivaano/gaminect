from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union, Awaitable
from pydantic import BaseModel, Field, validator


# https://inadarei.github.io/rfc-healthcheck/#name-the-checks-object-2
class Check(BaseModel):
    componentId: Optional[str] = Field(
        default=None,
        description="Unique identifier of an instance of a specific sub-component/dependency of a service.",
    )
    componentType: Optional[str] = Field(
        default=None, description="Type of the sub-component/dependency of a service."
    )
    observedValue: Any = Field(default=None, description="The observed value of the component.")
    observedUnit: Optional[str] = Field(default=None, description="The unit of the observed value.")
    status: Optional[str] = Field(default=None, description="Indicates the service status.")
    affectedEndpoints: Optional[List[str]] = Field(
        default=None, description="List of affected endpoints."
    )
    time: Optional[str] = Field(
        default=None, description="Datetime at which the 'observedValue' was recorded."
    )
    output: Optional[str] = Field(
        default=None,
        description=(
            'Raw error output, in case of "fail" or "warn" states. '
            'This field SHOULD be omitted for "pass" state.'
        ),
    )
    links: Optional[Dict[str, str]] = Field(default=None)  # TODO: missing description

    @validator("time")
    def validate_iso_8061(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
        except ValueError as exc:  # pragma: no cover
            raise exc
        return v


class HealthBody(BaseModel):
    status: str = Field(default=..., description="Indicates the service status.")
    version: Optional[str] = Field(default=None, description="The version of the service.")
    releaseId: Optional[str] = Field(default=None, description="The release ID of the service.")
    notes: Optional[List[str]] = Field(
        default=None, description="Notes relevant to the current status."
    )
    output: Optional[str] = Field(
        default=None,
        description=(
            'Raw error output, in case of "fail" or "warn" states. '
            'This field SHOULD be omitted for "pass" state.'
        ),
    )
    checks: Optional[Dict[str, List[Check]]] = Field(
        default=None,
        description=(
            "Provides detailed health statuses of additional downstream systems"
            " and endpoints which can affect the overall health of the main API."
        ),
    )
    links: Optional[Dict[str, str]] = Field(default=None, description="Links to related resources.")
    serviceId: Optional[str] = Field(default=None, description="The ID of the service.")
    description: Optional[str] = Field(default=None, description="The description of the service.")


class Condition(BaseModel):
    name: str = Field(default=..., description="The name of the condition. Must be unique.")
    calls: List[Callable[[], Union[Check, Awaitable[Check]]]] = Field(
        default=..., description="The function to call to check the condition."
    )
