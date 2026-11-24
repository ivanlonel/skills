# atomic-commits

An [Agent Skills](https://agentskills.io/specification) skill that makes AI
agents create atomic commits, write Conventional Commits messages, and handle
branches and pull requests. Repository conventions come first. A pt-BR part
activates only for Brazilian Portuguese projects.

Agents do not load this file. It is for people.

## Layout

| Path | Content |
|---|---|
| `SKILL.md` | Workflow and message rules. Agents load it when the skill fires. |
| `references/pt-br.md` | pt-BR rules: infinitive, AO1990 spelling, preferred verbs |
| `references/in-progress.md` | Merges, cherry-picks, reverts, and unmerged files |
| `references/branches.md` | Branch policy, naming, sync, merge, cleanup, backports |
| `references/pull-requests.md` | Pull request size, splitting, title, description |
| `references/emoji.md` | Emoji prefix table, for repositories that use one |
| `scripts/commit_check.py` | Checks a draft message, or a pull request's size. Python 3.8+, standard library only. It is not a Git hook. |

Run the checker's self-test with `python3 scripts/commit_check.py --self-test`.

## Hard rules

These apply in every repository and override repository conventions:

- Title: at most 72 columns, and 50 when possible.
- Body lines: at most 72 columns. URLs and code that cannot be split are
  exempt.
- The description completes "If applied, this commit will …" and has no
  punctuation at the end.
- pt-BR projects: pt-BR with AO1990 spelling, and the description in the
  infinitive ("Se aplicado, este commit irá …").

## Sources

The skill combines and reorganizes rules from these sources. Where they
conflict, the skill follows decisions made by its author.

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/)
- [Padrões de commits](https://github.com/iuricode/padroes-de-commits) (extra types and the emoji table)
- [GitLab `commit-messages` skill](https://gitlab.com/gitlab-org/ai/skills/-/tree/main/skills/commit-messages) (MIT)
- [GitHub awesome-copilot `git-commit` skill](https://github.com/github/awesome-copilot/tree/main/skills/git-commit) (MIT)
- [finolabs vibecode `commit-messages` skill](https://github.com/finolabs/vibecode/tree/main/skills/commit-messages)

## License

MIT
