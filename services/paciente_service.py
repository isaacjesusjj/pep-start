from datetime import date, datetime

from models.paciente import Paciente


class PacienteService:
    """Aplica as regras de negócio relacionadas aos pacientes."""

    def __init__(
        self,
        paciente_repository,
        alergia_repository,
        atendimento_repository,
    ):
        self.paciente_repository = paciente_repository
        self.alergia_repository = alergia_repository
        self.atendimento_repository = atendimento_repository

    @staticmethod
    def _validar_nome(nome):
        nome = " ".join(nome.split())
        if len(nome) < 3:
            raise ValueError("O nome deve possuir pelo menos 3 caracteres.")
        return nome

    @staticmethod
    def _validar_data_nascimento(data_nascimento):
        try:
            data_convertida = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        except ValueError as erro:
            raise ValueError("Use a data no formato AAAA-MM-DD.") from erro

        if data_convertida > date.today():
            raise ValueError("A data de nascimento não pode estar no futuro.")

        return data_convertida.isoformat()

    @staticmethod
    def _normalizar_telefone(telefone):
        if telefone is None or not telefone.strip():
            return None

        digitos = "".join(
            caractere for caractere in telefone if caractere.isdigit()
        )

        if len(digitos) not in (10, 11):
            raise ValueError("Informe um telefone com 10 ou 11 dígitos.")

        return digitos

    def cadastrar_paciente(self, nome, data_nascimento, telefone=None):
        paciente = Paciente(
            nome=self._validar_nome(nome),
            data_nascimento=self._validar_data_nascimento(data_nascimento),
            telefone=self._normalizar_telefone(telefone),
        )
        return self.paciente_repository.cadastrar(paciente)

    def listar_pacientes(self):
        return self.paciente_repository.listar()

    def buscar_por_id(self, paciente_id):
        return self.paciente_repository.buscar_por_id(paciente_id)

    def buscar_por_nome(self, nome):
        nome = nome.strip()
        if not nome:
            raise ValueError("Informe um nome para a busca.")
        return self.paciente_repository.buscar_por_nome(nome)

    def atualizar_paciente(self, paciente_id, nome, data_nascimento, telefone=None):
        paciente = self.buscar_por_id(paciente_id)
        if paciente is None:
            raise ValueError("Paciente não encontrado.")

        paciente.nome = self._validar_nome(nome)
        paciente.data_nascimento = self._validar_data_nascimento(data_nascimento)
        paciente.telefone = self._normalizar_telefone(telefone)

        self.paciente_repository.atualizar(paciente)
        return paciente

    def excluir_paciente(self, paciente_id):
        paciente = self.buscar_por_id(paciente_id)
        if paciente is None:
            raise ValueError("Paciente não encontrado.")

        possui_alergia = self.alergia_repository.existe_para_paciente(paciente_id)
        possui_atendimento = self.atendimento_repository.existe_para_paciente(
            paciente_id
        )

        if possui_alergia or possui_atendimento:
            raise ValueError(
                "Não é possível excluir o paciente porque existem "
                "registros clínicos associados."
            )

        return self.paciente_repository.excluir(paciente_id)
