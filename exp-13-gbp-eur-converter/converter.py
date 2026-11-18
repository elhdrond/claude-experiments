import os
import sys
import webbrowser
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv

HTML_FILE = Path(__file__).parent / "output.html"


MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def first_of_each_month(rows: list[tuple[str, float, float]]) -> list[tuple[str, float, float]]:
    """FR-03: keep only the first trading day per calendar month."""
    seen: set[str] = set()
    result = []
    for d, rate, eur in rows:
        month_key = d[:7]  # "YYYY-MM"
        if month_key not in seen:
            seen.add(month_key)
            result.append((d, rate, eur))
    return result


def build_html(gbp_amount: float, rows: list[tuple[str, float, float]], summary: dict) -> str:
    avg = summary["avg"]

    def row_class(rate: float) -> str:
        return "above" if rate >= avg else "below"

    def month_label(date_str: str) -> str:
        month_num = int(date_str[5:7])
        return MONTH_NAMES[month_num]

    rows_html = "\n".join(
        f'<tr class="month-header"><td colspan="3">{month_label(d)}</td></tr>\n'
        f'<tr class="{row_class(rate)}">'
        f"<td>{d}</td><td>{rate:.4f}</td><td>{eur:.2f}</td>"
        f"</tr>"
        for d, rate, eur in rows
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GBP → EUR {date.today().year}</title>
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
  .subtitle {{ color: #78716c; margin: 0 0 28px; font-size: 13px; }}

  .summary {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 28px;
  }}
  .card {{
    background: #fff;
    border: 1px solid #e7e5e4;
    border-radius: 8px;
    padding: 14px 20px;
    min-width: 120px;
  }}
  .card-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: .05em; color: #a8a29e; margin-bottom: 4px; }}
  .card-value {{ font-size: 22px; font-weight: 700; font-variant-numeric: tabular-nums; }}

  .legend {{
    display: flex;
    gap: 16px;
    margin-bottom: 12px;
    font-size: 12px;
    color: #78716c;
  }}
  .dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; vertical-align: middle; }}
  .dot.above {{ background: #16a34a; }}
  .dot.below {{ background: #dc2626; }}

  .table-wrap {{ overflow-x: auto; border-radius: 8px; border: 1px solid #e7e5e4; }}
  table {{ border-collapse: collapse; width: 100%; background: #fff; }}
  thead th {{
    background: #fafaf9;
    padding: 10px 16px;
    text-align: left;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .05em;
    color: #78716c;
    border-bottom: 1px solid #e7e5e4;
    font-weight: 600;
  }}
  td {{ padding: 8px 16px; border-bottom: 1px solid #f5f5f4; font-variant-numeric: tabular-nums; }}
  tr:last-child td {{ border-bottom: none; }}
  tr.above td:nth-child(2) {{ color: #16a34a; font-weight: 500; }}
  tr.below td:nth-child(2) {{ color: #dc2626; font-weight: 500; }}
  tr:hover td {{ background: #fafaf9; }}
  tr.month-header td {{
    background: #f5f5f4;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: .06em;
    color: #78716c;
    padding: 6px 16px;
    border-bottom: 1px solid #e7e5e4;
  }}

  @media (prefers-color-scheme: dark) {{
    body {{ background: #1c1917; color: #e7e5e4; }}
    .card {{ background: #292524; border-color: #3f3f3f; }}
    .card-label {{ color: #78716c; }}
    .table-wrap {{ border-color: #3f3f3f; }}
    table {{ background: #1c1917; }}
    thead th {{ background: #292524; border-color: #3f3f3f; color: #a8a29e; }}
    td {{ border-color: #292524; }}
    tr:hover td {{ background: #292524; }}
    tr.month-header td {{ background: #292524; color: #a8a29e; border-color: #3f3f3f; }}
  }}
</style>
</head>
<body>
<h1>GBP &rarr; EUR &mdash; {date.today().year}</h1>
<p class="subtitle">
  Converting <strong>£{gbp_amount:,.2f}</strong> &middot;
  {summary['total_months']} months &middot;
  {summary['start']} to {summary['end']}
</p>

<div class="summary">
  <div class="card">
    <div class="card-label">Months shown</div>
    <div class="card-value">{summary['total_months']}</div>
  </div>
  <div class="card">
    <div class="card-label">Avg rate</div>
    <div class="card-value">{summary['avg']:.4f}</div>
  </div>
  <div class="card">
    <div class="card-label">Best rate</div>
    <div class="card-value" style="color:#16a34a">{summary['max']:.4f}</div>
  </div>
  <div class="card">
    <div class="card-label">Worst rate</div>
    <div class="card-value" style="color:#dc2626">{summary['min']:.4f}</div>
  </div>
  <div class="card">
    <div class="card-label">Best day (€)</div>
    <div class="card-value" style="color:#16a34a">€{gbp_amount * summary['max']:,.2f}</div>
  </div>
</div>

<div class="legend">
  <span><span class="dot above"></span>Above average rate</span>
  <span><span class="dot below"></span>Below average rate</span>
</div>

<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>Date</th>
        <th>Rate (GBP/EUR)</th>
        <th>EUR Amount</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</div>
</body>
</html>"""


def main():
    load_dotenv()

    # FR-07: Read and validate GBP_AMOUNT
    raw = os.getenv("GBP_AMOUNT", "").strip()
    if not raw:
        print("Error: GBP_AMOUNT is not set in .env", file=sys.stderr)
        sys.exit(1)
    try:
        gbp_amount = float(raw)
    except ValueError:
        print(f"Error: GBP_AMOUNT must be a number, got '{raw}'", file=sys.stderr)
        sys.exit(1)
    if gbp_amount <= 0:
        print(f"Error: GBP_AMOUNT must be a positive number, got {gbp_amount}", file=sys.stderr)
        sys.exit(1)

    # FR-02: Single bulk request — trading days from Jan 1 of the current year to today
    start = date(date.today().year, 1, 1).isoformat()
    end = date.today().isoformat()
    url = f"https://api.frankfurter.app/{start}..{end}?from=GBP&to=EUR"

    # FR-08: Handle API errors
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Could not reach the frankfurter.app API — check your connection", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: API request timed out after 10 s", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: API returned HTTP {e.response.status_code}", file=sys.stderr)
        sys.exit(1)
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: API request failed — {e}", file=sys.stderr)
        sys.exit(1)

    raw_rates = data.get("rates", {})
    all_rows = sorted(
        (d, raw_rates[d]["EUR"], gbp_amount * raw_rates[d]["EUR"])
        for d in raw_rates
    )
    # FR-03: keep only the first trading day of each month
    rows = first_of_each_month(all_rows)

    # FR-04: Compute summary stats
    all_rates = [r for _, r, _ in rows]
    summary = {
        "total_months": len(rows),
        "avg": sum(all_rates) / len(all_rates),
        "min": min(all_rates),
        "max": max(all_rates),
        "start": rows[0][0],
        "end": rows[-1][0],
    }

    # FR-03 / FR-05: Generate HTML and open in browser
    HTML_FILE.write_text(build_html(gbp_amount, rows, summary), encoding="utf-8")
    webbrowser.open(HTML_FILE.as_uri())
    print(f"Opened {HTML_FILE}")


if __name__ == "__main__":
    main()
