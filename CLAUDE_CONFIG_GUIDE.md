# Claude Configuration Guide

> Practical reference for configuring and using Claude Code efficiently as a developer.

---

## 1. CLAUDE.md — Project Memory

`CLAUDE.md` is a Markdown file that Claude reads automatically at the start of every session. It is your persistent project context — no need to repeat the same instructions every time.

**Where to place it:**

| Location | Scope |
|----------|-------|
| `<repo-root>/CLAUDE.md` | Applies to that project only |
| `~/.claude/CLAUDE.md` | Applies to every project (global) |

**What to include:**

- Tech stack and framework versions
- Coding conventions (naming, indentation, patterns to avoid)
- Project structure overview
- Workflow rules ("always use GitFlow", "never push to main directly")
- Context the model would otherwise have to rediscover each session

**Example:**

```markdown
# My Project — Claude Context

## Stack
- PHP 8.2 / Laravel 11
- C# / .NET 8 / ASP.NET MVC
- MySQL 8 · SQL Server 2019
- Bootstrap 5 · JavaScript (vanilla)

## Rules
- GitFlow: feature/* → develop → main
- Never use AsEnumerable() before filtering in EF Core
- PHPDoc on all public methods

## Contacts
- Repo: github.com/elhdrond/claude-experiments
```

**Tips:**
- Keep it short and dense — Claude reads it every session, long files waste tokens
- Use bullet points, not prose
- Update it when the project evolves

---

## 2. settings.json — Permissions & Hooks

`.claude/settings.json` controls what Claude can do automatically without asking for permission, and what shell commands run on specific events (hooks).

**Location:**

| Path | Scope |
|------|-------|
| `<repo>/.claude/settings.json` | Project-level |
| `~/.claude/settings.json` | Global (all projects) |

**Permissions example — allow read-only bash without prompts:**

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git log*)",
      "Bash(git diff*)",
      "Bash(cat *)",
      "Bash(ls *)"
    ],
    "deny": [
      "Bash(git push --force*)",
      "Bash(rm -rf*)"
    ]
  }
}
```

**Hooks example — run tests after every file edit:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[Hook] File edited: checking syntax...'"
          }
        ]
      }
    ]
  }
}
```

**Available hook events:** `PreToolUse`, `PostToolUse`, `Notification`, `Stop`

---

## 3. Slash Commands

Type these directly in the Claude Code chat at any time:

| Command | What it does |
|---------|-------------|
| `/compact` | Summarises the conversation and frees context — use when the session gets long |
| `/clear` | Resets context completely — fresh start |
| `/help` | Lists all available commands |
| `/model` | Switch model mid-session (e.g. from Sonnet to Opus) |
| `/plan` | Toggle plan mode on/off |
| `/fast` | Toggle fast mode (faster output, may change model) |
| `/memory` | View or edit Claude's memory for the current project |
| `/permissions` | Open the permission mode picker |

**When to use `/compact` vs `/clear`:**
- `/compact` → keeps the conversation history as a summary, session continues
- `/clear` → wipes everything, start over (use for unrelated new tasks)

---

## 4. Plan Mode

Plan mode makes Claude **propose a plan before executing**. You review and approve (or reject) before any file is changed or command is run.

**How to activate:**
- Type `/plan` in chat
- Or toggle the plan switch in the Claude Code UI

**When to use it:**
- Multi-file changes where order matters
- Refactors that touch core logic
- Any task where you want to review the approach before Claude starts
- Destructive operations (deleting files, resetting branches)

**Workflow in plan mode:**
1. You describe the task
2. Claude explores and writes a plan
3. You review the plan — ask questions, request changes
4. You approve → Claude executes
5. Plan mode stays on for the next task

**Tip:** Plan mode is especially useful when starting a new feature. Turn it off for quick fixes and one-liners.

---

## 5. Prompt Engineering for Daily Dev Workflow

You do not need to master prompt engineering — a few habits make a big difference.

### Give context upfront

Bad:
> "Fix the bug"

Good:
> "In this C# ASP.NET MVC controller, the `GetCommissions` method returns a Cartesian explosion when loading related entities via EF Core. Fix it using `.AsSplitQuery()` and `.AsNoTracking()`."

### Paste real code, not descriptions

Claude works best with the actual code in front of it. Paste the function, the error message, the SQL query. Descriptions introduce ambiguity.

### Be specific about the output format

> "Return only the modified method, not the full class."
> "Give me the SQL with an explanation of each change as a comment."
> "Output a markdown table comparing the before/after."

### Chain-of-thought for complex problems

For analysis or architecture decisions, ask Claude to reason step by step:

> "Think through the tradeoffs of using a split query vs a single query for this relationship, then give me your recommendation."

### Iteration over perfection

Start with a broad request, then refine:
1. "Refactor this function" → review result
2. "Now add error handling for null inputs" → review
3. "Add PHPDoc comments" → done

This is faster than writing the perfect prompt upfront.

### Useful prompt templates

**Code review:**
```
Review this [language] code as a senior developer.
Check for: bugs, security issues, performance problems, style issues.
Be direct. Flag the 3 most important things first.

[paste code]
```

**SQL optimisation:**
```
Analyse this SQL query on [MySQL/SQL Server].
Identify bottlenecks and propose an optimised version.
Explain each change with a comment.

[paste query]
```

**Unit tests:**
```
Write [PHPUnit/xUnit] tests for this function.
Cover: happy path, edge cases (null, empty, boundary values), error scenarios.
Use realistic values, not "test123".

[paste function]
```

---

## 6. Context Management

Each Claude session has a token limit. When you approach it, the session slows down or gets cut off.

**Signs the context is getting full:**
- Responses get slower
- Claude starts forgetting earlier parts of the conversation
- You see a "context limit" warning

**Strategies:**

| Strategy | When to use |
|----------|-------------|
| `/compact` | Session is long but you want to continue the same task |
| `/clear` | Starting a completely different task |
| Split tasks into sessions | For large features — plan in one session, implement in another |
| Keep CLAUDE.md updated | So context from previous sessions is not lost |

**Golden rule:** One session = one focused task. Do not try to do everything in one conversation.

**For large repos:** Use `CLAUDE.md` to give Claude a map of the codebase. Otherwise it has to rediscover structure every session.

---

## Quick Reference Card

```
CLAUDE.md       → persistent project context (read every session)
settings.json   → auto-permissions + hooks
/compact        → summarise + free context
/clear          → reset everything
/plan           → review before execute
/model          → switch model
context tip     → one task per session, use /compact often
prompt tip      → paste real code, give context, be specific
```

---

*Last updated: 2026-11-10*
