import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from web_app.database import Base, criar_engine, criar_session_factory
from web_app.security import AcessoNegado, NaoAutenticado

# Importar os modelos registra todas as tabelas no metadata antes do create_all.
from web_app import models  # noqa: F401
from web_app.routes import admin, api, auth, pacientes


PASTA_WEB = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(PASTA_WEB / "templates"))


def create_app(*, database_url: str | None = None, secret_key: str | None = None, testing: bool = False):
    app = FastAPI(
        title="PEP Start Web",
        description="Projeto acadêmico de prontuário eletrônico com dados fictícios.",
        version="2.0.0",
        docs_url="/api/docs",
        redoc_url=None,
        openapi_url="/api/openapi.json",
    )

    chave = secret_key or os.getenv("PEP_START_SECRET_KEY")
    if not chave:
        # Adequado para desenvolvimento local. Em implantação real deve ser
        # substituído por segredo persistente via variável de ambiente.
        chave = "pep-start-desenvolvimento-troque-esta-chave"

    app.add_middleware(
        SessionMiddleware,
        secret_key=chave,
        max_age=8 * 60 * 60,
        same_site="lax",
        https_only=(os.getenv("PEP_START_HTTPS_ONLY", "0") == "1" and not testing),
    )
    app.mount("/static", StaticFiles(directory=str(PASTA_WEB / "static")), name="static")

    engine = criar_engine(database_url)
    SessionLocal = criar_session_factory(engine)
    app.state.engine = engine
    app.state.SessionLocal = SessionLocal
    Base.metadata.create_all(bind=engine)

    app.include_router(auth.router)
    app.include_router(pacientes.router)
    app.include_router(admin.router)
    app.include_router(api.router)

    @app.get("/health", include_in_schema=False)
    async def health_check():
        """Endpoint simples usado pela hospedagem para verificar se a aplicação está ativa."""
        return {"status": "ok"}

    @app.exception_handler(NaoAutenticado)
    async def nao_autenticado_handler(request: Request, exc: NaoAutenticado):
        return RedirectResponse(f"/login?next={request.url.path}", status_code=303)

    @app.exception_handler(AcessoNegado)
    async def acesso_negado_handler(request: Request, exc: AcessoNegado):
        return templates.TemplateResponse(
            request=request,
            name="erro.html",
            context={"titulo": "Acesso negado", "mensagem": exc.mensagem},
            status_code=403,
        )

    @app.middleware("http")
    async def cabecalhos_seguranca(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store" if request.url.path.startswith(("/pacientes", "/auditoria", "/api/")) else "no-cache"
        return response

    return app
