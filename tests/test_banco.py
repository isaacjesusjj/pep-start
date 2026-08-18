import sqlite3

import pytest

from database.conexao import conectar, obter_caminho_banco


def test_banco_cria_as_tres_tabelas(servicos):
    with conectar() as conexao:
        tabelas = {
            linha["name"]
            for linha in conexao.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

    assert {"pacientes", "alergias", "atendimentos"}.issubset(tabelas)


def test_chave_estrangeira_bloqueia_exclusao_direta(servicos):
    pacientes = servicos["pacientes"]
    prontuario = servicos["prontuario"]
    paciente = pacientes.cadastrar_paciente("Teste Banco", "2000-01-01", None)
    prontuario.registrar_alergia(paciente.id, "Alergia fictícia")

    with pytest.raises(sqlite3.IntegrityError):
        with conectar() as conexao:
            conexao.execute("DELETE FROM pacientes WHERE id = ?", (paciente.id,))


def test_cada_teste_usa_banco_temporario(servicos):
    assert "pep_start_teste.db" in str(obter_caminho_banco())
