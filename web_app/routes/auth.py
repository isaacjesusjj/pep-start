from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from shared.validacoes import normalizar_nome
from web_app.audit import registrar_auditoria
from web_app.database import get_db
from web_app.models import Usuario
from web_app.security import (
    PERFIL_ADMIN,
    csrf_token,
    gerar_hash_senha,
    obter_usuario_atual,
    validar_csrf,
    verificar_senha,
)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")


def contexto(request, **extras):
    return {"request": request, "csrf_token": csrf_token(request), **extras}


@router.get("/setup")
def setup_get(request: Request, db: Session = Depends(get_db)):
    total = db.scalar(select(func.count()).select_from(Usuario)) or 0
    if total > 0:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="setup.html",
        context=contexto(request, titulo="Configuração inicial"),
    )


@router.post("/setup")
async def setup_post(request: Request, db: Session = Depends(get_db)):
    total = db.scalar(select(func.count()).select_from(Usuario)) or 0
    if total > 0:
        return RedirectResponse("/login", status_code=303)

    form = await request.form()
    validar_csrf(request, form.get("csrf_token"))

    try:
        nome = normalizar_nome(str(form.get("nome", "")))
        email = str(form.get("email", "")).strip().lower()
        if "@" not in email or len(email) < 5:
            raise ValueError("Informe um e-mail válido.")
        senha_hash = gerar_hash_senha(str(form.get("senha", "")))

        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            perfil=PERFIL_ADMIN,
            ativo=True,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        registrar_auditoria(
            db,
            request,
            acao="CRIAR_ADMIN_INICIAL",
            recurso="usuario",
            usuario=usuario,
            recurso_id=usuario.id,
        )
        request.session["usuario_id"] = usuario.id
        request.session["csrf_token"] = csrf_token(request)
        return RedirectResponse("/dashboard", status_code=303)
    except ValueError as erro:
        db.rollback()
        return templates.TemplateResponse(
            request=request,
            name="setup.html",
            context=contexto(request, titulo="Configuração inicial", erro=str(erro)),
            status_code=400,
        )


@router.get("/login")
def login_get(request: Request, db: Session = Depends(get_db)):
    if obter_usuario_atual(request, db):
        return RedirectResponse("/dashboard", status_code=303)

    total = db.scalar(select(func.count()).select_from(Usuario)) or 0
    if total == 0:
        return RedirectResponse("/setup", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=contexto(request, titulo="Entrar"),
    )


@router.post("/login")
async def login_post(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    validar_csrf(request, form.get("csrf_token"))

    email = str(form.get("email", "")).strip().lower()
    senha = str(form.get("senha", ""))
    usuario = db.scalar(select(Usuario).where(Usuario.email == email))

    if not usuario or not usuario.ativo or not verificar_senha(senha, usuario.senha_hash):
        registrar_auditoria(
            db,
            request,
            acao="LOGIN_FALHOU",
            recurso="autenticacao",
            detalhes="Tentativa de login inválida.",
        )
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context=contexto(request, titulo="Entrar", erro="E-mail ou senha inválidos."),
            status_code=401,
        )

    request.session.clear()
    request.session["usuario_id"] = usuario.id
    request.session["csrf_token"] = csrf_token(request)
    registrar_auditoria(
        db,
        request,
        acao="LOGIN_SUCESSO",
        recurso="autenticacao",
        usuario=usuario,
    )
    return RedirectResponse("/dashboard", status_code=303)


@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    validar_csrf(request, form.get("csrf_token"))
    usuario = obter_usuario_atual(request, db)
    if usuario:
        registrar_auditoria(
            db,
            request,
            acao="LOGOUT",
            recurso="autenticacao",
            usuario=usuario,
        )
    request.session.clear()
    return RedirectResponse("/login", status_code=303)
