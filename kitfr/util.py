"""Utility things."""
# 1. std
# 2. 3rd
import crcmod  # or crcelk
# 3. local
from kitfr import const, exc

crc = crcmod.predefined.mkCrcFun('crc-ccitt-false')  # CRC16-CCITT, LE, polynom = 0x1021, initValue=0xFFFF.


def bytes2frame(data: bytes) -> bytes:
    """Wrap data into frame: <header><len><cmd>[data]<crc>."""
    if (l := len(data)) > 1024:  # cmd[1] + payload[1023]
        raise exc.KitFRFrameError(f"Data too long: {l} bytes.")
    return const.FRAME_HEADER + (inner := (len(data)).to_bytes(2, 'big') + data) + crc(inner).to_bytes(2, 'little')


def frame2bytes(data: bytes) -> bytes:
    """Unwrap frame.

    :todo: use struct
    """
    # 1. chk whole len
    if not (7 <= (l_raw := len(data)) <= 1030):
        # FIXME: 2 bytes (bulk 3342 × GetDocByNum from .88)
        raise exc.KitFRFrameError(f"Raw data bad len: {l_raw} bytes.")
    # 2. chk header
    if h := data[:2] != const.FRAME_HEADER:
        raise exc.KitFRFrameError(f"Bad header: {h.hex()}.")
    # 3. chk payload len
    if (l_inner := int.from_bytes(data[2:4], 'big')) != l_raw - 6:
        raise exc.KitFRFrameError(f"Bad payload len: {l_inner}.")
    # 4. chk crc
    if (crc_bandled := int.from_bytes(data[-2:], 'little')) != (crc_calced := crc(data[2:-2])):
        raise exc.KitFRFrameError(f"CRC bundled ({hex(crc_bandled)}) != CRC calculated ({hex(crc_calced)}).")
    return data[4:-2]
