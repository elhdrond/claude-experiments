from domain.entities import Maze, PathResult
from domain.ports import PathfinderStrategy


def compare_algorithms(maze: Maze, algorithms: list[PathfinderStrategy]) -> list[PathResult]:
    return [algorithm.find_path(maze) for algorithm in algorithms]
