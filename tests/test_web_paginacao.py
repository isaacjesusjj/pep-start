from web_app.models import Paciente


def test_lista_de_pacientes_tem_paginacao_de_dez_itens(web_context):
    app = web_context["app"]
    client = web_context["client"]
    with app.state.SessionLocal() as db:
        db.add_all([
            Paciente(nome=f"Paciente {indice:02d}", data_nascimento="2000-01-01", telefone=None)
            for indice in range(25)
        ])
        db.commit()

    primeira = client.get("/pacientes?page=1")
    segunda = client.get("/pacientes?page=2")
    terceira = client.get("/pacientes?page=3")

    assert "25 registro(s)" in primeira.text
    assert "Página 1 de 3" in primeira.text
    assert primeira.text.count("/pacientes/") >= 10
    assert "Página 2 de 3" in segunda.text
    assert "Página 3 de 3" in terceira.text
