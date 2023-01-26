#!/usr/bin/env python3
"""Main CLI module.

:todo: Call commands w/ separate functions.
"""
# 1. std
import sys
# 3. local
from kitfr import cmd, net, rsp, util, errs
# x. consts
TIMEOUT = 3
__COMMANDS = {
    'GetDeviceStatus': cmd.CmdGetDeviceStatus,
    'GetDeviceModel': cmd.CmdGetDeviceModel,
    'GetStorageStatus': cmd.CmdGetStorageStatus,
    'GetRegisterParms': cmd.CmdGetRegisterParms,
    'GetDocByNum': cmd.CmdGetDocByNum,
    'GetOFDXchgStatus': cmd.CmdGetOFDXchgStatus,
    'GetDateTime': cmd.CmdGetDateTime
}


def main():
    """CLI."""
    def __help():
        print(
            f"Usage: {sys.argv[0]} <host> <port> <command>\n"
            "Commands:\n\t" + "\n\t".join([f"{k}: {v.__doc__}" for k, v in __COMMANDS.items()])
        )
    if len(sys.argv) < 4 or sys.argv[3] not in __COMMANDS:
        __help()
        return
    cmd_class = __COMMANDS[sys.argv[3]]
    cmd_object = cmd_class(int(sys.argv[4])) if cmd_class == cmd.CmdGetDocByNum else cmd_class()  # FIXME: hack
    bytes_o = cmd_object.to_bytes()  # 1. make command...
    frame_o = util.bytes2frame(bytes_o)  # ..., frame it
    # print(frame_o.hex().upper())
    frame_i = net.send(sys.argv[1], int(sys.argv[2]), frame_o, TIMEOUT)    # 2. send
    # 3. dispatch response
    # - unwrap frame
    payload_i = util.frame2bytes(frame_i)
    # - ok/err
    ok, bytes_i = util.bytes_as_response(payload_i)
    # - dispatch last
    if ok:
        rsp_object = rsp.bytes2rsp(cmd_class.cmd_id, bytes_i)
        print(rsp_object.str())
    else:
        print("Err: %02x '%s'" % (bytes_i, errs.ERR_TEXT['ru'].get(bytes_i, '<Unknown>.')))
    # TODO: handle exceptions:
    # - TimeoutError (no host for socket.create_connection())
    # TODO: verbosity (e.g. `print(frame.hex().upper())`)
    # TODO: dry_run


if __name__ == '__main__':
    main()
