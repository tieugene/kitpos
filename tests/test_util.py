"""`util.py` tests."""

from kitpos import util
from tests.samples import RAW_Q, RAW_A


def test_bytes2frame():
    """Test wrapping bytes into frame."""
    for b_list in (RAW_Q, RAW_A):
        for b in b_list:
            assert util.bytes2frame(b[4:-2]) == b


def test_frame2bytes():
    for b_list in (RAW_Q, RAW_A):
        for b in b_list:
            assert util.frame2bytes(b) == b[4:-2]

# TODO: bytes_as_response
# TODO: err
