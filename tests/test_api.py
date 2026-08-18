from tests.web_helpers import criar_usuario, login, logout
from web_app.models import Paciente
from web_app.security import PERFIL_PROFISSIONAL, PERFIL_RECEPCAO


def test_api_recepcao_lista_e_cria_paciente_mas_nao_abre_prontuario(web_context):
    app = web_context["app"]
    client = web_context["client"]
    criar_usuario(app, nome="Recepção API", email="api-recepcao@teste.local", perfil=PERFIL_RECEPCAO)
    logout(client); login(client, "api-recepcao@teste.local", "SenhaTeste123")

    token = client.get("/api/v1/csrf").json()["csrf_token"]
    criado = client.post(
        "/api/v1/pacientes",
        headers={"X-CSRF-Token": token},
        json={"nome": "Paciente pela API", "data_nascimento": "2000-05-10", "telefone": "11911112222"},
    )
    assert criado.status_code == 201
    paciente_id = criado.json()["id"]

    lista = client.get("/api/v1/pacientes?per_page=5")
    assert lista.status_code == 200
    assert lista.json()["total"] == 1
    assert lista.json()["items"][0]["nome"] == "Paciente pela API"

    bloqueado = client.get(f"/api/v1/pacientes/{paciente_id}/prontuario")
    assert bloqueado.status_code == 403


def test_api_profissional_consulta_prontuario(web_context):
    app = web_context["app"]
    client = web_context["client"]
    with app.state.SessionLocal() as db:
        paciente = Paciente(nome="Paciente API Clínico", data_nascimento="1999-01-01", telefone=None)
        db.add(paciente); db.commit(); db.refresh(paciente); paciente_id = paciente.id
    criar_usuario(app, nome="Profissional API", email="api-prof@teste.local", perfil=PERFIL_PROFISSIONAL)
    logout(client); login(client, "api-prof@teste.local", "SenhaTeste123")

    resposta = client.get(f"/api/v1/pacientes/{paciente_id}/prontuario")
    assert resposta.status_code == 200
    assert resposta.json()["paciente"]["id"] == paciente_id
    assert resposta.json()["exames"] == []
