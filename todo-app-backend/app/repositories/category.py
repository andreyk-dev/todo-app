from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import CategoryORM

class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        # get all from db
        return list(self.db.scalars(select(CategoryORM)).all())

    def get_by_id(self, category_id: str) -> CategoryORM | None:
        # find category by primary key
        return self.db.get(CategoryORM, category_id)

    def create(self, name: str) -> CategoryORM:
        # create and fix changes
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete(self, category_orm: CategoryORM) -> None:
        # delete category from db
        self.db.delete(category_orm)
