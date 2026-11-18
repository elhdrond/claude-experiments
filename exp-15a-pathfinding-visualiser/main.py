import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from infrastructure.maze_loader import load_maze
from infrastructure.bfs import BFSPathfinder
from infrastructure.dfs import DFSPathfinder
from infrastructure.astar import AStarPathfinder
from infrastructure.dijkstra import DijkstraPathfinder
from use_cases.compare_algorithms import compare_algorithms
from interface.html_report import build_html

OUTPUT_FILE = Path(__file__).parent / "output.html"
MAZE_FILE = Path(__file__).parent / "maze.txt"


def main() -> None:
    maze = load_maze(MAZE_FILE)

    # FR-02: four independent, interchangeable strategies
    algorithms = [
        BFSPathfinder(),
        DFSPathfinder(),
        AStarPathfinder(),
        DijkstraPathfinder(),
    ]

    # FR-03: each returns path, explored set, steps
    results = compare_algorithms(maze, algorithms)

    # FR-04 / FR-05 / FR-06: self-contained HTML with colour-coded panels
    OUTPUT_FILE.write_text(build_html(maze, results), encoding="utf-8")

    # FR-07: open in default browser
    webbrowser.open(OUTPUT_FILE.as_uri())
    print(f"Report saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
