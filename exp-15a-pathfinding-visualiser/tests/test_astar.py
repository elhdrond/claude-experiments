from infrastructure.astar import AStarPathfinder, _manhattan
from domain.entities import Position


class TestManhattan:
    def test_same_cell(self):
        assert _manhattan(Position(0, 0), Position(0, 0)) == 0

    def test_horizontal(self):
        assert _manhattan(Position(0, 0), Position(0, 4)) == 4

    def test_vertical(self):
        assert _manhattan(Position(0, 0), Position(3, 0)) == 3

    def test_diagonal(self):
        assert _manhattan(Position(0, 0), Position(3, 4)) == 7


class TestAStarHappyPath:
    def test_finds_path(self, simple_maze):
        result = AStarPathfinder().find_path(simple_maze)
        assert result.found is True

    def test_path_starts_at_start(self, simple_maze):
        result = AStarPathfinder().find_path(simple_maze)
        assert result.path[0] == simple_maze.start

    def test_path_ends_at_end(self, simple_maze):
        result = AStarPathfinder().find_path(simple_maze)
        assert result.path[-1] == simple_maze.end

    def test_finds_shortest_path(self, trivial_maze):
        result = AStarPathfinder().find_path(trivial_maze)
        assert result.found is True
        assert len(result.path) == 2


class TestAStarNoPath:
    def test_returns_not_found(self, blocked_maze):
        result = AStarPathfinder().find_path(blocked_maze)
        assert result.found is False

    def test_path_is_empty(self, blocked_maze):
        result = AStarPathfinder().find_path(blocked_maze)
        assert result.path == []
