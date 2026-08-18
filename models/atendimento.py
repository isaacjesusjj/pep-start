class Atendimento:
    """Representa um atendimento registrado no histórico do paciente."""

    def __init__(
        self,
        paciente_id,
        data,
        motivo,
        observacao=None,
        atendimento_id=None,
    ):
        self.id = atendimento_id
        self.paciente_id = paciente_id
        self.data = data
        self.motivo = motivo
        self.observacao = observacao
