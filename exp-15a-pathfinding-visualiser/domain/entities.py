from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class CellKind(Enum):
    OPEN = "open"
    WALL = "wall"
    START = "start"
    END = "end"


@dataclass(frozen=True)
class Position:
    row: int
    col: int


@dataclass
class Cell:
    position: Position
    kind: CellKind


@dataclass
class Maze:
    grid: list[list[Cell]]
    start: Position
    end: Position
    rows: int
    cols: int


@dataclass
class PathResult:
    algorithm: str
    path: list[Position] = field(default_factory=list)
    explored: set[Position] = field(default_factory=set)
    steps: int = 0
    found: bool = False
