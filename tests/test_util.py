"""`util.py` tests."""

from kitpos import util
from tests.samples import RAW_Q, RAW_A


def test_bytes2frame():
    """Test wrapping bytes into frame."""
    for b_list in (RAW_Q, RAW_A):
        for b in b_list:
            assert util.frame_pack(b[4:-2]) == b


def test_frame2bytes():
    for b_list in (RAW_Q, RAW_A):
        for b in b_list:
            assert util.frame_unpack(b) == b[4:-2]

# TODO: frame_payload_dispatch
# TODO: err
