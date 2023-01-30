#!/usr/bin/env python3
"""Main CLI module.

:todo: Call commands w/ separate functions.
"""
# 1. std
from typing import List
import sys
import os
import datetime
# 3. local
from kitfr import cmd, net, rsp, util, errs
# x. consts
CONN_TIMEOUT = 3  # Too fast; can be 20+


def __cmd_01(_) -> cmd.CmdGetDeviceStatus:
    """Get POS status."""
    return cmd.CmdGetDeviceStatus()


def __cmd_04(_) -> cmd.CmdGetDeviceModel:
    """Get POS model."""
    return cmd.CmdGetDeviceModel()


def __cmd_08(_) -> cmd.CmdGetStorageStatus:
    """Get FS status."""
    return cmd.CmdGetStorageStatus()


def __cmd_0a(_) -> cmd.CmdGetRegisterParms:
    """Get POS/FS registering parameters."""
    return cmd.CmdGetRegisterParms()


def __cmd_10(_) -> cmd.CmdDocCancel:
    """Cancel current document."""
    return cmd.CmdDocCancel()


def __cmd_20(_) -> cmd.CmdGetCurSession:
    """Get session params."""
    return cmd.CmdGetCurSession()


def __cmd_21(v: List[str]) -> cmd.CmdSessionOpenBegin:
    """Begin opening session [0 (default)|1 - skip prn]."""
    if v:
        if v[0] not in {'0', '1'}:
            print("Skip printing must be '0' or '1'.")
        else:
            return cmd.CmdSessionOpenBegin(v[0] == '1')
    else:
        return cmd.CmdSessionOpenBegin()


def __cmd_22(_) -> cmd.CmdSessionOpenCommit:
    """Commit opening session."""
    return cmd.CmdSessionOpenCommit()


def __cmd_29(v: List[str]) -> cmd.CmdSessionCloseBegin:
    """Begin closing session [0 (default)|1 - skip prn]."""
    if v:
        if v[0] not in {'0', '1'}:
            print("Skip printing must be '0' or '1'.")
        else:
            return cmd.CmdSessionCloseBegin(v[0] == '1')
    else:
        return cmd.CmdSessionCloseBegin()


def __cmd_2a(_) -> cmd.CmdSessionCloseCommit:
    """Commit closing session."""
    return cmd.CmdSessionCloseCommit()


def __cmd_30(v: List[str]) -> cmd.CmdGetDocByNum:
    """Find document by its number <num>."""
    if v:
        return cmd.CmdGetDocByNum(int(v[0]))
    print("Doc number required.")


def __cmd_3a(v: List[str]) -> cmd.CmdReadDoc:
    """Get doc <num> content."""
    if v:
        return cmd.CmdReadDoc(int(v[0]))
    print("Doc number required.")


def __cmd_50(_) -> cmd.CmdGetOFDXchgStatus:
    """Get OFD exchange status."""
    return cmd.CmdGetOFDXchgStatus()


def __cmd_72(v: List[str]) -> cmd.CmdSetDateTime:
    """Set POS date/time to <yymmddHHMM>."""
    # FIXME: convert v[0] into datitime
    if v:
        dt = datetime.datetime.strptime(v[0], '%y%m%d%H%M')  # TODO: handle exception
        return cmd.CmdSetDateTime(dt)
    print("Date/time required (yymmddHHMM).")


def __cmd_73(_) -> cmd.CmdGetDateTime:
    """Get POS date/time."""
    return cmd.CmdGetDateTime()


__COMMANDS = {
    'GetDeviceStatus': __cmd_01,
    'GetDeviceModel': __cmd_04,
    'GetStorageStatus': __cmd_08,
    'GetRegisterParms': __cmd_0a,
    'DocCancel': __cmd_10,
    'GetCurSession': __cmd_20,
    'SessionOpenBegin': __cmd_21,
    'SessionOpenCommit': __cmd_22,
    'SessionCloseBegin': __cmd_29,
    'SessionCloseCommit': __cmd_2a,
    'GetDocInfo': __cmd_30,
    'GetDocContent': __cmd_3a,
    'GetOFDXchgStatus': __cmd_50,
    'SetDateTime': __cmd_72,
    'GetDateTime': __cmd_73,
}


def main():
    """CLI."""
    if len(sys.argv) < 4 or sys.argv[3] not in __COMMANDS:
        print(
            f"Usage: python3 {os.path.basename(__file__)} <host> <port> <command> [arg]\n"
            "Commands:\n\t" + "\n\t".join([f"{k}: {v.__doc__}" for k, v in __COMMANDS.items()])
        )
        return
    if (cmd_object := __COMMANDS[sys.argv[3]](sys.argv[4:])) is None:
        return
    cmd_class = type(cmd_object)
    bytes_o = cmd_object.to_bytes()  # 1. make command...
    frame_o = util.bytes2frame(bytes_o)  # ..., frame it
    # print(frame_o.hex().upper())
    # return
    frame_i = net.txrx(sys.argv[1], int(sys.argv[2]), frame_o, conn_timeout=30, txrx_timeout=0.1)    # 2. txrx
    # 3. dispatch response
    # - unwrap frame
    payload_i = util.frame2bytes(frame_i)
    # - ok/err
    ok, bytes_i = util.bytes_as_response(payload_i)
    # - dispatch last
    if ok:
        rsp_object = rsp.bytes2rsp(cmd_class.cmd_id, bytes_i)
        print(rsp_object.str('\n'))
    else:
        print("Err: %02x '%s'" % (bytes_i, errs.ERR_TEXT['ru'].get(bytes_i, '<Unknown>.')))
    # TODO: handle exceptions:
    # - TimeoutError (no host for socket.create_connection())
    # TODO: verbosity (e.g. `print(frame.hex().upper())`)
    # TODO: dry_run


if __name__ == '__main__':
    main()
