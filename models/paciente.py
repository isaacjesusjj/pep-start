class Paciente:
    """Representa um paciente cadastrado no PEP Start."""

    def __init__(self, nome, data_nascimento, telefone=None, paciente_id=None):
        self.id = paciente_id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone
