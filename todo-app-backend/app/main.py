# терминал бекенда
# venv\Scripts\activate
# uvicorn main:app --reload

# уникальные айди
from uuid import uuid4

from fastapi import FastAPI

# cors это механизм, который позволяет API обрабатывать запросы с других доменов (источников), обходя ограничения браузера.
from fastapi.middleware.cors import CORSMiddleware

# контекст мендеджер для лайфспана
from contextlib import asynccontextmanager


from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)


# CATEGORIES


class CategoriesArea(BaseModel):
    id: str
    name: str


class CategoriesCreateArea(BaseModel):
    name: str


class CategoriesUpdateArea(BaseModel):
    name: str | None = None


categories: list[CategoriesArea] = []


@app.get("/categories", status_code=status.HTTP_200_OK)
def get_categories() -> list[CategoriesArea]:
    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_categories(new_category: CategoriesCreateArea) -> CategoriesArea:
    new_cat = CategoriesArea(id=str(uuid4()), name=new_category.name)

    categories.append(new_cat)
    return new_cat


@app.patch("/categories/{category_id}")
def update_category(category_id: str, new_category: CategoriesUpdateArea):
    for category in categories:
        if category.id == category_id:
            if new_category.name:
                category.name = new_category.name

            return category


@app.delete("/categories/{category_id}")
def delete_category(category_id):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
