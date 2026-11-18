from domain.entities import CellKind, Maze, PathResult, Position

# FR-05 colour mapping
_CELL_COLOURS = {
    "start":    "#3b82f6",   # blue
    "end":      "#3b82f6",   # blue
    "path":     "#16a34a",   # green
    "explored": "#fed7aa",   # light orange
    "wall":     "#1c1917",   # dark
    "open":     "#ffffff",   # white
}


def _cell_colour(pos: Position, maze: Maze, result: PathResult) -> str:
    cell = maze.grid[pos.row][pos.col]
    if cell.kind == CellKind.START:
        return _CELL_COLOURS["start"]
    if cell.kind == CellKind.END:
        return _CELL_COLOURS["end"]
    if cell.kind == CellKind.WALL:
        return _CELL_COLOURS["wall"]
    if pos in result.path:
        return _CELL_COLOURS["path"]
    if pos in result.explored:
        return _CELL_COLOURS["explored"]
    return _CELL_COLOURS["open"]


def _render_grid(maze: Maze, result: PathResult) -> str:
    cell_px = max(10, min(28, 560 // max(maze.rows, maze.cols)))
    rows_html = []
    for r in range(maze.rows):
        cells = []
        for c in range(len(maze.grid[r])):
            pos = Position(r, c)
            colour = _cell_colour(pos, maze, result)
            cells.append(
                f'<div style="width:{cell_px}px;height:{cell_px}px;'
                f'background:{colour};flex-shrink:0"></div>'
            )
        rows_html.append(
            f'<div style="display:flex">{"".join(cells)}</div>'
        )
    return "\n".join(rows_html)


def _panel(maze: Maze, result: PathResult) -> str:
    grid_html = _render_grid(maze, result)
    found_badge = (
        '<span style="color:#16a34a;font-weight:600">✓ Found</span>'
        if result.found else
        '<span style="color:#dc2626;font-weight:600">✗ Not found</span>'
    )
    path_len = len(result.path)
    return f"""
<div style="background:#fff;border:1px solid #e7e5e4;border-radius:10px;padding:20px;min-width:0">
  <h2 style="margin:0 0 4px;font-size:16px">{result.algorithm}</h2>
  <div style="font-size:12px;color:#78716c;margin-bottom:12px">
    {found_badge} &nbsp;·&nbsp;
    Path: <strong>{path_len}</strong> cells &nbsp;·&nbsp;
    Explored: <strong>{len(result.explored)}</strong> cells &nbsp;·&nbsp;
    Steps: <strong>{result.steps}</strong>
  </div>
  <div style="overflow:auto;border:1px solid #e7e5e4;border-radius:6px;padding:4px;display:inline-block">
    {grid_html}
  </div>
</div>"""


def build_html(maze: Maze, results: list[PathResult]) -> str:
    panels = "\n".join(_panel(maze, r) for r in results)
    legend_items = [
        ("Start / End", _CELL_COLOURS["start"]),
        ("Path", _CELL_COLOURS["path"]),
        ("Explored", _CELL_COLOURS["explored"]),
        ("Wall", _CELL_COLOURS["wall"]),
        ("Unexplored", _CELL_COLOURS["open"]),
    ]
    legend_html = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:14px">'
        f'<span style="width:12px;height:12px;background:{colour};'
        f'border:1px solid #ccc;border-radius:2px;display:inline-block"></span>{label}</span>'
        for label, colour in legend_items
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pathfinding Visualiser</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: system-ui, sans-serif;
    font-size: 14px;
    background: #f5f5f4;
    color: #1c1917;
    padding: 32px 24px 64px;
  }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  .subtitle {{ color: #78716c; margin: 0 0 20px; font-size: 13px; }}
  .legend {{ font-size: 12px; color: #78716c; margin-bottom: 24px; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
  }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #1c1917; color: #e7e5e4; }}
    .grid > div {{ background: #292524 !important; border-color: #3f3f3f !important; }}
    .grid > div > div:first-child {{ color: #e7e5e4 !important; }}
  }}
</style>
</head>
<body>
<h1>Pathfinding Visualiser</h1>
<p class="subtitle">Maze: {maze.rows}×{maze.cols} &nbsp;·&nbsp;
BFS &amp; A* guarantee shortest path &nbsp;·&nbsp; DFS &amp; Dijkstra may differ</p>
<div class="legend">{legend_html}</div>
<div class="grid">
{panels}
</div>
</body>
</html>"""
