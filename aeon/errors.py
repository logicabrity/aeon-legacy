class AeonError(Exception):
    pass


class InvalidMeasurementState(AeonError):
    """
    This measurement is supposed to be running and isn't (or vice versa).

    Most often this means you're trying to start a measurement again, but it's
    already running because you forgot to stop it before.

    """
    pass


class UnknownMeasurement(AeonError):
    """
    The measurement in question can't be found in the records.

    """
    pass


class NoMeasurementRunning(AeonError):
    """
    There is no measurement running.

    """
    pass
