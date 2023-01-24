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


def _b2s(v: bytes) -> str:
    """Convert bytes of CP866 insto string."""
    return v.decode()  # FIXME: CP866


def _b2dt(v: Tuple[int, int, int, int, int]) -> datetime.datetime:
    """Convert 5xInt to datetime"""
    return datetime.datetime(2000 + v[0], v[1], v[2], v[3], v[4])


def _dt2str(dt: datetime.datetime) -> str:
    """Convert datime to string"""
    return dt.strftime('%Y-%m-%d %H:%M')


def _data_decode(data: bytes, fmt: str, cls) -> Tuple[Any]:
    """Check and decode data length against struct format."""
    if (l_data := len(data)) != (l_fmt := struct.calcsize(fmt)):
        raise exc.KitFRRspDecodeError(f"{cls.__name__}: bad data len: {l_data} (must be {l_fmt}).")
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
class _RspStub(RspBase):
    """Stub base for debugging."""
    payload: bytes

    @property
    def str(self) -> str:
        """Just dump payload."""
        return f"{len(self.payload)}: {self.payload.hex().upper()}"

    @staticmethod
    def from_bytes(data: bytes):
        """Just store."""
        return _RspStub(payload=data)


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
        v = _data_decode(data, '12sBBBBBBB?BB', RspGetDeviceStatus)
        return RspGetDeviceStatus(
            sn=_b2s(v[0]),
            datime=_b2dt(v[1:6]),
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
        # FIXME: chk len
        return RspGetDeviceModel(name=_b2s(data))


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
        v = _data_decode(data, '<BB??BBBBBB16sI', RspGetStorageStatus)
        return RspGetStorageStatus(
            phase=v[0],
            cur_doc=v[1],
            is_doc=v[2],
            is_session_open=v[3],
            flags=v[4],
            datime=_b2dt(v[5:10]),
            sn=_b2s(v[10]),
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
        v = _data_decode(data, '20s12sBBB', RspGetRegisterParms)
        return RspGetRegisterParms(
            rn=_b2s(v[0]).rstrip(),
            inn=_b2s(v[1]).rstrip(),
            mode=v[2],
            tax=v[3],
            agent=v[4]
        )


@dataclass
class ADoc(RspBase):
    """Archive document."""


@dataclass
class ADocRegRpt(ADoc):
    """Archive document. Registration report."""
    datime: datetime.datetime
    no: str
    fp: int  # repeate because of auto __str__
    inn: str
    rn: str
    tax: int
    mode: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<BBBBBII12s20sBB', cls)  # 49
        return cls(
            datime=_b2dt(v[0:5]),
            no=v[5],
            fp=v[6],
            inn=_b2s(v[7]).rstrip(),
            rn=_b2s(v[8]).rstrip(),
            tax=v[9],
            mode=v[10]
        )


@dataclass
class ADocReRegRpt(ADoc):
    """Archive document. Re-Registration report."""
    datime: datetime.datetime
    no: str
    fp: int
    inn: str
    rn: str
    tax: int
    mode: int
    reason: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<BBBBBII12s20sBBB', cls)  # 50
        return cls(
            datime=_b2dt(v[0:5]),
            no=v[5],
            fp=v[6],
            inn=_b2s(v[7]).rstrip(),
            rn=_b2s(v[8]).rstrip(),
            tax=v[9],
            mode=v[10],
            reason=v[11]
        )


ADOC_CLASS = {1: ADocRegRpt, 11: ADocReRegRpt}


@dataclass
class RspGetDocByNum(RspBase):
    """FD."""
    doc_type: int  # 1 byte, enum
    ofd: bool  # 1 byte
    doc: ADoc

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        if (l_data := len(data)) <= 3:
            raise exc.KitFRRspDecodeError(f"{cls.__name__}: too few data: {l_data} bytes.")
        # 1. decode last
        if (doc_class := ADOC_CLASS.get(doc_type := data[0])) is None:
            raise exc.KitFRRspDecodeError(f"{cls.__name__}: unknown doc type={doc_type}.")
        doc = doc_class.from_bytes(data[2:])
        # 2. init self
        return cls(doc_type=doc_type, ofd=bool(data[1]), doc=doc)


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
        v = _data_decode(data, '<BBHIBBBBB', RspGetOFDXchgStatus)  # 13
        return RspGetOFDXchgStatus(
            status=v[0],
            state_ofd=v[1],
            out_count=v[2],
            next_doc_n=v[3],
            next_doc_d=_b2dt(v[4:])
        )


@dataclass
class RspGetDateTime(RspBase):
    """FS date/time."""
    datime: datetime.datetime

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<HHBBBBB', cls)  # 9; TODO: quick hack of TLV
        if v[0] != 30000:
            raise exc.KitFRRspDecodeError(f"{cls.__name__}: bad TAG: {v[0]}")
        if v[1] != 5:
            raise exc.KitFRRspDecodeError(f"{cls.__name__}: bad TLV len: {v[1]}")
        return cls(
            datime=_b2dt(v[2:])
        )


class RspGetSomething(_RspStub):
    """Something."""
    ...  # N


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
