from datetime import date, datetime

from models.alergia import Alergia
from models.atendimento import Atendimento


class ProntuarioService:
    """Aplica regras sobre alergias, atendimentos e consulta do prontuário."""

    def __init__(
        self,
        paciente_repository,
        alergia_repository,
        atendimento_repository,
    ):
        self.paciente_repository = paciente_repository
        self.alergia_repository = alergia_repository
        self.atendimento_repository = atendimento_repository

    def _obter_paciente_ou_falhar(self, paciente_id):
        paciente = self.paciente_repository.buscar_por_id(paciente_id)
        if paciente is None:
            raise ValueError("Paciente não encontrado.")
        return paciente

    def registrar_alergia(self, paciente_id, descricao):
        self._obter_paciente_ou_falhar(paciente_id)
        descricao = " ".join(descricao.split())

        if not descricao:
            raise ValueError("A descrição da alergia é obrigatória.")

        if self.alergia_repository.existe_descricao_para_paciente(
            paciente_id,
            descricao,
        ):
            raise ValueError("Essa alergia já está registrada para o paciente.")

        alergia = Alergia(paciente_id=paciente_id, descricao=descricao)
        return self.alergia_repository.cadastrar(alergia)

    @staticmethod
    def _validar_data_atendimento(data_atendimento):
        try:
            data_convertida = datetime.strptime(data_atendimento, "%Y-%m-%d").date()
        except ValueError as erro:
            raise ValueError("Use a data no formato AAAA-MM-DD.") from erro

        if data_convertida > date.today():
            raise ValueError(
                "Um atendimento já realizado não pode ter data futura."
            )

        return data_convertida.isoformat()

    def registrar_atendimento(
        self,
        paciente_id,
        data_atendimento,
        motivo,
        observacao=None,
    ):
        paciente = self._obter_paciente_ou_falhar(paciente_id)
        data_validada = self._validar_data_atendimento(data_atendimento)

        if data_validada < paciente.data_nascimento:
            raise ValueError(
                "A data do atendimento não pode ser anterior ao nascimento."
            )

        motivo = " ".join(motivo.split())
        if not motivo:
            raise ValueError("O motivo do atendimento é obrigatório.")

        if observacao is not None:
            observacao = observacao.strip() or None

        atendimento = Atendimento(
            paciente_id=paciente_id,
            data=data_validada,
            motivo=motivo,
            observacao=observacao,
        )
        return self.atendimento_repository.cadastrar(atendimento)

    def consultar_prontuario(self, paciente_id):
        paciente = self._obter_paciente_ou_falhar(paciente_id)
        alergias = self.alergia_repository.listar_por_paciente(paciente_id)
        atendimentos = self.atendimento_repository.listar_por_paciente(paciente_id)

        return {
            "paciente": paciente,
            "alergias": alergias,
            "atendimentos": atendimentos,
        }
