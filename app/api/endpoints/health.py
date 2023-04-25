from datetime import datetime
from app.core.routing import APIRouter
from app.services.health import HealthService
from app.models.health import Condition, Check, HealthBody
import aiohttp
import psutil
import dns.resolver
router = APIRouter()


def health_mem() -> Check:
    check = Check(
        componentId="Process Memcheck",
        time=datetime.now().isoformat()
    )
    try:
        check.observedValue = psutil.Process().memory_info().rss / (1024 * 1024)
        check.observedUnit = 'Mb'
    except Exception as e:
        check.output = str(e)
        check.status = HealthService.warn_status.name
    return check


async def health_check_external_ip() -> Check:

    check = Check(
        componentId="External IP",
        time=datetime.now().isoformat()
    )

    try:
        headers = {
            "user-agent": f"curl/7.86.0"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://ipinfo.io', headers=headers) as response:
                response = await response.json()
                check.observedValue = response.get('ip')
                check.observedUnit = 'ip'
    except Exception as e:
        check.output = str(e)
        check.status = HealthService.fail_status.name

    return check


def health_dns() -> Check:
    check = Check(
        componentId="DNS Resolver",
        time=datetime.now().isoformat()
    )
    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ["8.8.8.8"]
        answer = resolver.resolve("google.com", "A")
        rrset = answer.response.answer[0]
        check.observedUnit = 'dns'
        check.observedValue = rrset.to_text()
    except Exception as e:
        check.output = str(e)
        check.status = HealthService.fail_status.name

    return check


conditions = Condition(name="External dependencies", calls=[health_mem, health_check_external_ip, health_dns])


router.add_api_route("/health", HealthService([conditions], allow_version=True, allow_description=True),
                     response_model=HealthBody, description="Service health checks")


