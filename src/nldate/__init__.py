import re
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
_UNIT_DAYS = {"day": 1, "week": 7, "month": 30}


def parse(s: str, today: date | None = None) -> date:
    """Parse common English dates relative to today (months mean 30 days)."""
    reference = date.today() if today is None else today
    text = " ".join(s.lower().split())

    if re.fullmatch(r"\d{4}([-/])\d{2}\1\d{2}", text):
        return date.fromisoformat(text.replace("/", "-"))

    offsets = {"today": 0, "tomorrow": 1, "day after tomorrow": 2}
    if text in offsets:
        return reference + timedelta(days=offsets[text])

    if text.startswith("next ") and text[5:] in _WEEKDAYS:
        target = _WEEKDAYS.index(text[5:])
        return reference + timedelta(days=(target - reference.weekday()) % 7)

    # Reduce relative phrases to a duration and a date to count from.
    relative = re.fullmatch(
        r"(?:in (\w+) (days?|weeks?|months?)|"
        r"(\w+) (days?|weeks?|months?) (from now|before .+))",
        text,
    )
    if relative:
        amount, unit, other_amount, other_unit, anchor = relative.groups()
        amount = amount or other_amount
        unit = unit or other_unit
        if amount.isdecimal():
            count = int(amount)
        elif amount in _NUMBERS:
            count = _NUMBERS[amount]
        else:
            raise ValueError(f"Unrecognized quantity: {amount!r}")
        days = count * _UNIT_DAYS[unit.rstrip("s")]
        if anchor and anchor.startswith("before "):
            return parse(anchor[7:], reference) - timedelta(days=days)
        return reference + timedelta(days=days)

    absolute = re.fullmatch(r"([a-z]+) (\d{1,2})(?:st|nd|rd|th)?(?:,? (\d{4}))?", text)
    if absolute:
        month, day, year = absolute.groups()
        if month in _MONTHS:
            return date(int(year) if year else reference.year, _MONTHS[month], int(day))

    raise ValueError(f"Unrecognized date: {s!r}")


def main() -> None:
    print("Hello from nldate!")
