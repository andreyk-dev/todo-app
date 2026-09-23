from unittest.mock import Mock

import pytest

from app.models.task import TaskORM
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskNotFoundError, TaskService


def test_list_tasks_returns_pydantic_models(
    service: TaskService,
    repository_mock: Mock,
) -> None:
    # имитируем ответ базы данных через мок
    repository_mock.get_all.return_value = [
        TaskORM(id="task-1", title="Изучить задачу №1", completed=False),
        TaskORM(id="task-2", title="Изучить задачу №2", completed=False),
    ]

    result = service.list_tasks()

    # сверяем полученный результат с ожидаемыми Pydantic-схемами
    assert result == [
        TaskSchema(id="task-1", title="Изучить задачу №1", completed=False),
        TaskSchema(id="task-2", title="Изучить задачу №2", completed=False),
    ]


def test_create_task_commits_created_task(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    created_task = TaskORM(id="task-1", title="Новая задача", completed=False)
    repository_mock.create.return_value = created_task

    result = service.create_task(TaskCreateSchema(title="Новая задача"))

    # проверяем репозиторий вызван с нужными аргументами и был сделан commit
    repository_mock.create.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": "Новая задача",
        "completed": False,
    }


@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_completed"),
    [
        pytest.param(
            TaskUpdateSchema(title="Обновить заголовок"),
            "Обновить заголовок",
            False,
        ),
        pytest.param(
            TaskUpdateSchema(completed=True),
            "Старая задача",
            True,
        ),
        pytest.param(
            TaskUpdateSchema(title="Готово", completed=True),
            "Готово",
            True,
        ),
    ],
)
def test_update_task_updates_only_passed_fields(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
    payload: TaskUpdateSchema,
    expected_title: str,
    expected_completed: bool,
) -> None:
    task = TaskORM(id="task-1", title="Старая задача", completed=False)
    repository_mock.get_by_id.return_value = task

    result = service.update_task("task-1", payload)

    repository_mock.get_by_id.assert_called_once_with(task_id="task-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": expected_title,
        "completed": expected_completed,
    }


def test_update_task_raises_when_task_not_found(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError):
        service.update_task("missing-task", TaskUpdateSchema(title="Неважно"))

    # убеждаемся что при ошибке транзакция в базу не фиксировалась
    db_mock.commit.assert_not_called()


def test_delete_task_success(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    # check success delete task
    task = TaskORM(id="task-1", title="Задача на удаление", completed=False)
    repository_mock.get_by_id.return_value = task

    service.delete_task("task-1")

    # репозиторий искал задачу с правильным ID
    repository_mock.get_by_id.assert_called_once_with(task_id="task-1")
    # проверяем что задача действительно передана в метод delete
    repository_mock.delete.assert_called_once_with(task)
    # проверяем что транзакция была зафиксирована
    db_mock.commit.assert_called_once_with()


def test_delete_task_raises_when_task_not_found(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    """Проверка: если задачи нет, метод выбрасывает ошибку и ничего не удаляет."""
    repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError):
        service.delete_task("missing-task")

    # гарантируем что при ошибке метод delete не вызывался и в БД ничего
    # не фиксировалось
    repository_mock.delete.assert_not_called()
    db_mock.commit.assert_not_called()
