import sys
import pytest
from pathlib import Path
from domain.entities import CellKind, Position


def test_loads_valid_maze(tmp_path):
    from infrastructure.maze_loader import load_maze
    f = tmp_path / "maze.txt"
    f.write_text("#####\n#S E#\n#####\n")
    maze = load_maze(f)
    assert maze.start == Position(1, 1)
    assert maze.end == Position(1, 3)
    assert maze.rows == 3
    assert maze.cols == 5


def test_missing_file_exits_1(tmp_path):
    from infrastructure.maze_loader import load_maze
    with pytest.raises(SystemExit) as exc:
        load_maze(tmp_path / "nonexistent.txt")
    assert exc.value.code == 1


def test_missing_start_exits_1(tmp_path):
    from infrastructure.maze_loader import load_maze
    f = tmp_path / "maze.txt"
    f.write_text("#####\n#  E#\n#####\n")
    with pytest.raises(SystemExit) as exc:
        load_maze(f)
    assert exc.value.code == 1


def test_missing_end_exits_1(tmp_path):
    from infrastructure.maze_loader import load_maze
    f = tmp_path / "maze.txt"
    f.write_text("#####\n#S  #\n#####\n")
    with pytest.raises(SystemExit) as exc:
        load_maze(f)
    assert exc.value.code == 1


def test_walls_parsed_correctly(tmp_path):
    from infrastructure.maze_loader import load_maze
    f = tmp_path / "maze.txt"
    f.write_text("#####\n#S E#\n#####\n")
    maze = load_maze(f)
    assert maze.grid[0][0].kind == CellKind.WALL
    assert maze.grid[1][1].kind == CellKind.START
    assert maze.grid[1][2].kind == CellKind.OPEN
    assert maze.grid[1][3].kind == CellKind.END
