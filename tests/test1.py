from datetime import date, timedelta
from nldate import parse
import pytest

def test_in_two_days():
    assert parse("in two days", date.today()) == date.today() + timedelta(days=2)


def test_in_three_days():
    assert parse("in 3 days", date.today() ) == date.today() + timedelta(days=3)


def test_ten_days_from_now():
    assert parse("ten days from now", date.today()) == date.today() + timedelta(days=10)


def test_day_after_tomorrow():
    assert parse("day after tomorrow", date.today()) == date.today() + timedelta(days=2)


def test_in_two_weeks():
    assert parse("in two weeks", date.today()) == date.today() + timedelta(weeks=2)


def test_in_three_weeks():
    assert parse("in 3 weeks", date.today()) == date.today() + timedelta(weeks=3)


def test_ten_weeks_from_now():
    assert parse("ten weeks from now", date.today()) == date.today() + timedelta(weeks=10)

def test_in_two_months():
    assert parse("in two months", date.today()) == date.today() + timedelta(days=60)  # Approximation

def test_specific_month():
    assert parse("october 15", date.today()) == date(date.today().year, 10, 15)

def test_today():
    assert parse("today", date.today()) == date.today()

def test_tomorrow():
    assert parse("tomorrow", date.today()) == date.today() + timedelta(days=1)

def test_without_today():
    assert parse("in two days") == date.today() + timedelta(days=2) 
    assert parse("in 3 days") == date.today() + timedelta(days=3)
    assert parse("ten days from now") == date.today() + timedelta(days=10)

def test_dates():
    assert parse("5 days before December 1st, 2025") == date(2025, 11, 26)

def test_next():
    assert parse("next Monday", date.today()) == date.today() + timedelta(days=(7 - date.today().weekday() + 0) % 7)
    assert parse("next Friday", date.today()) == date.today() + timedelta(days=(7 - date.today().weekday() + 4) % 7)
