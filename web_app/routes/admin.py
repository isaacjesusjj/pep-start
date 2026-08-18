import math

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from shared.validacoes import normalizar_nome
from web_app.audit import registrar_auditoria
from web_app.database import get_db
from web_app.models import Auditoria, Usuario
from web_app.security import (
    PERFIL_ADMIN,
    PERFIL_PROFISSIONAL,
    PERFIL_RECEPCAO,
    PERFIS_VALIDOS,
    csrf_token,
    gerar_hash_senha,
    perfis_html,
    validar_csrf,
)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")
PER_PAGE = 20


def contexto(request, usuario, **extras):
    return {
        "request": request,
        "usuario": usuario,
        "csrf_token": csrf_token(request),
        "PERFIL_ADMIN": PERFIL_ADMIN,
        "PERFIL_PROFISSIONAL": PERFIL_PROFISSIONAL,
        "PERFIL_RECEPCAO": PERFIL_RECEPCAO,
        **extras,
    }


@router.get("/usuarios")
def usuarios(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN)),
):
    lista = db.scalars(select(Usuario).order_by(Usuario.nome)).all()
    return templates.TemplateResponse(request=request, name="usuarios_lista.html", context=contexto(request, usuario, titulo="Usuários", usuarios=lista))


@router.get("/usuarios/novo")
def novo_usuario_get(request: Request, usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN))):
    return templates.TemplateResponse(request=request, name="usuario_form.html", context=contexto(request, usuario, titulo="Novo usuário", perfis=sorted(PERFIS_VALIDOS)))


@router.post("/usuarios/novo")
async def novo_usuario_post(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN)),
):
    form = await request.form(); validar_csrf(request, form.get("csrf_token"))
    try:
        nome = normalizar_nome(str(form.get("nome", "")))
        email = str(form.get("email", "")).strip().lower()
        perfil = str(form.get("perfil", "")).strip().upper()
        if "@" not in email:
            raise ValueError("Informe um e-mail válido.")
        if perfil not in PERFIS_VALIDOS:
            raise ValueError("Perfil inválido.")
        if db.scalar(select(Usuario).where(Usuario.email == email)):
            raise ValueError("Já existe um usuário com esse e-mail.")
        criado = Usuario(nome=nome, email=email, senha_hash=gerar_hash_senha(str(form.get("senha", ""))), perfil=perfil, ativo=True)
        db.add(criado); db.commit(); db.refresh(criado)
        registrar_auditoria(db, request, acao="CRIAR_USUARIO", recurso="usuario", recurso_id=criado.id, usuario=usuario, detalhes=f"Perfil criado: {perfil}.")
        return RedirectResponse("/usuarios", status_code=303)
    except ValueError as erro:
        db.rollback()
        return templates.TemplateResponse(request=request, name="usuario_form.html", context=contexto(request, usuario, titulo="Novo usuário", perfis=sorted(PERFIS_VALIDOS), erro=str(erro)), status_code=400)


@router.post("/usuarios/{usuario_id}/alternar")
async def alternar_usuario(
    usuario_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN)),
):
    form = await request.form(); validar_csrf(request, form.get("csrf_token"))
    alvo = db.get(Usuario, usuario_id)
    if not alvo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if alvo.id == usuario.id:
        raise HTTPException(status_code=400, detail="Você não pode desativar sua própria conta.")
    alvo.ativo = not alvo.ativo; db.commit()
    registrar_auditoria(db, request, acao="ALTERAR_STATUS_USUARIO", recurso="usuario", recurso_id=alvo.id, usuario=usuario, detalhes=f"Ativo={alvo.ativo}.")
    return RedirectResponse("/usuarios", status_code=303)


@router.get("/auditoria")
def auditoria(
    request: Request,
    page: int = 1,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN)),
):
    page = max(1, page)
    total = db.scalar(select(func.count()).select_from(Auditoria)) or 0
    paginas = max(1, math.ceil(total / PER_PAGE))
    page = min(page, paginas)
    eventos = db.scalars(
        select(Auditoria).options(joinedload(Auditoria.usuario)).order_by(Auditoria.criado_em.desc(), Auditoria.id.desc()).offset((page - 1) * PER_PAGE).limit(PER_PAGE)
    ).all()
    registrar_auditoria(db, request, acao="VISUALIZAR_AUDITORIA", recurso="auditoria", usuario=usuario)
    return templates.TemplateResponse(request=request, name="auditoria.html", context=contexto(request, usuario, titulo="Auditoria", eventos=eventos, page=page, paginas=paginas, total=total))
