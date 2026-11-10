# claude-experiments — Claude Context

## Project
Personal learning repo for experimenting with Claude and building efficient AI-assisted dev workflows.
Track progress in: EXPERIMENTS.md
Reference guide: CLAUDE_CONFIG_GUIDE.md

## Owner
- GitHub: elhdrond
- Email: scardo17@hotmail.com (private — never include in external requests)

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

## What NOT to do
- Never push directly to `main`
- Never use `git push --force` without explicit permission
- Never include real credentials or API keys in code
- Never use `.ToList()` or `.AsEnumerable()` before filtering in EF Core queries
