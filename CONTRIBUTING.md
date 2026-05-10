# Contributing

## Commit messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/). Releases and version bumps are generated automatically from commit messages by [`python-semantic-release`](https://python-semantic-release.readthedocs.io/), so the prefix matters.

Format:

```
<type>(<optional scope>): <short summary>

<optional body>

<optional footer>
```

### Types that trigger a release

| Prefix       | Bump  | Use for                                  |
| ------------ | ----- | ---------------------------------------- |
| `feat:`      | minor | A new user-facing feature                |
| `fix:`       | patch | A bug fix                                |
| `perf:`      | patch | A performance improvement                |

### Types that do NOT trigger a release

`docs:`, `chore:`, `refactor:`, `test:`, `style:`, `ci:`, `build:`

### Breaking changes

Append `!` after the type, **and** add a `BREAKING CHANGE:` footer:

```
feat!: drop support for Python 3.10

BREAKING CHANGE: minimum Python version is now 3.11
```

This forces a major bump.

### Examples

```
feat: add async batch insert
fix: handle empty vector in search
fix(client): retry on transient 503
docs: update README install command
chore(release): v0.1.0
```

### Don't

- Don't use generic messages like `update`, `wip`, `fixes`. They land as `unknown` in the changelog and trigger no release.
- Don't squash unrelated changes into one commit — one logical change per commit.
- Default merges (`Merge pull request #N ...`) are also categorized `unknown`. Prefer **squash-merge** with a Conventional title, or rebase.

## PRs

- Run `ruff check` and `black --check` before pushing.
- Keep the PR title in Conventional Commit form too — it becomes the squash-merge subject.
