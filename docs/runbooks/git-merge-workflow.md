# Git Merge Workflow Guide

Here's the standard process for merging any branch:

```bash
# 1. Make sure you're on a clean state
git status

# 2. Update everything from remote
git fetch origin

# 3. Switch to the branch you want to merge INTO
git checkout main

# 4. (Optional) Pull latest changes for main
git pull origin main

# 5. Merge the other branch
git merge origin/BranchName
# OR if it's a local branch:
git merge BranchName

# 6. If there are conflicts, resolve them:
#    - Edit the conflicted files
#    - git add <resolved-files>
#    - git commit

# 7. Push the merged changes
git push origin main
```

---

## Key Concepts

### Local vs Remote Branches

- `GiaGia` = local branch on your machine
- `origin/GiaGia` = remote branch on GitHub
- Use `origin/BranchName` to merge from GitHub directly

### Merge vs Rebase

**Merge:** Combines branches, creates a merge commit
- **Pros:** Safe, preserves history, easy to understand
- **Cons:** Creates extra merge commits
- **Use when:** Working on a team, merging feature branches

**Rebase:** Replays commits on top of another branch
- **Pros:** Clean linear history
- **Cons:** Rewrites history, can cause conflicts
- **Use when:** Cleaning up your own local commits before pushing

**For team collaboration, merging is usually safer than rebasing.**

---

## Handling Merge Conflicts

If the merge has conflicts, you'll see:

```bash
git merge origin/GiaGia
# CONFLICT (content): Merge conflict in file.md
```

### To Resolve Conflicts:

**1. Open the conflicted file in editor**

Look for conflict markers:
```
<<<<<<< HEAD
your changes
=======
their changes
>>>>>>> origin/GiaGia
```

**2. Edit to keep what you want, remove markers**

Choose one version or combine both, then delete the `<<<<<<<`, `=======`, and `>>>>>>>` lines.

**3. Stage the resolved file**
```bash
git add file.md
```

**4. Complete the merge**
```bash
git commit
```

**5. Push**
```bash
git push origin main
```

### Aborting a Merge

If you want to cancel the merge and start over:
```bash
git merge --abort
```

---

## Quick Reference Commands

### Branch Management
```bash
# See what branches exist
git branch -a

# See current branch
git branch

# Create and switch to new branch
git checkout -b new-branch-name

# Switch to existing branch
git checkout branch-name
```

### Viewing Changes
```bash
# See branch differences (files changed)
git diff main..other-branch --stat

# See detailed differences
git diff main..other-branch

# See commit history
git log --oneline --graph --all

# See what's different between branches
git log main..other-branch
```

### Merging
```bash
# Merge another branch into current
git merge other-branch

# Merge with default commit message
git merge other-branch --no-edit

# Merge remote branch
git merge origin/branch-name
```

### Aborting Operations
```bash
# Abort a merge in progress
git merge --abort

# Abort a rebase in progress
git rebase --abort

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes - DANGER!)
git reset --hard HEAD~1
```

### Remote Operations
```bash
# Fetch latest from remote (doesn't merge)
git fetch origin

# Pull = fetch + merge
git pull origin main

# Push to remote
git push origin branch-name

# See remote branches
git branch -r

# See all branches (local + remote)
git branch -a
```

---

## Common Scenarios

### Scenario 1: Merge teammate's branch into main

```bash
git fetch origin                    # Get latest from GitHub
git checkout main                   # Switch to main
git pull origin main               # Update main
git merge origin/teammate-branch   # Merge their work
git push origin main               # Push merged result
```

### Scenario 2: Update your feature branch with latest main

```bash
git checkout main                  # Switch to main
git pull origin main              # Get latest main
git checkout your-feature-branch  # Switch to your branch
git merge main                    # Merge main into your branch
# Resolve any conflicts
git push origin your-feature-branch
```

### Scenario 3: Merge your local work to main

```bash
git checkout main                 # Switch to main
git pull origin main             # Get latest
git merge your-feature-branch   # Merge your work
# Resolve any conflicts
git push origin main            # Push to remote
```

### Scenario 4: You have conflicts - step by step

```bash
git merge other-branch
# CONFLICT appears

# 1. Check which files have conflicts
git status

# 2. Open each conflicted file and fix it
#    (remove <<<, ===, >>> markers and choose what to keep)

# 3. Add resolved files
git add file1.md file2.md

# 4. Check status - should say "all conflicts fixed"
git status

# 5. Complete the merge
git commit

# 6. Push
git push origin main
```

---

## Best Practices

1. **Always fetch before merging** - Know what you're getting
   ```bash
   git fetch origin
   ```

2. **Check git status first** - Make sure working tree is clean
   ```bash
   git status
   ```

3. **Communicate with team** - Let them know you're merging

4. **Test after merging** - Make sure everything still works

5. **Use descriptive merge commit messages** - Explain what you merged and why

6. **Pull before push** - Update your branch before pushing
   ```bash
   git pull origin main
   git push origin main
   ```

7. **Don't force push to shared branches** - Especially main
   ```bash
   git push --force  # DON'T DO THIS on main!
   ```

8. **Create backups of important branches**
   ```bash
   git checkout -b backup-branch-name
   ```

---

## Troubleshooting

### "Your branch has diverged"
```bash
# Your local and remote have different commits
git fetch origin
git log --oneline --graph --all  # Visualize the divergence

# Option 1: Merge remote changes
git pull origin main

# Option 2: Rebase (if you haven't pushed yet)
git pull --rebase origin main
```

### "Please commit your changes or stash them"
```bash
# You have uncommitted work
# Option 1: Commit it
git add .
git commit -m "WIP: saving work"

# Option 2: Stash it temporarily
git stash
# Do your merge
git stash pop  # Restore your work
```

### "Already up to date"
```bash
# The branch you're merging is already in your history
# This is fine - nothing to do
```

### Merge created unwanted files
```bash
# Undo the merge
git reset --hard HEAD~1

# Or undo but keep the files
git reset --soft HEAD~1
```

---

## Visual Guide

### What a Merge Looks Like

**Before merge:**
```
main:          A---B---C
                        \
other-branch:            D---E
```

**After merge:**
```
main:          A---B---C-------M
                        \     /
other-branch:            D---E
```

M = merge commit that combines both histories

---

## When to Ask for Help

- You see "CONFLICT" and don't know which version to keep
- You accidentally merged the wrong branch
- You force-pushed and broke the remote branch
- Git says "detached HEAD state"
- You deleted commits you needed

**Pro tip:** If something goes wrong, DON'T PANIC. Git rarely loses data permanently. Ask for help before trying random commands.
