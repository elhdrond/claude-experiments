import heapq
from domain.entities import CellKind, Maze, PathResult, Position
from domain.ports import PathfinderStrategy


class DijkstraPathfinder(PathfinderStrategy):
    # FR-11: all open cells have equal weight (1) — equivalent to BFS on unweighted grids
    def find_path(self, maze: Maze) -> PathResult:
        heap: list[tuple[int, int, Position, list[Position]]] = [(0, 0, maze.start, [maze.start])]
        dist: dict[Position, int] = {maze.start: 0}
        explored: set[Position] = set()
        steps = 0
        counter = 1

        while heap:
            cost, _, current, path = heapq.heappop(heap)

            if current in explored:
                continue
            explored.add(current)
            steps += 1

            if current == maze.end:
                return PathResult(
                    algorithm="Dijkstra",
                    path=path,
                    explored=explored,
                    steps=steps,
                    found=True,
                )

            for neighbour in _neighbours(current, maze):
                new_cost = cost + 1
                if new_cost < dist.get(neighbour, float("inf")):
                    dist[neighbour] = new_cost
                    heapq.heappush(heap, (new_cost, counter, neighbour, path + [neighbour]))
                    counter += 1

        return PathResult(algorithm="Dijkstra", explored=explored, steps=steps)


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
