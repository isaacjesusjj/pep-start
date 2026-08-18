# Migração de SQLite para PostgreSQL

## Por que migrar?

SQLite é excelente para aprendizagem e execução local. PostgreSQL é mais apropriado quando o projeto precisa de servidor de banco, múltiplas conexões concorrentes, administração centralizada e recursos mais avançados.

## Suporte da aplicação web

A versão web usa SQLAlchemy e aceita a variável `DATABASE_URL`.

Exemplo:

```text
postgresql+psycopg://usuario:senha@localhost:5432/pep_start
```

O driver utilizado é `psycopg` 3.

## Migração dos dados existentes

1. faça backup do `pep_start.db`;
2. crie um banco PostgreSQL vazio;
3. instale `requirements.txt`;
4. execute:

```bash
python scripts/migrar_sqlite.py pep_start.db "postgresql+psycopg://usuario:senha@localhost:5432/pep_start"
```

O script:

- cria o schema do destino;
- copia as tabelas conhecidas na ordem das chaves estrangeiras;
- interrompe se encontrar dados já existentes no destino;
- ajusta sequências de IDs no PostgreSQL.

## Como testamos sem servidor PostgreSQL

A lógica de cópia é testada migrando um SQLite de origem para outro banco SQLite gerenciado pela mesma camada SQLAlchemy. Isso valida preservação de dados e fluxo do migrador.

A conexão real com PostgreSQL depende de um servidor externo e, por isso, deve ser validada no ambiente onde o PostgreSQL estiver disponível.
