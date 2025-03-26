from collections.abc import Sequence
from datetime import datetime, timedelta, timezone

from dateutil.relativedelta import relativedelta


class Plural:
    def __init__(self, value: int):
        self.value = value

    def __format__(self, format_spec: str):
        singular, _, plural = format_spec.partition("|")

        if not plural:
            plural = f"{singular}s"

        suffix = plural if abs(self.value) != 1 else singular
        return f"{self.value} {suffix}"


def human_join(seq: Sequence[str], delimiter: str = ", ", final: str = "and"):
    if not seq:
        return ""

    if len(seq) == 1:
        return str(seq[0])

    return f"{delimiter.join(map(str, seq[:-1]))} {final} {seq[-1]}"


def human_timedelta(
    end: datetime | timedelta,
    *,
    reference: datetime | None = None,
    accuracy: int | None = 3,
    brief: bool = False,
    suffix: bool = True,
):
    now = reference or datetime.now(timezone.utc)

    if isinstance(end, timedelta):
        end = now + end

    # Ensure timezone info and remove microseconds
    now = now.replace(tzinfo=now.tzinfo or timezone.utc, microsecond=0)
    end = end.replace(tzinfo=end.tzinfo or timezone.utc, microsecond=0)

    if end > now:
        delta = relativedelta(end, now)
        affix = ""
    else:
        delta = relativedelta(now, end)
        affix = " ago" if suffix else ""

    TIME_UNITS = [
        ("year", "y"),
        ("month", "mo"),
        ("day", "d"),
        ("hour", "h"),
        ("minute", "m"),
        ("second", "s"),
    ]

    result = []
    for unit, brief_unit in TIME_UNITS:
        value = getattr(delta, unit + "s")
        if value <= 0:
            continue

        if unit == "day":
            weeks = delta.weeks
            if weeks:
                value -= weeks * 7
                result.append(f"{weeks}w" if brief else format(Plural(weeks), "week"))

        if value > 0:
            result.append(f"{value}{brief_unit}" if brief else format(Plural(value), unit))

    if accuracy is not None:
        result = result[:accuracy]

    if not result:
        return "now"

    return " ".join(result) + affix if brief else human_join(result) + affix
