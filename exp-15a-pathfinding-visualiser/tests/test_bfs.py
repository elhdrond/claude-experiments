from infrastructure.bfs import BFSPathfinder


class TestBFSHappyPath:
    def test_finds_path(self, simple_maze):
        result = BFSPathfinder().find_path(simple_maze)
        assert result.found is True

    def test_path_starts_at_start(self, simple_maze):
        result = BFSPathfinder().find_path(simple_maze)
        assert result.path[0] == simple_maze.start

    def test_path_ends_at_end(self, simple_maze):
        result = BFSPathfinder().find_path(simple_maze)
        assert result.path[-1] == simple_maze.end

    def test_steps_recorded(self, simple_maze):
        result = BFSPathfinder().find_path(simple_maze)
        assert result.steps > 0

    def test_explored_non_empty(self, simple_maze):
        result = BFSPathfinder().find_path(simple_maze)
        assert len(result.explored) > 0

    def test_finds_shortest_path(self, trivial_maze):
        result = BFSPathfinder().find_path(trivial_maze)
        assert result.found is True
        assert len(result.path) == 2  # start + end only


class TestBFSNoPath:
    def test_returns_not_found(self, blocked_maze):
        result = BFSPathfinder().find_path(blocked_maze)
        assert result.found is False

    def test_path_is_empty(self, blocked_maze):
        result = BFSPathfinder().find_path(blocked_maze)
        assert result.path == []
