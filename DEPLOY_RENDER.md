# Colocar o PEP Start online no Render

O repositório já possui `render.yaml`, portanto o Render consegue criar a aplicação FastAPI e o PostgreSQL automaticamente como um Blueprint.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https%3A%2F%2Fgithub.com%2Fisaacjesusjj%2Fpep-start)

## Passos

1. Clique em **Deploy to Render** acima.
2. Entre ou crie uma conta Render usando o GitHub.
3. Autorize o acesso ao repositório `isaacjesusjj/pep-start` quando solicitado.
4. Revise o Blueprint e clique em **Deploy Blueprint / Apply**.
5. Aguarde o serviço ficar com status disponível.
6. Abra a URL terminada em `.onrender.com`.
7. No primeiro acesso, abra `/setup` e crie seu usuário `ADMIN`.

## O que o Blueprint cria

- aplicação FastAPI com Uvicorn;
- banco PostgreSQL;
- variável `DATABASE_URL` ligada automaticamente ao banco;
- chave secreta de sessão gerada pelo Render;
- cookie seguro para HTTPS;
- health check em `/health`.

## Observação sobre o plano gratuito

O plano gratuito é adequado para demonstrações e portfólio, não para produção. O web service pode entrar em suspensão depois de um período sem tráfego, e o PostgreSQL gratuito expira 30 dias após a criação. Use somente dados fictícios neste projeto acadêmico.
