import time
import pytest
from aeon.measurement import Measurement
from aeon.errors import InvalidMeasurementState


def test_cant_start_measurement_twice():
    m = Measurement("name", "group")
    m.start()
    with pytest.raises(InvalidMeasurementState):
        m.start()


def test_cant_stop_measurement_before_starting_it():
    m = Measurement("name", "group")
    with pytest.raises(InvalidMeasurementState):
        m.stop()


def test_cant_stop_measurement_twice():
    m = Measurement("name", "group")
    m.start()
    m.stop()
    with pytest.raises(InvalidMeasurementState):
        m.stop()


def test_starting_measurement_increases_number_of_calls():
    m = Measurement("name", "group")
    assert m.calls == 0
    m.start()
    assert m.calls == 1


def test_measurement_measures_something():
    m = Measurement("name", "group")

    m.start()
    time.sleep(1e-3)
    m.stop()
    elapsed = m.total_runtime
    assert elapsed > 0

    m.start()
    time.sleep(1e-3)
    m.stop()
    elapsed_again = m.total_runtime
    assert elapsed_again > elapsed


@pytest.mark.fixed
def test_measurement_has_name_and_group():
    m = Measurement("name", "group")
    assert m.name == "name"
    assert m.group == "group"
