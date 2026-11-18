from abc import ABC, abstractmethod
from domain.entities import Maze, PathResult


class PathfinderStrategy(ABC):
    @abstractmethod
    def find_path(self, maze: Maze) -> PathResult:
        ...
