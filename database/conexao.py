import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_SCHEMA = Path(__file__).resolve().parent / "schema.sql"

def obter_caminho_banco():
    caminho_configurado = os.getenv("PEP_START_DB_PATH")
    if caminho_configurado:
        return Path(caminho_configurado)
    return PASTA_PROJETO / "pep_start.db"

@contextmanager
def conectar():
    caminho_banco = obter_caminho_banco()
    caminho_banco.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()

def inicializar_banco():
    comandos_sql = CAMINHO_SCHEMA.read_text(encoding="utf-8")
    with conectar() as conexao:
        conexao.executescript(comandos_sql)
