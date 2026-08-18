from fastapi import Request
from sqlalchemy.orm import Session

from web_app.models import Auditoria, Usuario


def registrar_auditoria(
    db: Session,
    request: Request,
    *,
    acao: str,
    recurso: str,
    usuario: Usuario | None = None,
    recurso_id: int | str | None = None,
    detalhes: str | None = None,
):
    """Registra metadados do acesso sem gravar conteúdo clínico sensível."""

    ip = request.client.host if request.client else None
    evento = Auditoria(
        usuario_id=usuario.id if usuario else None,
        acao=acao,
        recurso=recurso,
        recurso_id=str(recurso_id) if recurso_id is not None else None,
        detalhes=detalhes,
        ip=ip,
    )
    db.add(evento)
    db.commit()
    return evento
