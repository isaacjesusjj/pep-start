from web_app.security import gerar_hash_senha, verificar_senha


def test_hash_de_senha_nao_armazena_senha_original():
    senha = "UmaSenhaSegura123"
    senha_hash = gerar_hash_senha(senha, iteracoes=1_000)

    assert senha not in senha_hash
    assert verificar_senha(senha, senha_hash) is True
    assert verificar_senha("senha-errada", senha_hash) is False


def test_respostas_clinicas_recebem_cabecalhos_de_seguranca(web_context):
    resposta = web_context["client"].get("/pacientes")

    assert resposta.headers["x-content-type-options"] == "nosniff"
    assert resposta.headers["x-frame-options"] == "DENY"
    assert resposta.headers["cache-control"] == "no-store"


def test_setup_inicial_nao_reabre_depois_do_primeiro_admin(web_context):
    resposta = web_context["client"].get("/setup", follow_redirects=False)
    assert resposta.status_code == 303
    assert resposta.headers["location"] == "/login"
