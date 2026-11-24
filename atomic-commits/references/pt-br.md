# pt-BR commit messages

Read this file when the commit language is pt-BR (SKILL.md, step 2). These
rules add to the rules in SKILL.md.

## Language rules

- **[hard]** Write the description, the body, and the free-text footer
  values in Brazilian Portuguese. Use the spelling of the 1990 Orthographic
  Agreement (AO1990).
- **[hard]** Start the description with a verb in the impersonal infinitive.
  The description completes the sentence "Se aplicado, este commit irá
  <descrição>." The description can start with "não" + infinitive.
- **[hard]** Keep domain terms and identifiers as they are: `endpoint`,
  `token`, `cache`, `deploy`, `pull request`, `enviar_lembrete`, `README`.
  Types, scopes, and footer tokens also stay in English.
- Default: start the description in lowercase, because Portuguese uses
  lowercase after a colon. A history that capitalizes descriptions is a
  convention, and it wins.
- Use `--lang pt-BR` when you run `commit_check.py`.

| Form | Example | Correct? |
|---|---|---|
| Infinitive | `fix: corrigir horário do lembrete` | Yes |
| "não" + infinitive | `fix: não exigir token em rotas públicas` | Yes |
| Third person | `fix: corrige horário do lembrete` | No |
| Gerund | `fix: corrigindo horário do lembrete` | No |
| Participle | `fix: horário do lembrete corrigido` | No |
| Noun | `fix: correção do horário do lembrete` | No |
| Imperative | `fix: corrija o horário do lembrete` | No |

## Verbs for each type

These are examples. Any infinitive that fits the change is correct.

| Type | Verbs |
|---|---|
| `feat` | adicionar, permitir, criar, exibir, suportar, implementar |
| `fix` | corrigir, evitar, tratar, impedir, restaurar |
| `docs` | documentar, descrever, explicar, atualizar |
| `test` | cobrir, testar, validar |
| `style` | formatar, padronizar, aplicar |
| `refactor` | extrair, renomear, simplificar, mover, reorganizar |
| `perf` | acelerar, reduzir, otimizar, indexar |
| `build` | gerar, empacotar, configurar |
| `ci` | rodar, executar, publicar |
| `chore` | ignorar, configurar, mover, atualizar |
| `chore(deps)` | atualizar, adicionar, remover, fixar |
| `raw` | atualizar, importar, carregar |
| `cleanup` | excluir, limpar, simplificar |
| `remove` | remover, excluir |
| `security` | bloquear, limitar, validar, proteger |
| `revert` | reverter |
| `init` | criar, iniciar |

## Preferred verbs

Nouns that are domain terms stay in English ("o deploy", "o cache"). For
verbs, prefer the standard Portuguese verb to an anglicism.

| Anglicism | Preferred verb |
|---|---|
| deletar | excluir, remover |
| setar | definir, configurar |
| resetar | redefinir, reiniciar |
| logar | registrar (log), entrar (login) |
| deslogar | sair |
| startar | iniciar |
| buildar | compilar, gerar |
| deployar | implantar, publicar |
| mergear | mesclar |
| debugar | depurar |
| printar | exibir, imprimir |
| parsear | interpretar, analisar |
| cachear | armazenar em cache |
| linkar | vincular |
| upar | enviar |
| dropar | descartar, excluir |

## AO1990 spelling traps

| Rule | Correct |
|---|---|
| Prefix + r or s: double the letter | microsserviço, contrassenha, autorrecuperação |
| Prefix + same vowel: hyphen | micro-otimização, auto-observação, anti-inflamatório |
| Prefix + other vowel: no hyphen | infraestrutura, autoatualização, semiautomático |
| `sub` + r, b, or h: hyphen | sub-rotina, sub-rede, sub-base |
| `sub` + other letters: no hyphen | subdiretório, submódulo, subpasta |
| `pré`, `pós`, `pró`: hyphen | pré-requisito, pós-processamento, pré-visualização |
| `co`, `re`: no hyphen | coautor, coexistir, reescrever, reexecutar, reindexar |
| "não" + noun or adjective: no hyphen | não autenticado, não nulo |
| No accent on `ei`, `oi` in paroxytones | ideia, heroico, assembleia |
| No trema | frequência, sequência, consequência |
| No differential accent (except pôr, pôde) | para (verb), pelo, polo |
| No circumflex in `-eem` | leem, veem, creem, deem |

## Branch names and pull requests

- In a branch name, write the task part in Portuguese, in lowercase kebab
  case, without accents: `feat/57-consultas-recorrentes`.
- Write the pull request title with the commit-title rules. Write the body
  in Portuguese, with these headings: `Resumo`, `Verificação`,
  `Não verificado`, `Revisão`.

## Example

```text
fix(agenda): enviar lembrete no fuso do paciente

Os lembretes saíam no horário do servidor (UTC). Pacientes de outros
fusos recebiam o aviso na hora errada.

Closes: #87
```
