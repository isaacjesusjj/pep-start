# Auditoria de acessos

A tabela `auditoria` registra ações relevantes para responder perguntas como:

- quem abriu um prontuário;
- quando ocorreu o acesso;
- qual recurso foi consultado;
- quem criou um usuário;
- quem registrou um exame ou prescrição;
- quando uma tentativa de login falhou.

## Campos principais

- `usuario_id`: usuário responsável, quando identificado;
- `acao`: evento realizado;
- `recurso`: tipo de recurso;
- `recurso_id`: identificador relacionado;
- `detalhes`: contexto não sensível;
- `ip`: endereço da requisição;
- `criado_em`: instante do evento.

## Decisão de privacidade

A auditoria **não copia resultado de exame, observação clínica, dose ou conteúdo de prescrição**. O log registra a existência da ação e o identificador necessário para rastreabilidade, evitando criar uma segunda cópia desnecessária do dado clínico.

## Limitação

A auditoria deste projeto é educacional. Ela não é append-only, assinada digitalmente ou enviada a um serviço externo de logs. Essas seriam evoluções relevantes para um sistema real.
