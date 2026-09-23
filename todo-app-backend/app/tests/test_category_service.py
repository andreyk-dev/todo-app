from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryNotFoundError, CategoryService


def test_list_category_returns_pydantic_models(
    service_category: CategoryService,
    repository_category_mock: Mock,
) -> None:
    """Проверка получения списка всех категорий через get_categories."""
    repository_category_mock.get_all.return_value = [
        CategoryORM(id="category-1", name="Категория №1"),
        CategoryORM(id="category-2", name="Категория №2"),
    ]

    result = service_category.get_categories()

    assert result == [
        CategorySchema(id="category-1", name="Категория №1"),
        CategorySchema(id="category-2", name="Категория №2"),
    ]


def test_create_category_commits_created_category(
    service_category: CategoryService,
    db_mock: Mock,
    repository_category_mock: Mock,
) -> None:
    """Проверка создания новой категории и фиксации коммита."""
    created_category = CategoryORM(id="category-1", name="Новая категория")
    repository_category_mock.create.return_value = created_category

    result = service_category.create_category(
        CategoryCreateSchema(name="Новая категория")
    )

    repository_category_mock.create.assert_called_once_with(name="Новая категория")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": "Новая категория",
    }


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdateSchema(name="Обновить имя"),
            "Обновить имя",
        ),
    ],
)
def test_update_category_updates_only_passed_fields(
    service_category: CategoryService,
    db_mock: Mock,
    repository_category_mock: Mock,
    payload: CategoryUpdateSchema,
    expected_name: str,
) -> None:
    """Проверка обновления названия существующей категории."""
    category = CategoryORM(id="category-1", name="Старая категория")
    repository_category_mock.get_by_id.return_value = category

    result = service_category.update_category("category-1", payload)

    repository_category_mock.get_by_id.assert_called_once_with(category_id="category-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": expected_name,
    }


def test_update_category_raises_when_not_found(
    service_category: CategoryService,
    db_mock: Mock,
    repository_category_mock: Mock,
) -> None:
    """Проверка выброса исключения CategoryNotFoundError
    при обновлении несуществующей категории."""
    repository_category_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        service_category.update_category(
            "missing-category", CategoryUpdateSchema(name="Неважно")
        )

    db_mock.commit.assert_not_called()


def test_delete_category_success(
    service_category: CategoryService,
    db_mock: Mock,
    repository_category_mock: Mock,
) -> None:
    """Проверка успешного удаления категории."""
    category = CategoryORM(id="category-1", name="Категория на удаление")
    repository_category_mock.get_by_id.return_value = category

    service_category.delete_category("category-1")

    repository_category_mock.get_by_id.assert_called_once_with(category_id="category-1")
    repository_category_mock.delete.assert_called_once_with(category)
    db_mock.commit.assert_called_once_with()


def test_delete_category_raises_when_not_found(
    service_category: CategoryService,
    db_mock: Mock,
    repository_category_mock: Mock,
) -> None:
    """Проверка выброса ошибки при удалении несуществующей категории."""
    repository_category_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        service_category.delete_category("missing-category")

    repository_category_mock.delete.assert_not_called()
    db_mock.commit.assert_not_called()
