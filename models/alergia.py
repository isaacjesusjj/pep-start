class Alergia:
    """Representa uma alergia associada a um paciente."""

    def __init__(self, paciente_id, descricao, alergia_id=None):
        self.id = alergia_id
        self.paciente_id = paciente_id
        self.descricao = descricao
