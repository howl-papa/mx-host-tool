import pytest

from mx_host.anticoll import inventory
from mx_host.session import ReaderSession, ReaderTimeout
from tests.sim_chip import SimChip


def test_rev_b_125c_ok():
    assert ReaderSession(SimChip(revision="B", temp_c=125)).command(b"\x01") == b"\x90\x00"


def test_no_response_retries_three_times():
    chip = SimChip(mode="no_response")
    with pytest.raises(ReaderTimeout):
        ReaderSession(chip).command(b"\x01")
    assert chip.calls == 3


@pytest.mark.parametrize("n", [5, 9])
def test_many_tags(n):
    assert len(inventory(SimChip(tags=n))) == n
