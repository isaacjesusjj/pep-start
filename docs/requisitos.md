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

## Evolução web — requisitos adicionais

**RF12 — Autenticar usuário.** O sistema deve permitir login por e-mail e senha armazenada por hash.

**RF13 — Controlar perfis.** O sistema deve diferenciar `ADMIN`, `RECEPCAO` e `PROFISSIONAL`.

**RF14 — Restringir prontuário.** O perfil Recepção não deve visualizar conteúdo clínico.

**RF15 — Gerenciar usuários.** Administradores devem criar e ativar/desativar usuários.

**RF16 — Registrar auditoria.** Ações relevantes devem gerar trilha de auditoria.

**RF17 — Registrar exames fictícios.** Profissional/Admin podem vincular exames a um paciente.

**RF18 — Registrar prescrições fictícias.** Profissional/Admin podem vincular prescrições a um paciente.

**RF19 — Paginar pacientes.** A interface web deve limitar a quantidade de pacientes exibidos por página.

**RF20 — Disponibilizar API REST.** O sistema deve expor endpoints de pacientes e prontuário respeitando autorização.

**RF21 — Suportar PostgreSQL.** A versão web deve aceitar configuração de banco PostgreSQL por URL.

**RNF09 — Segurança de senha.** Senhas devem ser armazenadas por função de derivação segura com salt.

**RNF10 — Proteção CSRF.** Operações de escrita web devem exigir token de sessão.

**RNF11 — Não cachear conteúdo clínico.** Respostas clínicas devem usar `Cache-Control: no-store`.

**RNF12 — Auditoria sem duplicação clínica.** Logs não devem copiar conteúdo clínico desnecessário.
