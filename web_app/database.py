import os
from pathlib import Path

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


PASTA_PROJETO = Path(__file__).resolve().parent.parent


class Base(DeclarativeBase):
    """Base declarativa usada pelos modelos SQLAlchemy da aplicação web."""


def obter_database_url() -> str:
    """Retorna a URL do banco.

    SQLite continua sendo o padrão para estudo. Ao definir DATABASE_URL com
    PostgreSQL, a mesma camada ORM passa a usar o banco mais avançado.
    """

    configurada = os.getenv("PEP_START_DATABASE_URL") or os.getenv("DATABASE_URL")
    if configurada:
        # Plataformas antigas às vezes fornecem postgres://. SQLAlchemy 2 usa
        # o nome postgresql e aqui explicitamos o driver psycopg 3.
        if configurada.startswith("postgres://"):
            configurada = "postgresql+psycopg://" + configurada[len("postgres://"):]
        elif configurada.startswith("postgresql://"):
            configurada = "postgresql+psycopg://" + configurada[len("postgresql://"):]
        return configurada

    caminho = PASTA_PROJETO / "pep_start.db"
    return f"sqlite:///{caminho}"


def criar_engine(database_url: str | None = None):
    url = database_url or obter_database_url()
    argumentos = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=argumentos, future=True)


def criar_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db(request: Request):
    """Dependência FastAPI que abre e fecha uma sessão por requisição."""

    SessionLocal = request.app.state.SessionLocal
    with SessionLocal() as sessao:
        yield sessao
