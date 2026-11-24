---
name: atomic-commits
description: >-
  Atomic commits, commit messages, branches, and pull requests: Conventional
  Commits, with repository conventions first and Brazilian Portuguese (pt-BR)
  rules for pt-BR repositories. Use when staging or splitting changes,
  committing, writing or reviewing a commit message, creating, naming or
  syncing a branch, resolving merge conflicts, reverting, backporting, merging
  a pull request, or writing a pull request description.
license: MIT
compatibility: Requires Git. scripts/commit_check.py requires Python 3.8 or later.
---

# Atomic commits

An **atomic commit** holds one logical change: complete, with its tests, and
nothing else. Its message tells a future reader what changed and why. This
skill gives the workflow and the default rules for commits, branches, and pull
requests.

## Precedence

1. **Hard rules** (marked **[hard]**) apply in every repository. No
   convention overrides them.
2. **Repository conventions** come next. A convention is an explicit rule
   (CONTRIBUTING.md, AGENTS.md, CLAUDE.md, a commitlint config). It can also
   be a pattern that most of the last 20 commits follow. With fewer
   commits, use all of them. Mixed history sets no convention.
3. **Defaults** apply where no convention exists. Each rule without
   **[hard]**, in this file and in the reference files, is a default.

Ignore these commits when you read the history: merge commits, bot commits
(Renovate, Dependabot), and commits that a tool or host made from a
template, such as `Initial commit`. A project's own first commit, such as
`init: criar estrutura do projeto`, counts. A repository with only ignored
commits has no history.

If a repository tool (a hook, commitlint) enforces a rule that contradicts a
hard rule, stop and ask the user.

## Workflow

Do the steps in order. Each step ends on its **Done when** condition.
For a request to only write or review a message, do steps 1, 2, 7, and 8.
Then show the message in a code block and stop.

### 1. Read the conventions

Read CONTRIBUTING.md, AGENTS.md, CLAUDE.md, and the commitlint config, if they
exist. Then read the recent history:

```bash
git log -20 --format='--- %an%n%B'
```

Record the convention for each item: message format (Conventional Commits or
other), type list, scopes, description case, emoji prefix, issue-reference
style, sign-off (`Signed-off-by`), and language.

**Done when:** each item has a convention, or "none".

### 2. Choose the commit language

Use **pt-BR** when one of these is true:

- The project instructions or the user ask for pt-BR commit messages.
- Most of the last 20 commits are in pt-BR.
- There is no history, no instruction about the commit language, and the
  project instructions are in pt-BR.

In all other cases, use the language of most of the last 20 commits. With no
history, use the language of the project instructions. With neither, use
English. The language of the user's request does not decide it.

If you use pt-BR, read [references/pt-br.md](references/pt-br.md) now.

**Done when:** you know the language, and you read `pt-br.md` if it is pt-BR.

### 3. Check the repository state

Run `git status`. If it shows a merge, cherry-pick, revert, rebase, or `am`
in progress, or unmerged paths, read
[references/in-progress.md](references/in-progress.md) and follow it.

**Done when:** no operation is in progress, or `in-progress.md` told you how
to continue.

### 4. Choose the branch

A branching scheme in the project instructions wins. Instructions that send
changes through pull requests are a scheme. Without a scheme:

- If the default branch gets its changes through pull requests, do not
  commit on it. Create a branch first.
- If the history shows direct commits to the default branch, commit on the
  current branch.
- If the repository has no remote, commit on the current branch.
- An explicit request from the user wins over these rules.

To detect pull requests, to create, name, or sync a branch, or to merge,
read [references/branches.md](references/branches.md).

**Done when:** you are on the branch that gets the commits.

### 5. Group the changes into atomic commits

Read the changes:

```bash
git -c core.quotePath=false status --short
git diff
git diff --staged
```

Commit the changes of the current task, or the changes that the user names.
Leave all other changes unstaged and list them for the user. If the user
asks to commit everything, group all changes.

Group the changes with these rules:

- One logical change per commit. A change can touch many files.
- Keep tests in the commit of the code that they test.
- Put refactoring, formatting, and dependency changes in their own commits.
- If a change fits two types, split it.
- When in doubt, split. Do not split when a part would not build or would
  lose its tests.
- Put a dependency change and its lockfile in the same commit.
- Regenerate tracked generated files the way the repository prescribes.
- Leave out secrets, `.env` files, credentials, and build or cache output.
- Order the commits so each one builds: formatting and refactoring, then
  dependencies, then features and fixes.

Before you commit a change, run its targeted tests, if the project has
tests. Do this for the user's work too. Run them in a way that leaves no
new files (caches) in the work tree. If a test fails, do not commit that
change: report the failure. If you cannot run the tests, say so in the
report.

**Done when:** each changed path is in one planned commit, or in the list of
changes that you leave out.

### 6. Stage one commit

```bash
git reset -q -- <paths of other commits>   # only if they are staged
git add -- <paths of this commit>
git diff --staged --name-only
```

- Use explicit paths. Put globs in quotes: `git add -- '*.test.*'`.
- Read non-ASCII paths with `git -c core.quotePath=false`, or use `-z`.
- Use only commands that need no input from a person. `git add -p` and
  `git add -i` wait for input.
- To stage part of a file, use a patch. Write the patch, then delete the
  hunks of the other commits. Delete whole hunks only. Then apply the
  patch to the index:

  ```bash
  git diff -- <file> > <patch>
  git apply --cached --recount <patch>
  ```

**Done when:** `git diff --staged --name-only` lists the planned paths and
no other paths.

### 7. Write the message

Write the message to a draft file. Use UTF-8 without a BOM, because some
shells change accented characters on the command line. Put the draft in the
Git directory, out of the work tree:

```bash
git rev-parse --absolute-git-dir   # the draft is <this path>/COMMIT_DRAFT
```

Delete the draft after the last commit.

Follow [Message rules](#message-rules).

**Done when:** the draft holds the full message.

### 8. Validate the message

Run the checker on the draft. Models miscount characters, so do not skip
this step. `<skill-dir>` is the folder of this file. On Windows, use
`python` if `python3` is not found.

```bash
python3 <skill-dir>/scripts/commit_check.py message <draft> <flags>
```

| Flag | Use it when |
|---|---|
| `--lang pt-BR` or `--lang en` | The commit language is pt-BR or English |
| `--types a,b,c` | The repository has its own type list |
| `--no-cc` | The repository does not use Conventional Commits |
| `--emoji` | The repository uses an emoji prefix |
| `--case upper` or `--case any` | The repository capitalizes descriptions, or has no rule |

Correct each `ERROR`. Correct each title-width `WARN` unless no clear title
is shorter.

**Done when:** the script prints `OK`, and no shorter clear title exists.

### 9. Commit

```bash
git commit -F <draft>
```

- Add `-s` if the repository uses sign-off.
- Keep hooks and signing on. Use `--no-verify` or `--no-gpg-sign` only when
  the user asks.
- If a hook fails, Git makes no commit. Correct the problem, stage again,
  and run the same command again. Do not use `--amend`, because it changes
  the previous commit.

**Done when:** Git prints the new commit.

### 10. Verify and report

```bash
git log -1 --format=%B
git status --porcelain
```

Make sure the accented characters are correct. Do steps 6 to 10 again for
each planned commit. Then report each commit (hash and title) and the
changes that you left out, with a question about them.

**Done when:** each planned commit exists, and the user has the report.

## Message rules

```text
type(scope)!: description

body

footers
```

### Title

- **[hard]** The title MUST NOT exceed 72 columns and SHOULD NOT exceed 50.
  Count the full line, with `type(scope)!: `. Emoji and CJK characters
  count 2 columns. Exception: a URL or code that you cannot split, and that
  must be in the title.
- **[hard]** The description completes the sentence "If applied, this
  commit will <description>." In English, start with the base verb: "add",
  not "added" or "adds".
- **[hard]** The description has no punctuation at the end. A closing
  backtick or parenthesis of code is correct.
- Start the description in lowercase. Proper nouns and identifiers keep
  their case.
- Make the title specific and clear without the diff or the issue tracker.
  Put issue references in footers.
- If the title joins two actions with "and", split the commit.
- To make a title shorter, use a more specific verb, or move details to the
  body. Remove the scope only when the area is obvious. Do not invent
  abbreviations.

### Types

| Type | Use it for |
|---|---|
| `feat` | A new capability, including the UI styling of a feature |
| `fix` | A bug fix, including UI and CSS fixes |
| `docs` | Documentation and code comments only |
| `test` | Test-only changes |
| `style` | Code formatting and lint fixes, with no change to logic |
| `refactor` | New structure, same behavior (performance work is `perf`) |
| `perf` | A change made for performance |
| `build` | The build system and packaging |
| `ci` | CI pipelines and infrastructure |
| `chore` | Repository and tool config (`.gitignore`, editor, linters), file moves and renames, other upkeep |
| `chore(deps)` | Adding, updating, or removing dependencies, with the lockfile |
| `raw` | Data and parameter files that the application reads (datasets, parameter tables, flag values) |
| `cleanup` | Dead code inside files: commented-out code, unused variables and imports |
| `remove` | Deleting whole files, directories, or features |
| `security` | Vulnerability fixes, authentication and authorization flaws, data exposure, hardening |
| `revert` | Reverting earlier commits |
| `init` | The first commit of a new repository |

Default release tools bump the version only for `feat`, `fix`, and breaking
changes.

The **scope** is optional. It is a noun that names the area of the change.
Use lowercase ASCII (`a-z`, `0-9`, `_ . / -`), and use scopes that the
history already uses. For a new area, use a short noun, such as the module
name. Leave the scope out when the change has no single area.

Use an emoji prefix only when the repository convention uses one. Then read
[references/emoji.md](references/emoji.md).

### Body

- **[hard]** Body lines MUST NOT exceed 72 columns. Exceptions: a line that
  holds only a URL, a `[1] https://…` reference line, and code.
- **[hard]** Put an empty line between the title and the body, and between
  paragraphs.
- Tell what changed and why. Leave out a reason that is obvious, and any
  "what" that the title already gives. A commit with only a title is
  correct when nothing relevant remains.
- Write only facts from the diff, the user, or the task. Do not invent a
  reason, an issue number, or a reviewer. If you do not know the reason,
  leave it out, and ask the user in your report.
- Do not list the changed files or retell the diff. The diff shows them.
- Put a long URL on its own line, or use a reference such as `[1]`.
- Use the canonical form of links: no link shorteners, affiliate links, or
  tracking parameters.
- When the commit holds work that another agent wrote, say so in the body.

### Footers

The footers are the last paragraph. Git reads them as **trailers** only if
each line has the form `Token: value`. Indent a continuation line.

- Write the tokens in English: `Closes`, `Refs`, `Reviewed-by`,
  `Co-authored-by`, `WIP`, `BREAKING-CHANGE`.
- Issue references:

  | Host | Footer |
  |---|---|
  | GitHub | `Closes: #57`, or `Closes: owner/repo#57` for another repository. GitHub does not document full URLs here. |
  | GitLab and other hosts | `Closes: https://gitlab.com/group/project/-/issues/57` |
  | Jira | `Refs: PROJ-123` |

- Use `Closes` when the user or the task says that the commit resolves the
  issue. Otherwise, use `Refs`.
- Take IDs from the user, the task, or the branch name.
- If the host asks for an attribution trailer, add it exactly as given.

### Breaking changes

A change is breaking when users of a public interface (an API, a CLI, a
configuration, a data format) must change their code or data. Mark each
breaking change in two places. Do this before version 1.0.0 too.

1. Put `!` before the colon in the title: `feat(api)!: …`.
2. Add one footer line: `BREAKING-CHANGE: <summary>`. Use the hyphen,
   because Git cannot read a token with a space. Git then loses all the
   trailers in that paragraph.

Put the migration steps in the body.

### Reverts, merges, and cherry-picks

- **Revert:** run `git revert --no-commit <sha>`. Then write a `revert:`
  title, the reason in the body, and a `Refs: <sha>` footer.
- **Merge commit:** keep the message that Git prepares.
- **Cherry-pick:** keep the original message. Use `-x`, so Git records the
  source commit.

### Interrupted work

When you commit work that stopped before it was complete, write a normal
title for what the work does. In the body, say what is missing. Add the
footer `WIP: <task label>`.

## Fixing your own unpushed commits

A commit is yours if you made it in this task. It is unpushed if
`git branch -r --contains <sha>` prints nothing. You can change your own
unpushed commits without asking:

- Correct the last commit: `git commit --amend -F <draft>`.
- Correct an earlier commit: `git commit --fixup=<sha>`, then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <sha>~1`.
- Split the last commit: `git reset HEAD~1`, then do steps 6 to 10 again.

For all other commits, ask the user first.

## Authority

Do these only when the user tells you to:

- Push, open a pull request, or merge a pull request.
- Change commits that are pushed or that other people made.
- Run `git reset --hard`, or force-push. Exception: your own pull request
  branch (see `branches.md`).
- Delete branches or worktrees that you did not create.

Never do these:

- Change the Git configuration.
- Bypass branch protection, even if your account can.
- Force-push the default branch.
- Make an empty commit.

## Example

```text
feat(agenda)!: exigir fuso horário nas consultas

Datas sem fuso eram lidas no horário do servidor. Consultas marcadas
em outros estados apareciam com uma hora de diferença.

Clientes da API devem enviar `inicio` e `fim` em ISO 8601 com
deslocamento, por exemplo `2026-03-10T14:00:00-03:00`.

BREAKING-CHANGE: `inicio` e `fim` sem fuso agora retornam 422
Refs: #57
```

One title for each type:

```text
feat(agenda): permitir consultas recorrentes
fix(agenda): respeitar horário de verão
docs: documentar variáveis de ambiente
test(estoque): cobrir baixa de item sem saldo
style: aplicar formatação do ruff
refactor(estoque): extrair cálculo de saldo
perf(busca): indexar produtos por código de barras
build: gerar wheel com hatchling
ci: rodar testes no Python 3.13
chore: ignorar arquivos .env
chore(deps): atualizar django para 5.2.1
raw: atualizar tabela de alíquotas de 2026
cleanup(estoque): excluir código comentado
remove: excluir módulo de relatórios legado
security(auth): limitar tentativas de login
revert: reverter cache de sessões em Redis
init: criar estrutura do projeto
```

## Reference files

Read each file only when its condition is true.

| File | Read it when |
|---|---|
| [references/pt-br.md](references/pt-br.md) | The commit language is pt-BR (step 2) |
| [references/in-progress.md](references/in-progress.md) | An operation is in progress, or paths are unmerged (step 3) |
| [references/branches.md](references/branches.md) | You detect how the default branch gets changes, create, name, sync, or merge a branch, or backport a fix |
| [references/pull-requests.md](references/pull-requests.md) | You write a pull request, or plan how to split work into pull requests |
| [references/emoji.md](references/emoji.md) | The repository uses an emoji prefix |
