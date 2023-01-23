"""Constants."""

import enum


FRAME_HEADER = b'\xB6\x29'


class IEnumCmd(enum.IntEnum):
    """Commands."""
    GetDeviceStatus = 0x01  # [Info] Get status
    GetDeviceModel = 0x04  # [Info]
    GetStorageStatus = 0x08  # [Info]
    GetRegisterParms = 0x0A
    CancelDoc = 0x10
    SendReceiptAutomatNum = 0x1F
    SessionOpenStart = 0x21
    SessionOpen = 0x22
    ReceiptOpen = 0x23
    ReceiptClose = 0x24
    CorrReceiptOpen = 0x25
    CorrReceiptClose = 0x26
    SessionCloseStart = 0x29
    SessionClose = 0x2A
    SendReceiptPos = 0x2B
    SendReceiptAgent = 0x2C
    SendReceiptPay = 0x2D
    SendCorrReceiptData = 0x2E
    GetDocByNum = 0x30
    SendCorrReceiptAutomatNum = 0x3F
    GetOFDXchgStatus = 0x50
    SetDateTime = 0x72  # [Settings]
    GetDateTime = 0x73
    Restart = 0xEF


class IEnumErr(enum.IntEnum):
    """Response error codes."""
    ...  # TODO
