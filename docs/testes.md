# Testes automatizados

Execute:

```bash
python -m pytest
```

## Estado atual

```text
28 testes aprovados
```

## Versão terminal

A suíte valida:

- criação do banco;
- chaves estrangeiras;
- cadastro e busca;
- atualização e exclusão;
- validações de nome, telefone e datas;
- alergia sem duplicidade;
- atendimento e prontuário;
- ordem cronológica;
- bloqueio de atendimento futuro/anterior ao nascimento.

## Versão web

A suíte valida:

- hash de senha;
- cabeçalhos de segurança;
- criação de administrador inicial;
- login e sessão usados pelos fluxos;
- Recepção pode cadastrar paciente;
- Recepção não acessa conteúdo clínico;
- Profissional registra exame e prescrição;
- Profissional não cria paciente;
- visualização clínica gera auditoria;
- paginação de 10 itens;
- API respeita permissões;
- escrita da API usa CSRF;
- migração preserva dados;
- script de migração executa diretamente.

## Bancos de teste

Os testes usam arquivos SQLite temporários. Isso evita misturar dados de teste com `pep_start.db`.

## PostgreSQL

A lógica de migração é testada contra um segundo banco SQLAlchemy SQLite. A integração com um servidor PostgreSQL real depende de infraestrutura externa e não é declarada como testada no ambiente local.
