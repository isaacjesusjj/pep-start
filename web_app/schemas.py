from pydantic import BaseModel


class PacienteEntrada(BaseModel):
    nome: str
    data_nascimento: str
    telefone: str | None = None


class PacienteSaida(BaseModel):
    id: int
    nome: str
    data_nascimento: str
    telefone: str | None = None


class PaginaPacientes(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int
    items: list[PacienteSaida]


class AlergiaSaida(BaseModel):
    id: int
    descricao: str


class AtendimentoSaida(BaseModel):
    id: int
    data: str
    motivo: str
    observacao: str | None = None


class ExameSaida(BaseModel):
    id: int
    nome: str
    data_exame: str
    status: str
    resultado: str | None = None
    observacao: str | None = None


class PrescricaoSaida(BaseModel):
    id: int
    medicamento: str
    dose: str
    frequencia: str
    data_prescricao: str
    observacao: str | None = None


class ProntuarioSaida(BaseModel):
    paciente: PacienteSaida
    alergias: list[AlergiaSaida]
    atendimentos: list[AtendimentoSaida]
    exames: list[ExameSaida]
    prescricoes: list[PrescricaoSaida]
