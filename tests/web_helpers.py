import re

from sqlalchemy import select

from web_app.models import Usuario
from web_app.security import gerar_hash_senha


def extrair_csrf(html: str) -> str:
    encontrado = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert encontrado, "Token CSRF não encontrado no HTML."
    return encontrado.group(1)


def logout(client):
    resposta = client.get("/dashboard")
    token = extrair_csrf(resposta.text)
    return client.post("/logout", data={"csrf_token": token}, follow_redirects=False)


def login(client, email: str, senha: str):
    resposta = client.get("/login")
    token = extrair_csrf(resposta.text)
    return client.post(
        "/login",
        data={"csrf_token": token, "email": email, "senha": senha},
        follow_redirects=False,
    )


def criar_usuario(app, *, nome: str, email: str, perfil: str, senha: str = "SenhaTeste123"):
    with app.state.SessionLocal() as db:
        usuario = Usuario(
            nome=nome,
            email=email,
            perfil=perfil,
            senha_hash=gerar_hash_senha(senha, iteracoes=1_000),
            ativo=True,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario.id


def obter_usuario(app, email: str):
    with app.state.SessionLocal() as db:
        return db.scalar(select(Usuario).where(Usuario.email == email))
