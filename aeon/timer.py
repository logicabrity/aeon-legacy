from time import time
from operator import attrgetter
from collections import defaultdict
from series import Series


class Timer(Series):
    """
    Extends Series to support queries and print nice measurement results.

    """
    def total_runtime(self):
        """
        Returns the sum of the runtime of all measurements.

        """
        return sum([m.total_runtime for m in self._measurements.itervalues()])

    def total_walltime(self):
        """
        Returns the time that has ellapsed since the timer was created in seconds.

        """
        return time() - self._created

    def calls(self, name, group=Series.default_group):
        """
        Returns the number of calls to the object of `group` with `name`.

        """
        measurement = self.get(name, group)
        return measurement.calls

    def time(self, name, group=Series.default_group):
        """
        Returns the total runtime of the measurement of `group` with `name`.

        """
        measurement = self.get(name, group)
        return measurement.total_runtime

    def time_per_call(self, name, group=Series.default_group):
        """
        Returns the average runtime for one execution of the measurement
        of `group` with `name`.

        """
        measurement = self.get(name, group)
        return measurement.time_per_call

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
                self._measurements.values(),
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
        for group, tot_t, share in self.grouped_timings():
            msg += "| {:18} | {:>8.3g} | {:>4.2g} |\n".format(group, tot_t, share)
        msg += separator + "\n"

        seconds = time() - self._created
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        msg += "Total wall time %d:%02d:%02d." % (h, m, s)

        return msg

    def grouped_timings(self):
        """
        Returns a list of tuples (group, runtime, share), sorted by decreasing runtime.

        It also describes either how much time went unaccounted for, or if
        there are multiple measurements at the same time at some point.

        """
        grouped_timings = defaultdict(float)
        for m in self._measurements.values():
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
