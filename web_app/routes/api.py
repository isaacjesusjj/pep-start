import math

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from shared.validacoes import normalizar_nome, normalizar_telefone, validar_data_nascimento
from web_app.audit import registrar_auditoria
from web_app.database import get_db
from web_app.models import Alergia, Atendimento, Exame, Paciente, Prescricao, Usuario
from web_app.schemas import PaginaPacientes, PacienteEntrada, PacienteSaida, ProntuarioSaida
from web_app.security import (
    PERFIL_ADMIN,
    PERFIL_PROFISSIONAL,
    PERFIL_RECEPCAO,
    csrf_token,
    perfis_api,
    usuario_api,
    validar_csrf,
)

router = APIRouter(prefix="/api/v1", tags=["API REST"])
PER_PAGE_MAX = 50


def paciente_basico(p):
    return {"id": p.id, "nome": p.nome, "data_nascimento": p.data_nascimento, "telefone": p.telefone}


@router.get("/csrf")
def api_csrf(request: Request, usuario: Usuario = Depends(usuario_api)):
    return {"csrf_token": csrf_token(request), "usuario": {"id": usuario.id, "perfil": usuario.perfil}}


@router.get("/pacientes", response_model=PaginaPacientes)
def api_pacientes(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    q: str = "",
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_api),
):
    page = max(1, page); per_page = min(PER_PAGE_MAX, max(1, per_page)); q = q.strip()
    count_stmt = select(func.count()).select_from(Paciente); query = select(Paciente)
    if q:
        filtro = Paciente.nome.ilike(f"%{q}%")
        count_stmt = count_stmt.where(filtro); query = query.where(filtro)
    total = db.scalar(count_stmt) or 0
    itens = db.scalars(query.order_by(Paciente.nome, Paciente.id).offset((page - 1) * per_page).limit(per_page)).all()
    registrar_auditoria(db, request, acao="API_LISTAR_PACIENTES", recurso="api", usuario=usuario)
    return {"page": page, "per_page": per_page, "total": total, "pages": max(1, math.ceil(total / per_page)), "items": [paciente_basico(p) for p in itens]}


@router.get("/pacientes/{paciente_id}", response_model=PacienteSaida)
def api_paciente(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_api),
):
    paciente = db.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    registrar_auditoria(db, request, acao="API_VISUALIZAR_PACIENTE", recurso="paciente", recurso_id=paciente.id, usuario=usuario)
    return paciente_basico(paciente)


@router.get("/pacientes/{paciente_id}/prontuario", response_model=ProntuarioSaida)
def api_prontuario(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_api(PERFIL_ADMIN, PERFIL_PROFISSIONAL)),
):
    paciente = db.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    alergias = db.scalars(select(Alergia).where(Alergia.paciente_id == paciente_id).order_by(Alergia.descricao)).all()
    atendimentos = db.scalars(select(Atendimento).where(Atendimento.paciente_id == paciente_id).order_by(Atendimento.data.desc())).all()
    exames = db.scalars(select(Exame).where(Exame.paciente_id == paciente_id).order_by(Exame.data_exame.desc())).all()
    prescricoes = db.scalars(select(Prescricao).where(Prescricao.paciente_id == paciente_id).order_by(Prescricao.data_prescricao.desc())).all()
    registrar_auditoria(db, request, acao="API_VISUALIZAR_PRONTUARIO", recurso="paciente", recurso_id=paciente.id, usuario=usuario)
    return {
        "paciente": paciente_basico(paciente),
        "alergias": [{"id": a.id, "descricao": a.descricao} for a in alergias],
        "atendimentos": [{"id": a.id, "data": a.data, "motivo": a.motivo, "observacao": a.observacao} for a in atendimentos],
        "exames": [{"id": e.id, "nome": e.nome, "data_exame": e.data_exame, "status": e.status, "resultado": e.resultado, "observacao": e.observacao} for e in exames],
        "prescricoes": [{"id": p.id, "medicamento": p.medicamento, "dose": p.dose, "frequencia": p.frequencia, "data_prescricao": p.data_prescricao, "observacao": p.observacao} for p in prescricoes],
    }


@router.post("/pacientes", status_code=201, response_model=PacienteSaida)
async def api_criar_paciente(
    request: Request,
    dados: PacienteEntrada,
    x_csrf_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(perfis_api(PERFIL_ADMIN, PERFIL_RECEPCAO)),
):
    validar_csrf(request, x_csrf_token)
    try:
        paciente = Paciente(
            nome=normalizar_nome(dados.nome),
            data_nascimento=validar_data_nascimento(dados.data_nascimento),
            telefone=normalizar_telefone(dados.telefone),
        )
        db.add(paciente); db.commit(); db.refresh(paciente)
        registrar_auditoria(db, request, acao="API_CRIAR_PACIENTE", recurso="paciente", recurso_id=paciente.id, usuario=usuario)
        return paciente_basico(paciente)
    except ValueError as erro:
        db.rollback(); raise HTTPException(status_code=422, detail=str(erro)) from erro
