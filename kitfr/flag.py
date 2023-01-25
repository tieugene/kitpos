"""Flags."""
from kitfr import const


class FSerr:
    """FS errors and warnings."""
    __v: int

    def __init__(self, b: int):
        self.__v = b

    def has_ready(self) -> bool:
        return const.IEnumFSphase in self.__v
