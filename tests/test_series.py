import pytest
from aeon.series import (
    Series, UnknownMeasurementError, NoMeasurementRunningError
)
from aeon.measurement import MeasurementStateError


def test_start_measurement():
    s = Series()
    s.start("one", "test_series")


def test_stop_measurement():
    s = Series()
    s.start("one", "test_series")
    s.stop("one", "test_series")


def test_cant_stop_nonexistent_measurement():
    s = Series()
    with pytest.raises(UnknownMeasurementError):
        s.stop("one", "test_series")


def test_can_retrieve_measurement():
    s = Series()
    s.start("one", "test_series")
    m = s.get("one", "test_series")


def test_there_is_a_default_group():
    s = Series()
    s.start("one")
    m = s.get("one")


def test_can_stop_last_started_measurement():
    s = Series()
    s.start("one")
    s.stop_last()

    with pytest.raises(MeasurementStateError):
        s.stop("one")  # this will have been stopped by stop_last


def test_more_than_one_measurement_can_run_at_the_same_time():
    # this might be a bug and not a feature
    s = Series()
    s.start("one")
    s.start("two")
    s.stop_last()
    s.stop("one")
