from datetime import datetime

from sync_buddy.scripts.formatters import Formatters


def test_datetime():
    full = Formatters.datetime('2022-07-01 17:54:16')
    assert isinstance(full, datetime)
    assert full.year == 2022
    assert full.month == 7
    assert full.day == 1
    assert full.hour == 17
    assert full.minute == 54
    assert full.second == 16

    date = Formatters.datetime('2022-07-01', '%Y-%m-%d')
    assert isinstance(date, datetime)
    assert date.year == 2022
    assert date.month == 7
    assert date.day == 1

    time = Formatters.datetime('17:54:16', '%H:%M:%S')
    assert isinstance(time, datetime)
    assert time.hour == 17
    assert time.minute == 54
    assert time.second == 16
