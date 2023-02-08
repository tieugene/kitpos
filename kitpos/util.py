"""Utility things."""
# 1. std
from typing import Union, Tuple
import struct
import datetime
import math
# 2. 3rd
import crcmod  # or crcelk
# 3. local
from kitpos import const, exc

crc = crcmod.predefined.mkCrcFun('crc-ccitt-false')  # CRC16-CCITT, LE, polynom = 0x1021, initValue=0xFFFF.


def l2b(val: bool) -> bytes:
    """Convert logical (bool) into a byte."""
    return b'\x01' if val else b'\x00'


def s2b(val: str) -> bytes:
    """Cenvert string to bytes."""
    return val.encode('cp866')


def ui2b_n(val: int, num: int) -> bytes:
    """Convert uint into n bytes."""
    return val.to_bytes(num, 'little')


def ui2b1(val: int) -> bytes:
    """Convert uint8 into byte."""
    return ui2b_n(val, 1)


def ui2b2(val: int) -> bytes:
    """Convert uint16 into 2x bytes (LE)."""
    return ui2b_n(val, 2)


def ui2b4(val: int) -> bytes:
    """Convert uint32 into 4x bytes (LE)."""
    return ui2b_n(val, 4)


def ui2vln(val: int) -> bytes:
    """Convert uintX into minimal bytes (LE)."""
    return ui2b_n(val, math.ceil(val.bit_length() / 8)) if val else b'\0'


def n2fvln(val: Union[int, float]) -> bytes:
    """Convert digit into FVLN."""
    if isinstance(val, int):
        return b'\0' + ui2vln(val)
    # float
    s_val = str(val)
    rpos = len(s_val) - s_val.index('.') - 1  # point position from right
    return ui2b1(rpos) + ui2vln(round(val * pow(10, rpos)))


def dt2b5(val: datetime.datetime) -> bytes:
    """Convert datetime into 5 bytes."""
    return struct.pack('BBBBB', val.year - 2000, val.month, val.day, val.hour, val.minute)


def b2hex(val: bytes) -> str:
    """Convert bytes to upper hex."""
    return val.hex().upper()


def b2l(val: bytes) -> bool:
    """Convert byte into bool."""
    return val == b'\x01'


def b2s(val: bytes) -> str:
    """Convert bytes of CP866 into string."""
    return val.decode('cp866')


def b2ui(val: bytes) -> int:
    """Convert bytes into UINT."""
    return int.from_bytes(val, 'little')


def fvln2n(val: bytes) -> Union[int, float]:
    """Convert FVLN bytes into number."""
    num = b2ui(val[1:])
    if pos := val[0]:
        return num / pow(10, pos)
    return num


def b2ut(val: bytes) -> datetime.datetime:
    """Convert bytes as unixtime into datetime."""
    return datetime.datetime.fromtimestamp(b2ui(val))  # TODO: tz, date only


def b2dt(val: Tuple[int, int, int, int, int]) -> datetime.datetime:
    """Convert 5xInt to datetime."""
    return datetime.datetime(2000 + val[0], val[1], val[2], val[3], val[4])


# ----
def bytes2frame(data: bytes) -> bytes:  # TODO: rename to frame_unpack
    """Wrap data into frame: <header><len><cmd>[data]<crc>."""
    if (l_data := len(data)) > 1024:  # cmd[1] + payload[1023]
        raise exc.KitPOSFrameError(f"Data too long: {l_data} bytes.")
    return const.FRAME_HEADER + (inner := l_data.to_bytes(2, 'big') + data) + crc(inner).to_bytes(2, 'little')


def frame2bytes(data: bytes) -> bytes:  # TODO: rename to frame_pack
    """Check and unwrap frame.

    :todo: use struct
    """
    # 1. chk whole len
    if (l_raw := len(data)) < 7:
        raise exc.KitPOSFrameError(f"Frame too small: {l_raw} bytes ({b2hex(data)}).")
    if l_raw > 1030:
        raise exc.KitPOSFrameError(f"Frame too big: {l_raw} bytes.")
    # 2. chk header
    if hdr := data[:2] != const.FRAME_HEADER:
        raise exc.KitPOSFrameError(f"Bad header: {b2hex(hdr)}.")
    # 3. chk payload len
    if (l_inner := int.from_bytes(data[2:4], 'big')) != l_raw - 6:
        raise exc.KitPOSFrameError(f"Bad payload len: shipped={l_inner} != real={l_raw - 6}.")
    # 4. chk crc
    if (crc_bandled := int.from_bytes(data[-2:], 'little')) != (crc_calced := crc(data[2:-2])):
        raise exc.KitPOSFrameError(f"CRC chk err: shipped=({hex(crc_bandled)}) != real=({hex(crc_calced)}).")
    return data[4:-2]


def bytes_as_response(data: bytes) -> Tuple[bool, Union[int, bytes]]:  # TODO: rename to ...
    """Expand response frame payload into (ok+data)/(err+code)."""
    # TODO: chk data len
    if (rsp_code := int(data[0])) == 0:  # 0 == ok
        return True, data[1:]
    if rsp_code == 1:  # 1 == err; 1 byte of errcode
        if len(data) != 2:
            raise exc.KitPOSFrameError(f"Bad error code len: {len(data) - 1} bytes.")
        return False, int(data[1])
    raise exc.KitPOSFrameError(f"Bad response code: {rsp_code}.")
