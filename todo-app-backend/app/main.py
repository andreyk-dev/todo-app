import logging

from app.core.logging import configure_logging
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router


app = FastAPI()


configure_logging()
logger = logging.getLogger('app.middleware')

request_counter: int = 0

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    expose_headers=['X-Request-Number'],
)


#count logs
@app.middleware('http')
async def count_requests(request: Request, call_next) -> Response:
    global request_counter

    request_counter += 1
    current_number = request_counter

    response: Response = await call_next(request)

    response.headers["X-Request-Number"] = str(current_number)

    return response

#logs
@app.middleware('http')
async def log_requests(request: Request, call_next) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)  # Работа самого эндпоинта
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response

app.include_router(router=task_router)
app.include_router(router=category_router)



