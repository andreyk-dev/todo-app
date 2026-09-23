from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.repositories.task import TaskRepository
from app.services.category import CategoryService
from app.services.task import TaskService


# --- Мок базы данных ---
@pytest.fixture
def db_mock() -> Mock:
    """Мок сессии базы данных SQLAlchemy."""
    return Mock(spec=Session)


# --- Фикстуры для задач (Task) ---
@pytest.fixture
def repository_mock() -> Mock:
    """Мок репозитория задач."""
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    """Сервис задач с подменой репозитория."""
    task_service = TaskService(db=db_mock)
    # защита подменяем оба возможных имени атрибута
    task_service.task_repository = repository_mock
    return task_service


# --- Фикстуры для категорий (Category) ---
@pytest.fixture
def repository_category_mock() -> Mock:
    """Мок репозитория категорий."""
    return Mock(spec=CategoryRepository)


@pytest.fixture
def service_category(db_mock: Mock, repository_category_mock: Mock) -> CategoryService:
    """Сервис категорий с правильным моком CategoryRepository."""
    category_service = CategoryService(db=db_mock)
    # защита подменяем оба возможных имени атрибута
    category_service.category_repository = repository_category_mock
    return category_service
