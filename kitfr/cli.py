"""CLI commands executors."""
# 1. std
from typing import Optional
import datetime
import json
# 3. local
from kitfr import cmd, tag, const


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


def __cmd_21(v: Optional[str]) -> cmd.CmdSessionOpenBegin:
    """Begin opening session [0 (default)|1 - skip prn]."""
    if v:
        if v not in {'0', '1'}:
            print("Skip printing must be '0' or '1'.")
        else:
            return cmd.CmdSessionOpenBegin(v == '1')
    else:
        return cmd.CmdSessionOpenBegin()


def __cmd_22() -> cmd.CmdSessionOpenCommit:
    """Commit opening session."""
    return cmd.CmdSessionOpenCommit()


def __cmd_29(v: Optional[str]) -> cmd.CmdSessionCloseBegin:
    """Begin closing session [0 (default)|1 - skip prn]."""
    if v:
        if v not in {'0', '1'}:
            print("Skip printing must be '0' or '1'.")
        else:
            return cmd.CmdSessionCloseBegin(v == '1')
    else:
        return cmd.CmdSessionCloseBegin()


def __cmd_2a() -> cmd.CmdSessionCloseCommit:
    """Commit closing session."""
    return cmd.CmdSessionCloseCommit()


def __cmd_30(v: Optional[str]) -> cmd.CmdGetDocInfo:
    """Get document info."""
    if v:
        return cmd.CmdGetDocInfo(int(v))
    print("Doc number required.")


def __cmd_3a(v: Optional[str]) -> cmd.CmdGetDocData:
    """Get doc content."""
    if v:
        return cmd.CmdGetDocData(int(v))
    print("Doc number required.")


def __cmd_50() -> cmd.CmdGetOFDXchgStatus:
    """Get OFD exchange status."""
    return cmd.CmdGetOFDXchgStatus()


def __cmd_72(v: Optional[str]) -> cmd.CmdSetDateTime:
    """Set POS date/time."""
    # FIXME: convert v[0] into datitime
    if v:
        dt = datetime.datetime.strptime(v, '%y%m%d%H%M')  # TODO: handle exception
        return cmd.CmdSetDateTime(dt)
    print("Date/time required (yymmddHHMM).")


def __cmd_73() -> cmd.CmdGetDateTime:
    """Get POS date/time."""
    return cmd.CmdGetDateTime()


def __cmd_25() -> cmd.CmdCorrReceiptBegin:
    """Corr. Receipt. Step #1/4 - begin."""
    return cmd.CmdCorrReceiptBegin()


def __cmd_2e(v: Optional[str]) -> cmd.CmdCorrReceiptData:
    """Corr. Receipt. Step #2/4 - send data."""
    __tags = [1021, 1203, 1173, 1055, 1031, 1081, 1215, 1216, 1217, 1102, 1103, 1104, 1105, 1106, 1107, 1174]
    if v:
        raw = json.loads(v)
        for t in __tags:   # - check: all required tags; TODO: mv 2 CmdCorrReceiptData.__init__
            if str(t) not in raw:
                raise RuntimeError(f"Tag {t} not found.")
        # 2. convert raw dict into TagDict
        td = tag.json2tagdict(raw)
        return cmd.CmdCorrReceiptData(td)
    print("data required ('<json>').")


def __cmd_3f(v: Optional[str]) -> cmd.CmdCorrReceiptAutomat:
    """Corr. Receipt. Step #3/4 - send automat number."""
    __tags = [1009, 1187, 1036]
    if v:
        # 0. load json
        raw = json.loads(v)
        for t in __tags:   # - check: all required tags
            if str(t) not in raw:
                raise RuntimeError(f"Tag {t} not found.")
        # 2. convert raw dict into TagDict
        td = tag.json2tagdict(raw)
        # 3. go
        return cmd.CmdCorrReceiptAutomat(td)
    print("data required ('<json>').")


def __cmd_26(v: Optional[str]) -> cmd.CmdCorrReceiptCommit:
    """Corr. Receipt. Step #4/4 - commit."""
    if v:
        # print(v[0])
        raw = json.loads(v)
        # TODO: chk value types
        return cmd.CmdCorrReceiptCommit(
            req_type=const.IEnumReceiptType(raw['type']),
            total=raw['total']
        )
    print("data required ('<json>').")


COMMANDS = {
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
    'CorrReceiptData': (__cmd_2e, '<json>'),
    'CorrReceiptAutomat': (__cmd_3f, '<json>'),
    'CorrReceiptCommit': (__cmd_26, '<json>')
}
