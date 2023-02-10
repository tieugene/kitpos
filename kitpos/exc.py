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


class KpeBytePack(Kpe):
    """Converting to bytes errors."""


class KpeByteUnpack(Kpe):
    """Converting from bytes errors."""


class KpeByteUnpackBool(KpeByteUnpack):
    """Converting from bytes to bool errors."""


class KpeByteUnpackFVLN(KpeByteUnpack):
    """Converting from FVLN to int/float errors."""


class KpeFrame(Kpe):
    """Base frame [un]wrap exception."""


class KpeFramePack(KpeFrame):
    """Frame wrap exceptions."""


class KpeFrameUnpack(KpeFrame):
    """Frame unwrap exceptions."""


class KpeTag(Kpe):
    """Base tag exception."""


class KpeTagUnjson(KpeTag):
    """Base json-to-tags conversion exceptions."""


class KpeTagPack(KpeTag):
    """Base tags-to-bytes conversion exceptions."""


class KpeTagUnpack(KpeTag):
    """Base bytes-to-tag conversion exceptions."""


class KpeCmd(Kpe):
    """Base cmd exception."""


class KpeCmdInit(KpeCmd):
    """Cmd.__init__ exceptions."""


class KpeCmdPack(KpeCmd):
    """Cmd-to-bytes exceptions."""


class KpeRspDecode(Kpe):
    """Response object decoding exceptions."""


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
