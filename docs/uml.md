# UML — PEP Start

## Casos de uso

```mermaid
flowchart LR
    U[Usuário autorizado]
    U --> A[Cadastrar paciente]
    U --> B[Listar pacientes]
    U --> C[Buscar paciente]
    U --> D[Atualizar paciente]
    U --> E[Registrar alergia]
    U --> F[Registrar atendimento]
    U --> G[Consultar prontuário]
    U --> H[Excluir paciente]
```

O ator representa quem opera a aplicação acadêmica. Nesta versão não há autenticação nem perfis distintos.

## Diagrama de classes simplificado

```mermaid
classDiagram
    class Paciente {
        +int id
        +str nome
        +str data_nascimento
        +str telefone
    }

    class Alergia {
        +int id
        +int paciente_id
        +str descricao
    }

    class Atendimento {
        +int id
        +int paciente_id
        +str data
        +str motivo
        +str observacao
    }

    Paciente "1" --> "0..*" Alergia
    Paciente "1" --> "0..*" Atendimento
```

### Cardinalidades

`1` significa exatamente um. `0..*` significa zero ou muitos. Portanto, um paciente pode não possuir registros ainda ou pode possuir vários.

## Classes de infraestrutura

Além das entidades, a implementação usa repositories e services. Eles foram omitidos do diagrama acima para manter a leitura inicial simples, mas o fluxo arquitetural está documentado em `arquitetura.md`.

## UML da evolução web

```mermaid
classDiagram
    class Paciente {
        +int id
        +str nome
        +str data_nascimento
        +str telefone
    }
    class Alergia
    class Atendimento
    class Exame {
        +str nome
        +str data_exame
        +str status
        +str resultado
    }
    class Prescricao {
        +str medicamento
        +str dose
        +str frequencia
    }
    class Usuario {
        +str email
        +str senha_hash
        +str perfil
        +bool ativo
    }
    class Auditoria {
        +str acao
        +str recurso
        +str recurso_id
        +datetime criado_em
    }

    Paciente "1" --> "0..*" Alergia
    Paciente "1" --> "0..*" Atendimento
    Paciente "1" --> "0..*" Exame
    Paciente "1" --> "0..*" Prescricao
    Usuario "1" --> "0..*" Auditoria
```

Na versão web, as classes acima são modelos ORM do SQLAlchemy. Elas representam dados e relacionamentos; as regras de autorização ficam separadas em `security.py` e nas rotas.
