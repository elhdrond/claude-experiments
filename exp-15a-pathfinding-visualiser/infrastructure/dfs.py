from domain.entities import CellKind, Maze, PathResult, Position
from domain.ports import PathfinderStrategy


class DFSPathfinder(PathfinderStrategy):
    # FR-02 / open question resolved: iterative to avoid Python recursion limits
    def find_path(self, maze: Maze) -> PathResult:
        stack: list[tuple[Position, list[Position]]] = [(maze.start, [maze.start])]
        visited: set[Position] = {maze.start}
        explored: set[Position] = set()
        steps = 0

        while stack:
            current, path = stack.pop()
            explored.add(current)
            steps += 1

            if current == maze.end:
                return PathResult(
                    algorithm="DFS",
                    path=path,
                    explored=explored,
                    steps=steps,
                    found=True,
                )

            for neighbour in _neighbours(current, maze):
                if neighbour not in visited:
                    visited.add(neighbour)
                    stack.append((neighbour, path + [neighbour]))

        return PathResult(algorithm="DFS", explored=explored, steps=steps)


def _neighbours(pos: Position, maze: Maze) -> list[Position]:
    candidates = [
        Position(pos.row - 1, pos.col),
        Position(pos.row + 1, pos.col),
        Position(pos.row, pos.col - 1),
        Position(pos.row, pos.col + 1),
    ]
    result = []
    for p in candidates:
        if 0 <= p.row < maze.rows and 0 <= p.col < len(maze.grid[p.row]):
            cell = maze.grid[p.row][p.col]
            if cell.kind != CellKind.WALL:
                result.append(p)
    return result
