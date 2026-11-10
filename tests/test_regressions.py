from datetime import date

import pytest

from nldate import parse


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2025-12-04", date(2025, 12, 4)),
        ("2025/12/04", date(2025, 12, 4)),
        ("2025/12/3", date(2025, 12, 3)),
        ("2025/1/3", date(2025, 1, 3)),
        ("2025-1-3", date(2025, 1, 3)),
        ("12/3/2025", date(2025, 12, 3)),
        ("12-3-2025", date(2025, 12, 3)),
        ("12/3", date(2025, 12, 3)),
        ("Dec 3rd, 2025", date(2025, 12, 3)),
        ("Dec. 3, 2025", date(2025, 12, 3)),
        ("3 December 2025", date(2025, 12, 3)),
        ("3rd Dec.", date(2025, 12, 3)),
        ("yesterday", date(2025, 1, 5)),
        ("day before yesterday", date(2025, 1, 4)),
        ("last Monday", date(2024, 12, 30)),
        ("last Friday", date(2025, 1, 3)),
        ("this Monday", date(2025, 1, 6)),
        ("Friday", date(2025, 1, 10)),
        ("two weeks from tomorrow", date(2025, 1, 21)),
        ("three days ago", date(2025, 1, 3)),
        ("in a week", date(2025, 1, 13)),
        ("in twenty-one days", date(2025, 1, 27)),
        ("in thirty two days", date(2025, 2, 7)),
        ("in 1 week and 2 days", date(2025, 1, 15)),
        ("1 year and 2 months after yesterday", date(2026, 3, 6)),
        ("5 days before 2025/12/3", date(2025, 11, 28)),
        ("2024/02/29", date(2024, 2, 29)),
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
    [
        "",
        "   ",
        "not a date",
        "2025-02-29",
        "2025-13-04",
        "February 30",
        "2025/02/29",
        "2025/13/04",
        "2025/12-04",
        "2025/0/3",
        "2025/12/32",
        "2025/2/29",
        "12/3/25",
        "in banana days",
        "in two weeks and",
        "in twenty twenty days",
    ],
)
def test_invalid_dates(text: str) -> None:
    with pytest.raises(ValueError):
        parse(text, date(2025, 1, 6))
