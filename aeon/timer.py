import warnings
from collections import defaultdict
from functools import update_wrapper
from operator import attrgetter
from os import path
from sys import modules
from time import time
from .measurement_store import MeasurementStore


class Timer(object):
    default_group = "default"

    def __init__(self):
        self.measurements = MeasurementStore()
        self._context = []

    def __call__(self, func_or_name, group=default_group):
        if callable(func_or_name):
            func = func_or_name
            name = func.__name__
            filename = modules[func.__module__].__file__
            module = path.splitext(path.basename(filename))[0]

            def decorated_func(*args, **kwargs):
                with self(name, module):
                    ret = func(*args, **kwargs)
                return ret
            update_wrapper(decorated_func, func)
            return decorated_func
        else:
            name = func_or_name
            self._context.append((name, group))
            if len(self._context) > 1:
                warnings.warn("You are nesting measurements in {}::{}.".format(name, group))
            return self

    def __enter__(self):
        if not self._context:
            raise ArgumentError("Please use aeon's contextmanager with",
                                "the measurement name (and optionally group) as ",
                                "argument.")
        self.measurements.start(*self._context[-1])

    def __exit__(self, type, value, traceback):
        self.measurements.stop(*self._context.pop())

    def method(self, met):
        """
        Decorator for methods that are to be included in the report.

        Basic usage:

            from time import sleep
            from aeon import timer

            class Foo(object):
                @timer.method
                def bar(self):
                    sleep(1)

            print timer

        """
        name = met.__name__

        def decorated_method(theirself, *args, **kwargs):
            group = theirself.__class__.__name__
            with self(name, group):
                ret = met(theirself, *args, **kwargs)
            return ret

        update_wrapper(decorated_method, met)
        return decorated_method

    def start(self, name, group=default_group):
        """
        Start measurement with `name` and `group`.
        Measurement is automatically created if it doesn't exist already.

        """
        self.measurements.start(name, group)

    def stop(self, name, group=default_group):
        """
        Stop measurement with `name` and `group`.

        """
        self.measurements.stop(name, group)

    def stop_last(self):
        """
        Stop the measurement that was started last.

        Helps avoiding repetitive typing of `name` and `group` when dealing
        with a sequence of measurements.

        """
        self.measurements.stop_last()

    def start_next(self, name, group=default_group):
        """
        Stop the last measurement to start a new one with `name` and `group`.

        Helps avoiding repetitive typing of `name` and `group` when dealing
        with a sequence of measurements.

        """
        self.measurements.start_next(name, group)

    def total_runtime(self):
        """
        Returns the sum of the runtime of all measurements.

        """
        return sum([m.total_runtime for m in self.measurements.all()])

    def total_walltime(self):
        """
        Returns the time that has ellapsed since the timer was created in seconds.

        """
        return time() - self.measurements.created

    def calls(self, name, group=default_group):
        """
        Returns the number of calls to the object of `group` with `name`.

        """
        return self.measurements.get(name, group).calls

    def time(self, name, group=default_group):
        """
        Returns the total runtime of the measurement of `group` with `name`.

        """
        return self.measurements.get(name, group).total_runtime

    def time_per_call(self, name, group=default_group):
        """
        Returns the average runtime for one execution of the measurement
        of `group` with `name`.

        """
        return self.measurements.get(name, group).time_per_call()

    def report(self, max_items=10):
        """
        Returns a report of the executed measurements.

        This includes the timings by group, as well as the `max_items`
        measurements with the most total runtime (by default 10).

        """
        msg = "Timings: Showing the up to {} slowest items.\n\n".format(max_items)
        separator = "+--------------------+------------------------------+--------+------------+--------------+\n"
        msg += separator
        msg += "| {:18} | {:28} | {:>6} | {:>10} | {:>12} |\n".format("class/module", "name", "calls", "total (s)", "per call (s)")
        msg += separator
        msg_row = "| {:18} | {:28} | {:>6} | {:>10.3g} | {:>12.3g} |\n"
        shown = 0
        for m in sorted(
                self.measurements.all(),
                key=attrgetter('total_runtime'),
                reverse=True):
            msg += msg_row.format(m.group, m.name, m.calls, m.total_runtime, m.time_per_call())
            shown += 1
            if shown >= max_items:
                break
        msg += separator + "\n"

        msg += "Timings grouped by class or module.\n\n"
        separator = "+--------------------+----------+------+\n"
        msg += separator
        msg += "| {:18} | {:>8} | {:>4} |\n".format('class/module', 'time (s)', '%')
        msg += separator
        for group, tot_t, share in self.grouped_measurements():
            msg += "| {:18} | {:>8.3g} | {:>4.3g} |\n".format(group, tot_t, share)
        msg += separator + "\n"

        seconds = self.total_walltime()
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        msg += "Total wall time %d:%02d:%02d." % (h, m, s)

        return msg

    def grouped_measurements(self):
        """
        Returns a list of tuples (group, runtime, share), sorted by decreasing runtime.

        It also describes either how much time went unaccounted for, or if
        there are multiple measurements at the same time at some point.

        """
        grouped_timings = defaultdict(float)
        for m in self.measurements.all():
            grouped_timings[m.group] += m.total_runtime

        recorded_time = self.total_runtime()
        wall_time = self.total_walltime()
        grouped_timings = [(group, tot_t, 100 * tot_t / wall_time) for group, tot_t in grouped_timings.iteritems()]

        diff = abs(recorded_time - wall_time)
        rel_diff = 100 * (1 - recorded_time / wall_time)
        rel_diff_desc = "redundant" if recorded_time > wall_time else "untimed"
        grouped_timings.append((rel_diff_desc, diff, rel_diff))

        grouped_timings = sorted(
            grouped_timings,
            key=lambda gt: gt[1],
            reverse=True)

        return grouped_timings

    def __str__(self):
        return self.report()
