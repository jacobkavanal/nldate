# nldate

`from nldate import parse` provides `parse(text, today=None) -> datetime.date`.
Omitting `today` uses the current date. Unrecognized or invalid dates raise
`ValueError`.

Supported inputs include:

- Year-first dates: `2025-12-03`, `2025/12/3`, `2025/1/3`.
- US month/day dates: `12/3/2025`, `12-3-2025`, `12/3`.
  Omitted years use the reference year; explicit years require four digits.
- Named dates: `December 3rd, 2025`, `Dec. 3`, `3 December 2025`.
- `today`, `now`, `tomorrow`, `yesterday`, and day before/after expressions.
- `next Monday`, `last Friday`, `this Tuesday`, or a weekday alone.
- `in two weeks`, `three days ago`, `two weeks from tomorrow`,
  `5 days before December 1st, 2025`, and
  `1 year and 2 months after yesterday`.

Quantities accept nonnegative integers, number words zero through ninety-nine,
and `a`/`an`. Compound durations use `and` or commas. Input ignores case and
extra whitespace. Numeric separators must match within a date.

Semantics: months are 30 days and years are 365 days, rather than calendar
arithmetic. Next/this/bare weekdays mean the next occurrence including today;
last weekdays mean the preceding occurrence, excluding today. Numeric year-last
dates always use US month/day order. These conventions avoid guessing from locale.

Run checks with `uv run pytest`, `uv run mypy src/`, `uv run ruff check`,
and `uv run ruff format --check`.
