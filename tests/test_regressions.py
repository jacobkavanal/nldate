from datetime import date

import pytest

from nldate import parse


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2025-12-04", date(2025, 12, 4)),
        ("2024-02-29", date(2024, 2, 29)),
        (" 2025-12-04 ", date(2025, 12, 4)),
        ("5 days before 2025-12-04", date(2025, 11, 29)),
        (" NEXT MONDAY ", date(2025, 1, 6)),
        ("next Sunday", date(2025, 1, 12)),
        ("october 15", date(2025, 10, 15)),
    ],
)
def test_fixed_reference(text: str, expected: date) -> None:
    assert parse(text, date(2025, 1, 6)) == expected


@pytest.mark.parametrize(
    "text",
    ["", "   ", "not a date", "2025-02-29", "2025-13-04", "February 30"],
)
def test_invalid_dates(text: str) -> None:
    with pytest.raises(ValueError):
        parse(text, date(2025, 1, 6))
