# Perguntas que um professor ou entrevistador pode fazer

## 1. Por que Python?

Porque o primeiro projeto tem foco em fundamentos. Python permite praticar lógica, funções, classes e banco de dados com menos código incidental.

## 2. Por que SQLite?

Porque é relacional, suporta SQL e chaves estrangeiras, mas não exige instalar e administrar um servidor. É suficiente para o escopo acadêmico local.

## 3. O que é uma chave primária?

É um campo que identifica de forma única cada registro. No projeto, `pacientes.id` identifica cada paciente.

## 4. O que é uma chave estrangeira?

É um campo que referencia uma chave de outra tabela. `alergias.paciente_id` e `atendimentos.paciente_id` apontam para `pacientes.id`.

## 5. Por que separar Service e Repository?

Repository sabe como acessar o banco. Service sabe quais regras devem ser cumpridas. Essa separação evita misturar SQL com decisões de negócio.

## 6. O que é CRUD?

Create, Read, Update e Delete. O projeto implementa cadastro, consultas, atualização e exclusão de pacientes.

## 7. Como o projeto evita SQL injection?

Usa consultas parametrizadas com `?`, em vez de concatenar diretamente as entradas do usuário no SQL.

## 8. Por que não posso excluir um paciente com atendimento?

Para evitar apagar a referência principal de registros clínicos. A regra existe tanto no Service quanto no banco com `ON DELETE RESTRICT`.

## 9. Por que as datas são guardadas como `AAAA-MM-DD`?

Porque esse formato é fácil de validar e ordenar cronologicamente como texto no SQLite.

## 10. Como os testes não alteram o banco real?

Cada teste cria um banco temporário e define `PEP_START_DB_PATH`, deixando `pep_start.db` fora da execução da suíte.

## 11. O que é `commit` e `rollback`?

`commit` confirma alterações no banco. `rollback` desfaz a transação quando ocorre uma exceção, reduzindo o risco de uma operação ficar parcialmente aplicada.

## 12. Esse projeto atende à LGPD?

Não se deve afirmar que um projeto educacional simples esteja pronto para conformidade real. Ele usa dados fictícios e algumas boas práticas, mas um sistema real exigiria controles técnicos, organizacionais e jurídicos muito mais amplos.

## 13. Por que não usou Flask ou Django?

Porque o objetivo do primeiro projeto é entender Python, SQL, CRUD e separação de responsabilidades sem esconder o funcionamento atrás de um framework.

## 14. Como o projeto poderia crescer?

Uma evolução poderia introduzir autenticação, API, interface web, banco servidor, auditoria e perfis de acesso. Isso deve ocorrer gradualmente.

## 15. Qual foi uma decisão importante de arquitetura?

Manter as entidades simples e retirar delas o SQL. A persistência fica nos repositories e as regras ficam nos services, tornando cada parte mais fácil de testar e explicar.
