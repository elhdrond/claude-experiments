import sys
from pathlib import Path
from domain.entities import Cell, CellKind, Maze, Position

_CHAR_MAP = {
    "#": CellKind.WALL,
    " ": CellKind.OPEN,
    "S": CellKind.START,
    "E": CellKind.END,
}


def load_maze(path: Path) -> Maze:
    # FR-08: file missing
    if not path.exists():
        print(f"Error: maze file not found: {path}", file=sys.stderr)
        sys.exit(1)

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        print("Error: maze file is empty", file=sys.stderr)
        sys.exit(1)

    grid: list[list[Cell]] = []
    start: Position | None = None
    end: Position | None = None

    for r, line in enumerate(lines):
        row: list[Cell] = []
        for c, ch in enumerate(line):
            kind = _CHAR_MAP.get(ch, CellKind.OPEN)
            pos = Position(r, c)
            if kind == CellKind.START:
                start = pos
            elif kind == CellKind.END:
                end = pos
            row.append(Cell(pos, kind))
        grid.append(row)

    # FR-08: missing S or E
    if start is None:
        print("Error: maze has no start marker 'S'", file=sys.stderr)
        sys.exit(1)
    if end is None:
        print("Error: maze has no end marker 'E'", file=sys.stderr)
        sys.exit(1)

    # FR-08: S and E same cell
    if start == end:
        print("Error: start and end are the same cell", file=sys.stderr)
        sys.exit(1)

    rows = len(grid)
    cols = max(len(row) for row in grid)
    return Maze(grid=grid, start=start, end=end, rows=rows, cols=cols)
