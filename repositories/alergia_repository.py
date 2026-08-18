from database.conexao import conectar
from models.alergia import Alergia


class AlergiaRepository:
    """Executa as operações de persistência da tabela alergias."""

    @staticmethod
    def _linha_para_alergia(linha):
        return Alergia(
            paciente_id=linha["paciente_id"],
            descricao=linha["descricao"],
            alergia_id=linha["id"],
        )

    def cadastrar(self, alergia):
        sql = """
            INSERT INTO alergias (paciente_id, descricao)
            VALUES (?, ?)
        """

        with conectar() as conexao:
            cursor = conexao.execute(
                sql,
                (alergia.paciente_id, alergia.descricao),
            )
            alergia.id = cursor.lastrowid

        return alergia

    def listar_por_paciente(self, paciente_id):
        sql = """
            SELECT id, paciente_id, descricao
            FROM alergias
            WHERE paciente_id = ?
            ORDER BY descricao COLLATE NOCASE, id
        """

        with conectar() as conexao:
            linhas = conexao.execute(sql, (paciente_id,)).fetchall()

        return [self._linha_para_alergia(linha) for linha in linhas]

    def existe_para_paciente(self, paciente_id):
        with conectar() as conexao:
            linha = conexao.execute(
                "SELECT 1 FROM alergias WHERE paciente_id = ? LIMIT 1",
                (paciente_id,),
            ).fetchone()

        return linha is not None

    def existe_descricao_para_paciente(self, paciente_id, descricao):
        sql = """
            SELECT 1
            FROM alergias
            WHERE paciente_id = ?
              AND descricao = ? COLLATE NOCASE
            LIMIT 1
        """

        with conectar() as conexao:
            linha = conexao.execute(sql, (paciente_id, descricao)).fetchone()

        return linha is not None
