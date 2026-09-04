# # терминал бекенда
# #venv\Scripts\activate
# # uvicorn main:app --reload

# # уникальные айди
# from uuid import uuid4

# from fastapi import FastAPI, status, Depends

# # cors это механизм, который позволяет API обрабатывать запросы с других доменов (источников), обходя ограничения браузера.
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# # для бд
# from sqlalchemy import create_engine, select
# from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, Session

# # контекст мендеджер для лайфспана
# from contextlib import asynccontextmanager

# #настройка бд, создание таблиц при запуске приложения (lifespan)
# # DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
# # engine = create_engine(DATABASE_URL)
# # Sessionlocal = sessionmaker[Session](bind=engine)


# # class Base(DeclarativeBase):
# #     id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


# # class TaskORM(Base):
# #     __tablename__ = "tasks"
# #     title: Mapped[str]
# #     completed: Mapped[bool] = mapped_column(default=False)


# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     Base.metadata.create_all(bind=engine)
#     yield


# app = FastAPI(lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_methods=["*"],
# )

# tasks: list[TaskSchema] = []

# # зависимость
# # def get_db():
# #     db = Sessionlocal()

# #     try:
# #         yield db
# #     finally:
# #         db.close()

# #конвертация данных
# def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
#     return TaskSchema(id = task_orm.id, title = task_orm.title, completed=task_orm.completed)


# class TaskSchema(BaseModel):
#     id: str
#     title: str
#     completed: bool


# class TaskCreateSchema(BaseModel):
#     title: str


# class TaskUpdateSchema(BaseModel):
#     title: str | None = None
#     completed: bool | None = None


# @app.get("/tasks")
# def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
#     tasks_from_db = db.scalars(select(TaskORM)).all() #возвращаем селектим данные из бд
#     return [task_orm_to_model(task) for task in tasks_from_db]


# @app.post("/tasks", status_code=status.HTTP_201_CREATED)
# def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
#     new_task = TaskORM(title=payload.title, completed=False)
#     db.add(new_task)
#     db.commit()
    
    
#     return task_orm_to_model(new_task)


# @app.patch("/tasks/{task_id}")
# def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
#     task_for_update = db.get(TaskORM, task_id)
#     if payload.title:
#         task_for_update.title = payload.title
#     if payload.completed:
#         task_for_update.completed = payload.completed

#     db.commit()
#     return task_for_update


# @app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_task(task_id, db: Session = Depends(get_db)) -> None:
#     task_for_delete = db.get(TaskORM, task_id)
#     db.delete(task_for_delete)
#     db.commit()


# # CATEGORIES


# class CategoriesArea(BaseModel):
#     id: str
#     name: str


# class CategoriesCreateArea(BaseModel):
#     name: str


# class CategoriesUpdateArea(BaseModel):
#     name: str | None = None


# categories: list[CategoriesArea] = []


# @app.get("/categories", status_code=status.HTTP_200_OK)
# def get_categories() -> list[CategoriesArea]:
#     return categories


# @app.post("/categories", status_code=status.HTTP_201_CREATED)
# def create_categories(new_category: CategoriesCreateArea) -> CategoriesArea:
#     new_cat = CategoriesArea(id=str(uuid4()), name=new_category.name)

#     categories.append(new_cat)
#     return new_cat


# @app.patch("/categories/{category_id}")
# def update_category(category_id: str, new_category: CategoriesUpdateArea):
#     for category in categories:
#         if category.id == category_id:
#             if new_category.name:
#                 category.name = new_category.name

#             return category


# @app.delete("/categories/{category_id}")
# def delete_category(category_id):
#     for category in categories:
#         if category.id == category_id:
#             categories.remove(category)
