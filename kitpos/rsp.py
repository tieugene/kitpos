"""Responses of commands.

:todo: dataclass(frozen=True)
"""
# 1. std
from typing import Tuple, Any, Dict
from dataclasses import dataclass
import struct
import datetime
# 3. local
from kitpos import const, flag, exc, util, tag


def _dt2str(datime: datetime.datetime) -> str:
    """Convert datime to string."""
    return datime.strftime('%Y-%m-%d %H:%M')


def _data_decode(data: bytes, fmt: str, cls) -> Tuple[Any]:
    """Check and decode data length against struct format."""
    if (l_data := len(data)) != (l_fmt := struct.calcsize(fmt)):
        raise exc.KitPOSRspDecodeError(f"{cls.__name__}: bad data len: {l_data} (must be {l_fmt}).")
    return struct.unpack(fmt, data)


@dataclass
class RspBase:
    """Base for response."""

    @property
    def cls_name(self) -> str:
        """Class name shorthand."""
        return self.__class__.__name__

    def str(self, sep: str = ', ') -> str:
        """Get response attrs as string."""
        return sep.join([f"{f}={self.__dict__[f]}" for f in self.__annotations__])

    def __str__(self) -> str:
        """Make string representation of response object."""
        return f"{self.cls_name}: {self.str()}"


@dataclass
class _RspStub(RspBase):
    """Stub base for response debugging."""

    payload: bytes

    def str(self, sep: str = ', ') -> str:
        """Just dump payload."""
        return f"{self.payload.hex().upper()} ({len(self.payload)})"

    @staticmethod
    def from_bytes(data: bytes):
        """Just store."""
        return _RspStub(payload=data)


@dataclass
class RspOK(RspBase):
    """Just OK."""

    def str(self, _: str = '') -> str:
        """Get response attrs as string."""
        return "OK"

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        if l_data := len(data):
            raise exc.KitPOSRspDecodeError(f"{cls.__name__}: bad data len: {l_data} (must be 0).")
        return RspOK()


@dataclass
class RspGetDeviceStatus(RspBase):
    """POS status (0x01)."""

    s_n: str
    datime: datetime.datetime
    err: bool  # Critical errors; TODO: chk 0/1
    prn_status: const.IEnumPrnStatus
    is_fs: bool  # TODO: chk 0/1
    fs_phase: const.IEnumFSphase
    wtf: int  # TODO: WTF tail 1 byte?

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '12sBBBBB?B?BB', RspGetDeviceStatus)
        return RspGetDeviceStatus(
            s_n=util.b2s(val[0]),
            datime=util.b2dt(val[1:6]),
            err=val[6],
            prn_status=const.IEnumPrnStatus(val[7]),
            is_fs=val[8],
            fs_phase=const.IEnumFSphase(val[9]),
            wtf=val[10]
        )


@dataclass
class RspGetDeviceModel(RspBase):
    """POS model (0x04)."""

    name: str

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        # FIXME: chk len
        return RspGetDeviceModel(name=util.b2s(data))


@dataclass
class RspGetStorageStatus(RspBase):
    """Fiscal storage status (0x08)."""

    phase: const.IEnumFSphase
    cur_doc_type: int  # TODO: enum
    is_doc: bool
    is_session_open: bool
    flags: flag.FSErrors
    datime: datetime.datetime
    s_n: str
    last_fdoc_n: int

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<BB??BBBBBB16sI', RspGetStorageStatus)
        return RspGetStorageStatus(
            phase=const.IEnumFSphase(val[0]),
            cur_doc_type=const.IEnumFSCurDoc(val[1]),
            is_doc=val[2],
            is_session_open=val[3],
            flags=flag.FSErrors(val[4]),
            datime=util.b2dt(val[5:10]),
            s_n=util.b2s(val[10]),
            last_fdoc_n=val[11]
        )


@dataclass
class RspGetRegisterParms(RspBase):
    """POS+FS registering parameters (0x0A)."""

    reg_n: str
    inn: str
    fr_mode: flag.FRModes
    tax: flag.TaxModes
    agent: flag.AgentModes

    @staticmethod
    def from_bytes(data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '20s12sBBB', RspGetRegisterParms)
        return RspGetRegisterParms(
            reg_n=util.b2s(val[0]).rstrip(),
            inn=util.b2s(val[1]).rstrip(),
            fr_mode=flag.FRModes(val[2]),
            tax=flag.TaxModes(val[3]),
            agent=flag.AgentModes(val[4])
        )


@dataclass
class RspGetCurSession(RspBase):
    """Current session params (0x20)."""

    opened: bool
    ses_n: int
    rcp_n: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<?HH', cls)
        return cls(
            opened=val[0],
            ses_n=val[1],
            rcp_n=val[2]
        )


@dataclass
class _RspSessionAnyCommit(RspBase):
    """Base for RspSessionOpenCommit/RspSessionCloseCommit."""

    ses_n: int
    fdoc_n: int
    fpd: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<HII', cls)
        return cls(
            ses_n=val[0],
            fdoc_n=val[1],
            fpd=val[2]
        )


class RspSessionOpenCommit(_RspSessionAnyCommit):
    """Opened session response."""


class RspSessionCloseCommit(_RspSessionAnyCommit):
    """Closed session response."""


@dataclass
class ADoc(RspBase):
    """Archive document."""


@dataclass
class ADocRegRpt(ADoc):
    """Archive document. Registration report."""

    datime: datetime.datetime
    fdoc_n: int
    fpd: int
    # ^^^ repeate because of auto __str__
    inn: str
    reg_n: str
    tax: flag.TaxModes  # TODO: really?
    mode: flag.FRModes  # TODO: really?

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<BBBBBII12s20sBB', cls)  # 47
        return cls(
            datime=util.b2dt(val[0:5]),
            fdoc_n=val[5],
            fpd=val[6],
            inn=util.b2s(val[7]).rstrip(),
            reg_n=util.b2s(val[8]).rstrip(),
            tax=flag.TaxModes(val[9]),
            mode=flag.FRModes(val[10])
        )


@dataclass
class ADocReRegRpt(ADoc):
    """Archive document. Re-Registration report."""

    datime: datetime.datetime
    fdoc_n: int
    fpd: int
    inn: str
    reg_n: str
    tax: flag.TaxModes  # TODO: really?
    mode: flag.FRModes  # TODO: really
    reason: const.IEnumReRegReason

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<BBBBBII12s20sBBB', cls)  # 48
        return cls(
            datime=util.b2dt(val[0:5]),
            fdoc_n=val[5],
            fpd=val[6],
            inn=util.b2s(val[7]).rstrip(),
            reg_n=util.b2s(val[8]).rstrip(),
            tax=flag.TaxModes(val[9]),
            mode=flag.FRModes(val[10]),
            reason=const.IEnumReRegReason(val[11])
        )


@dataclass
class _ADocSesRpt(ADoc):
    """Archive document. Session open/close report."""

    datime: datetime.datetime
    fdoc_n: int
    fpd: int
    ses_n: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<BBBBBIIH', cls)  # 15
        return cls(
            datime=util.b2dt(val[0:5]),
            fdoc_n=val[5],
            fpd=val[6],
            ses_n=val[7]
        )


class ADocSesOpenRpt(_ADocSesRpt):
    """Archive document. Session open report."""


class ADocSesCloseRpt(_ADocSesRpt):
    """Archive document. Session close report."""


@dataclass
class ADocReceipt(ADoc):
    """Archive document. Receipt."""

    datime: datetime.datetime
    fdoc_n: int
    fpd: int
    req_type: const.IEnumReceiptType
    total: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<BBBBBIIBBBBBB', cls)  # 19
        return cls(
            datime=util.b2dt(val[0:5]),
            fdoc_n=val[5],
            fpd=val[6],
            req_type=const.IEnumReceiptType(val[7]),
            total=(int.from_bytes(val[8:], 'little'))
        )


class ADocCorReceipt(ADocReceipt):
    """Archive document. Corr. Receipt.

    :not: Not documented.
    """


ADOC_CLASS = {
    const.IEnumADocType.RegRpt: ADocRegRpt,
    const.IEnumADocType.ReRegRpt: ADocReRegRpt,
    const.IEnumADocType.SesOpenRpt: ADocSesOpenRpt,
    const.IEnumADocType.SesCloseRpt: ADocSesCloseRpt,
    const.IEnumADocType.Receipt: ADocReceipt,
    const.IEnumADocType.CorReceipt: ADocCorReceipt,
}


@dataclass
class RspGetDocInfo(RspBase):
    """Document [meta-]info (0x30)."""

    doc_type: const.IEnumADocType
    ofd: bool  # TODO: chk 0/1
    doc: ADoc

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        if (l_data := len(data)) <= 3:
            raise exc.KitPOSRspDecodeError(f"{cls.__name__}: too few data: {l_data} bytes.")
        # 1. decode last
        doc_type = const.IEnumADocType(data[0])  # ValueSomething exception if unknown
        if (doc_class := ADOC_CLASS.get(doc_type)) is None:
            raise exc.KitPOSRspDecodeError(
                f"{cls.__name__}: Doc type={doc_type} unprocessable yet ({util.b2hex(data[1:])})."
            )
        doc = doc_class.from_bytes(data[2:])
        # 2. init self
        return cls(doc_type=doc_type, ofd=bool(data[1]), doc=doc)


@dataclass
class RspGetDocData(RspBase):
    """Document data (0x3A)."""

    tags: Dict[const.IEnumTag, Any]

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        return cls(tags=tag.tag_list_unpack(data))


@dataclass
class RspGetOFDXchgStatus(RspBase):
    """OFD exchange status (0x50)."""

    out_count: int
    next_doc_n: int
    next_doc_d: datetime.datetime

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<BBHIBBBBB', cls)  # 13
        return cls(  # Note: val[0..1] skipped as service
            out_count=val[2],
            next_doc_n=val[3],
            next_doc_d=util.b2dt(val[4:])
        )


@dataclass
class RspGetDateTime(RspBase):
    """POS date/time (0x73)."""

    datime: datetime.datetime

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<HHBBBBB', cls)  # 9; TODO: quick hack of TLV
        if val[0] != 30000:
            raise exc.KitPOSRspDecodeError(f"{cls.__name__}: bad TAG: {val[0]}")
        if val[1] != 5:
            raise exc.KitPOSRspDecodeError(f"{cls.__name__}: bad TLV len: {val[1]}")
        return cls(
            datime=util.b2dt(val[2:])
        )


@dataclass
class RspCorrReceiptCommit(RspBase):
    """Commit Corr. Receipt (0x26)."""

    sdoc_n: int  # (2) doc number in session
    fdoc_n: int  # (4) fiscal doc no
    fpd: int  # (4)

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<HII', cls)
        return cls(
            sdoc_n=val[0],
            fdoc_n=val[1],
            fpd=val[2]
        )


@dataclass
class RspReceiptCommit(RspBase):
    """Commit Receipt (0x24)."""

    sdoc_n: int  # (2) doc number in session
    fdoc_n: int  # (4) fiscal doc no
    fpd: int  # (4)
    datime: datetime.datetime  # (5) YMDHm
    ses_n: int  # (2)

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<HIIBBBBBH', cls)
        return cls(
            sdoc_n=val[0],
            fdoc_n=val[1],
            fpd=val[2],
            datime=util.b2dt(val[3:8]),
            ses_n=val[9]
        )


# ----
_CODE2CLASS = {
    const.IEnumCmd.GetDeviceStatus: RspGetDeviceStatus,
    const.IEnumCmd.GetDeviceModel: RspGetDeviceModel,
    const.IEnumCmd.GetStorageStatus: RspGetStorageStatus,
    const.IEnumCmd.GetRegisterParms: RspGetRegisterParms,
    const.IEnumCmd.DocCancel: RspOK,
    const.IEnumCmd.GetCurSession: RspGetCurSession,
    const.IEnumCmd.SessionOpenBegin: RspOK,
    const.IEnumCmd.SessionOpenCommit: RspSessionOpenCommit,
    const.IEnumCmd.SessionCloseBegin: RspOK,
    const.IEnumCmd.SessionCloseCommit: RspSessionCloseCommit,
    const.IEnumCmd.GetDocInfo: RspGetDocInfo,
    const.IEnumCmd.GetDocData: RspGetDocData,
    const.IEnumCmd.GetOFDXchgStatus: RspGetOFDXchgStatus,
    const.IEnumCmd.SetDateTime: RspOK,
    const.IEnumCmd.GetDateTime: RspGetDateTime,
    const.IEnumCmd.CorrReceiptBegin: RspOK,
    const.IEnumCmd.CorrReceiptData: RspOK,
    const.IEnumCmd.CorrReceiptAutomat: RspOK,
    const.IEnumCmd.CorrReceiptCommit: RspCorrReceiptCommit,
    const.IEnumCmd.ReceiptBegin: RspOK,
    const.IEnumCmd.ReceiptItem: RspOK,
    const.IEnumCmd.ReceiptPayment: RspOK,
    const.IEnumCmd.ReceiptAutomat: RspOK,
    const.IEnumCmd.ReceiptCommit: RspReceiptCommit,
}


def bytes2rsp(cmd_code: const.IEnumCmd, data: bytes) -> RspBase:
    """Decode inbound bytes into RspX object."""
    if (rsp := _CODE2CLASS.get(cmd_code)) is not None:
        return rsp.from_bytes(data)
    raise exc.KitPOSRspDecodeError(f"Unknown response object (cmd {cmd_code}): {util.b2hex(data)}")
