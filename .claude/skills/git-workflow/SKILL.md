# Git Workflow Skill

You are an expert in Git version control. This project uses **GitHub Flow** — a simple, branch-based workflow.

## GitHub Flow Overview

```
main ─────●─────●─────●─────●─────●───→ (always deployable)
           \         /     \     /
            feature-a      feature-b
```

**Principles:**
- `main` is always deployable
- Create short-lived feature branches from `main`
- Open PRs for code review
- Merge to `main` and delete the branch
- Tag releases for app store submissions

## Quick Reference

### Starting New Work
```bash
git checkout main
git pull origin main
git checkout -b feature/<name>
# or
git checkout -b fix/<name>
```

### During Development
```bash
# Commit frequently
git add .
git commit -m "feat: add navigation component"

# Keep branch updated with main
git fetch origin
git rebase origin/main
```

### Completing Work
```bash
# Push and create PR
git push -u origin feature/<name>

# After PR merged on GitHub, clean up locally
git checkout main
git pull origin main
git branch -d feature/<name>
```

### Local Merges (when not using PRs)
```bash
git checkout main
git merge --no-ff feature/<name>  # Always use --no-ff to preserve history
git push origin main
git branch -d feature/<name>
```

**IMPORTANT:** Always use `--no-ff` for merges to preserve branch history in the commit graph.

### Creating Releases
```bash
git checkout main
git tag -a v1.0.0 -m "Release 1.0.0 - Initial App Store submission"
git push origin v1.0.0
```

---

## Basic Commands

### Status and Information
```bash
git status                  # Show working tree status
git log --oneline -10       # Compact recent history
git diff                    # Show unstaged changes
git diff --staged           # Show staged changes
```

### Staging and Committing
```bash
git add <file>              # Stage specific file
git add .                   # Stage all changes
git add -p                  # Interactive staging (patch mode)
git commit -m "message"     # Commit with message
```

### Remote Operations
```bash
git push                    # Push to remote
git push -u origin <branch> # Push and set upstream
git pull                    # Fetch and merge from remote
git fetch                   # Fetch without merging
```

## Branch Management

### Viewing Branches
```bash
git branch                  # List local branches
git branch -a               # List all branches (local + remote)
```

### Creating and Switching
```bash
git checkout -b <name>      # Create and switch to branch
git switch -c <name>        # Create and switch (modern syntax)
git checkout <branch>       # Switch to branch
git switch <branch>         # Switch to branch (modern)
```

### Deleting Branches
```bash
git branch -d <name>        # Delete merged branch
git branch -D <name>        # Force delete branch
git push origin --delete <name>  # Delete remote branch
```

## Undoing Changes

### Unstaging Files
```bash
git restore --staged <file> # Unstage file (keep changes)
```

### Discarding Changes
```bash
git restore <file>          # Discard file changes
git clean -fd               # Remove untracked files and directories
git clean -n                # Dry run - show what would be removed
```

### Amending Commits
```bash
git commit --amend -m "new" # Amend with new message
git commit --amend --no-edit # Amend without changing message
```

**IMPORTANT**: Only amend commits that have NOT been pushed to remote.

### Reset Modes
```bash
git reset --soft HEAD~1     # Undo commit, keep changes staged
git reset --mixed HEAD~1    # Undo commit, unstage changes (default)
git reset --hard HEAD~1     # Undo commit, discard all changes
```

### Reverting (Safe for Shared History)
```bash
git revert <commit>         # Create new commit undoing changes
git revert HEAD             # Revert most recent commit
```

## Stashing

```bash
git stash                   # Stash current changes
git stash -u                # Include untracked files
git stash list              # List all stashes
git stash pop               # Apply and remove latest stash
git stash drop              # Remove latest stash
```

## Commit Message Guidelines

Follow conventional commit format:

```
<type>: <short description>

[optional body]
```

### Types
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation changes
- `style:` — Formatting, no code change
- `refactor:` — Code restructuring
- `test:` — Adding tests
- `chore:` — Maintenance tasks

### Examples
```bash
git commit -m "feat: add bottom navigation bar"
git commit -m "fix: resolve overflow in nav bar"
git commit -m "chore: update dependencies"
```

## Safety Guidelines

### Before Destructive Operations
```bash
git status
git log --oneline -5

# Create backup branch if unsure
git branch backup-$(date +%Y%m%d)
```

### Avoid These on main
- `git push --force` (use `--force-with-lease` if absolutely necessary)
- `git reset --hard` on pushed commits
- `git rebase` on pushed commits
- `git commit --amend` on pushed commits

### Recovery
```bash
git reflog                  # View all HEAD movements
git reset --hard HEAD@{n}   # Restore to reflog entry
```

## Project-Specific Notes

### Branch Naming
- `feature/<name>` — New features
- `fix/<name>` — Bug fixes
- `chore/<name>` — Maintenance tasks

### Release Tagging
Tag format: `vMAJOR.MINOR.PATCH`
```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git tag -a v1.1.0 -m "Release 1.1.0 - Added spaced repetition"
```

### Typical Workflow
1. `git checkout main && git pull`
2. `git checkout -b feature/my-feature`
3. Make commits with conventional messages
4. `git push -u origin feature/my-feature`
5. Create PR on GitHub (or merge locally with `--no-ff`)
6. Merge PR — use "Create a merge commit" option to preserve history
7. Delete feature branch
8. Tag release when submitting to app stores
