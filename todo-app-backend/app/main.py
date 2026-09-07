
from uuid import uuid4

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.models.task import TaskORM
from app.models.category import CategoryORM

from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
app.include_router(router=category_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)


# # 1 Схемы данных
# class CategorySchema(BaseModel):
#     id: str
#     name: str


# class CategoryCreateSchema(BaseModel):
#     name: str


# class CategoryUpdateSchema(BaseModel):
#     name: str | None = None


# categories: list[CategorySchema] = []



# @app.get("/categories", response_model=list[CategorySchema])
# def get_categories() -> list[CategorySchema]:
#     return categories


# @app.post(
#     "/categories",
#     response_model=CategorySchema,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_category(payload: CategoryCreateSchema) -> CategorySchema:
#     new_cat = CategorySchema(id=str(uuid4()), name=payload.name)
#     categories.append(new_cat)
#     return new_cat


# @app.patch("/categories/{category_id}", response_model=CategorySchema)
# def update_category(category_id: str, payload: CategoryUpdateSchema) -> CategorySchema:
#     for category in categories:
#         if category.id == category_id:
#             if payload.name is not None:
#                 category.name = payload.name
#             return category

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Category with id '{category_id}' not found",
#     )


# @app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_category(category_id: str) -> None:
#     for category in categories:
#         if category.id == category_id:
#             categories.remove(category)
#             return  

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Category with id '{category_id}' not found",
#     )