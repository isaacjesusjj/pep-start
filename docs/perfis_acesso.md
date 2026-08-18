# Perfis de acesso

A versão web utiliza **RBAC (Role-Based Access Control)**: permissões são associadas ao perfil do usuário.

| Operação | ADMIN | RECEPCAO | PROFISSIONAL |
|---|:---:|:---:|:---:|
| Listar/localizar pacientes | ✅ | ✅ | ✅ |
| Cadastrar paciente | ✅ | ✅ | ❌ |
| Atualizar cadastro | ✅ | ✅ | ❌ |
| Ver dados administrativos | ✅ | ✅ | ✅ |
| Ver prontuário clínico | ✅ | ❌ | ✅ |
| Registrar alergia | ✅ | ❌ | ✅ |
| Registrar atendimento | ✅ | ❌ | ✅ |
| Registrar exame | ✅ | ❌ | ✅ |
| Registrar prescrição | ✅ | ❌ | ✅ |
| Criar/ativar usuários | ✅ | ❌ | ❌ |
| Consultar auditoria | ✅ | ❌ | ❌ |

## Por que separar?

O princípio aplicado é o **menor privilégio**: cada pessoa recebe apenas os acessos necessários para sua atividade simulada. A Recepção não precisa ler resultados clínicos para cadastrar um telefone, por exemplo.
