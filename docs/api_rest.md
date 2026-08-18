# API REST — versão inicial

FastAPI gera automaticamente documentação OpenAPI em `/api/docs`.

## Conceitos

**API:** interface que permite que outro software interaja com o sistema.

**Endpoint:** uma combinação de caminho + método HTTP, como `GET /api/v1/pacientes`.

**REST:** estilo de API que organiza operações em recursos e utiliza métodos HTTP.

## Endpoints

### `GET /api/v1/csrf`

Retorna um token CSRF para operações de escrita dentro da sessão autenticada.

### `GET /api/v1/pacientes`

Lista pacientes com paginação.

Parâmetros:

- `page`;
- `per_page` (máximo 50);
- `q` para busca pelo nome.

### `GET /api/v1/pacientes/{id}`

Retorna dados administrativos do paciente.

### `GET /api/v1/pacientes/{id}/prontuario`

Somente `ADMIN` e `PROFISSIONAL`. Retorna alergias, atendimentos, exames e prescrições fictícias.

### `POST /api/v1/pacientes`

Somente `ADMIN` e `RECEPCAO`.

Exige o cabeçalho:

```text
X-CSRF-Token: <token>
```

Exemplo JSON:

```json
{
  "nome": "Paciente Fictício",
  "data_nascimento": "2000-01-01",
  "telefone": "11999999999"
}
```

## Limitação atual

A API reaproveita a sessão web. Para integração entre sistemas, uma evolução melhor seria autenticação própria por token, OAuth2/OIDC e escopos de acesso.
