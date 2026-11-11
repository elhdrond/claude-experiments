import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from domain.entities import Cell, CellKind, Maze, Position


def _make_maze(chars: list[str]) -> Maze:
    grid: list[list[Cell]] = []
    start = end = None
    char_map = {"#": CellKind.WALL, " ": CellKind.OPEN, "S": CellKind.START, "E": CellKind.END}
    for r, line in enumerate(chars):
        row = []
        for c, ch in enumerate(line):
            kind = char_map.get(ch, CellKind.OPEN)
            pos = Position(r, c)
            if kind == CellKind.START:
                start = pos
            elif kind == CellKind.END:
                end = pos
            row.append(Cell(pos, kind))
        grid.append(row)
    return Maze(grid=grid, start=start, end=end, rows=len(grid), cols=len(grid[0]))


@pytest.fixture
def simple_maze():
    """5×5 maze with a clear path from S to E."""
    return _make_maze([
        "#####",
        "#S  #",
        "### #",
        "#E  #",
        "#####",
    ])


@pytest.fixture
def blocked_maze():
    """Maze where S and E are separated by a wall — no path exists."""
    return _make_maze([
        "#####",
        "#S###",
        "#####",
        "###E#",
        "#####",
    ])


@pytest.fixture
def trivial_maze():
    """S and E are adjacent — single step."""
    return _make_maze([
        "#####",
        "#SE #",
        "#####",
    ])
