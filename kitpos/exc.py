"""Exceptions."""


class KitPOSError(RuntimeError):
    """KitPOS basic error"""
    ...


class KitPOSWarning(RuntimeWarning):
    """KitPOS basic warning"""
    ...


class KitPOSTxtError(KitPOSError):
    """KitPOS commented exceptions"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class KitPOSNetError(KitPOSTxtError):
    """KitPOS frame [un]wrap exceptions"""
    def __init__(self, msg: str):
        super().__init__(msg)


class KitPOSFrameError(KitPOSTxtError):
    """KitPOS frame [un]wrap exceptions"""
    def __init__(self, msg: str):
        super().__init__(msg)


class KitPOSResponseError(KitPOSError):
    """MFP error response"""
    rsname: str     # response name (AppResExt...)
    code: int       # Result/ErrorInfo/Code
    desc: str       # Result/ErrorInfo/Description

    def __init__(self, rsname: str, code: int, desc: str):
        super().__init__(self)
        self.rsname = rsname
        self.code = code
        self.desc = desc

    def __str__(self):
        return "Device response '{0}' error {1}: {2}".format(self.rsname, self.code, self.desc)


class KitPOSRspDecodeError(KitPOSTxtError):
    """KitPOS response object decoding exceptions"""
    def __init__(self, msg: str):
        super().__init__(msg)
