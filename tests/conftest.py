import pytest

from database.conexao import inicializar_banco
from repositories.alergia_repository import AlergiaRepository
from repositories.atendimento_repository import AtendimentoRepository
from repositories.paciente_repository import PacienteRepository
from services.paciente_service import PacienteService
from services.prontuario_service import ProntuarioService


@pytest.fixture
def servicos(tmp_path, monkeypatch):
    """Cria um banco temporário novo para cada teste."""

    banco_teste = tmp_path / "pep_start_teste.db"
    monkeypatch.setenv("PEP_START_DB_PATH", str(banco_teste))
    inicializar_banco()

    pacientes = PacienteRepository()
    alergias = AlergiaRepository()
    atendimentos = AtendimentoRepository()

    return {
        "pacientes": PacienteService(pacientes, alergias, atendimentos),
        "prontuario": ProntuarioService(pacientes, alergias, atendimentos),
        "paciente_repository": pacientes,
        "alergia_repository": alergias,
        "atendimento_repository": atendimentos,
    }
