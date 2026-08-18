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


@pytest.fixture
def web_context(tmp_path):
    """Aplicação web isolada com um administrador autenticado."""
    import re
    from fastapi.testclient import TestClient
    from web_app import create_app

    banco = tmp_path / "pep_start_web_teste.db"
    app = create_app(
        database_url=f"sqlite:///{banco}",
        secret_key="segredo-exclusivo-dos-testes",
        testing=True,
    )

    with TestClient(app) as client:
        resposta = client.get("/setup")
        token = re.search(
            r'name="csrf_token" value="([^"]+)"', resposta.text
        ).group(1)
        resposta = client.post(
            "/setup",
            data={
                "csrf_token": token,
                "nome": "Administrador Teste",
                "email": "admin@teste.local",
                "senha": "SenhaTeste123",
            },
            follow_redirects=False,
        )
        assert resposta.status_code == 303
        yield {"app": app, "client": client, "database_path": banco}
