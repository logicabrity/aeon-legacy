import pytest
import aeon.errors as err
from aeon.measurement_store import MeasurementStore


def test_start_measurement():
    s = MeasurementStore()
    s.start("one", "test_series")


def test_stop_measurement():
    s = MeasurementStore()
    s.start("one", "test_series")
    s.stop("one", "test_series")


def test_cant_stop_nonexistent_measurement():
    s = MeasurementStore()
    with pytest.raises(err.UnknownMeasurement):
        s.stop("one", "test_series")


def test_can_retrieve_measurement():
    s = MeasurementStore()
    s.start("one", "test_series")
    m = s.get("one", "test_series")


def test_there_is_a_default_group():
    s = MeasurementStore()
    s.start("one")
    m = s.get("one")


def test_can_stop_last_started_measurement():
    s = MeasurementStore()
    s.start("one")
    s.stop_last()

    with pytest.raises(err.InvalidMeasurementState):
        s.stop("one")  # this will have been stopped by stop_last


def test_start_next():
    s = MeasurementStore()
    s.start("one")
    s.start_next("two")

    with pytest.raises(err.InvalidMeasurementState):
        s.stop("one")  # this will have been stopped by start_next


def test_start_next_only_if_other_measurement_running():
    s = MeasurementStore()
    with pytest.raises(err.NoMeasurementRunning):
        s.start_next("two")


def test_cant_stop_last_if_not_started():
    s = MeasurementStore()
    with pytest.raises(err.NoMeasurementRunning):
        s.stop_last()


def test_more_than_one_measurement_can_run_at_the_same_time():
    # this might be a bug and not a feature
    s = MeasurementStore()
    s.start("one")
    s.start("two")
    s.stop_last()
    s.stop("one")
