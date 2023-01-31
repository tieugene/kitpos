"""Commands to send.

:todo: .to_frame()
"""
# 1. std
import datetime
from typing import Optional

# 3. local
from kitfr import const, util


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
    """Base CmdGetDocByNum/CmdReadDoc."""
    num: int

    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + util.ui2b4(self.num)


class CmdGetDocByNum(_CmdGetDocAny):  # TODO: GetDocInfo/Meta
    """0x30: Find document by its number."""
    cmd_id = const.IEnumCmd.GetDocInfo


class CmdReadDoc(_CmdGetDocAny):  # TODO: GetDocContent
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
        return super().to_bytes()\
            + b'\x30\x75\x05\x00'\
            + util.dt2b5(self.datime)


class CmdGetDateTime(_CmdBase):
    """0x73: Get POS date/time."""
    cmd_id = const.IEnumCmd.GetDateTime
