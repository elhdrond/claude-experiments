# Spec: GBP to EUR Historical Converter

> **Status:** Draft | In Review | Approved | **Implemented**
> **Date:** 2026-11-10
> **Author:** elhdrond

---

## 1. Goal

Allow elhdrond to quickly see the GBP→EUR converted value of a fixed pound amount
across every trading day of the current calendar year, using real historical daily
exchange rates from the public frankfurter.app API.

---

## 2. Actors

| Actor | Description |
|-------|-------------|
| User  | Developer (elhdrond) who runs the script locally from the project directory. |

---

## 3. Functional Requirements

| ID    | Requirement                                                                                                      | Priority |
|-------|------------------------------------------------------------------------------------------------------------------|----------|
| FR-01 | The system shall read the GBP amount to convert from the env var `GBP_AMOUNT` defined in a `.env` file.         | Must     |
| FR-02 | The system shall fetch historical daily GBP→EUR rates for all trading days from January 1 of the current year to today, using a single bulk request to the frankfurter.app API. | Must |
| FR-03 | The system shall generate a self-contained HTML file (`output.html`) showing only the first trading day of each month, one row per month (max 12 rows), grouped under a month-name header. | Must |
| FR-04 | The HTML output shall include a summary section showing: total months shown, average rate, minimum rate, and maximum rate across those 12 data points. | Must |
| FR-05 | The HTML output shall color-code each row based on whether that month's rate is above (green) or below (red) the annual average, so the user can spot favorable months at a glance. | Must |
| FR-06 | After generating the file, the system shall open `output.html` automatically in the default browser. | Must |
| FR-07 | The system shall exit with code 1 and a descriptive error message if `GBP_AMOUNT` is missing, non-numeric, zero, or negative. | Must |
| FR-08 | The system shall exit with code 1 and a descriptive error message if the API request fails (network error, non-200 response, or malformed JSON). | Must |

**Priority levels:** Must (non-negotiable) · Should (important) · Could (nice to have)

---

## 4. Non-Functional Requirements

| ID     | Requirement  | Metric                                                                       |
|--------|--------------|------------------------------------------------------------------------------|
| NFR-01 | Performance  | Script completes in < 10 s using a single bulk API call (not per-day calls). |
| NFR-02 | Reliability  | Non-zero exit code + human-readable message on any error.                    |
| NFR-03 | Security     | `GBP_AMOUNT` read from `.env`; `.env` excluded from version control via `.gitignore`. No API key required (frankfurter.app is public). |

---

## 5. Data Model

```
Input (read from .env):
  GBP_AMOUNT: float — amount in pounds sterling; must be > 0

API request:
  GET https://api.frankfurter.app/YYYY-01-01..today?from=GBP&to=EUR
  Response: { "rates": { "YYYY-MM-DD": { "EUR": float }, … } }

Output record (one row per month — first trading day of that month):
  date:        str   — calendar date of first trading day (YYYY-MM-DD)
  rate:        float — GBP→EUR closing rate on that day
  eur_amount:  float — GBP_AMOUNT × rate

Summary (computed from the 12 monthly data points):
  total_months: int   — number of months with data (max 12)
  avg_rate:     float — arithmetic mean of the 12 monthly rates
  min_rate:     float — lowest monthly rate
  max_rate:     float — highest monthly rate
```

---

## 6. Acceptance Criteria

```
Scenario: Happy path
  Given GBP_AMOUNT=3121 in .env
  When  the script is run (python converter.py)
  Then  output.html is created in the script's directory
  And   the HTML table contains one row per month (max 12), each showing the first trading day of that month
  And   each month has a header with the month name
  And   the summary section shows total months, avg, min, and max rate
  And   the default browser opens output.html automatically
```

```
Scenario: Missing environment variable
  Given GBP_AMOUNT is not set in .env
  When  the script is run
  Then  the script exits with code 1
  And   prints a message indicating GBP_AMOUNT is missing or empty
```

```
Scenario: Invalid amount (zero or negative)
  Given GBP_AMOUNT=0 (or -50) in .env
  When  the script is run
  Then  the script exits with code 1
  And   prints a message indicating GBP_AMOUNT must be a positive number
```

```
Scenario: API unreachable
  Given GBP_AMOUNT=100 in .env
  When  the script is run and the API returns a network error or non-200 status
  Then  the script exits with code 1
  And   prints a message indicating the API request failed and the error detail
```

---

## 7. Out of Scope

- Currency pairs other than GBP→EUR
- User-supplied date ranges (always Jan 1 of the current year to today)
- Reverse conversion (EUR→GBP)
- Plain-text stdout output (replaced by HTML)
- Caching or persisting API results
- A live web server or interactive UI

---

## 8. Open Questions

- [x] Should weekend/bank-holiday dates with no rate be shown as empty rows, skipped
      entirely, or filled with the previous trading day's rate?
      **Resolved:** Skip them — iterate only over dates returned by the API (trading days only).

---

## 9. Implementation Notes

- **Approach:** Single bulk GET to `frankfurter.app/{start}..{end}?from=GBP&to=EUR`, filter to first trading day per month, generate self-contained HTML, open in browser.
- **Files created:**
  - `exp-13-gbp-eur-converter/converter.py` — main script
  - `exp-13-gbp-eur-converter/tests/test_converter.py` — pytest suite (one class per acceptance scenario)
  - `exp-13-gbp-eur-converter/tests/conftest.py` — shared fixtures
  - `exp-13-gbp-eur-converter/.env.example` — template for `.env`
  - `.gitignore` — excludes `.env`, `output.html`, `__pycache__`
- **Dependencies:** `requests`, `python-dotenv`, `pytest` (install via `pip install requests python-dotenv pytest`)
