# Testes automatizados

## Ferramenta

O projeto usa `pytest` por possuir sintaxe simples e permitir testes pequenos e legíveis.

## Isolamento

Cada teste recebe um banco SQLite temporário criado pelo fixture `servicos` em `tests/conftest.py`. O banco real `pep_start.db` não é usado pelos testes.

A variável `PEP_START_DB_PATH` permite que a camada de conexão utilize o arquivo temporário.

## Casos cobertos

1. cadastro e busca por ID;
2. normalização de nome e telefone;
3. busca por parte do nome;
4. atualização de paciente;
5. exclusão de paciente sem histórico;
6. rejeição de nome curto;
7. rejeição de nascimento futuro;
8. rejeição de telefone inválido;
9. cadastro de alergia;
10. bloqueio de alergia duplicada;
11. registro e consulta de atendimento;
12. ordenação do histórico;
13. bloqueio de atendimento futuro;
14. bloqueio de atendimento anterior ao nascimento;
15. paciente inexistente;
16. bloqueio de exclusão pelo Service;
17. criação das tabelas;
18. bloqueio de exclusão direta pela FOREIGN KEY;
19. isolamento do banco de teste.

Alguns testes verificam mais de um comportamento, por isso a suíte possui menos funções de teste que a quantidade de verificações acima.

## Como executar

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

## Automação

O arquivo `.github/workflows/tests.yml` executa os testes automaticamente no GitHub Actions a cada push em `main` e em pull requests.

## Resultado validado antes da publicação

A versão preparada para o repositório foi validada localmente com compilação dos arquivos Python e execução integral da suíte de testes.
