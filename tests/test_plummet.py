from datetime import datetime, timedelta, timezone
from unittest import mock

import pendulum
import pytest

import plummet


def test_momentize__returns_timestamp_for_now_when_called_with_None():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    with plummet.frozen_time(frozen_moment):
        now = plummet.momentize()
        assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_string_without_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = plummet.momentize("2021-11-17T20:36:00")
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_string_with_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = plummet.momentize("2021-11-17T12:36:00-08:00")
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_datetime_without_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = plummet.momentize(datetime(2021, 11, 17, 20, 36, 00))
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_datetime_with_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = plummet.momentize(datetime(2021, 11, 17, 12, 36, 0, tzinfo=timezone(timedelta(hours=-8))))
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_pendulum_datetime_without_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = plummet.momentize(pendulum.parse("2021-11-17T20:36:00"))
    assert now == frozen_moment


def test_momentize__returns_timestamp_in_utc_from_pendulum_datetime_with_timezone():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    now = plummet.momentize(pendulum.parse("2021-11-17T12:36:00-08:00"))
    assert now == frozen_moment


def test_momentize__raises_error_if_unmappable_object_is_passed():
    with pytest.raises(plummet.PlummetError, match="Cannot create a moment"):
        plummet.momentize(object())


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
        assert plummet.moments_match(frozen_moment, moment)

    with pytest.raises(plummet.PlummetError, match="Moments do not match"):
        plummet.moments_match(frozen_moment, "1970-01-01T00:00:00+00:00")


@pytest.mark.skipif(not plummet.has_time_machine, reason="time-machine is not available")
def test_frozen_time__freezes_time_using_time_machine_if_available():
    pytest.importorskip("time_machine")
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    with plummet.frozen_time("2021-11-17T20:36:00+00:00"):
        pendulum_now = pendulum.now("UTC")
        datetime_now = datetime.now(tz=timezone.utc)

    assert pendulum_now == plummet.momentize(datetime_now) == frozen_moment


def test_frozen_time__freezes_time_using_pendulum_test():
    frozen_moment = pendulum.parse("2021-11-17T20:36:00+00:00")
    with mock.patch.object(plummet, "has_time_machine", new=False):
        with plummet.frozen_time("2021-11-17T20:36:00+00:00"):
            now = pendulum.now("UTC")

    assert now == frozen_moment
