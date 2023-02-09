"""Exceptions."""


class Kpe(RuntimeError):
    """Basic error."""

    def __str__(self):
        """Make string representation of exception."""
        if uplink := super().__str__():
            return f"{self.__class__.__name__}: {uplink}"
        return self.__class__.__name__
        # py3.11+ only
        # if '__notes__' in self.__dict__ and self.__notes__:
        #    retvalue += (': ' + ', '.join(self.__notes__))


class Kpw(RuntimeWarning):
    """Basic warning."""


class KpeNet(Kpe):
    """POS network connection errors."""


class KpeFrame(Kpe):
    """Frame [un]wrap exceptions."""


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


class KpeRspDecode(Kpe):
    """Response object decoding exceptions."""
