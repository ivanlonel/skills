# Pull requests

Read this file when you write a pull request, or plan how to split work into
pull requests. For what needs the user's approval, see SKILL.md,
"Authority".

## Size

Keep the diff of a pull request below **150,000 characters**. Measure it:

```bash
python3 <skill-dir>/scripts/commit_check.py pr-size origin/<base>
```

The count includes lockfiles and generated files. Binary files count only as
one line each.

If the diff is larger, split the work into two or more **atomic** pull
requests:

- Each pull request is one complete change set that a reviewer can
  understand alone. It builds, and its tests pass.
- Cut along the logical changes, never at a random point.
- Prefer independent pull requests, each one from the base.
- When one pull request needs another, open it after the other merges. Or
  stack it: target the branch of the other pull request. After the other
  pull request merges, rebase yours onto the base:
  `git rebase --onto origin/<base> <old-parent-tip> <branch>`.
- Plan the cuts before you write the code, not after.

One change that you cannot split can be larger. Then say why in the
description.

## Title

Use the commit-title rules (type, language, width), because a squash merge
makes the title a commit title.

## Description

Write the description in the commit language. Use these sections, each in
one to a few lines:

| Section | pt-BR heading | Content |
|---|---|---|
| Summary | Resumo | What changed and why |
| Verification | Verificação | The commands you ran and their results |
| Not verified | Não verificado | What you did not check |
| Review | Revisão | Who reviewed, or "not reviewed" |

- Do not copy the changelog entry. The changelog is the one record of a
  public change.
- On GitHub, add `Closes #N` to the description. A closing keyword in a
  commit closes the issue, but GitHub does not then list the pull request
  as linked.
- If the host asks for an attribution line, put it at the end.
- If another installed skill shapes pull request descriptions, follow it,
  and keep the four sections.

## Example (pt-BR)

```markdown
## Resumo

Exige fuso horário em `inicio` e `fim` das consultas. Datas sem fuso
eram lidas no horário do servidor.

## Verificação

`python -m pytest tests/agenda` → 31 passed

## Não verificado

Aplicativos móveis que ainda enviam datas sem fuso.

## Revisão

Não revisado.

Closes #57
```
