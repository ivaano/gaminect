#from app.api.api_v1.router import api1_router
from app.api.router import api_router
from fastapi import FastAPI
from app.core import config

app = FastAPI(title=config.PROJECT_NAME,
              description=config.PROJECT_DESCRIPTION,
              version=config.PROJECT_VERSION,
              openapi_url=f"{config.API_VERSION_STR}/openapi.json",
              docs_url=config.DOCS_URL,
              redoc_url=config.REDOC_URL)

app.include_router(api_router)
#app.include_router(api1_router, prefix=config.API_VERSION_STR)
