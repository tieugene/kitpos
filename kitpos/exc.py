"""Exceptions."""


class Kpe(RuntimeError):
    """KitPOS basic error."""


class Kpw(RuntimeWarning):
    """KitPOS basic warning."""


class KpeNoted(Kpe):
    """KitPOS annotated errer exceptions."""

    msg: str

    def __init__(self, msg: str):
        """No comments."""
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        """Make string representation of exception."""
        return self.msg


class KpeNet(KpeNoted):
    """KitPOS frame [un]wrap exceptions."""


class KpeFrame(KpeNoted):
    """KitPOS frame [un]wrap exceptions."""


class KpePOS(Kpe):
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


class KpeRspDecode(KpeNoted):
    """KitPOS response object decoding exceptions."""
