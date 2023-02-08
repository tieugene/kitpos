"""CLI commands executors."""
# 1. std
from typing import Optional, Dict
import datetime
# 3. local
from kitpos import cmd, tag, const
# x. const
JSON_ARG = '<json>'


def __cmd_01() -> cmd.CmdGetDeviceStatus:
    """Get POS status."""
    return cmd.CmdGetDeviceStatus()


def __cmd_04() -> cmd.CmdGetDeviceModel:
    """Get POS model."""
    return cmd.CmdGetDeviceModel()


def __cmd_08() -> cmd.CmdGetStorageStatus:
    """Get FS status."""
    return cmd.CmdGetStorageStatus()


def __cmd_0a() -> cmd.CmdGetRegisterParms:
    """Get POS/FS registering parameters."""
    return cmd.CmdGetRegisterParms()


def __cmd_10() -> cmd.CmdDocCancel:
    """Cancel current document."""
    return cmd.CmdDocCancel()


def __cmd_20() -> cmd.CmdGetCurSession:
    """Get session params."""
    return cmd.CmdGetCurSession()


def __cmd_21(val: Optional[str]) -> Optional[cmd.CmdSessionOpenBegin]:
    """Begin opening session [0 (default)|1 - skip prn]."""
    if val:
        if val not in {'0', '1'}:
            return print("Skip printing must be '0' or '1'.")  # == return None
        return cmd.CmdSessionOpenBegin(val == '1')
    return cmd.CmdSessionOpenBegin()


def __cmd_22() -> cmd.CmdSessionOpenCommit:
    """Commit opening session."""
    return cmd.CmdSessionOpenCommit()


def __cmd_29(val: Optional[str]) -> cmd.CmdSessionCloseBegin:
    """Begin closing session [0 (default)|1 - skip prn]."""
    if val:
        if val not in {'0', '1'}:
            return print("Skip printing must be '0' or '1'.")
        return cmd.CmdSessionCloseBegin(val == '1')
    return cmd.CmdSessionCloseBegin()


def __cmd_2a() -> cmd.CmdSessionCloseCommit:
    """Commit closing session."""
    return cmd.CmdSessionCloseCommit()


def __cmd_30(val: Optional[str]) -> Optional[cmd.CmdGetDocInfo]:
    """Get document info."""
    return cmd.CmdGetDocInfo(int(val)) if val else print("Doc number required.")


def __cmd_3a(val: Optional[str]) -> Optional[cmd.CmdGetDocData]:
    """Get doc content."""
    return cmd.CmdGetDocData(int(val)) if val else print("Doc number required.")


def __cmd_50() -> cmd.CmdGetOFDXchgStatus:
    """Get OFD exchange status."""
    return cmd.CmdGetOFDXchgStatus()


def __cmd_72(val: Optional[str]) -> Optional[cmd.CmdSetDateTime]:
    """Set POS date/time."""
    if val:
        datime = datetime.datetime.strptime(val, '%y%m%d%H%M')  # TODO: handle exception
        return cmd.CmdSetDateTime(datime)
    return print("Date/time required (yymmddHHMM).")


def __cmd_73() -> cmd.CmdGetDateTime:
    """Get POS date/time."""
    return cmd.CmdGetDateTime()


def __cmd_25() -> cmd.CmdCorrReceiptBegin:
    """Corr. Receipt. Step #1/4 - begin."""
    return cmd.CmdCorrReceiptBegin()


def __cmd_2e(val: Dict) -> cmd.CmdCorrReceiptData:
    """Corr. Receipt. Step #2/4 - send data."""
    return cmd.CmdCorrReceiptData(tag.json2tagdict(val))


def __cmd_3f(val: Dict) -> cmd.CmdCorrReceiptAutomat:
    """Corr. Receipt. Step #3/4 - send automat number (option)."""
    return cmd.CmdCorrReceiptAutomat(tag.json2tagdict(val))


def __cmd_26(val: Dict) -> cmd.CmdCorrReceiptCommit:
    """Corr. Receipt. Step #4/4 - commit."""
    # TODO: chk value types
    return cmd.CmdCorrReceiptCommit(
        req_type=const.IEnumReceiptType(val['type']),
        total=val['total']
    )


def __cmd_23() -> cmd.CmdReceiptBegin:
    """Receipt. Step #1/6 - begin."""
    return cmd.CmdReceiptBegin()


def __cmd_2b(val: Dict) -> cmd.CmdReceiptItem:
    """Receipt. Step #2/6 - send receipt item."""
    return cmd.CmdReceiptItem(tag.json2tagdict(val))


def __cmd_1f(val: Dict) -> cmd.CmdReceiptAutomat:
    """Receipt. Step #4/6 - send receipt automat details."""
    return cmd.CmdReceiptAutomat(tag.json2tagdict(val))


def __cmd_2d(val: Dict) -> cmd.CmdReceiptPayment:
    """Receipt. Step #5/6 - send receipt payment details."""
    return cmd.CmdReceiptPayment(tag.json2tagdict(val))


def __cmd_24(val: Dict) -> cmd.CmdReceiptCommit:
    """Receipt. Step #6/6 - commit."""
    # TODO: chk value types
    return cmd.CmdReceiptCommit(
        req_type=const.IEnumReceiptType(val['type']),
        total=val['total'],
        notes=val.get('notes')
    )


COMMANDS = {  # TODO: replace some functions w/ class directly
    'GetDeviceStatus': __cmd_01,
    'GetDeviceModel': __cmd_04,
    'GetStorageStatus': __cmd_08,
    'GetRegisterParms': __cmd_0a,
    'DocCancel': __cmd_10,
    'GetCurSession': __cmd_20,
    'SessionOpenBegin': (__cmd_21, '[0/1]'),
    'SessionOpenCommit': __cmd_22,
    'SessionCloseBegin': (__cmd_29, '[0/1]'),
    'SessionCloseCommit': __cmd_2a,
    'GetDocInfo': (__cmd_30, '<int>'),
    'GetDocData': (__cmd_3a, '<int>'),
    'GetOFDXchgStatus': __cmd_50,
    'SetDateTime': (__cmd_72, '<yymmddHHMM>'),
    'GetDateTime': __cmd_73,
    'CorrReceiptBegin': __cmd_25,
    'CorrReceiptData': (__cmd_2e, JSON_ARG),
    'CorrReceiptAutomat': (__cmd_3f, JSON_ARG),
    'CorrReceiptCommit': (__cmd_26, JSON_ARG),
    'ReceiptBegin': __cmd_23,
    'ReceiptItem': (__cmd_2b, JSON_ARG),
    'ReceiptAutomat': (__cmd_1f, JSON_ARG),
    'ReceiptPayment': (__cmd_2d, JSON_ARG),
    'ReceiptCommit': (__cmd_24, JSON_ARG)
}
