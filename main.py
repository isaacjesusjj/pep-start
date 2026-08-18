from datetime import datetime

from database.conexao import inicializar_banco
from repositories.alergia_repository import AlergiaRepository
from repositories.atendimento_repository import AtendimentoRepository
from repositories.paciente_repository import PacienteRepository
from services.paciente_service import PacienteService
from services.prontuario_service import ProntuarioService


paciente_repository = PacienteRepository()
alergia_repository = AlergiaRepository()
atendimento_repository = AtendimentoRepository()

paciente_service = PacienteService(
    paciente_repository,
    alergia_repository,
    atendimento_repository,
)
prontuario_service = ProntuarioService(
    paciente_repository,
    alergia_repository,
    atendimento_repository,
)


def formatar_data(data_iso):
    """Converte AAAA-MM-DD para DD/MM/AAAA para exibição."""

    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return data_iso


def solicitar_id():
    """Solicita e valida um identificador numérico positivo."""

    valor = input("Informe o ID do paciente: ").strip()
    if not valor.isdigit():
        raise ValueError("O ID deve ser um número inteiro.")

    paciente_id = int(valor)
    if paciente_id <= 0:
        raise ValueError("O ID deve ser maior que zero.")

    return paciente_id


def mostrar_paciente(paciente):
    telefone = paciente.telefone or "Não informado"
    print("\n------------------------------")
    print(f"ID: {paciente.id}")
    print(f"Nome: {paciente.nome}")
    print(f"Nascimento: {formatar_data(paciente.data_nascimento)}")
    print(f"Telefone: {telefone}")
    print("------------------------------")


def cadastrar_paciente():
    print("\n=== CADASTRAR PACIENTE ===")
    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (AAAA-MM-DD): ")
    telefone = input("Telefone (opcional): ")

    paciente = paciente_service.cadastrar_paciente(nome, nascimento, telefone)
    print("\nPaciente cadastrado com sucesso.")
    print(f"ID criado: {paciente.id}")


def listar_pacientes():
    print("\n=== PACIENTES ===")
    pacientes = paciente_service.listar_pacientes()

    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return

    for paciente in pacientes:
        mostrar_paciente(paciente)


def buscar_paciente():
    print("\n=== BUSCAR PACIENTE ===")
    print("1 - Buscar por ID")
    print("2 - Buscar por nome")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        paciente = paciente_service.buscar_por_id(solicitar_id())
        if paciente is None:
            print("\nPaciente não encontrado.")
            return
        mostrar_paciente(paciente)
    elif opcao == "2":
        pacientes = paciente_service.buscar_por_nome(
            input("Digite o nome ou parte dele: ")
        )
        if not pacientes:
            print("\nNenhum paciente encontrado.")
            return
        for paciente in pacientes:
            mostrar_paciente(paciente)
    else:
        print("\nOpção inválida.")


def atualizar_paciente():
    print("\n=== ATUALIZAR PACIENTE ===")
    paciente_id = solicitar_id()
    paciente = paciente_service.buscar_por_id(paciente_id)

    if paciente is None:
        print("\nPaciente não encontrado.")
        return

    mostrar_paciente(paciente)
    print("\nDeixe vazio para manter o valor atual.")

    nome = input(f"Nome [{paciente.nome}]: ").strip() or paciente.nome
    nascimento = (
        input(f"Nascimento [{paciente.data_nascimento}]: ").strip()
        or paciente.data_nascimento
    )
    telefone_atual = paciente.telefone or ""
    telefone = input(f"Telefone [{telefone_atual}]: ").strip() or telefone_atual

    atualizado = paciente_service.atualizar_paciente(
        paciente_id,
        nome,
        nascimento,
        telefone,
    )
    print("\nPaciente atualizado com sucesso.")
    mostrar_paciente(atualizado)


def registrar_alergia():
    print("\n=== REGISTRAR ALERGIA ===")
    paciente_id = solicitar_id()
    descricao = input("Descrição da alergia: ")
    alergia = prontuario_service.registrar_alergia(paciente_id, descricao)
    print("\nAlergia registrada com sucesso.")
    print(f"ID do registro: {alergia.id}")


def registrar_atendimento():
    print("\n=== REGISTRAR ATENDIMENTO ===")
    paciente_id = solicitar_id()
    data_atendimento = input("Data do atendimento (AAAA-MM-DD): ")
    motivo = input("Motivo do atendimento: ")
    observacao = input("Observação clínica fictícia (opcional): ")

    atendimento = prontuario_service.registrar_atendimento(
        paciente_id,
        data_atendimento,
        motivo,
        observacao,
    )
    print("\nAtendimento registrado com sucesso.")
    print(f"ID do atendimento: {atendimento.id}")


def consultar_prontuario():
    print("\n=== CONSULTAR PRONTUÁRIO ===")
    prontuario = prontuario_service.consultar_prontuario(solicitar_id())
    paciente = prontuario["paciente"]
    alergias = prontuario["alergias"]
    atendimentos = prontuario["atendimentos"]

    print("\n================================")
    print("          PRONTUÁRIO")
    print("================================")
    print(f"\nID: {paciente.id}")
    print(f"Paciente: {paciente.nome}")
    print(f"Nascimento: {formatar_data(paciente.data_nascimento)}")
    print(f"Telefone: {paciente.telefone or 'Não informado'}")

    print("\n--------------------------------")
    print("ALERGIAS")
    print("--------------------------------")
    if not alergias:
        print("Nenhuma alergia registrada.")
    else:
        for alergia in alergias:
            print(f"- {alergia.descricao}")

    print("\n--------------------------------")
    print("HISTÓRICO DE ATENDIMENTOS")
    print("--------------------------------")
    if not atendimentos:
        print("Nenhum atendimento registrado.")
    else:
        for atendimento in atendimentos:
            print(f"\nData: {formatar_data(atendimento.data)}")
            print(f"Motivo: {atendimento.motivo}")
            if atendimento.observacao:
                print(f"Observação: {atendimento.observacao}")


def excluir_paciente():
    print("\n=== EXCLUIR PACIENTE ===")
    paciente_id = solicitar_id()
    paciente = paciente_service.buscar_por_id(paciente_id)

    if paciente is None:
        print("\nPaciente não encontrado.")
        return

    mostrar_paciente(paciente)
    confirmacao = input("\nDigite SIM para confirmar a exclusão: ").strip().upper()
    if confirmacao != "SIM":
        print("\nExclusão cancelada.")
        return

    paciente_service.excluir_paciente(paciente_id)
    print("\nPaciente excluído com sucesso.")


def mostrar_menu():
    print("\n================================")
    print("           PEP START")
    print("================================")
    print("1 - Cadastrar paciente")
    print("2 - Listar pacientes")
    print("3 - Buscar paciente")
    print("4 - Atualizar paciente")
    print("5 - Registrar alergia")
    print("6 - Registrar atendimento")
    print("7 - Consultar prontuário")
    print("8 - Excluir paciente")
    print("0 - Sair")


def executar():
    """Inicializa o banco e mantém o menu ativo até a opção de saída."""

    inicializar_banco()

    while True:
        mostrar_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_paciente()
            elif opcao == "2":
                listar_pacientes()
            elif opcao == "3":
                buscar_paciente()
            elif opcao == "4":
                atualizar_paciente()
            elif opcao == "5":
                registrar_alergia()
            elif opcao == "6":
                registrar_atendimento()
            elif opcao == "7":
                consultar_prontuario()
            elif opcao == "8":
                excluir_paciente()
            elif opcao == "0":
                print("\nPEP Start encerrado.")
                break
            else:
                print("\nOpção inválida.")
        except ValueError as erro:
            print(f"\nErro: {erro}")
        except Exception as erro:
            print("\nOcorreu um erro inesperado.")
            print(f"Detalhes técnicos: {erro}")


if __name__ == "__main__":
    executar()
