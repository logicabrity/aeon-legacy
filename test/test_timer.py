import pytest
from aeon.timer import Timer

EPSILON = 1e-16


def test_total_runtime_sums_individual_runtimes():
    t = Timer()
    t.start("foo")
    t.stop("foo")
    assert t.time("foo") == t.total_runtime()

    t.start("bar")
    t.stop("bar")
    assert abs(t.total_runtime() - t.time("foo") - t.time("bar")) < EPSILON


def test_total_walltime_measures_time_passing():
    t = Timer()
    elapsed = t.total_walltime()
    elapsed_again = t.total_walltime()
    assert elapsed_again >= elapsed


@pytest.mark.fixed
def test_timer_per_call():
    t = Timer()
    for i in xrange(10):
        t.start("foo")
        t.stop("foo")
    assert abs(t.time_per_call("foo") - t.time("foo")/t.calls("foo")) < EPSILON


def test_can_return_a_report():
    t = Timer()
    print t.report()

    t.start("foo")
    t.stop("foo")
    t.start("bar")
    t.stop("bar")
    print t.report()
    print t.report(1)
    print t
