from datetime import datetime, timedelta, timezone

import pendulum
import pytest

from plummet import PlummetError, frozen_time, momentize, moments_match


def test_momentize__returns_timestamp_for_now_when_called_with_None():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    with frozen_time(frozen_moment):
        now = momentize()
        assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_string_without_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = momentize("2021-11-17T20:36:00")
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_string_with_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = momentize("2021-11-17T12:36:00-08:00")
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_datetime_without_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = momentize(datetime(2021, 11, 17, 20, 36, 00))
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_datetime_with_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = momentize(datetime(2021, 11, 17, 12, 36, 0, tzinfo=timezone(timedelta(hours=-8))))
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_pendulum_datetime_without_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = momentize(pendulum.parse("2021-11-17T20:36:00"))
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_pendulum_datetime_with_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = momentize(pendulum.parse("2021-11-17T12:36:00-08:00"))
    assert now == frozen_moment


def test_momentize__raises_error_if_unmappable_object_is_passed():
    with pytest.raises(PlummetError, match="Cannot create a moment"):
        momentize(object())


def test_moments_match__raises_error_if_moments_do_not_match():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    moments = [
        "2021-11-17T20:36:00",
        "2021-11-17T12:36:00-08:00",
        datetime(2021, 11, 17, 20, 36, 00),
        datetime(2021, 11, 17, 12, 36, 0, tzinfo=timezone(timedelta(hours=-8))),
        pendulum.parse("2021-11-17T20:36:00"),
        pendulum.parse("2021-11-17T12:36:00-08:00"),
    ]
    for moment in moments:
        assert moments_match(frozen_moment, moment)

    with pytest.raises(PlummetError, match="Moments do not match"):
        moments_match(frozen_moment, "1970-01-01T00:00:00+00:00")


def test_frozen_time__freezes_time_to_a_given_timestamp():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    with frozen_time("2021-11-17T20:36:00+00:00"):
        now = pendulum.now("UTC")

    assert now == frozen_moment
