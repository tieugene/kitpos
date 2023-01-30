"""Utility things."""
# 1. std
from typing import Union, Tuple
import struct
import datetime
# 2. 3rd
import crcmod  # or crcelk
# 3. local
from kitfr import const, exc

crc = crcmod.predefined.mkCrcFun('crc-ccitt-false')  # CRC16-CCITT, LE, polynom = 0x1021, initValue=0xFFFF.


def b2h(v: bytes) -> str:
    """Convert bytes to upper hex."""
    return v.hex().upper()


def b2s(v: bytes) -> str:
    """Convert bytes of CP866 into string."""
    return v.decode()  # FIXME: CP866


def b2dt(v: Tuple[int, int, int, int, int]) -> datetime.datetime:
    """Convert 5xInt to datetime"""
    return datetime.datetime(2000 + v[0], v[1], v[2], v[3], v[4])


def l2b(v: bool) -> bytes:
    """Convert logical (bool) into a byte."""
    return b'\x01' if v else b'\x00'


def ui2b2(v: int) -> bytes:
    """Convert uint16 into 2x bytes (LE)."""
    return v.to_bytes(2, 'little')


def ui2b4(v: int) -> bytes:
    """Convert uint32 into 4x bytes (LE)."""
    return v.to_bytes(4, 'little')


def dt2b(dt: datetime.datetime) -> bytes:
    """Convert datetime into 5 bytes."""
    return struct.pack('BBBBB', dt.year - 2000, dt.month, dt.day, dt.hour, dt.minute)


def bytes2frame(data: bytes) -> bytes:
    """Wrap data into frame: <header><len><cmd>[data]<crc>."""
    if (l := len(data)) > 1024:  # cmd[1] + payload[1023]
        raise exc.KitFRFrameError(f"Data too long: {l} bytes.")
    return const.FRAME_HEADER + (inner := (len(data)).to_bytes(2, 'big') + data) + crc(inner).to_bytes(2, 'little')


def frame2bytes(data: bytes) -> bytes:
    """Check and unwrap frame.

    :todo: use struct
    """
    # 1. chk whole len
    if (l_raw := len(data)) < 7:
        raise exc.KitFRFrameError(f"Frame too small: {l_raw} bytes ({b2h(data)}).")
    elif l_raw > 1030:
        raise exc.KitFRFrameError(f"Frame too big: {l_raw} bytes.")
    # 2. chk header
    if h := data[:2] != const.FRAME_HEADER:
        raise exc.KitFRFrameError(f"Bad header: {b2h(h)}.")
    # 3. chk payload len
    if (l_inner := int.from_bytes(data[2:4], 'big')) != l_raw - 6:
        raise exc.KitFRFrameError(f"Bad payload len: shipped={l_inner} != real={l_raw - 6}.")
    # 4. chk crc
    if (crc_bandled := int.from_bytes(data[-2:], 'little')) != (crc_calced := crc(data[2:-2])):
        raise exc.KitFRFrameError(f"CRC chk err: shipped=({hex(crc_bandled)}) != real=({hex(crc_calced)}).")
    return data[4:-2]


def bytes_as_response(data: bytes) -> Tuple[bool, Union[int, bytes]]:
    """Expand response into (ok+data)/(err+code)."""
    # TODO: chk data len
    if (rsp_code := int(data[0])) == 0:  # 0 == ok
        return True, data[1:]
    elif rsp_code == 1:  # 1 == err; 1 byte of errcode
        if len(data) != 2:
            raise exc.KitFRFrameError(f"Bad error code len: {len(data) - 1} bytes.")
        return False, int(data[1])
    else:
        raise exc.KitFRFrameError(f"Bad response code: {rsp_code}.")
