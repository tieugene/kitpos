"""Responses of commands."""
# 1. std
from typing import Tuple
from dataclasses import dataclass
import struct
import datetime
# 3. local
from kitfr import const, exc


def datime5(v: Tuple[int]):
    """Convert 5xInt to datetime"""
    return datetime.datetime(2000 + v[0], v[1], v[2], v[3], v[4])


class RspBase:
    """Base for response."""


@dataclass
class RspGetDeviceStatus(RspBase):
    """Get FR status."""
    sn: str
    datime: datetime.datetime
    crit_err: int
    status: int
    is_fs: bool
    phase: int
    wtf: int  # TODO: WTF tail 1 byte?

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        fmt = '12sBBBBBBB?BB'
        # print(data.hex().upper())
        if (l_data := len(data)) != struct.calcsize(fmt):
            raise exc.KitFRRspDecodeError(f"RspGetDeviceStatus: bad data len: {l_data}")  # TODO: auto class name
        v = struct.unpack(fmt, data)
        # print(v)
        return RspGetDeviceStatus(
            sn=v[0].decode(),
            datime=datime5(v[1:6]),
            crit_err=v[6],
            status=v[7],
            is_fs=v[8],
            phase=v[9],
            wtf=v[10]
        )


@dataclass
class RspGetDeviceModel(RspBase):
    """Get FR sn."""
    sn: str

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        return RspGetDeviceModel(sn=data.decode())


@dataclass
class RspGetStorageStatus(RspBase):
    """Get FR status."""
    phase: int
    cur_doc: int
    is_doc: bool
    is_session_open: bool
    flags: int
    datime: datetime.datetime
    sn: str
    last_doc_no: int
    # wtf: int

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        fmt = '<BB??BBBBBB16sI'
        # print(data.hex().upper())
        if (l_data := len(data)) != struct.calcsize(fmt):
            raise exc.KitFRRspDecodeError(f"RspGetStorageStatus: bad data len: {l_data}")  # TODO: auto class name
        v = struct.unpack(fmt, data)
        # print(v)
        return RspGetStorageStatus(
            phase=v[0],
            cur_doc=v[1],
            is_doc=v[2],
            is_session_open=v[3],
            flags=v[4],
            datime=datime5(v[5:10]),
            sn=v[10].decode(),
            last_doc_no=v[11]
        )


CODE2CLASS = {
    const.IEnumCmd.GetDeviceStatus: RspGetDeviceStatus,
    const.IEnumCmd.GetDeviceModel: RspGetDeviceModel,
    const.IEnumCmd.GetStorageStatus: RspGetStorageStatus,
}
