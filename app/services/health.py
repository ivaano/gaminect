from dataclasses import dataclass, field
from collections import defaultdict

from starlette._utils import is_async_callable
from anyio import to_thread
import anyio
from typing import Callable, Dict, List, DefaultDict, Optional, cast, Union, Awaitable

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from app.models.health import Condition, Check, HealthBody


@dataclass(frozen=True)
class Status:
    code: int
    name: str


@dataclass
class HealthService:
    conditions: List[Condition] = field(default_factory=list)
    allow_version: bool = field(default=False)
    version: Optional[str] = field(default=None)

    allow_description: bool = field(default=False)
    description: Optional[str] = field(default=None)

    release_id: Callable[..., Optional[None]] = field(default=lambda: None)
    service_id: Optional[str] = field(default=None)

    pass_status: Status = field(default=Status(code=200, name="pass"))
    fail_status: Status = field(default=Status(code=503, name="fail"))
    warn_status: Status = field(default=Status(code=200, name="warn"))

    allow_output: bool = field(default=True)

    links: Optional[Dict[str, str]] = field(default=None)
    notes: Callable[..., Optional[List[str]]] = field(default=lambda: None)

    def __post_init__(self):
        HealthService.__call__ = self.prepare_call()

    def prepare_call(self):
        def endpoint(
            self: "HealthService",
            request: Request,
            release_id: Optional[str] = Depends(self.release_id),
            notes: Optional[List[str]] = Depends(self.notes),
            checks: Dict[str, List[Check]] = Depends(self.run_conditions),
        ) -> JSONResponse:
            app = cast(FastAPI, request.app)
            status = self._get_service_status(checks)

            if self.version:
                version = self.version
            elif self.allow_version:
                version = app.version
            else:
                version = None

            if self.description:
                description = self.description
            elif self.allow_description:
                description = app.description
            else:
                description = None

            body = HealthBody(
                status=status.name,
                version=version,
                description=description,
                releaseId=release_id,
                serviceId=self.service_id,
                notes=notes,
                links=self.links,
                output=None,  # TODO: add output
                checks=checks or None,
            )
            return JSONResponse(
                content=body.dict(exclude_none=True),
                status_code=status.code,
                media_type="application/health+json",
            )

        return endpoint

    async def run_conditions(self) -> Dict[str, List[Check]]:
        results: DefaultDict[str, List[Check]] = defaultdict(list)

        async def _run_condition(
            name: str, call: Callable[[], Union[Check, Awaitable[Check]]]
        ) -> None:
            if is_async_callable(call):
                result = await call()
            else:
                result = await to_thread.run_sync(call)
            result = cast(Check, result)
            if result.dict(exclude_none=True):
                results[name].append(result)

        async with anyio.create_task_group() as tg:
            for condition in self.conditions:
                for call in condition.calls:
                    tg.start_soon(_run_condition, condition.name, call)

        return results

    def _get_service_status(self, checks: Dict[str, List[Check]]) -> Status:
        total_checks = 0
        warns = 0
        for checklist in checks.values():
            for check in checklist:
                total_checks += 1
                if check.status == self.fail_status.name:
                    return self.fail_status
                if check.status == self.warn_status.name:
                    warns += 1
        if checks and warns == total_checks:
            return self.warn_status
        return self.pass_status