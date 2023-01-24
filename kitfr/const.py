"""Constants."""
# 1. std
import enum


FRAME_HEADER = b'\xB6\x29'


class IEnumCmd(enum.IntEnum):
    """Commands."""
    GetDeviceStatus = 0x01  # [Info] Get status, ~args~
    GetDeviceModel = 0x04  # [Info], ~args~
    GetStorageStatus = 0x08  # [Info], ~args~
    GetRegisterParms = 0x0A  # [Info]
    CancelDoc = 0x10  # [RegFS]
    SendReceiptAutomatNum = 0x1F  # [Receipt]
    SessionOpenStart = 0x21  # [Session]
    SessionOpen = 0x22  # [Session]
    ReceiptOpen = 0x23  # [Receipt]
    ReceiptClose = 0x24  # [Receipt]
    CorrReceiptOpen = 0x25  # [CorRcpt]
    CorrReceiptClose = 0x26  # [CorRcpt]
    SessionCloseStart = 0x29  # [Session]
    SessionClose = 0x2A  # [Session]
    SendReceiptPos = 0x2B  # [Receipt]
    SendReceiptAgent = 0x2C  # [Receipt]
    SendReceiptPay = 0x2D  # [Receipt]
    SendCorrReceiptData = 0x2E  # [CorRcpt]
    GetDocByNum = 0x30  # [Archive]
    SendCorrReceiptAutomatNum = 0x3F  # [CorRcpt]
    # ResetMGM = 0x40
    GetOFDXchgStatus = 0x50  # [Info]
    SetDateTime = 0x72  # [Settings]
    GetDateTime = 0x73  # [Settings]
    Restart = 0xEF


class IEnumErr(enum.IntEnum):
    """Response error codes."""
    ...  # TODO
