# PEP Start — Prontuário Eletrônico Educacional

Projeto acadêmico em Python para estudar os fundamentos de um **Prontuário Eletrônico do Paciente (PEP)** por meio de uma aplicação de terminal com SQLite.

> **Uso exclusivamente educacional.** O projeto utiliza apenas dados fictícios e não foi projetado, validado ou certificado para uso clínico real.

## Objetivo

O PEP Start foi criado para praticar, de forma progressiva e explicável:

- lógica de programação em Python;
- Programação Orientada a Objetos em nível introdutório;
- CRUD;
- SQL e SQLite;
- chaves primárias e estrangeiras;
- relacionamentos 1:N;
- separação entre Model, Service e Repository;
- validações e regras de negócio;
- testes automatizados com pytest;
- documentação e organização de repositório GitHub.

## Funcionalidades

- cadastrar pacientes;
- listar pacientes;
- buscar paciente por ID;
- buscar paciente por nome ou parte do nome;
- atualizar cadastro;
- excluir paciente sem registros clínicos associados;
- registrar alergias fictícias;
- impedir alergias duplicadas para o mesmo paciente;
- registrar atendimentos fictícios;
- consultar prontuário resumido;
- exibir histórico do atendimento mais recente para o mais antigo;
- impedir atendimento em data futura;
- impedir atendimento anterior ao nascimento do paciente;
- preservar relacionamentos com chaves estrangeiras.

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| SQLite | Banco de dados local |
| `sqlite3` | Comunicação entre Python e SQLite |
| pytest | Testes automatizados |
| GitHub Actions | Execução automática dos testes |
| Mermaid | Diagramas na documentação |

A aplicação principal usa apenas bibliotecas da própria instalação do Python. O `pytest` é necessário somente para executar os testes automatizados localmente.

## Arquitetura

```text
Usuário
  ↓
main.py
  ↓
Services
  ↓
Repositories
  ↓
SQLite
```

### Responsabilidades

- **Models:** representam Paciente, Alergia e Atendimento.
- **Services:** aplicam validações e regras de negócio.
- **Repositories:** executam SQL e convertem resultados do banco em objetos.
- **Database:** cria e gerencia conexões com o SQLite.
- **main.py:** apresenta o menu e recebe a interação do usuário.

Essa separação foi mantida propositalmente simples para que um estudante iniciante/intermediário consiga acompanhar o fluxo completo.

## Estrutura de pastas

```text
pep-start/
├── .github/
│   └── workflows/
│       └── tests.yml
├── database/
│   ├── __init__.py
│   ├── conexao.py
│   └── schema.sql
├── docs/
│   ├── arquitetura.md
│   ├── documentacao_academica.md
│   ├── modelagem_banco.md
│   ├── perguntas_e_respostas.md
│   ├── requisitos.md
│   ├── regras_negocio.md
│   ├── roteiro_apresentacao.md
│   ├── testes.md
│   └── uml.md
├── models/
│   ├── __init__.py
│   ├── alergia.py
│   ├── atendimento.py
│   └── paciente.py
├── repositories/
│   ├── __init__.py
│   ├── alergia_repository.py
│   ├── atendimento_repository.py
│   └── paciente_repository.py
├── services/
│   ├── __init__.py
│   ├── paciente_service.py
│   └── prontuario_service.py
├── tests/
│   ├── conftest.py
│   ├── test_banco.py
│   ├── test_pacientes.py
│   └── test_prontuario.py
├── .gitignore
├── executar.bat
├── executar.sh
├── main.py
├── pytest.ini
├── requirements-dev.txt
├── testar.bat
├── testar.sh
└── README.md
```

## Banco de dados

O sistema usa três tabelas principais:

```text
pacientes 1 ─────── N alergias
    │
    └────────────── N atendimentos
```

O arquivo `database/schema.sql` cria as tabelas automaticamente na primeira execução.

O banco local é salvo em:

```text
pep_start.db
```

Esse arquivo está no `.gitignore`, portanto os dados locais não devem ser enviados ao GitHub.

## Como executar do zero

### 1. Pré-requisito

Instale Python 3.10 ou superior e confirme:

```bash
python --version
```

No Windows, também pode funcionar:

```bash
py --version
```

### 2. Baixe o projeto

```bash
git clone https://github.com/isaacjesusjj/pep-start.git
cd pep-start
```

Também é possível baixar o ZIP do repositório e extrair a pasta.

### 3. Execute

Windows:

```bat
executar.bat
```

ou:

```bash
py main.py
```

Linux/macOS:

```bash
./executar.sh
```

ou:

```bash
python3 main.py
```

Na primeira execução, o banco e as tabelas são criados automaticamente.

## Exemplo de uso

```text
================================
           PEP START
================================
1 - Cadastrar paciente
2 - Listar pacientes
3 - Buscar paciente
4 - Atualizar paciente
5 - Registrar alergia
6 - Registrar atendimento
7 - Consultar prontuário
8 - Excluir paciente
0 - Sair
```

Exemplo fictício:

```text
Nome: Maria Oliveira
Nascimento: 1999-03-14
Telefone: 11999999999
```

Depois é possível registrar alergias e atendimentos fictícios e consultar tudo pela opção `7 - Consultar prontuário`.

## Testes automatizados

Instale a dependência de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Execute:

```bash
python -m pytest
```

ou:

```bash
pytest
```

No Windows também existe:

```bat
testar.bat
```

No Linux/macOS:

```bash
./testar.sh
```

A suíte cobre cadastro, busca, atualização, exclusão, validações, alergias, atendimentos, prontuário, ordenação do histórico e integridade por chave estrangeira.

## Testes automáticos no GitHub

O workflow `.github/workflows/tests.yml` executa automaticamente:

1. checkout do código;
2. Python 3.12;
3. instalação do pytest;
4. validação de sintaxe com `compileall`;
5. execução de todos os testes.

Ele roda em `push` para `main` e em pull requests.

## Segurança e privacidade

Este projeto não implementa autenticação porque o objetivo do Projeto 1 é trabalhar fundamentos de Python, CRUD e banco de dados. Autenticação e controle de acesso serão estudados em projetos posteriores.

Mesmo assim, algumas medidas são aplicadas:

- consultas SQL parametrizadas com `?`;
- `FOREIGN KEY` para manter relacionamentos válidos;
- `ON DELETE RESTRICT` para impedir exclusão direta de paciente com histórico;
- validações na camada Service;
- banco local ignorado pelo Git;
- dados de demonstração exclusivamente fictícios.

Em um PEP real, seriam necessárias medidas muito mais fortes, como autenticação, autorização por perfil, trilhas de auditoria, criptografia, gestão de sessões, registros de acesso e políticas institucionais adequadas à LGPD.

## Limitações

- aplicação somente em terminal;
- um único contexto de usuário, sem login;
- não possui interface web;
- não possui prescrições, exames ou agenda;
- SQLite é adequado ao projeto educacional, não a um cenário hospitalar de larga escala;
- não há integração com sistemas externos;
- não deve ser usado com dados reais.

## Melhorias futuras

- autenticação;
- diferentes perfis de acesso;
- auditoria de acessos;
- interface web;
- exames e prescrições fictícias;
- paginação de pacientes;
- exportação de relatórios;
- migração para PostgreSQL em projeto mais avançado;
- API REST em evolução posterior.

## Documentação acadêmica

A pasta [`docs/`](docs/) contém:

- requisitos funcionais e não funcionais;
- regras de negócio;
- arquitetura;
- modelagem do banco;
- UML;
- documentação acadêmica completa;
- estratégia e evidências de testes;
- roteiro para apresentação;
- perguntas e respostas para professor ou entrevista.

## Padrão de commits sugerido

```text
feat: adiciona cadastro e consulta de pacientes
feat: implementa alergias e atendimentos
feat: adiciona consulta de prontuario
fix: reforca validacoes de datas e relacionamentos
test: adiciona testes automatizados do sistema
docs: adiciona documentacao academica e README
ci: executa testes automaticamente no GitHub Actions
```

### Prefixos

- `feat`: nova funcionalidade;
- `fix`: correção;
- `test`: testes;
- `docs`: documentação;
- `ci`: integração contínua;
- `refactor`: reorganização sem alterar a funcionalidade;
- `chore`: manutenção geral.

## Autor

**Isaac de Jesus**

Projeto desenvolvido para estudo e portfólio acadêmico em Análise e Desenvolvimento de Sistemas, com foco em TI aplicada à saúde.

## Aviso

Este software é uma simulação acadêmica. Os exemplos e informações clínicas usados na documentação e nos testes são fictícios e não representam orientação médica ou um prontuário destinado a uso assistencial.
