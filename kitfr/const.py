"""Constants."""
# 1. std
import enum


FRAME_HEADER = b'\xB6\x29'


@enum.unique
class _IEnumPrintable(enum.IntEnum):
    def __str__(self):
        return f"{self.name}({self.value})"


@enum.unique
class IEnumCmd(enum.IntEnum):
    """Commands."""
    GetDeviceStatus = 0x01            # ✓ [Info] Get status
    GetDeviceModel = 0x04             # ✓ [Info]
    GetStorageStatus = 0x08           # ✓ [Info]
    GetRegisterParms = 0x0A           # ✓ [Info]
    DocCancel = 0x10                  # [RegFS]
    ReceiptSendAutomatNum = 0x1F      # [Receipt]
    GetCurSession = 0x20              # [Session]
    SessionOpenBegin = 0x21           # [Session]
    SessionOpenCommit = 0x22          # [Session]
    ReceiptBegin = 0x23               # [Receipt]
    ReceiptCommit = 0x24              # [Receipt]
    CorrReceiptBegin = 0x25           # [CorRcpt]
    CorrReceiptCommit = 0x26          # [CorRcpt]
    SessionCloseBegin = 0x29          # [Session]
    SessionCloseCommit = 0x2A         # [Session]
    ReceiptSendPos = 0x2B             # [Receipt]
    ReceiptSendAgent = 0x2C           # [Receipt]
    ReceiptSendPay = 0x2D             # [Receipt]
    CorrReceiptSendData = 0x2E        # [CorRcpt]
    GetDocByNum = 0x30                # … [Archive]
    CorrReceiptSendAutomatNum = 0x3F  # [CorRcpt]
    # ResetMGM = 0x40
    GetOFDXchgStatus = 0x50           # ✓ [Info]
    SetDateTime = 0x72                # [Settings]
    GetDateTime = 0x73                # ✓ [Settings]
    Restart = 0xEF


@enum.unique
class IEnumPrnStatus(_IEnumPrintable):
    """Printing device status.

    Used:
    - ...
    """
    OK = 0
    Offline = 1  # Prn device is not connected
    NoPaper = 2  # Out of paper
    PaperJam = 3
    CoverOpened = 5
    CutErr = 6
    HWErr = 7


@enum.unique
class IEnumFSphase(_IEnumPrintable):
    """FS live phase.

    Used:
    - ...
    """
    Ready = 1  # Ready for fiscalization
    Fisc = 3  # Fiscalization mode
    Post = 7  # Post-fiscal mode (sending FD to OFD)
    Arch = 5  # Reading data from archive


@enum.unique
class IEnumFSCurDoc(_IEnumPrintable):
    """FS current document type.

    Used:
    - ...
    """
    Empty = 0x00
    RegRpt = 0x01  # FR registration report
    SesOpenRpt = 0x02  # Session opening report
    Receipt = 0x04
    SesCloseRpt = 0x08  # Session closing report
    FSCloseRpt = 0x10  # Fiscal mode close report
    FSChgRpt = 0x12  # Re-registration due FS replacing report
    ReRegRpt = 0x13  # Reregistration report
    CorReceipt = 0x14  # Corr. receipt
    SattleRpt = 0x17  # Sattlement report


@enum.unique
class IEnumADocType(_IEnumPrintable):
    """Archive document types.

    Used:
    - RspGetDocByNum
    """
    RegRpt = 1  # FR registration report
    ReRegRpt = 11  # Reregistration report
    SesOpenRpt = 2  # Session opening report
    SattleRpt = 21  # Sattlement report
    Receipt = 3
    CorReceipt = 31  # Corr. receipt
    BSO = 4
    CorBSO = 41
    SesCloseRpt = 5  # Session closing report
    FSCloseRpt = 6  # Fiscal mode close report
    OpConfirm = 7  # Operator's confirmation


class IEnumReRegReason(_IEnumPrintable):
    """Reason for reregistration."""
    FS = enum.auto()  # Changing FS
    OFD = enum.auto()  # Changing OFD
    User = enum.auto()  # Changing user's requisitions
    FR = enum.auto()  # Changing FR settings (OFD INN + place/user)


class IEnumReceiptType(_IEnumPrintable):
    """Receipt type."""
    In = enum.auto()  # Incoming
    InRet = enum.auto()  # Incoming return
    Out = enum.auto()  # Outcome
    OutRet = enum.auto()  # Outcom return


class IFlagFSErr(enum.IntFlag):
    """FS errors and warnings.

    Used:
    - flag.FSErr > 0x...
    """
    Exp3d = 1  # Expired 3 days
    Exp30d = 2  # Expired 30 days
    Full90 = 4  # FS filled upt to 90%
    Timeout = 8  # OFD timeout
    Crit = 0x80  # Critical error


class IFlagFRMode(enum.IntFlag):
    """FR working mode.
    Used:
    - flag.FRModes > 0x...
    """
    Enc = enum.auto()  # Encryption
    Alone = enum.auto()  # Autonomous mode
    Auto = enum.auto()  # Automatic mode
    Srv = enum.auto()  # Service sector
    BSO = enum.auto()  # BSO(1)/Receipt(0) mode
    iNet = enum.auto()  # FR is Internet device


class IFlagTax(enum.IntFlag):
    """Tax type."""
    General = enum.auto()
    Simple = enum.auto()
    SimpleP = enum.auto()
    ENVD = enum.auto()
    ESD = enum.auto()
    PSN = enum.auto()


class IFlagAgent(enum.IntFlag):
    """Agent types."""
    Mode0 = enum.auto()
    Mode1 = enum.auto()
    Mode2 = enum.auto()
    Mode3 = enum.auto()
    Mode4 = enum.auto()
    Mode5 = enum.auto()
