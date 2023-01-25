"""Responses of commands."""
# 1. std
from typing import Tuple, Union, Any
from dataclasses import dataclass
import struct
import datetime
# 3. local
from kitfr import const, exc, util, flag


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
    """FR status (0x01)."""
    sn: str
    datime: datetime.datetime
    err: bool  # Critical errors; TODO: chk 0/1
    prn_status: const.IEnumPrnStatus
    is_fs: bool  # TODO: chk 0/1
    fs_phase: const.IEnumFSphase
    wtf: int  # TODO: WTF tail 1 byte?

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '12sBBBBB?B?BB', RspGetDeviceStatus)
        return RspGetDeviceStatus(
            sn=_b2s(v[0]),
            datime=_b2dt(v[1:6]),
            err=v[6],
            prn_status=const.IEnumPrnStatus(v[7]),
            is_fs=v[8],
            fs_phase=const.IEnumFSphase(v[9]),
            wtf=v[10]
        )


@dataclass
class RspGetDeviceModel(RspBase):
    """FR sn (0x04)."""
    name: str

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        # FIXME: chk len
        return RspGetDeviceModel(name=_b2s(data))


@dataclass
class RspGetStorageStatus(RspBase):
    """FS status (0x08)."""
    phase: const.IEnumFSphase
    cur_doc: int
    is_doc: bool
    is_session_open: bool
    flags: flag.FSErrors
    datime: datetime.datetime
    sn: str
    last_doc_no: int

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<BB??BBBBBB16sI', RspGetStorageStatus)
        return RspGetStorageStatus(
            phase=const.IEnumFSphase(v[0]),
            cur_doc=const.IEnumFSCurDoc(v[1]),
            is_doc=v[2],
            is_session_open=v[3],
            flags=flag.FSErrors(v[4]),
            datime=_b2dt(v[5:10]),
            sn=_b2s(v[10]),
            last_doc_no=v[11]
        )


@dataclass
class RspGetRegisterParms(RspBase):
    """FR/FS registering parameters (0x0A)."""
    rn: str
    inn: str
    fr_mode: flag.FRModes
    tax: flag.TaxModes
    agent: flag.AgentModes

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '20s12sBBB', RspGetRegisterParms)
        return RspGetRegisterParms(
            rn=_b2s(v[0]).rstrip(),
            inn=_b2s(v[1]).rstrip(),
            fr_mode=flag.FRModes(v[2]),
            tax=flag.TaxModes(v[3]),
            agent=flag.AgentModes(v[4])
        )


@dataclass
class ADoc(RspBase):
    """Archive document."""


@dataclass
class ADocRegRpt(ADoc):
    """Archive document. Registration report."""
    datime: datetime.datetime
    no: int
    fp: int
    # ^^^ repeate because of auto __str__
    inn: str
    rn: str
    tax: flag.TaxModes  # TODO: really?
    mode: flag.FRModes  # TODO: really?

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<BBBBBII12s20sBB', cls)  # 47
        return cls(
            datime=_b2dt(v[0:5]),
            no=v[5],
            fp=v[6],
            inn=_b2s(v[7]).rstrip(),
            rn=_b2s(v[8]).rstrip(),
            tax=flag.TaxModes(v[9]),
            mode=flag.FRModes(v[10])
        )


@dataclass
class ADocReRegRpt(ADoc):
    """Archive document. Re-Registration report."""
    datime: datetime.datetime
    no: int
    fp: int
    inn: str
    rn: str
    tax: flag.TaxModes  # TODO: really?
    mode: flag.FRModes  # TODO: really
    reason: const.IEnumReRegReason

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<BBBBBII12s20sBBB', cls)  # 48
        return cls(
            datime=_b2dt(v[0:5]),
            no=v[5],
            fp=v[6],
            inn=_b2s(v[7]).rstrip(),
            rn=_b2s(v[8]).rstrip(),
            tax=flag.TaxModes(v[9]),
            mode=flag.FRModes(v[10]),
            reason=const.IEnumReRegReason(v[11])
        )


@dataclass
class _ADocSesRpt(ADoc):
    """Archive document. Session open/close report."""
    datime: datetime.datetime
    no: int
    fp: int
    sno: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<BBBBBIIH', cls)  # 15
        return cls(
            datime=_b2dt(v[0:5]),
            no=v[5],
            fp=v[6],
            sno=v[7]
        )


class ADocSesOpenRpt(_ADocSesRpt):
    """Archive document. Session open report"""


class ADocSesCloseRpt(_ADocSesRpt):
    """Archive document. Session close report"""


@dataclass
class ADocReceipt(ADoc):
    """Archive document. Receipt."""
    datime: datetime.datetime
    no: int
    fp: int
    req_type: const.IEnumReceiptType
    amount: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<BBBBBIIBBBBBB', cls)  # 19
        return cls(
            datime=_b2dt(v[0:5]),
            no=v[5],
            fp=v[6],
            req_type=const.IEnumReceiptType(v[7]),
            amount=(int.from_bytes(v[8:], 'little'))
        )


ADOC_CLASS = {
    const.IEnumADocType.RegRpt: ADocRegRpt,
    const.IEnumADocType.ReRegRpt: ADocReRegRpt,
    const.IEnumADocType.SesOpenRpt: ADocSesOpenRpt,
    const.IEnumADocType.SesCloseRpt: ADocSesCloseRpt,
    const.IEnumADocType.Receipt: ADocReceipt
}


@dataclass
class RspGetDocByNum(RspBase):
    """FD (0x30)."""
    doc_type: const.IEnumADocType
    ofd: bool  # TODO: chk 0/1
    doc: ADoc

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        if (l_data := len(data)) <= 3:
            raise exc.KitFRRspDecodeError(f"{cls.__name__}: too few data: {l_data} bytes.")
        # 1. decode last
        doc_type = const.IEnumADocType(data[0])  # ValueSomething exception if unknown
        if (doc_class := ADOC_CLASS.get(doc_type)) is None:
            raise exc.KitFRRspDecodeError(f"{cls.__name__}: Doc type={doc_type} unprocessable yet.")
        doc = doc_class.from_bytes(data[2:])
        # 2. init self
        return cls(doc_type=doc_type, ofd=bool(data[1]), doc=doc)


@dataclass
class RspGetOFDXchgStatus(RspBase):
    """OFD exchange status (0x50)."""
    out_count: int
    next_doc_n: int
    next_doc_d: datetime.datetime

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        v = _data_decode(data, '<BBHIBBBBB', RspGetOFDXchgStatus)  # 13
        return RspGetOFDXchgStatus(  # Note: v[0..1] skipped as service
            out_count=v[2],
            next_doc_n=v[3],
            next_doc_d=_b2dt(v[4:])
        )


@dataclass
class RspGetDateTime(RspBase):
    """FS date/time (0x73)."""
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
_CODE2CLASS = {
    const.IEnumCmd.GetDeviceStatus: RspGetDeviceStatus,
    const.IEnumCmd.GetDeviceModel: RspGetDeviceModel,
    const.IEnumCmd.GetStorageStatus: RspGetStorageStatus,
    const.IEnumCmd.GetRegisterParms: RspGetRegisterParms,
    const.IEnumCmd.GetDocByNum: RspGetDocByNum,
    const.IEnumCmd.GetOFDXchgStatus: RspGetOFDXchgStatus,
    const.IEnumCmd.GetDateTime: RspGetDateTime,
}


def bytes2rsp(cmd_code: const.IEnumCmd, data: bytes) -> RspBase:
    """Decode inbound bytes into RspX object."""
    if (rsp := _CODE2CLASS.get(cmd_code)) is not None:
        return rsp.from_bytes(data)
    raise exc.KitFRRspDecodeError(f"Unknown response object (cmd {cmd_code}): {util.b2h(data)}")
