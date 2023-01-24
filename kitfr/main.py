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
    frame_o = util.bytes2frame(cmd_object.to_bytes())  # 1. make command | frame it
    # print(frame_o.hex().upper())
    # return
    # 2. send
    frame_i = net.send(sys.argv[1], int(sys.argv[2]), frame_o, TIMEOUT)
    # 3. dispatch response
    ok, rsp_object = rsp.frame2rsp(cmd_class.cmd_id, frame_i)
    if ok:
        print(rsp_object.str)
    else:
        print("Err: %02x '%s'" % (rsp_object, errs.ERR_TEXT['ru'].get(rsp_object, '<Unknown>.')))
    # TODO: handle exceptions:
    # - TimeoutError (no host for socket.create_connection())
    # TODO: verbosity (e.g. `print(frame.hex().upper())`)
    # TODO: dry_run


if __name__ == '__main__':
    main()
