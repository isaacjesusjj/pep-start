# Roteiro de apresentação — PEP Start

## 1. Problema

Informações de pacientes e atendimentos precisam estar organizadas e relacionadas para que o histórico seja consultado de forma consistente.

## 2. Solução

O PEP Start é uma aplicação acadêmica de terminal que cadastra pacientes e relaciona alergias e atendimentos fictícios utilizando Python e SQLite.

## 3. Como funciona

Mostrar o menu, cadastrar um paciente fictício, registrar uma alergia, registrar um atendimento e consultar o prontuário.

## 4. Tecnologias

Python para lógica e objetos, SQLite para persistência, SQL para CRUD, pytest para testes e GitHub Actions para automação.

## 5. Demonstração sugerida

1. executar `python main.py`;
2. cadastrar paciente;
3. listar paciente;
4. registrar alergia;
5. registrar atendimento;
6. consultar prontuário;
7. tentar excluir o paciente e mostrar o bloqueio.

## 6. Banco de dados

Explicar as tabelas `pacientes`, `alergias` e `atendimentos`, a chave primária `id` e a chave estrangeira `paciente_id`.

## 7. Segurança

Explicar consultas parametrizadas, integridade referencial, dados fictícios e por que autenticação ainda é uma limitação desta versão.

## 8. O que aprendi

CRUD, relacionamentos, classes, repositories, services, validações, exceções, testes e organização de repositório.

## 9. Melhorias futuras

Interface web, autenticação, auditoria, perfis de acesso, exames e migração para um banco servidor em projeto mais avançado.

## Complemento para apresentar a versão web

1. Mostre a versão terminal e explique que ela foi a base para aprender CRUD e SQL.
2. Abra a versão web e faça login.
3. Compare os três perfis e demonstre que Recepção não consegue abrir conteúdo clínico.
4. Registre um exame ou prescrição fictícia com perfil Profissional.
5. Entre como Administrador e mostre o evento na auditoria.
6. Mostre a paginação da lista de pacientes.
7. Abra `/api/docs` e explique o conceito de endpoint.
8. Mostre `DATABASE_URL` e o script de migração para explicar a evolução SQLite → PostgreSQL.
