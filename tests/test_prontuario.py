from datetime import date, timedelta

import pytest


def criar_paciente(servicos):
    return servicos["pacientes"].cadastrar_paciente(
        "Maria Oliveira",
        "1999-03-14",
        "11999999999",
    )


def test_registrar_alergia_e_impedir_duplicidade(servicos):
    paciente = criar_paciente(servicos)
    prontuario = servicos["prontuario"]

    criada = prontuario.registrar_alergia(paciente.id, "  Dipirona  ")
    assert criada.descricao == "Dipirona"

    with pytest.raises(ValueError, match="já está registrada"):
        prontuario.registrar_alergia(paciente.id, "dipirona")


def test_registrar_atendimento_e_consultar_prontuario(servicos):
    paciente = criar_paciente(servicos)
    prontuario = servicos["prontuario"]

    prontuario.registrar_alergia(paciente.id, "Penicilina")
    atendimento = prontuario.registrar_atendimento(
        paciente.id,
        "2026-08-18",
        "Consulta de acompanhamento",
        "Registro fictício para teste.",
    )

    resultado = prontuario.consultar_prontuario(paciente.id)

    assert atendimento.id == 1
    assert resultado["paciente"].id == paciente.id
    assert [a.descricao for a in resultado["alergias"]] == ["Penicilina"]
    assert len(resultado["atendimentos"]) == 1
    assert resultado["atendimentos"][0].motivo == "Consulta de acompanhamento"


def test_atendimentos_sao_listados_do_mais_recente(servicos):
    paciente = criar_paciente(servicos)
    prontuario = servicos["prontuario"]

    prontuario.registrar_atendimento(paciente.id, "2026-08-01", "Primeiro")
    prontuario.registrar_atendimento(paciente.id, "2026-08-18", "Segundo")

    historico = prontuario.consultar_prontuario(paciente.id)["atendimentos"]

    assert [item.data for item in historico] == ["2026-08-18", "2026-08-01"]


def test_impedir_atendimento_futuro(servicos):
    paciente = criar_paciente(servicos)
    data_futura = (date.today() + timedelta(days=1)).isoformat()

    with pytest.raises(ValueError, match="data futura"):
        servicos["prontuario"].registrar_atendimento(
            paciente.id,
            data_futura,
            "Teste",
        )


def test_impedir_atendimento_anterior_ao_nascimento(servicos):
    paciente = criar_paciente(servicos)

    with pytest.raises(ValueError, match="anterior ao nascimento"):
        servicos["prontuario"].registrar_atendimento(
            paciente.id,
            "1990-01-01",
            "Teste",
        )


def test_impedir_registro_para_paciente_inexistente(servicos):
    with pytest.raises(ValueError, match="Paciente não encontrado"):
        servicos["prontuario"].registrar_alergia(9999, "Teste")


def test_impedir_exclusao_quando_ha_registro_clinico(servicos):
    paciente = criar_paciente(servicos)
    prontuario = servicos["prontuario"]
    pacientes = servicos["pacientes"]

    prontuario.registrar_atendimento(
        paciente.id,
        "2026-08-18",
        "Consulta fictícia",
    )

    with pytest.raises(ValueError, match="registros clínicos associados"):
        pacientes.excluir_paciente(paciente.id)
