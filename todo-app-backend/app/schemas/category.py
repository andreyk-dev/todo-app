from pydantic import BaseModel, ConfigDict

#Category

class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None





