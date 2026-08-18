# PEP Start — Prontuário Eletrônico Educacional

Projeto acadêmico em Python para estudar a evolução de um **Prontuário Eletrônico do Paciente (PEP)**: começa com uma aplicação de terminal e avança para uma aplicação web com autenticação, perfis, auditoria, API REST e suporte de evolução para PostgreSQL.

> **Uso exclusivamente educacional.** Todos os dados clínicos devem ser fictícios. O projeto não foi projetado, validado ou certificado para atendimento clínico real.

## Evolução do projeto

O repositório preserva duas etapas de aprendizado:

- **Versão 1 — Terminal:** Python + `sqlite3` + Services + Repositories.
- **Versão 2 — Web:** FastAPI + SQLAlchemy + templates HTML + sessões + perfis + auditoria + API REST.

A versão web usa o mesmo banco SQLite por padrão, então pacientes já cadastrados pela versão de terminal continuam disponíveis.

## Funcionalidades

### Pacientes

- cadastrar, listar, buscar e atualizar pacientes;
- paginação de 10 pacientes por página na interface web;
- busca por nome ou telefone;
- preservação de integridade dos registros clínicos.

### Prontuário fictício

- alergias;
- atendimentos;
- exames fictícios;
- prescrições fictícias;
- ordenação cronológica do histórico;
- validação de datas em relação ao nascimento do paciente e ao dia atual.

### Autenticação e perfis

Existem três perfis:

| Perfil | Principais permissões |
|---|---|
| `RECEPCAO` | cadastrar, localizar e atualizar dados administrativos de pacientes |
| `PROFISSIONAL` | consultar prontuário e registrar alergias, atendimentos, exames e prescrições fictícias |
| `ADMIN` | acesso completo, gerenciamento de usuários e consulta da auditoria |

A Recepção **não visualiza conteúdo clínico**. Um Profissional **não administra usuários nem auditoria**.

### Auditoria

O sistema registra eventos como:

- login bem-sucedido ou falho;
- visualização de paciente/prontuário;
- criação e atualização de paciente;
- registro de exame, prescrição, alergia e atendimento;
- uso da API;
- criação e ativação/desativação de usuários.

A auditoria guarda metadados da ação, usuário, recurso, horário e IP. Ela evita copiar conteúdo de exames, prescrições e observações clínicas para o log.

### API REST

A versão 2 possui API inicial em:

```text
/api/v1
```

Principais endpoints:

```text
GET  /api/v1/csrf
GET  /api/v1/pacientes
GET  /api/v1/pacientes/{id}
GET  /api/v1/pacientes/{id}/prontuario
POST /api/v1/pacientes
```

A documentação OpenAPI interativa fica em:

```text
http://127.0.0.1:8000/api/docs
```

A API respeita os mesmos perfis da interface web.

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| SQLite | Banco padrão para estudo local |
| FastAPI | Interface web e API REST |
| Uvicorn | Servidor ASGI local |
| SQLAlchemy 2 | ORM/camada de persistência da versão web |
| Jinja2 | Templates HTML |
| SessionMiddleware | Sessões autenticadas |
| PBKDF2-SHA256 | Hash de senhas |
| PostgreSQL | Banco opcional para evolução avançada |
| psycopg 3 | Driver PostgreSQL |
| pytest | Testes automatizados |
| GitHub Actions | Integração contínua |
| Mermaid | Diagramas |

### O que é FastAPI?

FastAPI é um framework Python para aplicações web e APIs. Neste projeto ele recebe requisições HTTP, escolhe a rota correta e devolve HTML ou JSON.

### O que é ORM?

ORM significa **Object-Relational Mapping**. O SQLAlchemy permite representar tabelas como classes Python. Ele não elimina o banco relacional: por trás, continua gerando e executando SQL. A versão 1 permanece no repositório justamente para permitir comparar SQL direto com ORM.

## Arquitetura

### Versão 1

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

### Versão 2

```text
Navegador / Cliente API
          ↓
        FastAPI
          ↓
 Autenticação + Perfis
          ↓
 Rotas HTML / API REST
          ↓
      SQLAlchemy ORM
          ↓
 SQLite ou PostgreSQL
          ↓
        Auditoria
```

## Estrutura principal

```text
pep-start/
├── .github/workflows/tests.yml
├── database/
│   ├── conexao.py
│   └── schema.sql
├── docs/
├── models/                  # versão terminal
├── repositories/            # versão terminal
├── services/                # versão terminal
├── shared/                  # validações compartilhadas
├── scripts/
│   └── migrar_sqlite.py
├── web_app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── pacientes.py
│   │   ├── admin.py
│   │   └── api.py
│   ├── templates/
│   ├── static/
│   ├── audit.py
│   ├── database.py
│   ├── models.py
│   └── security.py
├── tests/
├── main.py                  # terminal
├── web.py                   # aplicação web
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Como executar a versão web

### 1. Clonar

```bash
git clone https://github.com/isaacjesusjj/pep-start.git
cd pep-start
```

### 2. Criar ambiente virtual (recomendado)

Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar chave de sessão

Para desenvolvimento local o sistema possui uma chave padrão didática. Para qualquer ambiente compartilhado, configure uma chave própria.

Windows PowerShell:

```powershell
$env:PEP_START_SECRET_KEY="troque-por-uma-chave-longa-e-aleatoria"
```

Linux/macOS:

```bash
export PEP_START_SECRET_KEY="troque-por-uma-chave-longa-e-aleatoria"
```

### 5. Iniciar

```bash
python web.py
```

Acesse:

```text
http://127.0.0.1:8000
```

Na primeira execução, você será direcionado para `/setup`, onde cria o primeiro usuário `ADMIN`. Depois que existe um usuário, essa configuração inicial não pode mais criar outro administrador.

## Executar a versão de terminal

```bash
python main.py
```

A versão de terminal continua disponível como registro da primeira etapa do aprendizado.

## Testes automatizados

Instale as dependências de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Execute:

```bash
python -m pytest
```

Estado atual da suíte:

```text
28 testes aprovados
```

Os testes cobrem:

- CRUD e validações da versão 1;
- integridade por chave estrangeira;
- hash e verificação de senha;
- cabeçalhos de segurança;
- perfis de acesso;
- bloqueio de conteúdo clínico para Recepção;
- criação de exame e prescrição por Profissional;
- auditoria de visualização;
- paginação;
- API REST e autorização;
- migração SQLite para outro banco SQLAlchemy;
- execução direta do script de migração.

## PostgreSQL

A aplicação web pode utilizar PostgreSQL definindo `DATABASE_URL`.

Exemplo:

```text
postgresql+psycopg://usuario:senha@localhost:5432/pep_start
```

Windows PowerShell:

```powershell
$env:DATABASE_URL="postgresql+psycopg://usuario:senha@localhost:5432/pep_start"
python web.py
```

### Migrar dados do SQLite

Primeiro faça backup de `pep_start.db` e use um banco PostgreSQL de destino **vazio**.

```bash
python scripts/migrar_sqlite.py pep_start.db "postgresql+psycopg://usuario:senha@localhost:5432/pep_start"
```

O mesmo mecanismo de migração é testado automaticamente usando SQLite como banco de destino. Um servidor PostgreSQL real não faz parte da suíte local do projeto.

Veja [`docs/migracao_postgresql.md`](docs/migracao_postgresql.md).

## Segurança e privacidade

Medidas implementadas para aprendizado:

- senhas armazenadas com PBKDF2-SHA256 e salt aleatório;
- sessões assinadas;
- token CSRF em formulários e escrita via API;
- autorização por perfil;
- auditoria de acessos;
- SQL parametrizado/ORM;
- `FOREIGN KEY` e `ON DELETE RESTRICT`;
- cabeçalhos `X-Content-Type-Options`, `X-Frame-Options` e `Referrer-Policy`;
- `Cache-Control: no-store` em páginas clínicas e API;
- opção de cookie `Secure` via `PEP_START_HTTPS_ONLY=1`;
- conteúdo clínico não copiado para detalhes da auditoria;
- banco local ignorado pelo Git;
- dados de demonstração exclusivamente fictícios.

Isso **não torna o sistema adequado para uso real em saúde**. Um produto real exigiria análise de riscos, infraestrutura protegida, criptografia adequada, gestão institucional de identidade, backups, disponibilidade, monitoramento, políticas de retenção, revisão jurídica/LGPD e requisitos regulatórios aplicáveis.

## Limitações atuais

- projeto acadêmico, não software médico;
- sessão web baseada em cookie, não OAuth2/OIDC;
- API usa a sessão web existente e não possui tokens próprios para integrações externas;
- não há recuperação de senha;
- não há MFA;
- não há bloqueio progressivo de tentativas de login;
- auditoria não é criptograficamente imutável;
- migração PostgreSQL não é testada contra servidor PostgreSQL real no CI;
- não há upload de documentos ou integração com sistemas de saúde externos.

## Documentação

A pasta [`docs/`](docs/) inclui:

- requisitos;
- regras de negócio;
- arquitetura;
- UML;
- modelagem do banco;
- perfis e permissões;
- auditoria;
- segurança web;
- API REST;
- migração para PostgreSQL;
- testes;
- documentação acadêmica;
- roteiro de apresentação;
- perguntas e respostas.

## Autor

**Isaac de Jesus**

Projeto desenvolvido para estudo e portfólio acadêmico em Análise e Desenvolvimento de Sistemas, com foco em TI aplicada à saúde.
