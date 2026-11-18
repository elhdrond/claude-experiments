from infrastructure.dfs import DFSPathfinder


class TestDFSHappyPath:
    def test_finds_path(self, simple_maze):
        result = DFSPathfinder().find_path(simple_maze)
        assert result.found is True

    def test_path_starts_at_start(self, simple_maze):
        result = DFSPathfinder().find_path(simple_maze)
        assert result.path[0] == simple_maze.start

    def test_path_ends_at_end(self, simple_maze):
        result = DFSPathfinder().find_path(simple_maze)
        assert result.path[-1] == simple_maze.end

    def test_steps_recorded(self, simple_maze):
        result = DFSPathfinder().find_path(simple_maze)
        assert result.steps > 0


class TestDFSNoPath:
    def test_returns_not_found(self, blocked_maze):
        result = DFSPathfinder().find_path(blocked_maze)
        assert result.found is False

    def test_path_is_empty(self, blocked_maze):
        result = DFSPathfinder().find_path(blocked_maze)
        assert result.path == []
