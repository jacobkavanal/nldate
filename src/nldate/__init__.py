import re
from calendar import monthrange
from datetime import date, timedelta

_NUMBERS = {
    word: number
    for number, word in enumerate(
        [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
            "twenty",
        ]
    )
}
_MONTHS = {
    month: number
    for number, month in enumerate(
        [
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
        ],
        start=1,
    )
}
_WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
_MONTHS.update({name[:3]: number for name, number in list(_MONTHS.items())})
_NUMBERS.update({"a": 1, "an": 1})
_NUMBERS.update(
    dict(
        zip(
            ["thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"],
            range(30, 100, 10),
            strict=True,
        )
    )
)
_UNIT_DAYS = {"day": 1, "week": 7, "month": 30, "year": 365}


def _duration(text: str) -> tuple[int, int, int]:
    """Read one or more quantities, rejecting any unmatched text."""
    months = days = approximate_days = 0
    terms = re.split(r"\s+and\s+|,\s*", text)
    for term in terms:
        match = re.fullmatch(r"(.+?) (days?|weeks?|months?|years?)", term)
        if not match:
            raise ValueError(f"Unrecognized duration: {text!r}")
        amount, unit = match.groups()
        words = amount.replace("-", " ").split()
        if amount.isdecimal():
            count = int(amount)
        elif amount in _NUMBERS:
            count = _NUMBERS[amount]
        elif (
            len(words) == 2
            and words[0] in _NUMBERS
            and _NUMBERS[words[0]] >= 20
            and _NUMBERS[words[0]] % 10 == 0
            and words[1] in _NUMBERS
            and 1 <= _NUMBERS[words[1]] <= 9
        ):
            count = _NUMBERS[words[0]] + _NUMBERS[words[1]]
        else:
            raise ValueError(f"Unrecognized quantity: {amount!r}")
        unit = unit.rstrip("s")
        approximate_days += count * _UNIT_DAYS[unit]
        if unit in {"month", "year"}:
            months += count * (12 if unit == "year" else 1)
        else:
            days += count * _UNIT_DAYS[unit]
    return months, days, approximate_days


def _shift(reference: date, duration: str, direction: int) -> date:
    """Shift calendar months first, clamp the day, then shift days."""
    months, days, _ = _duration(duration)
    year, month_index = divmod(
        reference.year * 12 + reference.month - 1 + direction * months, 12
    )
    if not 1 <= year <= 9999:
        raise ValueError("Date falls outside the supported year range")
    month = month_index + 1
    day = min(reference.day, monthrange(year, month)[1])
    try:
        return date(year, month, day) + timedelta(days=direction * days)
    except OverflowError as error:
        raise ValueError("Date falls outside the supported year range") from error


def parse(s: str, today: date | None = None) -> date:
    """Parse English dates; `in` durations retain 30-day month approximations."""
    reference = date.today() if today is None else today
    text = " ".join(s.lower().split())

    numeric = re.fullmatch(r"(\d{4})([-/])(\d{1,2})\2(\d{1,2})", text)
    if numeric:
        year, _, month, day = numeric.groups()
        return date(int(year), int(month), int(day))

    # Year-last numeric dates follow US month/day order.
    numeric = re.fullmatch(r"(\d{1,2})([-/])(\d{1,2})(?:\2(\d{4}))?", text)
    if numeric:
        month, _, day, year = numeric.groups()
        return date(int(year) if year else reference.year, int(month), int(day))

    offsets = {
        "today": 0,
        "now": 0,
        "tomorrow": 1,
        "yesterday": -1,
        "day after tomorrow": 2,
        "the day after tomorrow": 2,
        "day before yesterday": -2,
        "the day before yesterday": -2,
    }
    if text in offsets:
        return reference + timedelta(days=offsets[text])

    weekday = re.fullmatch(
        r"(?:(next|last|this) )?(" + "|".join(_WEEKDAYS) + r")", text
    )
    if weekday:
        direction, name = weekday.groups()
        difference = _WEEKDAYS.index(name) - reference.weekday()
        days = -((-difference) % 7 or 7) if direction == "last" else difference % 7
        return reference + timedelta(days=days)

    period = re.fullmatch(r"(next|last|this) (day|week|month|year)", text)
    if period:
        direction, unit = period.groups()
        sign = {"next": 1, "last": -1, "this": 0}[direction]
        return _shift(reference, f"1 {unit}", sign)

    # Reduce relative phrases to a duration and a date to count from.
    if text.startswith("in "):
        # Preserve the original assignment tests' fixed 30-day months.
        _, _, days = _duration(text[3:])
        return reference + timedelta(days=days)
    if text.endswith(" ago"):
        return _shift(reference, text[:-4], -1)

    relative = re.fullmatch(r"(.+?) (before|after|from) (.+)", text)
    if relative:
        duration, direction, anchor = relative.groups()
        return _shift(
            parse(anchor, reference), duration, -1 if direction == "before" else 1
        )

    absolute = re.fullmatch(
        r"([a-z]+)\.? (\d{1,2})(?:st|nd|rd|th)?(?:,? (\d{4}))?", text
    )
    if absolute:
        month, day, year = absolute.groups()
        if month in _MONTHS:
            return date(int(year) if year else reference.year, _MONTHS[month], int(day))

    absolute = re.fullmatch(
        r"(\d{1,2})(?:st|nd|rd|th)? ([a-z]+)\.?(?:,? (\d{4}))?", text
    )
    if absolute:
        day, month, year = absolute.groups()
        if month in _MONTHS:
            return date(int(year) if year else reference.year, _MONTHS[month], int(day))

    raise ValueError(f"Unrecognized date: {s!r}")


def main() -> None:
    print("Hello from nldate!")
