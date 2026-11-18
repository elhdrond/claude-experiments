from infrastructure.dijkstra import DijkstraPathfinder


class TestDijkstraHappyPath:
    def test_finds_path(self, simple_maze):
        result = DijkstraPathfinder().find_path(simple_maze)
        assert result.found is True

    def test_path_starts_at_start(self, simple_maze):
        result = DijkstraPathfinder().find_path(simple_maze)
        assert result.path[0] == simple_maze.start

    def test_path_ends_at_end(self, simple_maze):
        result = DijkstraPathfinder().find_path(simple_maze)
        assert result.path[-1] == simple_maze.end

    def test_finds_shortest_path(self, trivial_maze):
        result = DijkstraPathfinder().find_path(trivial_maze)
        assert result.found is True
        assert len(result.path) == 2


class TestDijkstraNoPath:
    def test_returns_not_found(self, blocked_maze):
        result = DijkstraPathfinder().find_path(blocked_maze)
        assert result.found is False

    def test_path_is_empty(self, blocked_maze):
        result = DijkstraPathfinder().find_path(blocked_maze)
        assert result.path == []
