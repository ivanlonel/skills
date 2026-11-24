# Emoji prefix

Read this file only when the repository convention uses an emoji prefix
(SKILL.md, "Types"). Without that convention, write no emoji.

## Rules

- Put the emoji before the type: `✨ feat(agenda): permitir recorrência`.
- Use the form that the history uses: the character (`✨`) or the code
  (`:sparkles:`).
- Choose the emoji that matches the commit type. If several match, use the
  one that the history uses most.
- A character emoji counts 2 columns. A code counts its characters
  (`:sparkles:` is 10).
- For interrupted work, use 🚧 with the `WIP:` footer.
- Run `commit_check.py` with `--emoji`.

## Table

The types follow the type rules in SKILL.md. "Any" means the type of the
change.

| Emoji | Code | Use | Type |
|---|---|---|---|
| ✨ | `:sparkles:` | New feature | `feat` |
| 💄 | `:lipstick:` | UI styling | `feat` or `fix` |
| 🐛 | `:bug:` | Bug fix | `fix` |
| 📚 | `:books:` | Documentation | `docs` |
| 💡 | `:bulb:` | Code comments | `docs` |
| 🧪 | `:test_tube:` | Tests | `test` |
| ✅ | `:white_check_mark:` | Add a test | `test` |
| ✔️ | `:heavy_check_mark:` | Approval test | `test` |
| 🤡 | `:clown_face:` | Mocks | `test` |
| 👌 | `:ok_hand:` | Review changes that only reformat | `style` |
| ♻️ | `:recycle:` | Refactoring | `refactor` |
| ⚡ | `:zap:` | Performance | `perf` |
| 📦 | `:package:` | Packaging (`package.json` scripts, build) | `build` |
| 🧱 | `:bricks:` | Infrastructure | `ci` |
| 🔧 | `:wrench:` | Configuration | `chore` |
| 🙈 | `:see_no_evil:` | `.gitignore` | `chore` |
| 🚚 | `:truck:` | Move or rename | `chore` |
| ➕ | `:heavy_plus_sign:` | Add a dependency | `chore(deps)` |
| ➖ | `:heavy_minus_sign:` | Remove a dependency | `chore(deps)` |
| ⬆️ | `:arrow_up:` | Upgrade a dependency or submodule | `chore(deps)` |
| ⬇️ | `:arrow_down:` | Downgrade a dependency or submodule | `chore(deps)` |
| 🗃️ | `:card_file_box:` | Data | `raw` |
| 🧹 | `:broom:` | Code cleanup | `cleanup` |
| 🗑️ | `:wastebasket:` | Remove a file | `remove` |
| 🔒️ | `:lock:` | Security | `security` |
| 💥 | `:boom:` | Revert changes | `revert` |
| 🎉 | `:tada:` | Initial commit | `init` |
| 🚧 | `:construction:` | Work in progress | Any |
| ♿ | `:wheelchair:` | Accessibility | Any |
| 💫 | `:dizzy:` | Animations and transitions | Any |
| 📱 | `:iphone:` | Responsive layout | Any |
| 🔍️ | `:mag:` | SEO | Any |
| 📝 | `:pencil:` | Text | Any |
| 🏷️ | `:label:` | Type annotations | Any |
| 🥅 | `:goal_net:` | Error handling | Any |
| 🚀 | `:rocket:` | Deploy | Any |
| 🔖 | `:bookmark:` | Version tag | Any |
| 🔜 | `:soon:` | Task list | Any |
