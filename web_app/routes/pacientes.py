import math
from datetime import date

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from shared.validacoes import (
    normalizar_nome,
    normalizar_telefone,
    texto_obrigatorio,
    validar_data_clinica,
    validar_data_nascimento,
)
from web_app.audit import registrar_auditoria
from web_app.database import get_db
from web_app.models import Alergia, Atendimento, Exame, Paciente, Prescricao, Usuario
from web_app.security import (
    PERFIL_ADMIN,
    PERFIL_PROFISSIONAL,
    PERFIL_RECEPCAO,
    csrf_token,
    perfis_html,
    usuario_html,
    validar_csrf,
)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")
PER_PAGE = 10


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


def buscar_paciente_ou_404(db: Session, paciente_id: int):
    paciente = db.get(Paciente, paciente_id)
    if not paciente:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    return paciente


@router.get("/")
def inicio():
    return RedirectResponse("/dashboard", status_code=303)


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_html),
):
    dados = {
        "pacientes": db.scalar(select(func.count()).select_from(Paciente)) or 0,
        "atendimentos": db.scalar(select(func.count()).select_from(Atendimento)) or 0,
        "exames": db.scalar(select(func.count()).select_from(Exame)) or 0,
        "prescricoes": db.scalar(select(func.count()).select_from(Prescricao)) or 0,
    }
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=contexto(request, usuario, titulo="Dashboard", dados=dados),
    )


@router.get("/pacientes")
def listar_pacientes(
    request: Request,
    page: int = 1,
    q: str = "",
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_html),
):
    page = max(1, page)
    q = q.strip()
    filtros = []
    if q:
        termo = f"%{q}%"
        filtros.append(or_(Paciente.nome.ilike(termo), Paciente.telefone.ilike(termo)))

    count_stmt = select(func.count()).select_from(Paciente)
    query_stmt = select(Paciente)
    if filtros:
        count_stmt = count_stmt.where(*filtros)
        query_stmt = query_stmt.where(*filtros)

    total = db.scalar(count_stmt) or 0
    paginas = max(1, math.ceil(total / PER_PAGE))
    if page > paginas:
        page = paginas

    pacientes = db.scalars(
        query_stmt.order_by(Paciente.nome, Paciente.id)
        .offset((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="pacientes_lista.html",
        context=contexto(
            request,
            usuario,
            titulo="Pacientes",
            pacientes=pacientes,
            page=page,
            paginas=paginas,
            total=total,
            q=q,
        ),
    )


@router.get("/pacientes/novo")
def novo_paciente_get(
    request: Request,
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN, PERFIL_RECEPCAO)),
):
    return templates.TemplateResponse(
        request=request,
        name="paciente_form.html",
        context=contexto(request, usuario, titulo="Novo paciente", paciente=None),
    )


@router.post("/pacientes/novo")
async def novo_paciente_post(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN, PERFIL_RECEPCAO)),
):
    form = await request.form()
    validar_csrf(request, form.get("csrf_token"))
    try:
        paciente = Paciente(
            nome=normalizar_nome(str(form.get("nome", ""))),
            data_nascimento=validar_data_nascimento(str(form.get("data_nascimento", ""))),
            telefone=normalizar_telefone(str(form.get("telefone", ""))),
        )
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        registrar_auditoria(
            db,
            request,
            acao="CRIAR_PACIENTE",
            recurso="paciente",
            recurso_id=paciente.id,
            usuario=usuario,
        )
        return RedirectResponse(f"/pacientes/{paciente.id}", status_code=303)
    except ValueError as erro:
        db.rollback()
        return templates.TemplateResponse(
            request=request,
            name="paciente_form.html",
            context=contexto(request, usuario, titulo="Novo paciente", paciente=None, erro=str(erro)),
            status_code=400,
        )


@router.get("/pacientes/{paciente_id}/editar")
def editar_paciente_get(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN, PERFIL_RECEPCAO)),
):
    paciente = buscar_paciente_ou_404(db, paciente_id)
    return templates.TemplateResponse(
        request=request,
        name="paciente_form.html",
        context=contexto(request, usuario, titulo="Editar paciente", paciente=paciente),
    )


@router.post("/pacientes/{paciente_id}/editar")
async def editar_paciente_post(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN, PERFIL_RECEPCAO)),
):
    paciente = buscar_paciente_ou_404(db, paciente_id)
    form = await request.form()
    validar_csrf(request, form.get("csrf_token"))
    try:
        paciente.nome = normalizar_nome(str(form.get("nome", "")))
        paciente.data_nascimento = validar_data_nascimento(str(form.get("data_nascimento", "")))
        paciente.telefone = normalizar_telefone(str(form.get("telefone", "")))
        db.commit()
        registrar_auditoria(
            db,
            request,
            acao="ATUALIZAR_PACIENTE",
            recurso="paciente",
            recurso_id=paciente.id,
            usuario=usuario,
        )
        return RedirectResponse(f"/pacientes/{paciente.id}", status_code=303)
    except ValueError as erro:
        db.rollback()
        return templates.TemplateResponse(
            request=request,
            name="paciente_form.html",
            context=contexto(request, usuario, titulo="Editar paciente", paciente=paciente, erro=str(erro)),
            status_code=400,
        )


@router.get("/pacientes/{paciente_id}")
def detalhe_paciente(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_html),
):
    paciente = buscar_paciente_ou_404(db, paciente_id)
    pode_ver_clinico = usuario.perfil in {PERFIL_ADMIN, PERFIL_PROFISSIONAL}

    alergias = atendimentos = exames = prescricoes = []
    if pode_ver_clinico:
        alergias = db.scalars(select(Alergia).where(Alergia.paciente_id == paciente_id).order_by(Alergia.descricao)).all()
        atendimentos = db.scalars(select(Atendimento).where(Atendimento.paciente_id == paciente_id).order_by(Atendimento.data.desc(), Atendimento.id.desc())).all()
        exames = db.scalars(select(Exame).where(Exame.paciente_id == paciente_id).order_by(Exame.data_exame.desc(), Exame.id.desc())).all()
        prescricoes = db.scalars(select(Prescricao).where(Prescricao.paciente_id == paciente_id).order_by(Prescricao.data_prescricao.desc(), Prescricao.id.desc())).all()

    registrar_auditoria(
        db,
        request,
        acao="VISUALIZAR_PACIENTE" if not pode_ver_clinico else "VISUALIZAR_PRONTUARIO",
        recurso="paciente",
        recurso_id=paciente.id,
        usuario=usuario,
        detalhes="Visualização administrativa." if not pode_ver_clinico else "Visualização clínica autorizada.",
    )

    return templates.TemplateResponse(
        request=request,
        name="paciente_detalhe.html",
        context=contexto(
            request,
            usuario,
            titulo=f"Paciente {paciente.nome}",
            paciente=paciente,
            pode_ver_clinico=pode_ver_clinico,
            alergias=alergias,
            atendimentos=atendimentos,
            exames=exames,
            prescricoes=prescricoes,
            hoje=date.today().isoformat(),
        ),
    )


@router.post("/pacientes/{paciente_id}/alergias")
async def registrar_alergia(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN, PERFIL_PROFISSIONAL)),
):
    paciente = buscar_paciente_ou_404(db, paciente_id)
    form = await request.form(); validar_csrf(request, form.get("csrf_token"))
    try:
        descricao = texto_obrigatorio(str(form.get("descricao", "")), "A descrição da alergia")
        existente = db.scalar(select(Alergia).where(Alergia.paciente_id == paciente_id, func.lower(Alergia.descricao) == descricao.lower()))
        if existente:
            raise ValueError("Essa alergia já está registrada para o paciente.")
        db.add(Alergia(paciente_id=paciente.id, descricao=descricao)); db.commit()
        registrar_auditoria(db, request, acao="REGISTRAR_ALERGIA", recurso="paciente", recurso_id=paciente.id, usuario=usuario)
        return RedirectResponse(f"/pacientes/{paciente.id}#alergias", status_code=303)
    except ValueError as erro:
        db.rollback(); return RedirectResponse(f"/pacientes/{paciente.id}?erro={str(erro)}", status_code=303)


@router.post("/pacientes/{paciente_id}/atendimentos")
async def registrar_atendimento(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN, PERFIL_PROFISSIONAL)),
):
    paciente = buscar_paciente_ou_404(db, paciente_id)
    form = await request.form(); validar_csrf(request, form.get("csrf_token"))
    try:
        data_registro = validar_data_clinica(str(form.get("data", "")), paciente.data_nascimento)
        motivo = texto_obrigatorio(str(form.get("motivo", "")), "O motivo")
        observacao = str(form.get("observacao", "")).strip() or None
        db.add(Atendimento(paciente_id=paciente.id, data=data_registro, motivo=motivo, observacao=observacao)); db.commit()
        registrar_auditoria(db, request, acao="REGISTRAR_ATENDIMENTO", recurso="paciente", recurso_id=paciente.id, usuario=usuario)
        return RedirectResponse(f"/pacientes/{paciente.id}#atendimentos", status_code=303)
    except ValueError as erro:
        db.rollback(); return RedirectResponse(f"/pacientes/{paciente.id}?erro={str(erro)}", status_code=303)


@router.post("/pacientes/{paciente_id}/exames")
async def registrar_exame(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN, PERFIL_PROFISSIONAL)),
):
    paciente = buscar_paciente_ou_404(db, paciente_id)
    form = await request.form(); validar_csrf(request, form.get("csrf_token"))
    try:
        nome = texto_obrigatorio(str(form.get("nome", "")), "O nome do exame")
        data_exame = validar_data_clinica(str(form.get("data_exame", "")), paciente.data_nascimento)
        status_exame = str(form.get("status", "SOLICITADO")).strip().upper()
        if status_exame not in {"SOLICITADO", "REALIZADO", "CONCLUIDO"}:
            raise ValueError("Status de exame inválido.")
        resultado = str(form.get("resultado", "")).strip() or None
        observacao = str(form.get("observacao", "")).strip() or None
        exame = Exame(paciente_id=paciente.id, nome=nome, data_exame=data_exame, status=status_exame, resultado=resultado, observacao=observacao)
        db.add(exame); db.commit(); db.refresh(exame)
        registrar_auditoria(db, request, acao="REGISTRAR_EXAME", recurso="exame", recurso_id=exame.id, usuario=usuario, detalhes=f"Paciente ID {paciente.id}; conteúdo clínico não registrado na auditoria.")
        return RedirectResponse(f"/pacientes/{paciente.id}#exames", status_code=303)
    except ValueError as erro:
        db.rollback(); return RedirectResponse(f"/pacientes/{paciente.id}?erro={str(erro)}", status_code=303)


@router.post("/pacientes/{paciente_id}/prescricoes")
async def registrar_prescricao(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_html(PERFIL_ADMIN, PERFIL_PROFISSIONAL)),
):
    paciente = buscar_paciente_ou_404(db, paciente_id)
    form = await request.form(); validar_csrf(request, form.get("csrf_token"))
    try:
        medicamento = texto_obrigatorio(str(form.get("medicamento", "")), "O medicamento")
        dose = texto_obrigatorio(str(form.get("dose", "")), "A dose")
        frequencia = texto_obrigatorio(str(form.get("frequencia", "")), "A frequência")
        data_prescricao = validar_data_clinica(str(form.get("data_prescricao", "")), paciente.data_nascimento)
        observacao = str(form.get("observacao", "")).strip() or None
        prescricao = Prescricao(paciente_id=paciente.id, medicamento=medicamento, dose=dose, frequencia=frequencia, data_prescricao=data_prescricao, observacao=observacao)
        db.add(prescricao); db.commit(); db.refresh(prescricao)
        registrar_auditoria(db, request, acao="REGISTRAR_PRESCRICAO", recurso="prescricao", recurso_id=prescricao.id, usuario=usuario, detalhes=f"Paciente ID {paciente.id}; conteúdo clínico não registrado na auditoria.")
        return RedirectResponse(f"/pacientes/{paciente.id}#prescricoes", status_code=303)
    except ValueError as erro:
        db.rollback(); return RedirectResponse(f"/pacientes/{paciente.id}?erro={str(erro)}", status_code=303)
