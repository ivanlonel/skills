# Operations in progress and unmerged files

Read this file when `git status` shows a merge, cherry-pick, revert, rebase,
or `am` in progress, or unmerged paths (SKILL.md, step 3).

In a subdirectory, run each command in this file as `git -C <root> …`.
`git rev-parse --show-toplevel` prints the root.

## 1. Find the operation

Run each command alone. Do not chain them with `&&`, because a check that
finds nothing exits with status 1 and stops the chain.

```bash
git rev-parse -q --verify --symbolic-full-name MERGE_HEAD
git rev-parse -q --verify --symbolic-full-name CHERRY_PICK_HEAD
git rev-parse -q --verify --symbolic-full-name REVERT_HEAD
git -c core.quotePath=false diff --name-only --diff-filter=U --no-relative
git status --long
```

- A `rev-parse` command prints a ref name when its operation is in progress.
- The `diff` command lists unmerged files. It also finds conflicts that have
  no ref, for example after `git stash pop`.

These texts in `git status --long` show a multi-step operation. If you see
one, stop and tell the user:

- "rebase in progress"
- "You are in the middle of an am session"
- "Cherry-pick currently in progress"
- "Revert currently in progress"

**Done when:** you know the operation and the unmerged files, or you
stopped.

## 2. Resolve the conflicts

The index holds the result of the operation. Do not unstage files, and do
not split the commit. If you unstage a file, Git drops the changes of the
other side or removes a conflict entry.

1. Read both sides of each conflict. Keep the intent of each side.
2. If the two intents contradict, stop and ask the owner of the other change.
3. Run the targeted tests again. The resolution is part of the change.

**Done when:** each conflict has a resolution, or you asked the owner.

## 3. Stage the resolved files

Run `git status --porcelain=v2`. A line that starts with `u` shows an
unmerged file. Stage a file yourself only if all these conditions are true:

- The line starts with `u UU N...` or `u AA N...`.
- Each mode on the line is `100644`, `100755`, or `000000`.
- `git diff --no-relative` does not show `Binary files differ` for the file.

For all other unmerged files, ask the user. Git cannot find conflict markers
in them. Stage each one only after the user resolves it:
`git add -- <path>`.

Stage the files that you resolved:

- Git 2.56 or later: `git add --resolved -- <paths>`.
- Earlier Git: run `git diff --check -- <paths>`. If it shows no
  "leftover conflict marker" line, run `git add -- <paths>`. Ignore
  whitespace warnings that come from the other branch.

Then find the other edits:

```bash
git -c core.quotePath=false diff --name-only --no-relative
git ls-files --others --exclude-standard
```

Skip the files that are still unmerged. Show the other paths to the user,
and ask if they belong to this commit. Stage only the paths that the user
approves.

**Done when:** no unmerged file remains, and the index holds only approved
paths.

## 4. Commit

| Operation | Command and message |
|---|---|
| Merge | `git commit --no-edit`, with no paths and no `--cleanup`. Keep the message that Git prepared, with its `Conflicts:` lines. |
| Cherry-pick | `git commit --no-edit`. Keep the original message and the `(cherry picked from commit …)` line from `-x`. |
| Revert | Write a `revert:` message (SKILL.md, "Reverts, merges, and cherry-picks"). Validate it, then run `git commit -F <draft>` with no paths. |

Then continue with SKILL.md, step 10.

**Done when:** the commit exists, and `git status` shows no operation in
progress.
