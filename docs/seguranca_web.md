# Segurança da versão web

## Hash de senha

Senhas não são armazenadas em texto puro. O projeto usa `PBKDF2-HMAC-SHA256` com salt aleatório.

O hash serve para verificar a senha sem precisar conhecer ou armazenar a senha original.

## Sessão

Após login, o navegador recebe um cookie de sessão assinado. O servidor usa a sessão para identificar o usuário em cada requisição.

## CSRF

Formulários e operações de escrita da API exigem token CSRF. Isso reduz o risco de outro site induzir o navegador autenticado a executar uma ação sem intenção do usuário.

## Autorização

Autenticação responde **quem é o usuário**. Autorização responde **o que ele pode fazer**.

As rotas verificam o perfil antes de executar operações restritas.

## Cabeçalhos

A aplicação define:

- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: same-origin`;
- `Cache-Control: no-store` em conteúdo clínico/API.

## Dados fictícios

Nenhuma dessas medidas é justificativa para inserir dados reais. O projeto permanece exclusivamente acadêmico.
