"""Flags."""
# 1. std
import enum
# 3. local
from kitpos import const

x_table = str.maketrans({'0': '.', '1': '+'})


class _Flags:
    """Base for flag classes.

    :todo: Metaclass
    """

    _v: int
    _v_cls: enum.IntEnum

    def __init__(self, val: int):
        self._v = val

    def is_set(self, flg: enum.IntFlag) -> bool:
        """Check the flag is set."""
        return bool(flg & self._v)

    def as_bytes(self) -> bytes:
        """Get value as byte."""
        return self._v.to_bytes(1, 'little')

    def __str__(self) -> str:
        return f"{bin(self._v)[2:].zfill(8).translate(x_table)} ({self._v:02X}h)"


class FSErrors(_Flags):
    """FS errors and warnings.

    Used:
    - ...
    """

    _v_cls: const.IFlagFSErr


class FRModes(_Flags):
    """FR work mode.

    Used:
    - ...
    """

    _v_cls: const.IFlagFRMode


class TaxModes(_Flags):
    """Tax modes.

    Used:
    - ...
    """

    _v_cls: const.IFlagTax


class AgentModes(_Flags):
    """Agent modes.

    Used:
    - ...
    """

    _v_cls: const.IFlagAgent
