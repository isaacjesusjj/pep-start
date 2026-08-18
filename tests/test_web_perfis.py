from sqlalchemy import func, select

from tests.web_helpers import criar_usuario, extrair_csrf, login, logout
from web_app.models import Auditoria, Exame, Paciente, Prescricao
from web_app.security import PERFIL_PROFISSIONAL, PERFIL_RECEPCAO


def test_recepcao_cadastra_paciente_mas_nao_acessa_conteudo_clinico(web_context):
    app = web_context["app"]
    client = web_context["client"]
    criar_usuario(app, nome="Recepção Teste", email="recepcao@teste.local", perfil=PERFIL_RECEPCAO)
    logout(client)
    assert login(client, "recepcao@teste.local", "SenhaTeste123").status_code == 303

    resposta = client.get("/pacientes/novo")
    assert resposta.status_code == 200
    token = extrair_csrf(resposta.text)
    resposta = client.post(
        "/pacientes/novo",
        data={
            "csrf_token": token,
            "nome": "Paciente Recepção",
            "data_nascimento": "2000-01-01",
            "telefone": "11999999999",
        },
        follow_redirects=False,
    )
    assert resposta.status_code == 303

    detalhe = client.get(resposta.headers["location"])
    assert "Informações clínicas restritas" in detalhe.text
    paciente_id = int(resposta.headers["location"].split("/")[-1])

    bloqueado = client.post(
        f"/pacientes/{paciente_id}/exames",
        data={"csrf_token": token, "nome": "Exame fictício"},
    )
    assert bloqueado.status_code == 403


def test_profissional_registra_exame_e_prescricao_mas_nao_cria_paciente(web_context):
    app = web_context["app"]
    client = web_context["client"]
    with app.state.SessionLocal() as db:
        paciente = Paciente(nome="Paciente Clínico", data_nascimento="1990-01-01", telefone=None)
        db.add(paciente); db.commit(); db.refresh(paciente); paciente_id = paciente.id

    criar_usuario(app, nome="Profissional Teste", email="profissional@teste.local", perfil=PERFIL_PROFISSIONAL)
    logout(client)
    assert login(client, "profissional@teste.local", "SenhaTeste123").status_code == 303

    assert client.get("/pacientes/novo").status_code == 403
    detalhe = client.get(f"/pacientes/{paciente_id}")
    assert detalhe.status_code == 200
    assert "Exames fictícios" in detalhe.text
    token = extrair_csrf(detalhe.text)

    exame = client.post(
        f"/pacientes/{paciente_id}/exames",
        data={
            "csrf_token": token,
            "nome": "Hemograma fictício",
            "data_exame": "2026-08-18",
            "status": "CONCLUIDO",
            "resultado": "Resultado acadêmico",
            "observacao": "Somente demonstração",
        },
        follow_redirects=False,
    )
    assert exame.status_code == 303

    prescricao = client.post(
        f"/pacientes/{paciente_id}/prescricoes",
        data={
            "csrf_token": token,
            "medicamento": "Medicamento fictício A",
            "dose": "10 mg",
            "frequencia": "1 vez ao dia",
            "data_prescricao": "2026-08-18",
            "observacao": "Sem validade clínica",
        },
        follow_redirects=False,
    )
    assert prescricao.status_code == 303

    with app.state.SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Exame)) == 1
        assert db.scalar(select(func.count()).select_from(Prescricao)) == 1


def test_acesso_ao_prontuario_gera_evento_de_auditoria(web_context):
    app = web_context["app"]
    client = web_context["client"]
    with app.state.SessionLocal() as db:
        paciente = Paciente(nome="Paciente Auditável", data_nascimento="2001-02-03", telefone=None)
        db.add(paciente); db.commit(); db.refresh(paciente); paciente_id = paciente.id

    resposta = client.get(f"/pacientes/{paciente_id}")
    assert resposta.status_code == 200

    with app.state.SessionLocal() as db:
        evento = db.scalar(
            select(Auditoria)
            .where(Auditoria.acao == "VISUALIZAR_PRONTUARIO", Auditoria.recurso_id == str(paciente_id))
            .order_by(Auditoria.id.desc())
        )
        assert evento is not None
        assert "clínica" in evento.detalhes


def test_recepcao_nao_acessa_usuarios_nem_auditoria(web_context):
    app = web_context["app"]
    client = web_context["client"]
    criar_usuario(app, nome="Recepção Restrita", email="restrita@teste.local", perfil=PERFIL_RECEPCAO)
    logout(client); login(client, "restrita@teste.local", "SenhaTeste123")

    assert client.get("/usuarios").status_code == 403
    assert client.get("/auditoria").status_code == 403
