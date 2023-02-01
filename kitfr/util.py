"""Utility things."""
# 1. std
from typing import Union, Tuple
import struct
import datetime
import math
# 2. 3rd
import crcmod  # or crcelk
# 3. local
from kitfr import const, exc

crc = crcmod.predefined.mkCrcFun('crc-ccitt-false')  # CRC16-CCITT, LE, polynom = 0x1021, initValue=0xFFFF.


def l2b(v: bool) -> bytes:
    """Convert logical (bool) into a byte."""
    return b'\x01' if v else b'\x00'


def s2b(v: str) -> bytes:
    """Cenvert string to bytes."""
    return v.encode('cp866')


def _ui2b(v: int, w: int) -> bytes:
    """Convert uint into w bytes."""
    return v.to_bytes(w, 'little')


def ui2b1(v: int) -> bytes:
    """Convert uint8 into byte."""
    return _ui2b(v, 1)


def ui2b2(v: int) -> bytes:
    """Convert uint16 into 2x bytes (LE)."""
    return _ui2b(v, 2)


def ui2b4(v: int) -> bytes:
    """Convert uint32 into 4x bytes (LE)."""
    return _ui2b(v, 4)


def ui2vln(v: int) -> bytes:
    """Convert uintX into minimal bytes (LE)."""
    if v:
        return _ui2b(v, math.ceil(v.bit_length()/8))
    else:
        return b'\0'


def n2fvln(v: Union[int, float]) -> bytes:
    """Convert digit into FVLN."""
    if isinstance(v, int):
        return b'\0' + ui2vln(v)
    else:  # float
        s = str(v)
        rpos = len(s) - s.index('.') - 1  # point position from right
        return ui2b1(rpos) + ui2vln(round(v * pow(10, rpos)))


def dt2b5(v: datetime.datetime) -> bytes:
    """Convert datetime into 5 bytes."""
    return struct.pack('BBBBB', v.year - 2000, v.month, v.day, v.hour, v.minute)


def b2hex(v: bytes) -> str:
    """Convert bytes to upper hex."""
    return v.hex().upper()


def b2l(v: bytes) -> bool:
    """Convert byte into bool."""
    return v == b'\x01'


def b2s(v: bytes) -> str:
    """Convert bytes of CP866 into string."""
    return v.decode('cp866')


def b2ui(v: bytes) -> int:
    """Convert bytes into UINT."""
    return int.from_bytes(v, 'little')


def fvln2n(v: bytes) -> Union[int, float]:
    """Convert FVLN bytes into number."""
    num = b2ui(v[1:])
    if pos := v[0]:
        return num / pow(10, pos)
    else:
        return num


def b2ut(v: bytes) -> datetime.datetime:
    """Convert bytes as unixtime into datetime."""
    return datetime.datetime.fromtimestamp(b2ui(v))  # TODO: tz, date only


def b2dt(v: Tuple[int, int, int, int, int]) -> datetime.datetime:
    """Convert 5xInt to datetime"""
    return datetime.datetime(2000 + v[0], v[1], v[2], v[3], v[4])


# ----
def bytes2frame(data: bytes) -> bytes:  # TODO: rename to frame_unpack
    """Wrap data into frame: <header><len><cmd>[data]<crc>."""
    if (l := len(data)) > 1024:  # cmd[1] + payload[1023]
        raise exc.KitFRFrameError(f"Data too long: {l} bytes.")
    return const.FRAME_HEADER + (inner := (len(data)).to_bytes(2, 'big') + data) + crc(inner).to_bytes(2, 'little')


def frame2bytes(data: bytes) -> bytes:  # TODO: rename to frame_pack
    """Check and unwrap frame.

    :todo: use struct
    """
    # 1. chk whole len
    if (l_raw := len(data)) < 7:
        raise exc.KitFRFrameError(f"Frame too small: {l_raw} bytes ({b2hex(data)}).")
    elif l_raw > 1030:
        raise exc.KitFRFrameError(f"Frame too big: {l_raw} bytes.")
    # 2. chk header
    if h := data[:2] != const.FRAME_HEADER:
        raise exc.KitFRFrameError(f"Bad header: {b2hex(h)}.")
    # 3. chk payload len
    if (l_inner := int.from_bytes(data[2:4], 'big')) != l_raw - 6:
        raise exc.KitFRFrameError(f"Bad payload len: shipped={l_inner} != real={l_raw - 6}.")
    # 4. chk crc
    if (crc_bandled := int.from_bytes(data[-2:], 'little')) != (crc_calced := crc(data[2:-2])):
        raise exc.KitFRFrameError(f"CRC chk err: shipped=({hex(crc_bandled)}) != real=({hex(crc_calced)}).")
    return data[4:-2]


def bytes_as_response(data: bytes) -> Tuple[bool, Union[int, bytes]]:  # TODO: rename to ...
    """Expand response frame payload into (ok+data)/(err+code)."""
    # TODO: chk data len
    if (rsp_code := int(data[0])) == 0:  # 0 == ok
        return True, data[1:]
    elif rsp_code == 1:  # 1 == err; 1 byte of errcode
        if len(data) != 2:
            raise exc.KitFRFrameError(f"Bad error code len: {len(data) - 1} bytes.")
        return False, int(data[1])
    else:
        raise exc.KitFRFrameError(f"Bad response code: {rsp_code}.")
