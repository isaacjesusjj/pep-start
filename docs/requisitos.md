# Requisitos — PEP Start

## Requisitos funcionais

**RF01 — Cadastrar paciente.** O sistema deve cadastrar nome, data de nascimento e telefone opcional, gerando o ID automaticamente.

**RF02 — Listar pacientes.** O sistema deve exibir os pacientes cadastrados em ordem alfabética.

**RF03 — Buscar paciente por ID.** O sistema deve localizar um paciente pelo seu identificador único.

**RF04 — Buscar paciente por nome.** O sistema deve aceitar nome completo ou parte do nome.

**RF05 — Atualizar paciente.** O sistema deve permitir alterar nome, data de nascimento e telefone, preservando o ID.

**RF06 — Registrar alergia.** O sistema deve vincular uma alergia fictícia a um paciente existente.

**RF07 — Listar alergias.** O sistema deve apresentar as alergias associadas ao paciente.

**RF08 — Registrar atendimento.** O sistema deve registrar data, motivo e observação opcional para paciente existente.

**RF09 — Consultar histórico.** O sistema deve exibir os atendimentos do mais recente para o mais antigo.

**RF10 — Exibir prontuário resumido.** O sistema deve reunir dados cadastrais, alergias e atendimentos.

**RF11 — Excluir paciente.** O sistema deve excluir paciente apenas quando não houver registros clínicos associados.

## Requisitos não funcionais

**RNF01 — Python.** A aplicação deve ser implementada em Python.

**RNF02 — SQLite.** A persistência deve utilizar banco SQLite local.

**RNF03 — Execução local.** O núcleo do sistema deve funcionar sem internet ou servidor web.

**RNF04 — Clareza.** Nomes de arquivos, classes, métodos e variáveis devem ser compreensíveis para estudo.

**RNF05 — Validação.** Entradas essenciais devem ser validadas antes da persistência.

**RNF06 — Dados fictícios.** O projeto não deve utilizar dados clínicos reais.

**RNF07 — Integridade.** Relacionamentos entre pacientes, alergias e atendimentos devem ser protegidos por chaves estrangeiras.

**RNF08 — Reprodutibilidade.** O repositório deve possuir instruções de execução e testes automatizados.
