# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a practice project for setting up and testing CodeRabbit integration.

## Purpose

- Configure CodeRabbit for automated code reviews
- Test CodeRabbit's functionality and features
- Experiment with CodeRabbit configuration options

## CodeRabbit CLI Integration

CodeRabbit CLI is installed globally and available for all projects.

### Authentication
Already authenticated. If re-authentication is needed:
```bash
coderabbit auth login
```

### Usage with Claude Code

CodeRabbit is NOT called automatically. Explicitly request it when needed.

**Example prompts:**
- "Implement [feature] then run coderabbit --prompt-only and fix any issues"
- "Review the current changes with coderabbit --plain"

### Common Commands

```bash
# Token-efficient review (optimized for AI)
coderabbit --prompt-only

# Detailed review with full feedback
coderabbit --plain

# Review only uncommitted changes
coderabbit --type uncommitted

# Review all changes
coderabbit --type all

# Specify base branch for comparison
coderabbit --base develop

# Check auth status
coderabbit auth status
```

### When to Use --type Option

**`--type uncommitted`** (default in most cases)
- Use when: You have existing committed code and made new changes
- Reviews: Only the working directory changes (unstaged + staged)
- Best for: Incremental development, feature additions

**`--type all`**
- Use when: You want to review the entire codebase
- Reviews: All changes in the repository
- Best for: Initial project review, major refactoring

**No `--type` flag**
- If new project with no commits: Same as `--type all`
- If existing project: Defaults to `--type uncommitted`

### Recommended Workflow

**IMPORTANT: Review BEFORE committing**

1. **Implement code/feature** - Write your code
2. **Review with CodeRabbit** - Run review on uncommitted changes
   ```bash
   coderabbit --prompt-only --type uncommitted
   ```
3. **Fix issues** - Claude creates task list from findings and fixes them systematically
4. **Commit clean code** - After all fixes are applied, commit the polished code

**Why review before commit:**
- Fix issues before they enter git history
- Avoid multiple fix commits
- Catch problems before CI/CD
- Keep commit history clean

**Typical prompt:**
```
Implement [feature] then run coderabbit --prompt-only --type uncommitted
and fix any issues before committing
```
