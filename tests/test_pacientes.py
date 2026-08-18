import pytest


def test_cadastrar_e_buscar_paciente(servicos):
    pacientes = servicos["pacientes"]

    criado = pacientes.cadastrar_paciente(
        "  Maria   Oliveira  ",
        "1999-03-14",
        "(11) 99999-9999",
    )

    encontrado = pacientes.buscar_por_id(criado.id)

    assert criado.id == 1
    assert encontrado.nome == "Maria Oliveira"
    assert encontrado.data_nascimento == "1999-03-14"
    assert encontrado.telefone == "11999999999"


def test_listar_e_buscar_por_parte_do_nome(servicos):
    pacientes = servicos["pacientes"]
    pacientes.cadastrar_paciente("Ana Souza", "2000-01-10", None)
    pacientes.cadastrar_paciente("Mariana Lima", "2001-02-20", None)

    encontrados = pacientes.buscar_por_nome("ana")

    assert [paciente.nome for paciente in encontrados] == [
        "Ana Souza",
        "Mariana Lima",
    ]


def test_atualizar_paciente(servicos):
    pacientes = servicos["pacientes"]
    criado = pacientes.cadastrar_paciente("Carlos Lima", "1995-06-20", None)

    atualizado = pacientes.atualizar_paciente(
        criado.id,
        "Carlos de Lima",
        "1995-06-20",
        "11 3333-4444",
    )

    assert atualizado.nome == "Carlos de Lima"
    assert atualizado.telefone == "1133334444"


def test_excluir_paciente_sem_registros(servicos):
    pacientes = servicos["pacientes"]
    criado = pacientes.cadastrar_paciente("João Silva", "1990-05-15", None)

    assert pacientes.excluir_paciente(criado.id) is True
    assert pacientes.buscar_por_id(criado.id) is None


def test_rejeitar_nome_curto_data_futura_e_telefone_invalido(servicos):
    pacientes = servicos["pacientes"]

    with pytest.raises(ValueError, match="pelo menos 3"):
        pacientes.cadastrar_paciente("A", "2000-01-01", None)

    with pytest.raises(ValueError, match="futuro"):
        pacientes.cadastrar_paciente("Pessoa Teste", "2999-01-01", None)

    with pytest.raises(ValueError, match="10 ou 11"):
        pacientes.cadastrar_paciente("Pessoa Teste", "2000-01-01", "123")
