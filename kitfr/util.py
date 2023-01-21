"""Utility things."""
from typing import Union, Tuple

import crcmod  # or crcelk

from kitfr import const, exc, rsp

crc = crcmod.predefined.mkCrcFun('crc-ccitt-false')  # CRC16-CCITT, LE, polynom = 0x1021, initValue=0xFFFF.


def bytes2frame(data: bytes) -> bytes:
    """Wrap data into frame: <header><len><cmd>[data]<crc>.

    :todo: use struct
    """
    if (l := len(data)) > 1024:  # cmd[1] + payload[1023]
        raise exc.KitFRFrameError(f"Data too long: {l} bytes.")
    inner = (len(data)).to_bytes(2, 'big') + data
    return const.FRAME_HEADER + inner + crc(inner).to_bytes(2, 'little')


def frame2bytes(data: bytes) -> bytes:
    """Unwrap frame.

    :todo: use struct
    """
    # 1. chk whole len
    if not (7 <= (l_raw := len(data)) <= 1030):
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


def frame2rsp(cmd_code: const.IEnumCmd, frame: bytes) -> Tuple[bool, Union[int, rsp.RspBase]]:
    """Decode inbound frame into response object."""
    data = frame2bytes(frame)
    # 5. chk response code
    if (rsp_code := int(data[0])) == 0:  # 0 == ok
        return True, rsp.CODE2CLASS[cmd_code].from_bytes(data[1:])  # FIXME: class
    elif rsp_code == 1:  # 1 == err; 1 byte of errcode
        if (l_err_code := len(data) - 1) != 1:
            raise exc.KitFRFrameError(f"Bad error payload len: {l_err_code}")
        return False, int(data[1])
    else:
        raise exc.KitFRFrameError(f"Bad response code: {rsp_code}")
