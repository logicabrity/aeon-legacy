import time
from util import AeonError


class MeasurementStateError(AeonError):
    """
    A measurement is supposed to be running and isn't (or vice versa).

    Most often, this means that a measurement for a particular piece of code is
    already running and can't be started a second time. In that case, the
    measurement needs to be stopped before restarting it.

    """
    pass


class Measurement(object):
    """
    Saves number of calls and total running time of a method.

    """
    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.calls = 0
        self.total_runtime = 0.0
        self.__running = False
        self.__start = 0.0

    def start(self):
        if self.__running:
            raise MeasurementStateError(
                "Measurement '{name}[{group}]' is already running. Needs to be "
                "stopped first. In interactive use, try 'from aeon "
                "import default_timer; default_timer.reset()' to reset "
                "the default timer (or reset whichever customized timer "
                "you are using).".format(
                    name=self.name, group=self.group))
        self.__running = True
        self.calls += 1
        self.__start = time.time()

    def stop(self):
        if not self.__running:
            raise MeasurementStateError(
                "Measurement '{name}[{group}]' is not running. "
                "Needs to be started first.".format(
                    name=self.name, group=self.group))
        self.__running = False
        self.total_runtime += time.time() - self.__start

    def time_per_call(self):
        return self.total_runtime / self.calls
