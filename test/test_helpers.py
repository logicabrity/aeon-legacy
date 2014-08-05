from aeon.helpers import default_timer, ftimed, mtimed, timed
from aeon.timer import Timer
import pytest

def test_decorated_function():
    timer = Timer()

    @ftimed(timer)
    def my_func():
        pass

    my_func()
    assert timer.calls('my_func', 'test_helpers') == 1


def test_decorated_function_default_timer():

    @ftimed  # without parantheses
    def my_func():
        pass

    for i in xrange(2):
        my_func()
    assert default_timer.calls('my_func', 'test_helpers') == 2

    @ftimed()  # with parentheses
    def my_func_alt():
        pass

    for i in xrange(2):
        my_func_alt()
    assert default_timer.calls('my_func_alt', 'test_helpers') == 2


def test_decorated_method():
    timer = Timer()

    class Foo(object):
        @mtimed(timer)
        def bar(self):
            pass

    foo = Foo()
    for i in xrange(3):
        foo.bar()
    assert timer.calls('bar', 'Foo') == 3


def test_decorated_method_default_timer():
    class Foo(object):
        @mtimed()  # with parentheses
        def bar(self):
            pass

        @mtimed  # without parentheses
        def bar_alt(self):
            pass

    foo = Foo()
    for i in xrange(3):
        foo.bar()
        foo.bar_alt()

    assert default_timer.calls('bar', 'Foo') == 3
    assert default_timer.calls('bar_alt', 'Foo') == 3


def test_return_values_of_functions_and_methods_should_not_be_affected():
    @ftimed
    def returns_one():
        return 1
    assert returns_one() == 1

    class MyClass(object):
        @mtimed
        def returns_two(self):
            return 2
    mo = MyClass()
    assert mo.returns_two() == 2


def test_context():
    timer = Timer()

    for i in xrange(4):
        with timed('context', 'test_helpers', timer=timer):
            pass
    assert timer.calls('context', 'test_helpers') == 4


def test_context_without_group_should_use_default_group():
    timer = Timer()

    for i in xrange(4):
        with timed('context_alt', timer=timer):
            pass
    assert timer.calls('context_alt', Timer.default_group) == 4


def test_context_default_timer():
    for i in xrange(3):
        with timed('context_default'):
            pass
    assert default_timer.calls('context_default') == 3


def test_context_is_exception_safe():
    class ExampleError(Exception):
        pass

    with pytest.raises(ExampleError):
        with timed("exception_test"):
            raise ExampleError("Example")

    with timed("exception_test"):
        print "We can do this because the last measurement was stopped gracefully."
