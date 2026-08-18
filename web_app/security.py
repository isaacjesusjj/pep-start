import hashlib
import hmac
import secrets
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from web_app.database import get_db
from web_app.models import Usuario


PERFIL_ADMIN = "ADMIN"
PERFIL_RECEPCAO = "RECEPCAO"
PERFIL_PROFISSIONAL = "PROFISSIONAL"
PERFIS_VALIDOS = {PERFIL_ADMIN, PERFIL_RECEPCAO, PERFIL_PROFISSIONAL}


@dataclass
class NaoAutenticado(Exception):
    destino: str = "/login"


@dataclass
class AcessoNegado(Exception):
    mensagem: str = "Você não possui permissão para esta ação."


def gerar_hash_senha(senha: str, *, iteracoes: int = 260_000) -> str:
    if len(senha) < 8:
        raise ValueError("A senha deve possuir pelo menos 8 caracteres.")
    salt = secrets.token_hex(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt.encode(), iteracoes)
    return f"pbkdf2_sha256${iteracoes}${salt}${hash_bytes.hex()}"


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        algoritmo, iteracoes, salt, hash_salvo = senha_hash.split("$", 3)
        if algoritmo != "pbkdf2_sha256":
            return False
        calculado = hashlib.pbkdf2_hmac(
            "sha256", senha.encode(), salt.encode(), int(iteracoes)
        ).hex()
        return hmac.compare_digest(calculado, hash_salvo)
    except (TypeError, ValueError):
        return False


def csrf_token(request: Request) -> str:
    token = request.session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf_token"] = token
    return token


def validar_csrf(request: Request, token_recebido: str | None):
    esperado = request.session.get("csrf_token")
    if not esperado or not token_recebido or not hmac.compare_digest(esperado, token_recebido):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token CSRF inválido.")


def obter_usuario_atual(request: Request, db: Session) -> Usuario | None:
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return None
    usuario = db.get(Usuario, int(usuario_id))
    if not usuario or not usuario.ativo:
        request.session.clear()
        return None
    return usuario


def usuario_html(request: Request, db: Session = Depends(get_db)) -> Usuario:
    usuario = obter_usuario_atual(request, db)
    if usuario is None:
        raise NaoAutenticado()
    return usuario


def perfis_html(*perfis):
    def dependencia(usuario: Usuario = Depends(usuario_html)):
        if usuario.perfil not in perfis:
            raise AcessoNegado()
        return usuario
    return dependencia


def usuario_api(request: Request, db: Session = Depends(get_db)) -> Usuario:
    usuario = obter_usuario_atual(request, db)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Autenticação necessária.")
    return usuario


def perfis_api(*perfis):
    def dependencia(usuario: Usuario = Depends(usuario_api)):
        if usuario.perfil not in perfis:
            raise HTTPException(status_code=403, detail="Perfil sem permissão.")
        return usuario
    return dependencia
