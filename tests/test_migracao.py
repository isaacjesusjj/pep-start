import sqlite3

from sqlalchemy import create_engine, text

from database.conexao import inicializar_banco
from scripts.migrar_sqlite import migrar_sqlite


def test_migracao_sqlite_para_banco_sqlalchemy_preserva_dados(tmp_path, monkeypatch):
    origem = tmp_path / "origem.db"
    destino = tmp_path / "destino.db"
    monkeypatch.setenv("PEP_START_DB_PATH", str(origem))
    inicializar_banco()

    with sqlite3.connect(origem) as conexao:
        conexao.execute(
            "INSERT INTO pacientes (nome, data_nascimento, telefone) VALUES (?, ?, ?)",
            ("Paciente Migração", "2000-01-01", "11999999999"),
        )
        conexao.commit()

    resultado = migrar_sqlite(origem, f"sqlite:///{destino}")
    assert resultado["pacientes"] == 1

    engine = create_engine(f"sqlite:///{destino}")
    with engine.connect() as conexao:
        nome = conexao.execute(text("SELECT nome FROM pacientes WHERE id = 1")).scalar_one()
    assert nome == "Paciente Migração"


def test_script_de_migracao_pode_ser_executado_diretamente():
    import subprocess
    import sys

    resultado = subprocess.run(
        [sys.executable, "scripts/migrar_sqlite.py", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert resultado.returncode == 0
    assert "Migra o PEP Start" in resultado.stdout
