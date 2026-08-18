from database.conexao import conectar
from models.atendimento import Atendimento


class AtendimentoRepository:
    """Executa as operações de persistência da tabela atendimentos."""

    @staticmethod
    def _linha_para_atendimento(linha):
        return Atendimento(
            paciente_id=linha["paciente_id"],
            data=linha["data"],
            motivo=linha["motivo"],
            observacao=linha["observacao"],
            atendimento_id=linha["id"],
        )

    def cadastrar(self, atendimento):
        sql = """
            INSERT INTO atendimentos (paciente_id, data, motivo, observacao)
            VALUES (?, ?, ?, ?)
        """

        with conectar() as conexao:
            cursor = conexao.execute(
                sql,
                (
                    atendimento.paciente_id,
                    atendimento.data,
                    atendimento.motivo,
                    atendimento.observacao,
                ),
            )
            atendimento.id = cursor.lastrowid

        return atendimento

    def listar_por_paciente(self, paciente_id):
        sql = """
            SELECT id, paciente_id, data, motivo, observacao
            FROM atendimentos
            WHERE paciente_id = ?
            ORDER BY data DESC, id DESC
        """

        with conectar() as conexao:
            linhas = conexao.execute(sql, (paciente_id,)).fetchall()

        return [self._linha_para_atendimento(linha) for linha in linhas]

    def existe_para_paciente(self, paciente_id):
        with conectar() as conexao:
            linha = conexao.execute(
                "SELECT 1 FROM atendimentos WHERE paciente_id = ? LIMIT 1",
                (paciente_id,),
            ).fetchone()

        return linha is not None
