from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from web_app.database import Base


def agora_utc_sem_timezone():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    data_nascimento: Mapped[str] = mapped_column(Text, nullable=False)
    telefone: Mapped[str | None] = mapped_column(Text, nullable=True)

    alergias: Mapped[list["Alergia"]] = relationship(back_populates="paciente")
    atendimentos: Mapped[list["Atendimento"]] = relationship(back_populates="paciente")
    exames: Mapped[list["Exame"]] = relationship(back_populates="paciente")
    prescricoes: Mapped[list["Prescricao"]] = relationship(back_populates="paciente")

    __table_args__ = (Index("idx_pacientes_nome_web", "nome"),)


class Alergia(Base):
    __tablename__ = "alergias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id", ondelete="RESTRICT"), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    paciente: Mapped[Paciente] = relationship(back_populates="alergias")

    __table_args__ = (UniqueConstraint("paciente_id", "descricao", name="uq_alergia_paciente_descricao"),)


class Atendimento(Base):
    __tablename__ = "atendimentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id", ondelete="RESTRICT"), nullable=False)
    data: Mapped[str] = mapped_column(Text, nullable=False)
    motivo: Mapped[str] = mapped_column(Text, nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    paciente: Mapped[Paciente] = relationship(back_populates="atendimentos")


class Exame(Base):
    __tablename__ = "exames"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id", ondelete="RESTRICT"), nullable=False)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    data_exame: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="SOLICITADO")
    resultado: Mapped[str | None] = mapped_column(Text, nullable=True)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    paciente: Mapped[Paciente] = relationship(back_populates="exames")


class Prescricao(Base):
    __tablename__ = "prescricoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id", ondelete="RESTRICT"), nullable=False)
    medicamento: Mapped[str] = mapped_column(Text, nullable=False)
    dose: Mapped[str] = mapped_column(Text, nullable=False)
    frequencia: Mapped[str] = mapped_column(Text, nullable=False)
    data_prescricao: Mapped[str] = mapped_column(Text, nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    paciente: Mapped[Paciente] = relationship(back_populates="prescricoes")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(Text, nullable=False)
    perfil: Mapped[str] = mapped_column(String(30), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=agora_utc_sem_timezone)

    auditorias: Mapped[list["Auditoria"]] = relationship(back_populates="usuario")


class Auditoria(Base):
    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    acao: Mapped[str] = mapped_column(String(80), nullable=False)
    recurso: Mapped[str] = mapped_column(String(80), nullable=False)
    recurso_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    detalhes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip: Mapped[str | None] = mapped_column(String(80), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=agora_utc_sem_timezone)

    usuario: Mapped[Usuario | None] = relationship(back_populates="auditorias")

    __table_args__ = (Index("idx_auditoria_criado_em", "criado_em"),)
