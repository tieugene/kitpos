"""Flags."""
import enum

from kitfr import const


class _Flags:
    """Base for flag classes.

    :todo: Metaclass
    """
    _v: int
    _v_cls: enum.IntEnum

    def __init__(self, b: int):
        self._v = b

    def is_set(self, f: enum.IntFlag) -> bool:
        """Check the flag is set."""
        return bool(f & self._v)

    def __str__(self) -> str:
        return f"{bin(self._v)[2:]} ({self._v:02X}h)"
        # TODO: lexpand(8) by 0
        # TODO: replace '01' > '.+'


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
