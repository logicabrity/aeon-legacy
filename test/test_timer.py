import pytest
import time
from aeon.timer import Timer
from aeon.measurement_store import MeasurementStore

EPSILON = 1e-16


def test_context():
    timer = Timer()

    for i in range(4):
        with timer('context', 'test_helpers'):
            pass
    assert timer.calls('context', 'test_helpers') == 4


def test_context_without_group_should_use_default_group():
    timer = Timer()

    for i in range(4):
        with timer('context_alt'):
            pass
    assert timer.calls('context_alt', Timer.default_group) == 4


def test_context_is_exception_safe():
    class ExampleError(Exception):
        pass

    timer = Timer()
    with pytest.raises(ExampleError):
        with timer("exception_test"):
            raise ExampleError("Example")

    with timer("exception_test"):
        print("We can do this because the last measurement was stopped gracefully.")


def test_decorated_function():
    timer = Timer()

    @timer
    def my_func():
        pass

    my_func()
    assert timer.calls('my_func', 'test_timer') == 1

    @timer
    def my_func_two(a):
        pass

    my_func_two(1)
    assert timer.calls('my_func_two', 'test_timer') == 1


def test_decorated_function_keeps_docstring():
    timer = Timer()

    @timer
    def my_func():
        """ my docstring """

    my_func()

    assert my_func.__doc__ == " my docstring "


def test_decorated_method():
    timer = Timer()

    class Foo(object):
        @timer.method
        def bar(self):
            pass

        @timer.method
        def baz(self, a):
            pass

    foo = Foo()
    foo.bar()
    foo.baz(1)
    assert timer.calls('bar', 'Foo') == 1
    assert timer.calls('baz', 'Foo') == 1


def test_nested_methods():
    timer = Timer()

    class Foo(object):
        @timer.method
        def __init__(self):
            self.nested()
            self.nested()

        @timer.method
        def nested(self):
            pass

    f = Foo()
    assert timer.calls('__init__', 'Foo') == 1
    assert timer.calls('nested', 'Foo') == 2


def test_return_values_of_functions_and_methods_should_not_be_affected():
    timer = Timer()

    @timer
    def returns_one():
        return 1
    assert returns_one() == 1

    class MyClass(object):
        @timer.method
        def returns_two(self):
            return 2
    mo = MyClass()
    assert mo.returns_two() == 2


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
    time.sleep(1e-3)
    elapsed_again = t.total_walltime()
    assert elapsed_again >= elapsed


@pytest.mark.fixed
def test_timer_per_call():
    t = Timer()
    for i in range(10):
        t.start("foo")
        t.stop("foo")
    assert abs(t.time_per_call("foo") - t.time("foo")/t.calls("foo")) < EPSILON


def test_can_return_a_report():
    t = Timer()
    print(t.report())

    t.start("foo")
    t.stop("foo")
    t.start("bar")
    t.stop("bar")
    print(t.report())
    print(t.report(1))
    print(t)
