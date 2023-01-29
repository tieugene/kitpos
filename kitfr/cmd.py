"""Commands to send.

:todo: .to_frame()
"""
# 1. std
import datetime
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


class CmdGetDocByNum(_CmdBase):
    """0x30: Find document by its number."""
    cmd_id = const.IEnumCmd.GetDocByNum
    num: int

    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + self.num.to_bytes(4, 'little')


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
            + util.dt2b(self.datime)


class CmdGetDateTime(_CmdBase):
    """0x73: Get POS date/time."""
    cmd_id = const.IEnumCmd.GetDateTime
