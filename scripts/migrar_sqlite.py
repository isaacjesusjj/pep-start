"""Migra os dados do PEP Start de SQLite para outro banco SQLAlchemy.

Uso para PostgreSQL:
    python scripts/migrar_sqlite.py pep_start.db \
        "postgresql+psycopg://usuario:senha@localhost/pep_start"

O destino deve estar vazio. A função também pode ser testada com outro SQLite,
o que permite validar a lógica sem exigir um servidor PostgreSQL durante os testes.
"""

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Permite executar este arquivo diretamente a partir da pasta scripts/.
PASTA_PROJETO = Path(__file__).resolve().parent.parent
if str(PASTA_PROJETO) not in sys.path:
    sys.path.insert(0, str(PASTA_PROJETO))

from sqlalchemy import DateTime, create_engine, func, select

from web_app.database import Base
from web_app import models  # noqa: F401 - registra tabelas no metadata


def _converter_linha(table, row):
    dados = dict(row)
    for coluna in table.columns:
        if coluna.name not in dados or dados[coluna.name] is None:
            continue
        if isinstance(coluna.type, DateTime) and isinstance(dados[coluna.name], str):
            texto = dados[coluna.name].replace("Z", "+00:00")
            try:
                dados[coluna.name] = datetime.fromisoformat(texto)
            except ValueError:
                dados[coluna.name] = datetime.strptime(dados[coluna.name], "%Y-%m-%d %H:%M:%S")
    return dados


def migrar_sqlite(caminho_origem: str | Path, database_url_destino: str) -> dict[str, int]:
    origem = Path(caminho_origem)
    if not origem.exists():
        raise FileNotFoundError(f"Banco de origem não encontrado: {origem}")

    engine = create_engine(
        database_url_destino,
        connect_args={"check_same_thread": False} if database_url_destino.startswith("sqlite") else {},
        future=True,
    )
    Base.metadata.create_all(engine)

    resultado = {}
    with sqlite3.connect(origem) as source:
        source.row_factory = sqlite3.Row
        tabelas_origem = {
            row["name"] for row in source.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }

        with engine.begin() as destino:
            for table in Base.metadata.sorted_tables:
                if table.name not in tabelas_origem:
                    resultado[table.name] = 0
                    continue

                quantidade_destino = destino.scalar(select(func.count()).select_from(table)) or 0
                if quantidade_destino:
                    raise RuntimeError(
                        f"A tabela de destino '{table.name}' não está vazia. "
                        "A migração foi interrompida para evitar duplicidade."
                    )

                linhas = source.execute(f'SELECT * FROM "{table.name}"').fetchall()
                if linhas:
                    destino.execute(table.insert(), [_converter_linha(table, row) for row in linhas])
                resultado[table.name] = len(linhas)

            if engine.dialect.name == "postgresql":
                for table in Base.metadata.sorted_tables:
                    if "id" not in table.c:
                        continue
                    destino.exec_driver_sql(
                        f"SELECT setval(pg_get_serial_sequence('{table.name}', 'id'), "
                        f"COALESCE((SELECT MAX(id) FROM {table.name}), 1), "
                        f"(SELECT MAX(id) IS NOT NULL FROM {table.name}))"
                    )

    engine.dispose()
    return resultado


def main():
    parser = argparse.ArgumentParser(description="Migra o PEP Start SQLite para PostgreSQL ou outro banco SQLAlchemy.")
    parser.add_argument("origem", help="Caminho para o arquivo SQLite de origem.")
    parser.add_argument("destino", help="DATABASE_URL do banco de destino.")
    args = parser.parse_args()

    resultado = migrar_sqlite(args.origem, args.destino)
    print("Migração concluída:")
    for tabela, quantidade in resultado.items():
        print(f"- {tabela}: {quantidade} registro(s)")


if __name__ == "__main__":
    main()
