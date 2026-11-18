# claude-experiments

Personal learning repository for experimenting with Claude and building efficient AI-assisted development workflows.

## About

This repo tracks hands-on experiments across different areas of AI-assisted development, using **Spec Driven Development (SDD)** and **Clean Architecture** as core methodologies.

Each experiment has a spec file, an implementation, and a test suite.

## Structure

```
claude-experiments/
├── CLAUDE.md                        ← project memory loaded by Claude every session
├── EXPERIMENTS.md                   ← experiment tracking log
├── specs/                           ← spec files (one per experiment)
├── exp-13-gbp-eur-converter/        ← GBP→EUR historical converter
└── exp-15a-pathfinding-visualiser/  ← pathfinding visualiser (BFS, DFS, A*, Dijkstra)
```

## Experiments

| ID | Title | Status | Stack |
|----|-------|--------|-------|
| EXP-13 | GBP→EUR Historical Converter | ✅ Done | Python · frankfurter.app API |
| EXP-15A | Pathfinding Visualiser | ✅ Done | Python · Clean Architecture |
| EXP-15B | Mini Search Engine | ⬜ To do | Python · Clean Architecture |

Full tracking in [EXPERIMENTS.md](./EXPERIMENTS.md).

## Methodology

**Spec Driven Development (SDD):**
1. Write spec (`specs/<name>.md`) before any code
2. Review and approve the spec
3. Implement strictly from the spec
4. Generate tests from acceptance criteria
5. Verify implementation matches spec

**Clean Architecture (Python):**
```
domain/          ← entities, zero external imports
use_cases/       ← orchestration
infrastructure/  ← I/O, algorithms, external services
interface/       ← HTML output, CLI
```

## Setup

```bash
git clone https://github.com/elhdrond/claude-experiments
cd claude-experiments

# EXP-13
cd exp-13-gbp-eur-converter
pip install requests python-dotenv pytest
cp .env.example .env   # set GBP_AMOUNT
python converter.py

# EXP-15A
cd exp-15a-pathfinding-visualiser
python main.py
```

## GitFlow

- `main` → tagged releases
- `develop` → integration branch
- `feature/<name>` → one feature per branch, PR into develop
