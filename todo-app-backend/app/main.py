from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router


<<<<<<< HEAD
=======
# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     # Base.metadata.create_all(bind=engine)
#     yield


>>>>>>> 2dcb89290b22b47b6d61acee155fb862892c948b
app = FastAPI()
app.include_router(router=task_router)
app.include_router(router=category_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)


