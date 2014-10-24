from os import path
from sys import modules
from functools import wraps
from contextlib import contextmanager
from timer import Timer

default_timer = Timer()  # Series would also work here

class timed(object):
    """
    Context manager to time a piece of code.

    Basic usage just assigns a name to the measurement::

        from aeon import timed

        with timed('my_measurement'):
            sleep(1)

    To have a set of measurements grouped in the report, use the optional
    second argument::

        with timed('my_measurement', 'general_frobnication'):
            sleep(1)

    Finally, to use a timer object of your own choosing, use the `timer`
    argument::

        special_timer = timer()

        with timed('my_measurement', timer=special_timer):
            sleep(1)

    """
    def __init__(self, name, group=default_timer.default_group, timer=default_timer):
        self.timer = timer
        self.name = name
        self.group = group

    def __enter__(self):
        self.timer.start(self.name, self.group)

    def __exit__(self, type, value, traceback):
        self.timer.stop(self.name, self.group)


def mtimed(method_or_timer=default_timer):
    """
    Decorator for class methods that are to be included in the report.

    Basic usage:

        from aeon import mtimed

        class Foo(object):
            @mtimed
            def bar(self):
                sleep(1)

    Passing an argument to `mtimed` allows you to specify which timer
    instance this measurement should appear in::

        foo_timer = timer()

        class Foo(object):
            @mtimed(foo_timer)
            def bar(self):
                sleep(1)

    """
    def decorator(method):
        name = method.__name__

        @wraps(method)
        def decorated_method(self, *args, **kwargs):
            group = self.__class__.__name__
            with timed(name, group, timer):
                ret = method(self, *args, **kwargs)
            return ret

        return decorated_method

    if callable(method_or_timer):
        # the user called mtimed without arguments, python thus calls it with
        # the method to decorate (which is callable). Use the default_timer
        # object and return the decorated method.
        timer = default_timer
        return decorator(method_or_timer)
    # the user called mtimed with a timing object. Bind it to the timer name
    # and return the decorator itself. That's how python handles decorators which
    # take arguments.
    timer = method_or_timer
    return decorator


def ftimed(fn_or_timer=default_timer):
    """
    Decorator for functions that are to be included in the report.

    """
    def decorator(fn):
        name = fn.__name__
        filename = modules[fn.__module__].__file__
        module = path.splitext(path.basename(filename))[0]

        @wraps(fn)
        def decorated_function(*args, **kwargs):
            with timed(name, module, timer):
                ret = fn(*args, **kwargs)
            return ret

        return decorated_function

    if callable(fn_or_timer):
        # the user called ftimed without arguments, python thus calls it with
        # the method to decorate (which is callable). Use the default Timings
        # object and return the decorated function.
        timer = default_timer
        return decorator(fn_or_timer)
    # the user called ftimed with a timing object. Bind it to the timer name
    # and return the decorator itself. That's how python handles decorators which
    # take arguments.
    timer = fn_or_timer
    return decorator
