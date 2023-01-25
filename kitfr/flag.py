"""Flags."""
from kitfr import const


class FSerr:
    """FS errors and warnings."""
    __v: int

    def __init__(self, b: int):
        self.__v = b

    def __f(self, f: const.FEnumFSErr) -> bool:
        return bool(f & self.__v)

    def __str__(self) -> str:
        def __b2c(__i: int) -> str:
            return '+' if __i else '.'
        return ''.join([__b2c(f & self.__v) for f in (
            const.FEnumFSErr.Crit,
            const.FEnumFSErr.Timeout,
            const.FEnumFSErr.Full90,
            const.FEnumFSErr.Exp30d,
            const.FEnumFSErr.Exp3d
        )])

    @property
    def has_exp3d(self) -> bool:
        """Is expired on 3 days."""
        return self.__f(const.FEnumFSErr.Exp3d)

    @property
    def has_exp30d(self) -> bool:
        """Is expired on 30 days."""
        return self.__f(const.FEnumFSErr.Exp30d)

    @property
    def has_full90(self) -> bool:
        """FS is 90% filled."""
        return self.__f(const.FEnumFSErr.Full90)

    @property
    def has_timeout(self) -> bool:
        """OFD timeout."""
        return self.__f(const.FEnumFSErr.Timeout)

    @property
    def has_crit(self) -> bool:
        """FS Critical error."""
        return self.__f(const.FEnumFSErr.Crit)
