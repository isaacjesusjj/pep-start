# Documentação acadêmica — PEP Start

## 1. Introdução

O Prontuário Eletrônico do Paciente é um exemplo relevante de aplicação de sistemas de informação na saúde. O PEP Start foi criado como uma simulação acadêmica reduzida para estudar desenvolvimento de software sem utilizar dados reais ou tentar reproduzir toda a complexidade de um sistema hospitalar.

## 2. Contextualização

Sistemas de saúde precisam relacionar informações de uma pessoa ao longo do tempo. Mesmo em uma demonstração simples, dados cadastrais, alergias e atendimentos não devem existir de forma desconectada.

## 3. Problema

O problema abordado é a organização estruturada de informações básicas de pacientes e registros clínicos fictícios, permitindo consulta posterior do histórico.

## 4. Justificativa

O domínio de prontuário permite aplicar conhecimentos de ADS a um contexto realista: modelagem de dados, regras de negócio, CRUD, integridade, privacidade e testes.

## 5. Objetivo geral

Desenvolver uma aplicação em Python capaz de organizar informações fictícias de pacientes e seu histórico básico utilizando banco de dados relacional SQLite.

## 6. Objetivos específicos

- cadastrar, consultar e atualizar pacientes;
- relacionar alergias e atendimentos;
- impedir registros órfãos;
- consultar um prontuário resumido;
- praticar SQL e POO introdutória;
- automatizar testes de regras importantes;
- documentar arquitetura e execução.

## 7. Público-alvo

O software representa, apenas para fins acadêmicos, uma aplicação local utilizada por um usuário autorizado de uma pequena clínica ou ambulatório. Não há perfis reais ou autenticação nesta versão.

## 8. Requisitos

Os requisitos completos estão em `requisitos.md`. Os principais são cadastro e pesquisa de pacientes, registro de alergias e atendimentos, consulta do prontuário e proteção da exclusão quando existe histórico.

## 9. Regras de negócio

As regras completas estão em `regras_negocio.md`. Destacam-se a obrigatoriedade de paciente existente, datas válidas, proteção de relacionamentos e uso exclusivo de dados fictícios.

## 10. Tecnologias utilizadas

Python foi usado para aplicação e lógica de negócio. SQLite foi usado como banco relacional local. A biblioteca padrão `sqlite3` realiza a comunicação com o banco. pytest automatiza os testes e GitHub Actions permite repeti-los a cada alteração publicada.

## 11. Arquitetura

A aplicação é dividida em Models, Services, Repositories e Database. `main.py` realiza a interação. Essa divisão reduz mistura de responsabilidades sem criar uma arquitetura empresarial desnecessária.

## 12. Modelagem

Existem três entidades principais: Paciente, Alergia e Atendimento. Paciente possui relacionamento de um para muitos com Alergia e de um para muitos com Atendimento.

## 13. Banco de dados

As três tabelas são criadas por `database/schema.sql`. As chaves estrangeiras protegem a integridade. As datas são armazenadas no formato ISO `AAAA-MM-DD`.

## 14. Desenvolvimento

O desenvolvimento foi dividido em análise do problema, requisitos, regras de negócio, casos de uso, UML, modelagem do banco, estrutura de pastas, implementação, testes e documentação. Essa sequência permite compreender o motivo de cada arquivo antes de programar.

## 15. Segurança e LGPD

O projeto não utiliza dados reais. As consultas SQL são parametrizadas e o banco local não é versionado. Chaves estrangeiras impedem registros inconsistentes. Entretanto, um PEP real exigiria autenticação, autorização, auditoria, criptografia e processos institucionais. Portanto, o projeto não deve ser apresentado como sistema clinicamente pronto ou como solução completa de conformidade com a LGPD.

## 16. Testes

A suíte automatizada cria banco temporário para cada teste e verifica operações de pacientes, regras de datas, alergias, atendimentos, histórico, exclusão e integridade do banco.

## 17. Resultados

A versão atual fornece um núcleo funcional de PEP educacional executável no terminal. O sistema persiste dados no SQLite, aplica as regras propostas e possui testes automatizados reproduzíveis.

## 18. Limitações

Não há autenticação, interface gráfica, integração externa, prescrições, exames ou infraestrutura para múltiplos usuários. SQLite e terminal foram escolhas conscientes para manter o projeto adequado ao nível introdutório/intermediário.

## 19. Melhorias futuras

As próximas evoluções podem incluir autenticação, auditoria, interface web, diferentes perfis, API e banco de dados servidor. Essas funcionalidades devem ser introduzidas em projetos posteriores para preservar a progressão pedagógica.

## 20. Conclusão

O PEP Start demonstra como fundamentos de programação e banco de dados podem ser aplicados a TI em saúde. Mais importante que a quantidade de funcionalidades é a capacidade de compreender o fluxo completo entre entrada do usuário, regras de negócio, objetos, SQL e persistência, além de conseguir testar e explicar essas decisões.

---

# Evolução 2 — aplicação web e segurança

Após a versão inicial de terminal, o PEP Start foi evoluído para demonstrar novos conceitos de ADS sem remover a implementação original. A nova etapa adicionou FastAPI, SQLAlchemy ORM, interface HTML, autenticação, autorização por perfil, trilha de auditoria, exames e prescrições fictícias, paginação, API REST e opção de PostgreSQL.

## Justificativa da evolução

A versão 1 é adequada para aprender CRUD, SQL e organização de código. A versão 2 introduz problemas que surgem quando mais de uma pessoa utiliza um sistema: identificação do usuário, definição do que cada perfil pode consultar, rastreabilidade de acessos e comunicação por HTTP.

## Segurança e LGPD — relação prática

O projeto não afirma conformidade legal ou regulatória. Entretanto, aplica conceitos relevantes para estudo: menor privilégio, hash de senha, sessão, proteção CSRF, auditoria e minimização do conteúdo armazenado em logs. O uso continua restrito a dados fictícios.

## Banco mais avançado

SQLite permanece como opção local. PostgreSQL foi incluído como caminho de evolução por meio da configuração `DATABASE_URL` e de um script de migração que copia dados existentes para um banco SQLAlchemy vazio.

## API

A API REST permite explorar integração entre sistemas. Nesta etapa ela reutiliza a sessão da interface web; autenticação por tokens e OAuth2 ficam documentadas como evolução posterior adequada para integrações externas.
