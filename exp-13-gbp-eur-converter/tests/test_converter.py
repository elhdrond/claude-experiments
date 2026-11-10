"""
Tests for converter.py — one test class per acceptance scenario from the spec.
See: specs/exp-13-gbp-eur-converter.md § 6. Acceptance Criteria
"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import requests

import converter


# Two days in January, one in February, one in March — exercises month filtering
SAMPLE_RATES = {
    "2026-01-02": {"EUR": 1.2103},
    "2026-01-05": {"EUR": 1.2089},  # second Jan day — should be filtered out
    "2026-02-02": {"EUR": 1.1950},
    "2026-03-02": {"EUR": 1.2200},
}
EXPECTED_MONTHS = 3  # Jan, Feb, Mar


def make_api_response(rates=None):
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {"rates": rates or SAMPLE_RATES}
    return mock


@pytest.fixture(autouse=True)
def no_dotenv():
    """Prevent load_dotenv() from reading a real .env file during tests."""
    with patch("converter.load_dotenv"):
        yield


@pytest.fixture(autouse=True)
def no_browser():
    """Prevent the browser from opening during tests."""
    with patch("webbrowser.open"):
        yield


@pytest.fixture(autouse=True)
def tmp_output(tmp_path, monkeypatch):
    """Redirect output.html to a temp directory so tests don't write to the project."""
    monkeypatch.setattr(converter, "HTML_FILE", tmp_path / "output.html")
    return tmp_path / "output.html"


# ---------------------------------------------------------------------------
# Scenario: Happy path
# ---------------------------------------------------------------------------

class TestHappyPath:
    def test_generates_output_html(self, monkeypatch, tmp_output):
        """FR-03: output.html is created."""
        monkeypatch.setenv("GBP_AMOUNT", "3121")
        with patch("requests.get", return_value=make_api_response()):
            converter.main()
        assert tmp_output.exists()

    def test_html_contains_one_row_per_month(self, monkeypatch, tmp_output):
        """FR-03: one data row per month (first trading day only), not per trading day."""
        monkeypatch.setenv("GBP_AMOUNT", "3121")
        with patch("requests.get", return_value=make_api_response()):
            converter.main()
        html = tmp_output.read_text(encoding="utf-8")
        # thead row + month-header rows + data rows
        data_rows = html.count('class="above"') + html.count('class="below"')
        assert data_rows == EXPECTED_MONTHS

    def test_second_trading_day_of_month_is_excluded(self, monkeypatch, tmp_output):
        """FR-03: Jan 5 (second Jan trading day) must not appear — only Jan 2."""
        monkeypatch.setenv("GBP_AMOUNT", "100")
        with patch("requests.get", return_value=make_api_response()):
            converter.main()
        html = tmp_output.read_text(encoding="utf-8")
        assert "2026-01-02" in html
        assert "2026-01-05" not in html

    def test_html_contains_month_headers(self, monkeypatch, tmp_output):
        """FR-03: each month has a header row with the month name."""
        monkeypatch.setenv("GBP_AMOUNT", "100")
        with patch("requests.get", return_value=make_api_response()):
            converter.main()
        html = tmp_output.read_text(encoding="utf-8")
        assert "January" in html
        assert "February" in html
        assert "March" in html

    def test_html_contains_correct_eur_amount(self, monkeypatch, tmp_output):
        """FR-03: EUR amount is GBP_AMOUNT × rate, 2 decimal places."""
        monkeypatch.setenv("GBP_AMOUNT", "3121")
        with patch("requests.get", return_value=make_api_response()):
            converter.main()
        html = tmp_output.read_text(encoding="utf-8")
        assert "3777.35" in html  # 3121 × 1.2103

    def test_html_contains_summary_stats(self, monkeypatch, tmp_output):
        """FR-04: summary section with avg, min, max rate and total months."""
        monkeypatch.setenv("GBP_AMOUNT", "100")
        with patch("requests.get", return_value=make_api_response()):
            converter.main()
        html = tmp_output.read_text(encoding="utf-8")
        assert str(EXPECTED_MONTHS) in html  # total months shown
        assert "1.1950" in html              # min rate (Feb)
        assert "1.2200" in html              # max rate (Mar)

    def test_html_color_codes_rows(self, monkeypatch, tmp_output):
        """FR-05: rows are marked 'above' or 'below' average."""
        monkeypatch.setenv("GBP_AMOUNT", "100")
        with patch("requests.get", return_value=make_api_response()):
            converter.main()
        html = tmp_output.read_text(encoding="utf-8")
        assert 'class="above"' in html
        assert 'class="below"' in html

    def test_opens_browser_automatically(self, monkeypatch, tmp_output):
        """FR-06: browser is opened with the generated file."""
        monkeypatch.setenv("GBP_AMOUNT", "100")
        with patch("requests.get", return_value=make_api_response()):
            with patch("webbrowser.open") as mock_open:
                converter.main()
        mock_open.assert_called_once()


# ---------------------------------------------------------------------------
# Scenario: Missing environment variable
# ---------------------------------------------------------------------------

class TestMissingEnvVar:
    def test_exits_with_code_1(self, monkeypatch):
        monkeypatch.delenv("GBP_AMOUNT", raising=False)
        with pytest.raises(SystemExit) as exc:
            converter.main()
        assert exc.value.code == 1

    def test_prints_error_message(self, monkeypatch, capsys):
        monkeypatch.delenv("GBP_AMOUNT", raising=False)
        with pytest.raises(SystemExit):
            converter.main()
        assert "GBP_AMOUNT" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Scenario: Invalid amount (zero or negative)
# ---------------------------------------------------------------------------

class TestInvalidAmount:
    @pytest.mark.parametrize("value", ["0", "-50", "-0.01"])
    def test_zero_or_negative_exits_with_code_1(self, monkeypatch, value):
        monkeypatch.setenv("GBP_AMOUNT", value)
        with pytest.raises(SystemExit) as exc:
            converter.main()
        assert exc.value.code == 1

    @pytest.mark.parametrize("value", ["0", "-50"])
    def test_zero_or_negative_prints_error(self, monkeypatch, capsys, value):
        monkeypatch.setenv("GBP_AMOUNT", value)
        with pytest.raises(SystemExit):
            converter.main()
        assert "positive" in capsys.readouterr().err.lower()

    def test_non_numeric_exits_with_code_1(self, monkeypatch):
        monkeypatch.setenv("GBP_AMOUNT", "abc")
        with pytest.raises(SystemExit) as exc:
            converter.main()
        assert exc.value.code == 1

    def test_non_numeric_prints_error(self, monkeypatch, capsys):
        monkeypatch.setenv("GBP_AMOUNT", "abc")
        with pytest.raises(SystemExit):
            converter.main()
        assert "GBP_AMOUNT" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Scenario: API unreachable
# ---------------------------------------------------------------------------

class TestApiUnreachable:
    def test_connection_error_exits_with_code_1(self, monkeypatch):
        monkeypatch.setenv("GBP_AMOUNT", "100")
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(SystemExit) as exc:
                converter.main()
        assert exc.value.code == 1

    def test_connection_error_prints_error(self, monkeypatch, capsys):
        monkeypatch.setenv("GBP_AMOUNT", "100")
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(SystemExit):
                converter.main()
        assert "api" in capsys.readouterr().err.lower()

    def test_timeout_exits_with_code_1(self, monkeypatch):
        monkeypatch.setenv("GBP_AMOUNT", "100")
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            with pytest.raises(SystemExit) as exc:
                converter.main()
        assert exc.value.code == 1

    def test_http_500_exits_with_code_1(self, monkeypatch):
        monkeypatch.setenv("GBP_AMOUNT", "100")
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        with patch("requests.get", return_value=mock_response):
            with pytest.raises(SystemExit) as exc:
                converter.main()
        assert exc.value.code == 1
