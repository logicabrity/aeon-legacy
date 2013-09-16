from time import time
from util import AeonError
from measurement import Measurement


class UnknownMeasurementError(AeonError):
    """ The measurement in question can't be found in the records. """
    pass


class NoMeasurementRunningError(AeonError):
    """ There is no measurement running. """
    pass


class Series(object):
    """
    Manages a series of measurements.

    They are stored by the measurements' group and name, which most
    often is module/function or class/method. However, these could also
    be user-defined.

    """
    default_group = "default"

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Reset the internal data.

        """
        self.__last = None
        self._measurements = {}
        self._created = time()

    def __key(self, name, group=default_group):
        """
        Returns the key with which a measurement is stored in the measurements dict.

        """
        return group + "::" + name

    def _exists(self, name, group=default_group):
        """
        Returns True if a measurement with `name` of `group` exists.

        """
        key = self.__key(name, group)
        return key in self._measurements

    def get(self, name, group=default_group):
        """
        Returns the measurement with `name` in `group` or raise an exception.

        """
        key = self.__key(name, group)
        try:
            return self._measurements[key]
        except KeyError:
            print "Known measurements (in format group::name):\n\t{}.".format(
                self._measurements.keys())
            raise UnknownMeasurementError("Can't find measurement '{}' of "
                                          "group '{}'.".format(name, group))

    def _put(self, measurement):
        """
        Save the `measurement` object in the measurements dict.

        """
        key = self.__key(measurement.name, measurement.group)
        self._measurements[key] = measurement

    def start(self, name, group=default_group):
        """
        Start a measurement with `name` and `group`.

        If it is a new measurement, it will be created. If it isn't, the
        existing measurement will continue.

        """
        if self._exists(name, group):
            measurement = self.get(name, group)
            measurement.start()
        else:
            measurement = Measurement(name, group)
            measurement.start()
            self._put(measurement)
        self.__last = measurement

    def stop(self, name, group=default_group):
        """
        Stop the measurement `name` of `group`.

        """
        measurement = self.get(name, group)
        measurement.stop()
        self.__last = None

    def stop_last(self):
        """
        Stop the last started measurement.

        This method exists to avoid repeating the measurement name to
        stop the measurement started last when starting measurements by
        hand using `start`.

        """
        if self.__last is None:
            raise NoMeasurementRunningError("There is no measurement to stop.")
        self.__last.stop()

    def start_next(self, name, group=default_group):
        """
        Stops the last measurement to start a new one with `name` and `group`.

        """
        if self.__last is None:
            raise NoMeasurementRunningError("There is no measurement to stop.")
        self.stop_last()
        self.start(name, group)
