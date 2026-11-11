from domain.entities import Maze, PathResult
from domain.ports import PathfinderStrategy


def find_path(maze: Maze, algorithm: PathfinderStrategy) -> PathResult:
    return algorithm.find_path(maze)
