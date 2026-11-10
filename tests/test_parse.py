from datetime import date, timedelta

import pytest

from nldate import parse

REFERENCE = date(2025, 1, 6)


def test_in_two_days():
    assert parse("in two days", REFERENCE) == REFERENCE + timedelta(days=2)


def test_in_three_days():
    assert parse("in 3 days", REFERENCE) == REFERENCE + timedelta(days=3)


def test_ten_days_from_now():
    assert parse("ten days from now", REFERENCE) == REFERENCE + timedelta(days=10)


def test_day_after_tomorrow():
    assert parse("day after tomorrow", REFERENCE) == REFERENCE + timedelta(days=2)


def test_in_two_weeks():
    assert parse("in two weeks", REFERENCE) == REFERENCE + timedelta(weeks=2)


def test_in_three_weeks():
    assert parse("in 3 weeks", REFERENCE) == REFERENCE + timedelta(weeks=3)


def test_ten_weeks_from_now():
    assert parse("ten weeks from now", REFERENCE) == REFERENCE + timedelta(weeks=10)


def test_in_two_months():
    assert parse("in two months", REFERENCE) == REFERENCE + timedelta(
        days=60
    )  # Approximation


def test_specific_month():
    assert parse("october 15", REFERENCE) == date(REFERENCE.year, 10, 15)


def test_today():
    assert parse("today", REFERENCE) == REFERENCE


def test_tomorrow():
    assert parse("tomorrow", REFERENCE) == REFERENCE + timedelta(days=1)


def test_without_today(monkeypatch: pytest.MonkeyPatch):
    class FixedDate(date):
        @classmethod
        def today(cls) -> date:
            return REFERENCE

    monkeypatch.setattr("nldate.date", FixedDate)
    assert parse("in two days") == REFERENCE + timedelta(days=2)
    assert parse("in 3 days") == REFERENCE + timedelta(days=3)
    assert parse("ten days from now") == REFERENCE + timedelta(days=10)


def test_dates():
    assert parse("5 days before December 1st, 2025") == date(2025, 11, 26)


def test_next():
    assert parse("next Monday", REFERENCE) == REFERENCE + timedelta(
        days=(7 - REFERENCE.weekday() + 0) % 7
    )
    assert parse("next Friday", REFERENCE) == REFERENCE + timedelta(
        days=(7 - REFERENCE.weekday() + 4) % 7
    )
