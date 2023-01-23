"""Commands to send.

:todo: .to_frame()
"""
# 3. local
from kitfr import const


class _CmdBase:
    """Base for commands."""
    cmd_id: const.IEnumCmd

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return self.cmd_id.value.to_bytes(1, 'little')


class CmdGetDeviceStatus(_CmdBase):
    """Get FR status."""
    cmd_id = const.IEnumCmd.GetDeviceStatus


class CmdGetDeviceModel(_CmdBase):
    """Get FR model."""
    cmd_id = const.IEnumCmd.GetDeviceModel


class CmdGetStorageStatus(_CmdBase):
    """Get FS status."""
    cmd_id = const.IEnumCmd.GetStorageStatus


class CmdGetDocByNum(_CmdBase):
    """Find document by its number."""
    cmd_id = const.IEnumCmd.GetDocByNum
    num: int

    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + self.num.to_bytes(4, 'little')
