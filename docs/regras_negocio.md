# Regras de negócio — PEP Start

**RN01 — ID único.** Cada paciente deve possuir identificador único para evitar ambiguidade entre pessoas com nomes iguais.

**RN02 — ID automático.** O usuário não escolhe o ID; o SQLite o gera automaticamente.

**RN03 — Nome obrigatório.** O nome não pode ficar vazio e deve ter pelo menos três caracteres após normalização de espaços.

**RN04 — Atendimento vinculado.** Todo atendimento deve pertencer a um paciente existente.

**RN05 — Alergia vinculada.** Toda alergia deve pertencer a um paciente existente.

**RN06 — Paciente deve existir.** Não é possível registrar informações clínicas para um ID inexistente.

**RN07 — Data obrigatória.** Todo atendimento deve possuir uma data válida no formato `AAAA-MM-DD`.

**RN08 — Histórico ordenado.** Atendimentos devem ser apresentados do mais recente para o mais antigo.

**RN09 — Exclusão protegida.** Pacientes com alergias ou atendimentos associados não podem ser excluídos.

**RN10 — Dados fictícios.** Demonstrações, testes e documentação utilizam apenas dados inventados.

**RN11 — Sem atendimento futuro.** Um atendimento registrado como histórico não pode possuir data posterior ao dia atual.

**RN12 — Atendimento após nascimento.** A data do atendimento não pode ser anterior à data de nascimento do paciente.

**RN13 — Alergia não duplicada.** A mesma descrição de alergia não deve ser registrada mais de uma vez para o mesmo paciente, ignorando diferença entre maiúsculas e minúsculas.

**RN14 — Telefone opcional e normalizado.** Quando informado, o telefone deve conter 10 ou 11 dígitos; caracteres de formatação são removidos antes do armazenamento.

## Regras adicionadas na versão web

**RN15 — Primeiro usuário administrador.** A configuração inicial só cria um administrador quando ainda não existe nenhum usuário.

**RN16 — Recepção sem prontuário.** O perfil `RECEPCAO` pode trabalhar com dados administrativos, mas não visualizar ou registrar conteúdo clínico.

**RN17 — Profissional sem administração.** O perfil `PROFISSIONAL` pode trabalhar com prontuário, mas não criar usuários nem abrir auditoria.

**RN18 — Administração de usuários.** Apenas `ADMIN` cria usuários e altera seu status.

**RN19 — Auto-desativação proibida.** O administrador autenticado não pode desativar a própria conta pela interface.

**RN20 — Registro clínico datado.** Exames e prescrições fictícias não podem ter data futura nem anterior ao nascimento do paciente.

**RN21 — Auditoria obrigatória.** Visualização de prontuário e alterações relevantes devem gerar evento de auditoria.

**RN22 — Auditoria mínima.** O evento deve identificar ação e recurso sem copiar conteúdo clínico para o campo de detalhes.

**RN23 — API respeita perfis.** Usar a API não pode contornar as restrições da interface web.

**RN24 — Migração segura.** O migrador deve recusar destino que já contenha registros, reduzindo risco de duplicidade.
