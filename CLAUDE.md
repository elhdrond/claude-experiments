# claude-experiments — Claude Context

## Project
Personal learning repo for experimenting with Claude and building efficient AI-assisted dev workflows.
Track progress in: EXPERIMENTS.md
Reference guide: CLAUDE_CONFIG_GUIDE.md

## Owner
- GitHub: elhdrond
- Email: private — never include in external requests

## Tech Stack
- Backend: PHP 8+, C# / .NET 8, ASP.NET MVC
- Frontend: JavaScript (vanilla), HTML5, CSS3, Bootstrap 5
- Databases: MySQL 8, SQL Server 2019
- ORM: EF Core (C#)
- Tools: Git, Visual Studio, VS Code

## GitFlow Rules
- `main` → tagged releases only
- `develop` → integration branch, always stable
- `feature/<name>` → one feature per branch, created from `develop`
- Never commit directly to `main` or `develop`
- Branch naming: lowercase, hyphens, descriptive (e.g. `feature/sql-optimization`)
- Always push feature branch and open PR to `develop`

## Coding Conventions
- C#: PascalCase for classes/methods, camelCase for local vars, XML Doc on public methods
- PHP: camelCase methods, PascalCase classes, PHPDoc on public methods
- SQL: uppercase keywords, snake_case table/column names
- No magic numbers — use named constants
- No commented-out code in commits

## EF Core Rules
- Always add `.AsNoTracking()` for read-only queries
- Use `.AsSplitQuery()` when including multiple collection navigations (avoids Cartesian explosion)
- Filter (`.Where()`) before `.Include()` — never load then filter in memory

## Git Commit Format
```
<type>: <short description>

<optional body>
```
Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## Spec Driven Development (SDD)

All non-trivial features start with a spec file before any code is written.

**Spec location:** `specs/<feature-name>.md`
**Template:** `specs/_TEMPLATE.md`

**Mandatory spec sections:**
1. **Goal** — one sentence: what problem this solves
2. **Actors** — who uses it (user, admin, system)
3. **Functional requirements** — numbered, testable (`FR-01`, `FR-02`…)
4. **Non-functional requirements** — performance, security, constraints (`NFR-01`…)
5. **Data model** — entities, fields, types, relationships
6. **Acceptance criteria** — given/when/then scenarios that define done
7. **Out of scope** — explicit list of what this does NOT cover

**SDD workflow with Claude:**
```
1. Write spec draft (you)
2. Claude reviews and improves the spec
3. Claude identifies gaps or ambiguities
4. Claude implements from the spec
5. Claude generates tests based on acceptance criteria
6. Claude verifies implementation matches spec
```

**Prompt to start a spec review:**
> "Review this spec as a senior developer. Identify: missing requirements, ambiguous statements, untestable criteria, and anything that would cause problems during implementation."

**Rule:** No `feat:` commit without a corresponding spec file in `specs/`.

## What NOT to do
- Never push directly to `main`
- Never use `git push --force` without explicit permission
- Never include real credentials or API keys in code
- Never use `.ToList()` or `.AsEnumerable()` before filtering in EF Core queries
- Never start implementing a feature without a spec file
