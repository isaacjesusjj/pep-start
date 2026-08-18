from database.conexao import conectar
from models.paciente import Paciente


class PacienteRepository:
    """Executa as operações de persistência da tabela pacientes."""

    @staticmethod
    def _linha_para_paciente(linha):
        if linha is None:
            return None

        return Paciente(
            nome=linha["nome"],
            data_nascimento=linha["data_nascimento"],
            telefone=linha["telefone"],
            paciente_id=linha["id"],
        )

    def cadastrar(self, paciente):
        sql = """
            INSERT INTO pacientes (nome, data_nascimento, telefone)
            VALUES (?, ?, ?)
        """

        with conectar() as conexao:
            cursor = conexao.execute(
                sql,
                (paciente.nome, paciente.data_nascimento, paciente.telefone),
            )
            paciente.id = cursor.lastrowid

        return paciente

    def listar(self):
        sql = """
            SELECT id, nome, data_nascimento, telefone
            FROM pacientes
            ORDER BY nome COLLATE NOCASE, id
        """

        with conectar() as conexao:
            linhas = conexao.execute(sql).fetchall()

        return [self._linha_para_paciente(linha) for linha in linhas]

    def buscar_por_id(self, paciente_id):
        sql = """
            SELECT id, nome, data_nascimento, telefone
            FROM pacientes
            WHERE id = ?
        """

        with conectar() as conexao:
            linha = conexao.execute(sql, (paciente_id,)).fetchone()

        return self._linha_para_paciente(linha)

    def buscar_por_nome(self, nome):
        sql = """
            SELECT id, nome, data_nascimento, telefone
            FROM pacientes
            WHERE nome LIKE ? COLLATE NOCASE
            ORDER BY nome COLLATE NOCASE, id
        """

        with conectar() as conexao:
            linhas = conexao.execute(sql, (f"%{nome}%",)).fetchall()

        return [self._linha_para_paciente(linha) for linha in linhas]

    def atualizar(self, paciente):
        sql = """
            UPDATE pacientes
            SET nome = ?, data_nascimento = ?, telefone = ?
            WHERE id = ?
        """

        with conectar() as conexao:
            cursor = conexao.execute(
                sql,
                (
                    paciente.nome,
                    paciente.data_nascimento,
                    paciente.telefone,
                    paciente.id,
                ),
            )
            return cursor.rowcount > 0

    def excluir(self, paciente_id):
        with conectar() as conexao:
            cursor = conexao.execute(
                "DELETE FROM pacientes WHERE id = ?",
                (paciente_id,),
            )
            return cursor.rowcount > 0
