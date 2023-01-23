"""Responses of commands.

:todo: .from_frame(bytes)?
"""
# 1. std
from typing import Tuple, Union
from dataclasses import dataclass
import struct
import datetime
# 3. local
from kitfr import const, exc, util


def dt_from_ints(v: Tuple[int]) -> datetime.datetime:
    """Convert 5xInt to datetime"""
    return datetime.datetime(2000 + v[0], v[1], v[2], v[3], v[4])


def dt2str(dt: datetime.datetime) -> str:
    """Convert datime to string"""
    return dt.strftime('%Y-%m-%d %H:%M')


@dataclass
class RspBase:
    """Base for response."""

    @property
    def _cn(self) -> str:
        """Class name shorthand."""
        return self.__class__.__name__

    @property
    def str(self) -> str:
        """Stub."""
        return ''

    def __str__(self) -> str:
        return f"{self._cn}: {self.str}"


@dataclass
class RspStub(RspBase):
    """Stub base for debugging."""
    payload: bytes

    @property
    def str(self) -> str:
        """Just dump payload."""
        return f"{len(self.payload)}: {self.payload.hex().upper()}"

    @staticmethod
    def from_bytes(data: bytes):
        """Just store."""
        return RspStub(payload=data)


@dataclass
class RspGetDeviceStatus(RspBase):
    """FR status."""
    sn: str
    datime: datetime.datetime
    err: int  # Critical errors
    status: int
    is_fs: bool
    phase: int
    wtf: int  # TODO: WTF tail 1 byte?

    @property
    def str(self) -> str:
        """String object representation."""
        return\
            f"sn={self.sn}, " \
            f"datime={dt2str(self.datime)}, " \
            f"err={self.err}, " \
            f"status={self.status}, " \
            f"is_fs={self.is_fs}, " \
            f"phase={self.phase}, " \
            f"wtf={self.wtf}"

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        fmt = '12sBBBBBBB?BB'
        if (l_data := len(data)) != struct.calcsize(fmt):
            raise exc.KitFRRspDecodeError(f"RspGetDeviceStatus: bad data len: {l_data}")  # TODO: auto class name
        v = struct.unpack(fmt, data)
        return RspGetDeviceStatus(
            sn=v[0].decode(),
            datime=dt_from_ints(v[1:6]),
            err=v[6],
            status=v[7],
            is_fs=v[8],
            phase=v[9],
            wtf=v[10]
        )


@dataclass
class RspGetDeviceModel(RspBase):
    """FR sn."""
    name: str

    @property
    def str(self) -> str:
        """String object representation."""
        return f"name={self.name}"

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        return RspGetDeviceModel(name=data.decode())


@dataclass
class RspGetStorageStatus(RspBase):
    """FS status."""
    phase: int
    cur_doc: int
    is_doc: bool
    is_session_open: bool
    flags: int
    datime: datetime.datetime
    sn: str
    last_doc_no: int

    @property
    def str(self) -> str:
        """String object representation."""
        return\
            f"phase={self.phase}, " \
            f"cur_doc={self.cur_doc}, " \
            f"is_doc={self.is_doc}, " \
            f"is_session_open={self.is_session_open}, " \
            f"flags={self.flags}, " \
            f"datime={dt2str(self.datime)}, " \
            f"sn={self.sn}, " \
            f"last_doc_no={self.last_doc_no}"

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
            datime=dt_from_ints(v[5:10]),
            sn=v[10].decode(),
            last_doc_no=v[11]
        )


class RspGetRegisterParms(RspStub):
    """FR/FS registering parameters."""
    ...


# ----
CODE2CLASS = {
    const.IEnumCmd.GetDeviceStatus: RspGetDeviceStatus,
    const.IEnumCmd.GetDeviceModel: RspGetDeviceModel,
    const.IEnumCmd.GetStorageStatus: RspGetStorageStatus,
    const.IEnumCmd.GetRegisterParms: RspGetRegisterParms,
}


def frame2rsp(cmd_code: const.IEnumCmd, frame: bytes) -> Tuple[bool, Union[int, RspBase]]:
    """Decode inbound frame into response object."""
    data = util.frame2bytes(frame)
    # 5. chk response code
    if (rsp_code := int(data[0])) == 0:  # 0 == ok
        return True, CODE2CLASS[cmd_code].from_bytes(data[1:])  # FIXME: class
    elif rsp_code == 1:  # 1 == err; 1 byte of errcode
        if (l_err_code := len(data) - 1) != 1:
            raise exc.KitFRFrameError(f"Bad error payload len: {l_err_code}")
        return False, int(data[1])
    else:
        raise exc.KitFRFrameError(f"Bad response code: {rsp_code}")
