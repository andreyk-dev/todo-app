from dataclasses import dataclass
import os
@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str 
    cors_allowed_origins: list[str] 


def get_settings() -> Settings:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "Переменная окружения DATABASE_URL не найдена! "
            "Проверь наличие файла .env и настройки docker-compose.yml"
        )
    return Settings(
        DATABASE_URL=database_url,
        cors_allowed_origins = ["http://localhost:3000"],
    )