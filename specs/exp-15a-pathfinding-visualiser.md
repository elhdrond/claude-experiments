# Spec: Pathfinding Visualiser — BFS, DFS, A\*, Dijkstra

> **Status:** Draft | In Review | Approved | **Implemented**
> **Date:** 2026-11-11
> **Author:** elhdrond / Claude

---

## 1. Goal

Demonstrate and compare four classic pathfinding algorithms (BFS, DFS, A\*, Dijkstra)
on the same maze, producing a self-contained HTML report that shows — side by side —
how each algorithm explores the space and the path it finds.

---

## 2. Actors

| Actor  | Description                                                                      |
| ------ | -------------------------------------------------------------------------------- |
| User   | Developer who runs the script locally to learn how pathfinding algorithms differ |
| System | Python script that generates the HTML report                                     |

---

## 3. Functional Requirements

| ID    | Requirement                                                                                                                                                                                    | Priority |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| FR-01 | The system shall load a maze from a plain-text file (`maze.txt`) where `#` = wall, ` ` = open cell, `S` = start, `E` = end.                                                                    | Must     |
| FR-02 | The system shall implement BFS, DFS, A\* and Dijkstra as independent, interchangeable pathfinding strategies.                                                                                  | Must     |
| FR-03 | Each algorithm shall return: the path found (ordered list of cells), the set of explored cells, and the number of steps taken to find the path.                                                | Must     |
| FR-04 | The system shall generate a self-contained `output.html` file showing all four algorithm results side by side, one panel per algorithm.                                                        | Must     |
| FR-05 | Each panel shall colour-code cells: start (blue), end (blue), wall (dark), explored but not on path (light orange), path (green), unexplored (white).                                          | Must     |
| FR-06 | Each panel shall display a summary: algorithm name, path length, cells explored, and whether a path was found.                                                                                 | Must     |
| FR-07 | The system shall open `output.html` automatically in the default browser after generation.                                                                                                     | Must     |
| FR-08 | The system shall exit with code 1 and a descriptive error if `maze.txt` is missing, malformed (no S or E), or S and E are the same cell.                                                       | Must     |
| FR-09 | The system shall include a default `maze.txt` so the script works out of the box without manual setup.                                                                                         | Must     |
| FR-10 | A\* shall use Manhattan distance as its heuristic function.                                                                                                                                    | Must     |
| FR-11 | Dijkstra shall treat all open cells as having equal weight (1), making it equivalent to BFS on unweighted grids — the difference in explored cells may be visible depending on implementation. | Should   |

---

## 4. Non-Functional Requirements

| ID     | Requirement  | Metric                                                                                                                                                                           |
| ------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NFR-01 | Performance  | Completes in < 5 s for mazes up to 50×50 cells                                                                                                                                   |
| NFR-02 | Portability  | No dependencies beyond Python standard library + one optional package for HTML templating if needed                                                                              |
| NFR-03 | Architecture | Must follow Clean Architecture: domain entities have zero external imports; infrastructure layer contains all algorithm implementations; interface layer handles HTML generation |
| NFR-04 | Testability  | Each algorithm is independently testable with a simple grid — no HTML or file I/O required in unit tests                                                                         |

---

## 5. Data Model

```
Domain entities (no external imports):

  Position:
    row: int
    col: int

  Cell:
    position: Position
    kind: Enum(OPEN, WALL, START, END)

  Maze:
    grid: list[list[Cell]]
    start: Position
    end: Position
    rows: int
    cols: int

  PathResult:
    algorithm: str
    path: list[Position]        # ordered from start to end; empty if no path
    explored: set[Position]     # all cells the algorithm visited
    steps: int                  # total iterations until path found or exhausted
    found: bool

Use cases:
  FindPath(maze: Maze, algorithm: PathfinderStrategy) → PathResult
  CompareAlgorithms(maze: Maze, algorithms: list[PathfinderStrategy]) → list[PathResult]

Infrastructure (implements PathfinderStrategy interface):
  BFSPathfinder
  DFSPathfinder
  AStarPathfinder
  DijkstraPathfinder

Interface:
  MazeLoader        — reads maze.txt → Maze
  HTMLReportBuilder — list[PathResult] + Maze → output.html
```

---

## 6. Acceptance Criteria

```
Scenario: Happy path — path exists
  Given a valid maze.txt with a reachable path from S to E
  When  the script is run (python main.py)
  Then  output.html is generated with four panels (one per algorithm)
  And   each panel shows the maze with colour-coded cells
  And   BFS and A* find the shortest path
  And   DFS finds a valid path (not necessarily shortest)
  And   each panel shows path length, cells explored, and found=True
  And   the browser opens automatically
```

```
Scenario: No path exists
  Given a maze.txt where S and E are separated by walls with no opening
  When  the script is run
  Then  output.html is generated
  And   each panel shows found=False and an empty path
  And   explored cells show how far each algorithm got before giving up
```

```
Scenario: Missing maze file
  Given maze.txt does not exist in the script directory
  When  the script is run
  Then  the script exits with code 1
  And   prints a message indicating maze.txt was not found
```

```
Scenario: Malformed maze — missing S or E
  Given a maze.txt that contains no S or no E marker
  When  the script is run
  Then  the script exits with code 1
  And   prints a message indicating which marker is missing
```

---

## 7. Out of Scope

- Animated step-by-step exploration (static snapshot only)
- User-editable mazes via UI
- Weighted edges (all open cells have equal cost)
- Diagonal movement (only up/down/left/right)
- Maze generation algorithms
- Saving results to a database or file other than output.html

---

## 8. Open Questions

- [x] Should DFS use recursive or iterative implementation?
      **Resolved:** Iterative — avoids Python recursion limits on large mazes.
- [x] Should the default maze be hand-crafted or generated?
      **Resolved:** Auto-generated by Claude and included as a static `maze.txt` file (no runtime generation algorithm needed).

---

## 9. Implementation Notes

- **Approach:** Clean Architecture — domain entities with zero external imports; four independent algorithm classes in infrastructure; use cases orchestrate; interface layer builds self-contained HTML.
- **DFS decision:** Iterative (stack-based) to avoid Python recursion limits on large mazes.
- **Default maze:** Hand-designed 20×20 maze included as `maze.txt` (FR-09).
- **Files created:**
  - `main.py` — entry point
  - `maze.txt` — default maze
  - `domain/entities.py` — Position, Cell, CellKind, Maze, PathResult
  - `domain/ports.py` — PathfinderStrategy ABC
  - `use_cases/find_path.py` — FindPath use case
  - `use_cases/compare_algorithms.py` — CompareAlgorithms use case
  - `infrastructure/maze_loader.py` — MazeLoader
  - `infrastructure/bfs.py` — BFSPathfinder
  - `infrastructure/dfs.py` — DFSPathfinder (iterative)
  - `infrastructure/astar.py` — AStarPathfinder (Manhattan heuristic)
  - `infrastructure/dijkstra.py` — DijkstraPathfinder (equal weights)
  - `interface/html_report.py` — HTMLReportBuilder
  - `tests/` — 35 tests (100% pass)

### Proposed project structure (Clean Architecture)

```
exp-15a-pathfinding-visualiser/
├── main.py                        ← entry point: load maze, run algorithms, generate HTML
├── maze.txt                       ← default maze (FR-09)
├── domain/
│   ├── __init__.py
│   ├── entities.py                ← Position, Cell, CellKind, Maze, PathResult
│   └── ports.py                   ← PathfinderStrategy (abstract base class)
├── use_cases/
│   ├── __init__.py
│   ├── find_path.py               ← FindPath use case
│   └── compare_algorithms.py      ← CompareAlgorithms use case
├── infrastructure/
│   ├── __init__.py
│   ├── maze_loader.py             ← reads maze.txt → Maze
│   ├── bfs.py                     ← BFSPathfinder
│   ├── dfs.py                     ← DFSPathfinder
│   ├── astar.py                   ← AStarPathfinder
│   └── dijkstra.py                ← DijkstraPathfinder
├── interface/
│   ├── __init__.py
│   └── html_report.py             ← HTMLReportBuilder → output.html
└── tests/
    ├── conftest.py
    ├── test_bfs.py
    ├── test_dfs.py
    ├── test_astar.py
    ├── test_dijkstra.py
    └── test_maze_loader.py
```

### Dependency rule (Clean Architecture)

```
interface → use_cases → domain  ✅
infrastructure → domain         ✅
domain → anything else          ❌ never
```
