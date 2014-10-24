from time import time
from errors import InvalidMeasurementState


class Measurement(object):
    """
    Saves number of calls and total running time of a method.

    """
    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.calls = 0
        self.total_runtime = 0.0
        self._running = False
        self._start = 0.0

    def start(self):
        if self._running:
            raise InvalidMeasurementState(
                "Measurement '{name}[{group}]' is already running. Needs to be "
                "stopped first. In interactive use, try 'from aeon "
                "import default_timer; default_timer.reset()' to reset "
                "the default timer (or reset whichever customized timer "
                "you are using).".format(
                    name=self.name, group=self.group))
        self._running = True
        self.calls += 1
        self._start = time()

    def stop(self):
        if not self._running:
            raise InvalidMeasurementState(
                "Measurement '{name}[{group}]' is not running. "
                "Needs to be started first.".format(
                    name=self.name, group=self.group))
        self._running = False
        self.total_runtime += time() - self._start

    def time_per_call(self):
        return self.total_runtime / self.calls
