import heapq
from domain.entities import CellKind, Maze, PathResult, Position
from domain.ports import PathfinderStrategy


def _manhattan(a: Position, b: Position) -> int:
    # FR-10: Manhattan distance heuristic
    return abs(a.row - b.row) + abs(a.col - b.col)


class AStarPathfinder(PathfinderStrategy):
    def find_path(self, maze: Maze) -> PathResult:
        # heap entries: (f, g, position, path)
        start_h = _manhattan(maze.start, maze.end)
        heap: list[tuple[int, int, int, Position, list[Position]]] = [
            (start_h, 0, 0, maze.start, [maze.start])
        ]
        visited: set[Position] = set()
        explored: set[Position] = set()
        steps = 0
        counter = 1  # tie-breaker

        while heap:
            f, g, _, current, path = heapq.heappop(heap)

            if current in visited:
                continue
            visited.add(current)
            explored.add(current)
            steps += 1

            if current == maze.end:
                return PathResult(
                    algorithm="A*",
                    path=path,
                    explored=explored,
                    steps=steps,
                    found=True,
                )

            for neighbour in _neighbours(current, maze):
                if neighbour not in visited:
                    new_g = g + 1
                    h = _manhattan(neighbour, maze.end)
                    heapq.heappush(heap, (new_g + h, new_g, counter, neighbour, path + [neighbour]))
                    counter += 1

        return PathResult(algorithm="A*", explored=explored, steps=steps)


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
