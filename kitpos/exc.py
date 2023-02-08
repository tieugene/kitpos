"""Exceptions."""


class KitPOSError(RuntimeError):
    """KitPOS basic error."""


class KitPOSWarning(RuntimeWarning):
    """KitPOS basic warning."""


class KitPOSTxtError(KitPOSError):
    """KitPOS commented exceptions."""

    msg: str

    def __init__(self, msg: str):
        """No comments."""
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        """Make string representation of exception."""
        return self.msg


class KitPOSNetError(KitPOSTxtError):
    """KitPOS frame [un]wrap exceptions."""


class KitPOSFrameError(KitPOSTxtError):
    """KitPOS frame [un]wrap exceptions."""


class KitPOSResponseError(KitPOSError):
    """POS error response."""

    code: int       # Result/ErrorInfo/Code
    desc: str       # Result/ErrorInfo/Description

    def __init__(self, rsname: str, code: int, desc: str):
        """Make new POS error reponse.

        :param code: Pre-defined code
        :param desc: Error description
        """
        super().__init__(self)
        self.rsname = rsname
        self.code = code
        self.desc = desc

    def __str__(self):
        """Make string representation of the exception."""
        return f"Device response '{self.rsname}' error {self.code}: {self.desc}"


class KitPOSRspDecodeError(KitPOSTxtError):
    """KitPOS response object decoding exceptions."""
