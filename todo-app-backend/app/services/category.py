
from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def get_categories(self) -> list[CategorySchema]:
        # get all categories
        categories_orm = self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in categories_orm]

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        # create
        category_orm = self.category_repository.create(name=category_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(self, category_id, category_update: CategoryUpdateSchema) -> CategorySchema:
        # update by id
        category_for_update = self.category_repository.get_by_id(category_id=category_id)
        if not category_for_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"Categoty with id - {category_id} not found"
            )   

        if category_update.name is not None:
            category_for_update.name = category_update.name

        self.db.commit()
        return CategorySchema.model_validate(category_for_update)
    
    def delete_category(self, category_id: str) -> None:
        # delete category
        category_for_delete = self.category_repository.get_by_id(category_id=category_id)

        if not category_for_delete:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"Categoty with id - {category_id} not found"
                    )   
        

        self.category_repository.delete(category_for_delete)
        self.db.commit()


