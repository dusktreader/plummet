import datetime
from typing import Union

import buzz
import pendulum

try:
    import time_machine

    has_time_machine = True
except ImportError:
    has_time_machine = False


class PlummetError(buzz.Buzz):
    """
    Custom exception for the plummet package
    """

    pass


AGGREGATE_TYPE = Union[None, str, datetime.datetime, pendulum.DateTime]


def frozen_time(moment: AGGREGATE_TYPE = None):
    """
    Returns the ``pendulum.test()`` context manager initialized with
    a momentized timestamp.

    If time-machine is installed, it will use ``travel()`` instead so
    that calls to datetime.now() are also affected.

    """
    if has_time_machine:
        return time_machine.travel(momentize(moment), tick=False)
    else:
        return pendulum.test(momentize(moment))


def momentize(moment: AGGREGATE_TYPE = None):
    """
    Produces a pendulum.DateTime instance in UTC given a string
    timestamp, a datetime instance, a pendulum instance, or the
    current time (if passed None).

    Raises an exception if another type is passed.
    """
    if moment is None:
        return pendulum.now("UTC")
    elif isinstance(moment, str):
        return pendulum.parse(moment, tz="UTC")
    elif isinstance(moment, datetime.datetime):
        return pendulum.instance(moment).in_tz("UTC")
    elif isinstance(moment, pendulum.DateTime):
        return moment.in_tz("UTC")
    else:
        raise PlummetError(f"Cannot create a moment from {moment}")


def moments_match(moment1: AGGREGATE_TYPE, moment2: AGGREGATE_TYPE):
    """
    Checks that two moments match. If they do not, raises an exception.
    """
    fixed_moment1 = momentize(moment1)
    fixed_moment2 = momentize(moment2)
    PlummetError.require_condition(
        fixed_moment1 == fixed_moment2,
        f"Moments do not match: {fixed_moment1} != {fixed_moment2}",
    )
    return True
