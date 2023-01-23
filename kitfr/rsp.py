"""Responses of commands.

:todo: .from_frame(bytes)?
"""
# 1. std
from typing import Tuple, Union, Any
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


def data_decode(data: bytes, fmt: str, cls) -> Tuple[Any]:
    """Check data length against struct format."""
    if (l_data := len(data)) != struct.calcsize(fmt):
        raise exc.KitFRRspDecodeError(f"{cls.__name__}: bad data len: {l_data}")
    return struct.unpack(fmt, data)


@dataclass
class RspBase:
    """Base for response."""

    @property
    def _cn(self) -> str:
        """Class name shorthand."""
        return self.__class__.__name__

    @property
    def str(self) -> str:  # TODO: auto
        """Stub."""
        return ", ".join([f"{f}={self.__dict__[f]}" for f in self.__annotations__])

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

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        v = data_decode(data, '12sBBBBBBB?BB', RspGetDeviceStatus)
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

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        v = data_decode(data, '<BB??BBBBBB16sI', RspGetStorageStatus)
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


@dataclass
class RspGetRegisterParms(RspBase):
    """FR/FS registering parameters."""
    rn: str
    inn: str
    mode: int
    tax: int
    agent: int

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        v = data_decode(data, '20s12sBBB', RspGetRegisterParms)
        return RspGetRegisterParms(
            rn=v[0].decode().rstrip(),
            inn=v[1].decode().rstrip(),
            mode=v[2],
            tax=v[3],
            agent=v[4]
        )


class RspGetDocByNum(RspStub):
    """FD."""
    ...  # N


@dataclass
class RspGetOFDXchgStatus(RspBase):
    """OFD exchange status."""
    status: int
    state_ofd: int
    out_count: int
    next_doc_n: int
    next_doc_d: datetime.datetime

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        v = data_decode(data, '<BBHIBBBBB', RspGetOFDXchgStatus)  # 13
        return RspGetOFDXchgStatus(
            status=v[0],
            state_ofd=v[1],
            out_count=v[2],
            next_doc_n=v[3],
            next_doc_d=dt_from_ints(v[4:])
        )


class RspGetDateTime(RspStub):
    """FS date/time."""
    ...  # 9


# ----
CODE2CLASS = {
    const.IEnumCmd.GetDeviceStatus: RspGetDeviceStatus,
    const.IEnumCmd.GetDeviceModel: RspGetDeviceModel,
    const.IEnumCmd.GetStorageStatus: RspGetStorageStatus,
    const.IEnumCmd.GetRegisterParms: RspGetRegisterParms,
    const.IEnumCmd.GetDocByNum: RspGetDocByNum,
    const.IEnumCmd.GetOFDXchgStatus: RspGetOFDXchgStatus,
    const.IEnumCmd.GetDateTime: RspGetDateTime,
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
