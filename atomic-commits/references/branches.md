# Branches

Read this file when you create, name, sync, or merge a branch, or backport a
fix (SKILL.md, step 4). For what needs the user's approval, see SKILL.md,
"Authority".

The model is **trunk-based**: the default branch is always releasable, and
changes reach it through short-lived branches. A branching scheme in the
project instructions wins over this model.

## Find the default branch and how it gets changes

```bash
git symbolic-ref --short refs/remotes/origin/HEAD
```

If that fails, use `gh repo view --json defaultBranchRef` on GitHub, or the
equivalent command of the host.

The default branch gets its changes through **pull requests** if one of
these is true:

- The project instructions send changes through pull requests.
- The host shows merged pull requests (`gh pr list --state merged --limit 5`).
- The history has `Merge pull request #` commits, titles that end in `(#N)`,
  or commits that GitHub committed for another author.

If none is true, commit on the current branch. This also applies when the
repository has no remote, or when you cannot reach the host.

## Create a branch

```bash
GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never git fetch
git switch -c <name> origin/<base>
```

The two variables stop a credential prompt, which would wait for a person.
If `git fetch` fails, or the repository has no remote, use
`git switch -c <name>` from the current commit. Say so in your report.
If `git switch` refuses because of local changes, do the same, and sync the
branch later.

Use a worktree only for parallel agent runs, one worktree for each run:
`git worktree add -b <name> <path> origin/<base>`. Put it in the worktree
folder of the repository, if it has one.

## Name a branch

- Use `<type>/<task>`, in lowercase kebab case: `fix/88-parser-null`.
- `<type>` is the main commit type of the branch, or `hotfix`.
- Put the task ID first when the project tracks tasks.
- Write `<task>` in the commit language, without accents.
- A branch that the host named for its own worktree keeps its name.

## Keep a branch short-lived

A branch lives for days, not weeks. Split large work into pull requests
that each keep the default branch releasable (see `pull-requests.md`).

## Sync a branch

Bring the base in before you open a pull request. Also bring it in when the
base changes the files that you change.

| Branch | Sync |
|---|---|
| Not pushed | `git fetch`, then `git rebase origin/<base>` |
| Your own pull request branch: you created it, and only you push to it | Rebase it, then force-push with a lease (below) |
| Other people push to it | `git merge origin/<base>`. Rebase only when the user tells you to. |

Force-push with a lease that names the remote commit you rebased from:

```bash
old=$(git rev-parse origin/<branch>)   # before the rebase
git rebase origin/<base>
git push --force-with-lease=<branch>:$old --force-if-includes origin <branch>
```

If the host has a sync tool for its worktrees, use it.

## Resolve conflicts

Resolve conflicts on the branch, not on the default branch. Use
`in-progress.md` for the commands. Keep the intent of both sides. If the
intents contradict, ask the owner of the other change. Run the targeted
tests again.

## Merge a pull request

1. Merge only when the user tells you to.
2. Merge through the pull request, after the required checks and reviews
   pass.
3. Do not bypass branch protection. If the host rejects a direct push, open
   a pull request.
4. Prefer a rebase merge, which keeps a linear history of atomic commits.
   Pin it to the reviewed head, so a later push cannot join the merge:

   ```bash
   gh pr merge <number> --rebase --match-head-commit <sha>
   ```

   If the repository does not allow a rebase merge, use a merge commit. Use
   a squash merge only when it is the only method allowed, because it
   joins the atomic commits into one.

## Clean up after a merge

- Delete the head branch on the host only if you created it. No running
  session or run may use it. Use `gh pr merge --delete-branch`, or the
  automatic deletion of the repository.
- Remove only the worktrees and branches that you created, when nothing
  uses them:
  - `git worktree remove <path>`. This also deletes the ignored files in
    that worktree.
  - `git branch -d <branch>`. Use `-D` only with the owner's approval.

## Hotfix and backport

1. Fix the default branch first, through a normal pull request.
2. For each supported older line, create a branch from `release/X.Y`, and
   copy the fix with `git cherry-pick -x <sha>`. Open one pull request for
   each line.
3. If the fix applies only to an older line, start on that line.
4. If `release/X.Y` does not exist, create it from the latest tag of that
   line (the highest `vX.Y.Z`).
