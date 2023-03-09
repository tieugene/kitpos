"""Responses of commands.

Copyright 2023 TI_Eugene <ti.eugene@gmail.com>
This file is part of the kitpos project.
You may use this file under the terms of the GPLv3 license.

:todo: dataclass(frozen=True)
"""
# 1. std
from typing import Tuple, Any, Dict
from dataclasses import dataclass
import struct
import datetime
import ipaddress
# 3. local
from kitpos import const, flag, exc, util, tag


def _dt2str(datime: datetime.datetime) -> str:
    """Convert datime to string."""
    return datime.strftime('%Y-%m-%d %H:%M')


def _data_decode(data: bytes, fmt: str, cls) -> Tuple[Any]:
    """Check and decode data length against struct format."""
    if (l_data := len(data)) != (l_fmt := struct.calcsize(fmt)):
        raise exc.KpeRspUnpack(f"{cls.__name__}: bad data len: {l_data} (must be {l_fmt}).")
    return struct.unpack(fmt, data)


@dataclass
class RspBase:
    """Base for response."""

    def cls_name(self) -> str:
        """Class name shorthand."""
        return self.__class__.__name__

    def to_str(self, sep: str = ', ') -> str:
        """Get response attrs as string."""
        return sep.join([f"{f}={self.__dict__[f]}" for f in self.__annotations__])  # FIXME: pylint: disable=E1101

    def __str__(self) -> to_str:
        """Make string representation of response object."""
        return f"{self.cls_name()}: {self.to_str()}"


@dataclass
class _RspStub(RspBase):
    """Stub base for response debugging."""

    payload: bytes

    def to_str(self, sep: str = ', ') -> str:
        """Just dump payload."""
        return f"{self.payload.hex().upper()} ({len(self.payload)})"

    @classmethod
    def from_bytes(cls, data: bytes):
        """Just store."""
        return cls(payload=data)


@dataclass
class RspOK(RspBase):
    """Just OK."""

    def to_str(self, _: str = '') -> str:
        """Get response attrs as string."""
        return "OK"  # TODO: ''?

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        if l_data := len(data):
            raise exc.KpeRspUnpack(f"{cls.__name__}: bad data len: {l_data} (must be 0).")
        return cls()


@dataclass
class RspGetDeviceStatus(RspBase):
    """0x01: Get POS status."""

    f_n: str
    datime: datetime.datetime
    err: bool  # Critical errors; TODO: chk 0/1
    prn_status: const.IEnumPrnStatus
    is_fs: bool  # TODO: chk 0/1
    fs_phase: const.IEnumFSphase
    wtf: int  # TODO: WTF tail 1 byte?

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '12sBBBBB?B?BB', cls)
        try:
            v_7 = const.IEnumPrnStatus(val[7])
            v_9 = const.IEnumFSphase(val[9])
        except ValueError as __e:
            raise exc.KpeRspUnpack(__e) from __e
        return cls(
            f_n=util.b2s(val[0]),
            datime=util.b2dt(val[1:6]),
            err=val[6],
            prn_status=v_7,
            is_fs=val[8],
            fs_phase=v_9,
            wtf=val[10]
        )


@dataclass
class RspGetDeviceFN(RspBase):
    """0x02: Get POS factory number."""

    f_n: str

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        return cls(f_n=util.b2s(data).strip())


@dataclass
class RspGetDeviceFWVer(RspBase):
    """0x03: Get POS firmware version."""

    ver: str

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        return cls(ver=util.b2s(data).strip())


@dataclass
class RspGetDeviceModel(RspBase):
    """0x04: Get POS model."""

    name: str

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        # FIXME: chk len
        return cls(name=util.b2s(data))


@dataclass
class RspGetStorageFN(RspBase):
    """0x05: Get FS factory number."""

    f_n: str

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        return cls(f_n=util.b2s(data).strip())


@dataclass
class RspGetStorageFWVer(RspBase):
    """0x06: Get FS firmware version."""

    ver: str

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        return cls(ver=util.b2s(data).strip())


@dataclass
class RspGetStorageExpired(RspBase):
    """0x07: Get FS date expired."""

    date: datetime.date
    rest: int
    done: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, 'BBBBB', cls)
        return cls(
            date=util.b2d(val[:3]),
            rest=val[3],
            done=val[4])


@dataclass
class RspGetStorageStatus(RspBase):
    """0x08: Get FS status."""
    # pylint: disable=R0902

    phase: const.IEnumFSphase
    cur_doc_type: int  # TODO: enum
    is_doc: bool
    is_session_open: bool
    flags: flag.FSErrors
    datime: datetime.datetime
    s_n: str
    last_fdoc_n: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '<BB??BBBBBB16sI', cls)
        try:
            v_0 = const.IEnumFSphase(val[0])
            v_1 = const.IEnumFSCurDoc(val[1])
            v_4 = flag.FSErrors(val[4])
        except ValueError as __e:
            raise exc.KpeRspUnpack(__e) from __e
        return cls(
            phase=v_0,
            cur_doc_type=v_1,
            is_doc=val[2],
            is_session_open=val[3],
            flags=v_4,
            datime=util.b2dt(val[5:10]),
            s_n=util.b2s(val[10]),
            last_fdoc_n=val[11]
        )


@dataclass
class RspGetRegisterParms(RspBase):
    """0x0A: Get POS/FS registering parameters."""

    reg_n: str
    inn: str
    fr_mode: flag.FRModes
    tax: flag.TaxModes
    agent: flag.AgentModes

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '20s12sBBB', cls)
        try:
            v_2 = flag.FRModes(val[2])
            v_3 = flag.TaxModes(val[3])
            v_4 = flag.AgentModes(val[4])
        except ValueError as __e:
            raise exc.KpeRspUnpack(__e) from __e
        return cls(
            reg_n=util.b2s(val[0]).rstrip(),
            inn=util.b2s(val[1]).rstrip(),
            fr_mode=v_2,
            tax=v_3,
            agent=v_4
        )


@dataclass
class RspGetDeviceCfgVer(RspBase):
    """0x0B: Get POS config version."""

    ver: str

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        return cls(ver=util.b2s(data).strip())


@dataclass
class RspGetNetParms(RspBase):
    """0x0E: Get current network parameters."""
    ip: ipaddress.IPv4Address
    mask: ipaddress.IPv4Address
    gw: ipaddress.IPv4Address

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        val = _data_decode(data, '>III', cls)
        return cls(
            ip=ipaddress.IPv4Address(val[0]),
            mask=ipaddress.IPv4Address(val[1]),
            gw=ipaddress.IPv4Address(val[2])
        )

    def to_str(self, sep: str = ', ') -> str:
        """Get response attrs as string."""
        return f"ip={format(self.ip)}{sep}mask={format(self.mask)}{sep}gw={format(self.gw)}"


@dataclass
class RspGetCurSession(RspBase):
    """0x20: Get current session params."""

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
    """0x22: Commit opening session."""


class RspSessionCloseCommit(_RspSessionAnyCommit):
    """0x2A: Commit closing session."""


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
        try:
            v_9 = flag.TaxModes(val[9])
            v_10 = flag.FRModes(val[10])
        except ValueError as __e:
            raise exc.KpeRspUnpack(__e) from __e
        return cls(
            datime=util.b2dt(val[0:5]),
            fdoc_n=val[5],
            fpd=val[6],
            inn=util.b2s(val[7]).rstrip(),
            reg_n=util.b2s(val[8]).rstrip(),
            tax=v_9,
            mode=v_10
        )


@dataclass
class ADocReRegRpt(ADoc):
    """Archive document. Re-Registration report."""
    # pylint: disable=R0902

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
        try:
            v_9 = flag.TaxModes(val[9])
            v_10 = flag.FRModes(val[10])
            v_11 = const.IEnumReRegReason(val[11])
        except ValueError as __e:
            raise exc.KpeRspUnpack(__e) from __e
        return cls(
            datime=util.b2dt(val[0:5]),
            fdoc_n=val[5],
            fpd=val[6],
            inn=util.b2s(val[7]).rstrip(),
            reg_n=util.b2s(val[8]).rstrip(),
            tax=v_9,
            mode=v_10,
            reason=v_11
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
        try:
            v_7 = const.IEnumReceiptType(val[7])
        except ValueError as __e:
            raise exc.KpeRspUnpack(__e) from __e
        return cls(
            datime=util.b2dt(val[0:5]),
            fdoc_n=val[5],
            fpd=val[6],
            req_type=v_7,
            total=int.from_bytes(val[8:], 'little')  # Note: specioal UINT40
        )


class ADocCorReceipt(ADocReceipt):
    """Archive document. Corr. Receipt.

    :note: Not documented.
    """


ADOC_CLASS = {
    const.IEnumADocType.REG_RPT: ADocRegRpt,
    const.IEnumADocType.RE_REG_RPT: ADocReRegRpt,
    const.IEnumADocType.SES_OPEN_RPT: ADocSesOpenRpt,
    const.IEnumADocType.SES_CLOSE_RPT: ADocSesCloseRpt,
    const.IEnumADocType.RECEIPT: ADocReceipt,
    const.IEnumADocType.COR_RECEIPT: ADocCorReceipt,
}


@dataclass
class RspGetDocInfo(RspBase):
    """0x30: Get document info."""

    doc_type: const.IEnumADocType
    ofd: bool  # TODO: chk 0/1
    doc: ADoc

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        if (l_data := len(data)) <= 3:
            raise exc.KpeRspUnpack(f"{cls.__name__}: too few data: {l_data} bytes.")
        # 1. decode last
        try:
            doc_type = const.IEnumADocType(data[0])
        except ValueError as __e:
            raise exc.KpeRspUnpack(__e) from __e
        if (doc_class := ADOC_CLASS.get(doc_type)) is None:
            raise exc.KpeRspUnpack(
                f"{cls.__name__}: Doc type={doc_type} unprocessable yet ({util.b2hex(data[1:])})."
            )
        doc = doc_class.from_bytes(data[2:])
        # 2. init self
        return cls(doc_type=doc_type, ofd=bool(data[1]), doc=doc)  # TODO: ofd=i2l(...)


@dataclass
class RspGetUnsentDocNum(_RspStub):
    """0x32: Number of FD not confirmed by OFD."""


@dataclass
class RspGetStorageActResult(_RspStub):
    """0x33: Get FS activation result."""


@dataclass
class RspGetDocData(RspBase):
    """0x3A: Read document content."""

    tags: Dict[const.IEnumTag, Any]

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        return cls(tags=tag.tagdict_unpack(data))


@dataclass
class RspGetOFDXchgStatus(RspBase):
    """0x50: Get OFD exchange status."""

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
    """0x73: Get POS date/time."""

    datime: datetime.datetime

    @classmethod
    def from_bytes(cls, data: bytes):
        """Deserialize object."""
        __tag, __val = tag.tag_unpack(data)
        if __tag != const.IEnumTag.TAG_30000:
            raise exc.KpeRspUnpack(f"{cls.__name__}: bad TAG: {__tag}")
        return cls(
            datime=__val
        )


@dataclass
class RspGetDeviceNetParms(_RspStub):
    """0x75: Get POS network settings."""


@dataclass
class RspGetDeviceOFDParms(_RspStub):
    """0x77: Get POS OFD settings."""


@dataclass
class RspGetPrnLineLen(_RspStub):
    """0xBB: Get print line length (symbols)."""


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
            ses_n=val[8]
        )


# ----
_CODE2CLASS = {
    const.IEnumCmd.GET_POS_STATUS: RspGetDeviceStatus,
    const.IEnumCmd.GET_POS_FN: RspGetDeviceFN,
    const.IEnumCmd.GET_POS_FW_VER: RspGetDeviceFWVer,
    const.IEnumCmd.GET_POS_MODEL: RspGetDeviceModel,
    const.IEnumCmd.GET_FS_FN: RspGetStorageFN,
    const.IEnumCmd.GET_FS_FW_VER: RspGetStorageFWVer,
    const.IEnumCmd.GET_FS_EXPIRED: RspGetStorageExpired,
    const.IEnumCmd.GET_FS_STATUS: RspGetStorageStatus,
    const.IEnumCmd.GET_REG_PARMS: RspGetRegisterParms,
    const.IEnumCmd.GET_POS_CFG_VER: RspGetDeviceCfgVer,
    const.IEnumCmd.GET_NET_PARM: RspGetNetParms,
    const.IEnumCmd.DOC_CANCEL: RspOK,
    const.IEnumCmd.GET_CUR_SES: RspGetCurSession,
    const.IEnumCmd.SES_OPEN_BEGIN: RspOK,
    const.IEnumCmd.SES_OPEN_COMMIT: RspSessionOpenCommit,
    const.IEnumCmd.SES_CLOSE_BEGIN: RspOK,
    const.IEnumCmd.SES_CLOSE_COMMIT: RspSessionCloseCommit,
    const.IEnumCmd.GET_DOC_INFO: RspGetDocInfo,
    const.IEnumCmd.GET_UNSENT_DOC_NUM: RspGetUnsentDocNum,
    const.IEnumCmd.GET_FS_REG_RESULT: RspGetStorageActResult,
    const.IEnumCmd.GET_DOC_DATA: RspGetDocData,
    const.IEnumCmd.GET_OFD_XCHG_STATUS: RspGetOFDXchgStatus,
    const.IEnumCmd.SET_DATETIME: RspOK,
    const.IEnumCmd.GET_DATETIME: RspGetDateTime,
    const.IEnumCmd.GET_POS_NET_PARM: RspGetDeviceNetParms,
    const.IEnumCmd.GET_POS_OFD_PARM: RspGetDeviceOFDParms,
    const.IEnumCmd.GET_PRN_LINE_LEN: RspGetPrnLineLen,
    const.IEnumCmd.COR_RCP_BEGIN: RspOK,
    const.IEnumCmd.COR_RCP_DATA: RspOK,
    const.IEnumCmd.COR_RCP_AUTOMAT: RspOK,
    const.IEnumCmd.COR_RCP_COMMIT: RspCorrReceiptCommit,
    const.IEnumCmd.RCP_BEGIN: RspOK,
    const.IEnumCmd.RCP_ITEM: RspOK,
    const.IEnumCmd.RCP_PAYMENT: RspOK,
    const.IEnumCmd.RCP_AUTOMAT: RspOK,
    const.IEnumCmd.RCP_COMMIT: RspReceiptCommit,
}


def bytes2rsp(cmd_code: const.IEnumCmd, data: bytes) -> RspBase:
    """Decode inbound bytes into RspX object."""
    if (rsp := _CODE2CLASS.get(cmd_code)) is not None:
        return rsp.from_bytes(data)
    raise exc.KpeRspUnpack(f"Unknown response object (cmd {cmd_code}): {util.b2hex(data)}")
