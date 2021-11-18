# Plummet

Methods for testing with [pendulum](https://pendulum.eustace.io/) timestamps.

The most useful method for testing is the [frozen_time()](#frozen_time)
method which allows you to fix a moment in time so that all calls to
`pendulum.now()` return the provided timestamp.


## Methods

Here is a breakdown of the methods provided, what they do, and examples of how to use them


### momentize()

This method is used to turn a variety of different timestamps into pendulum.DateTime instances
in the UTC timezone.


#### Accepted types

* String timestamps (anything that pendulum can parse)
* datetime.datetime instances
* pendulum.DateTime instances (that might be in other timezones)
* None -- returns the current moment in UTC


#### Examples

Get the current time in UTC:

```
>>> momentize()
DateTime(2021, 11, 17, 21, 15, 0, 20728, tzinfo=Timezone('UTC'))
```


Convert a string timestamp:

```
>>> momentize("2021-11-17 21:29:00")
DateTime(2021, 11, 17, 21, 29, 0, tzinfo=Timezone('UTC'))
```
See [pendulum's documentation](https://pendulum.eustace.io/docs/#parsing) for more info.


Convert a datetime.datetime:

```
>>> momentize(datetime.datetime(2021, 11, 17, 21, 29, 0))
DateTime(2021, 11, 17, 21, 29, 0, tzinfo=Timezone('UTC'))
```


If momentize cannot convert the provided object, it will raise an exception.


### moments_match()

This method is used to compare two possibly different forms of timestamps to make sure they
are exactly equal. Under the hood, it is using `momentize()` to convert the arguments to
`pendulum.DateTime` instances and then compares the two.


#### Accepted types

* String timestamps (anything that pendulum can parse)
* datetime.datetime instances
* pendulum.DateTime instances (that might be in other timezones)
* None -- compares the current moment in UTC


#### Examples

Compare a string to a `datetime.datetime`:

```
>>> moments_match("2021-11-17 21:41:00", datetime.datetime(2021, 11, 17, 21, 41, 0))
True
```


Compare a `pendulum.DateTime` to a `datetime.datetime` in different timezones:

```
>>> moments_match(
...     pendulum.datetime(
...         2021, 11, 17, 13, 44, 0,
...         tz="America/Los_Angeles",
...         ),
...     datetime.datetime(
...         2021, 11, 17, 16, 44, 0,
...         tzinfo=datetime.timezone(datetime.timedelta(hours=-4)),
...     ),
... )
...
True
```


### frozen_time()

The `frozen_time` method is the main functionality of this package. It allows you to freeze the
time returned by `pendulum.now()` (and it's relatives) to a given moment.


#### Accepted types

* String timestamps (anything that pendulum can parse)
* datetime.datetime instances
* pendulum.DateTime instances (that might be in other timezones)
* None -- freeze at the current moment in UTC


#### Examples

Freeze time at a specific moment:

```
>>> with frozen_time("2021-11-17 22:03:00"):
...     now = pendulum.now("UTC")
...     print(now)
...
2021-11-17T22:03:00+00:00
```


## Testing

To run the testing suite:

```
$ make test
```


To run the full set of quality checks:

```
$ make qa
```
