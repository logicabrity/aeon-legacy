from time import time
from .errors import UnknownMeasurement, NoMeasurementRunning
from .measurement import Measurement


class MeasurementStore(object):
    """
    Manages a series of measurements.

    """
    def __init__(self):
        self.reset()

    def reset(self):
        """
        Reset the internal data.

        """
        self.running_measurement = None
        self.store = {}
        self.created = time()

    def _key(self, name, group=""):
        """
        Returns the key with which a measurement is stored in the measurements dict.

        """
        return group + "::" + name

    def _put(self, measurement):
        """
        Store the `measurement` object in the measurements dict.

        """
        key = self._key(measurement.name, measurement.group)
        self.store[key] = measurement

    def all(self):
        """
        Return an iterator over all measurements.

        """
        return self.store.itervalues()

    def exists(self, name, group=""):
        """
        Returns True if a measurement with `name` of `group` exists.

        """
        key = self._key(name, group)
        return key in self.store

    def get(self, name, group=""):
        """
        Returns the measurement with `name` in `group` or raise an exception.

        """
        key = self._key(name, group)
        try:
            return self.store[key]
        except KeyError:
            print "Known measurements (in format group::name):\n\t{}.".format(
                self.store.keys())
            raise UnknownMeasurement("Can't find measurement '{}' of "
                                     "group '{}'.".format(name, group))

    def start(self, name, group=""):
        """
        Start a measurement with `name` and `group`.

        Will create a new measurement if it doesn't exist already.

        """
        try:
            measurement = self.get(name, group)
        except UnknownMeasurement:
            measurement = Measurement(name, group)
            self._put(measurement)
        measurement.start()
        self.running_measurement = measurement

    def stop(self, name, group=""):
        """
        Stop the measurement `name` of `group`.

        """
        measurement = self.get(name, group)
        measurement.stop()
        self.running_measurement = None

    def stop_last(self):
        """
        Stop the last started measurement.

        This method exists to avoid repeating the measurement name to
        stop the measurement started last when starting measurements by
        hand using `start`.

        """
        if self.running_measurement is None:
            raise NoMeasurementRunning("There is no measurement to stop.")
        self.running_measurement.stop()
        self.running_measurement = None

    def start_next(self, name, group=""):
        """
        Stops the last measurement to start a new one with `name` and `group`.

        """
        if self.running_measurement is None:
            raise NoMeasurementRunning("There is no measurement to stop.")
        self.stop_last()
        self.start(name, group)
