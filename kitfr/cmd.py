"""Commands to send.

:todo: .to_frame()
"""
# 1. std
import datetime
from typing import Optional
# 3. local
from kitfr import const, util, tag


class _CmdBase:
    """Base for commands."""
    cmd_id: const.IEnumCmd

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return self.cmd_id.value.to_bytes(1, 'little')


class CmdGetDeviceStatus(_CmdBase):
    """0x01: Get POS status."""
    cmd_id = const.IEnumCmd.GetDeviceStatus


class CmdGetDeviceModel(_CmdBase):
    """0x04: Get POS model."""
    cmd_id = const.IEnumCmd.GetDeviceModel


class CmdGetStorageStatus(_CmdBase):
    """0x08: Get FS status."""
    cmd_id = const.IEnumCmd.GetStorageStatus


class CmdGetRegisterParms(_CmdBase):
    """0x0A: Get POS/FS registering parameters."""
    cmd_id = const.IEnumCmd.GetRegisterParms


class CmdDocCancel(_CmdBase):
    """0x10: Cancel any opened document."""
    cmd_id = const.IEnumCmd.DocCancel


class CmdGetCurSession(_CmdBase):
    """0x20: Get current session params."""
    cmd_id = const.IEnumCmd.GetCurSession


class _CmdSessionAnyBegin(_CmdBase):
    """Base for CmdSessionOpenBegin/CmdSessioCloseBegin"""
    skip_prn: Optional[bool]  # Skip printing report (None = False)

    def __init__(self, skip_prn: Optional[bool] = None):
        super().__init__()
        self.skip_prn = skip_prn

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        retvalue = super().to_bytes()
        if self.skip_prn is not None:
            retvalue += util.l2b(self.skip_prn)
        return retvalue


class CmdSessionOpenBegin(_CmdSessionAnyBegin):
    """0x21: Begin opening session."""
    cmd_id = const.IEnumCmd.SessionOpenBegin


class CmdSessionOpenCommit(_CmdBase):
    """0x22: Commit opening session."""
    cmd_id = const.IEnumCmd.SessionOpenCommit


class CmdSessionCloseBegin(_CmdSessionAnyBegin):
    """0x29: Begin closing session."""
    cmd_id = const.IEnumCmd.SessionCloseBegin


class CmdSessionCloseCommit(_CmdBase):
    """0x2A: Commit opening session."""
    cmd_id = const.IEnumCmd.SessionCloseCommit


class _CmdGetDocAny(_CmdBase):
    """Base CmdGetDocInfo/CmdGetDocData."""
    num: int

    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + util.ui2b4(self.num)


class CmdGetDocInfo(_CmdGetDocAny):
    """0x30: Find document by its number."""
    cmd_id = const.IEnumCmd.GetDocInfo


class CmdGetDocData(_CmdGetDocAny):
    """0x3A: Read document content."""
    cmd_id = const.IEnumCmd.GetDocData


class CmdGetOFDXchgStatus(_CmdBase):
    """0x50: Get OFD exchange status."""
    cmd_id = const.IEnumCmd.GetOFDXchgStatus


class CmdSetDateTime(_CmdBase):
    """0x72: Set POS date/time."""
    cmd_id = const.IEnumCmd.SetDateTime
    datime: datetime.datetime

    def __init__(self, datime: datetime.datetime):
        super().__init__()
        self.datime = datime

    def to_bytes(self) -> bytes:
        """Serialize to bytes.

        :note: const: TAG=30000 + LEN=5
        """
        return super().to_bytes() \
            + b'\x30\x75\x05\x00' \
            + util.dt2b5(self.datime)


class CmdGetDateTime(_CmdBase):
    """0x73: Get POS date/time."""
    cmd_id = const.IEnumCmd.GetDateTime


class CmdCorrReceiptBegin(_CmdBase):
    """0x25: Corr. Receipt. Step #1 - begin.

    Response: RspOK
    """
    cmd_id = const.IEnumCmd.CorrReceiptBegin


class CmdCorrReceiptData(_CmdBase):
    """0x2E: Corr. Receipt. Step #2 - send data.

    Response: RspOK
    """
    cmd_id = const.IEnumCmd.CorrReceiptData
    payload: tag.TagDict

    def __init__(self, payload: tag.TagDict):
        super().__init__()
        # TODO: chk 1031+1081+1215+1216+1217 == sum(1102..1107)
        self.payload = payload

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + tag.tag_dict_pack(self.payload)


class CmdCorrReceiptAutomat(_CmdBase):
    """0x3F: Corr. Receipt. Step #3 - send automat number.

    Response: RspOK
    """
    cmd_id = const.IEnumCmd.CorrReceiptAutomat
    payload: tag.TagDict

    def __init__(self, payload: tag.TagDict):
        super().__init__()
        self.payload = payload

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + tag.tag_dict_pack(self.payload)


class CmdCorrReceiptCommit(_CmdBase):
    """0x26: Corr. Receipt. Step #4 (last) - commit.

    Response: RspCorrReceiptCommit
    """
    cmd_id = const.IEnumCmd.CorrReceiptCommit
    req_type: const.IEnumReceiptType
    total: int

    def __init__(self, req_type: const.IEnumReceiptType, total: int):
        super().__init__()
        self.req_type = req_type
        self.total = total

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + util.ui2b1(self.req_type) + util.ui2vln(self.total)
