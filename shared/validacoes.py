from datetime import date, datetime


def normalizar_nome(nome: str) -> str:
    nome = " ".join((nome or "").split())
    if len(nome) < 3:
        raise ValueError("O nome deve possuir pelo menos 3 caracteres.")
    return nome


def validar_data(data_texto: str, *, mensagem: str = "Use a data no formato AAAA-MM-DD.") -> str:
    try:
        valor = datetime.strptime(data_texto, "%Y-%m-%d").date()
    except (TypeError, ValueError) as erro:
        raise ValueError(mensagem) from erro
    return valor.isoformat()


def validar_data_nascimento(data_texto: str) -> str:
    valor = validar_data(data_texto)
    if valor > date.today().isoformat():
        raise ValueError("A data de nascimento não pode estar no futuro.")
    return valor


def validar_data_clinica(data_texto: str, data_nascimento: str) -> str:
    valor = validar_data(data_texto)
    hoje = date.today().isoformat()
    if valor > hoje:
        raise ValueError("Um registro clínico realizado não pode ter data futura.")
    if valor < data_nascimento:
        raise ValueError("A data do registro não pode ser anterior ao nascimento.")
    return valor


def normalizar_telefone(telefone: str | None) -> str | None:
    if telefone is None or not telefone.strip():
        return None
    digitos = "".join(c for c in telefone if c.isdigit())
    if len(digitos) not in (10, 11):
        raise ValueError("Informe um telefone com 10 ou 11 dígitos.")
    return digitos


def texto_obrigatorio(valor: str | None, campo: str, minimo: int = 1) -> str:
    valor = " ".join((valor or "").split())
    if len(valor) < minimo:
        raise ValueError(f"{campo} é obrigatório.")
    return valor
