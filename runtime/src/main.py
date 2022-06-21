import time

from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from .api.api_v1.api import api_router
from .core import config
from .db.session import Session
from .monitoring import init_monitoring

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/docs',
    redoc_url='/redoc',
    root_path=config.API_PREFIX,
)

# CORS
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.include_router(api_router, prefix=config.API_V1_STR)

logger, metrics, tracer = init_monitoring()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.middleware("http")
async def measure_requests_time_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url.path} Duration: {process_time}")
    return response

handler = Mangum(app)
