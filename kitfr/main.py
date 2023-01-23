#!/usr/bin/env python3
"""Main CLI module."""
import cmd
# 1. std
import sys
# 3. local
from kitfr import cmd, net, rsp, util, errs

__COMMANDS = {
    'GetDeviceStatus': (cmd.CmdGetDeviceStatus, "Get FR status."),
    'GetDeviceModel': (cmd.CmdGetDeviceModel, "Get FR model."),
    'GetStorageStatus': (cmd.CmdGetStorageStatus, "Get FS status.")
}


def main():
    """CLI."""
    def __help():
        print(
            f"Usage: {sys.argv[0]} <host> <port> <command>\n"
            "Commands:\n\t" + "\n\t".join([f"{k}: {v[1]}" for k, v in __COMMANDS.items()])
        )
    if len(sys.argv) < 4 or sys.argv[3] not in __COMMANDS:
        __help()
        return
    cmd_class = __COMMANDS[sys.argv[3]][0]
    frame_o = util.bytes2frame(cmd_class().to_bytes())  # 1. make command | frame it
    # 2. send
    frame_i = net.send(sys.argv[1], int(sys.argv[2]), frame_o, 3)
    # 3. dispatch response
    ok, rsp_object = rsp.frame2rsp(cmd_class.cmd_id, frame_i)
    if ok:
        print(rsp_object)
    else:
        print("Err: %02x '%s'" % (rsp_object, errs.ERR_TEXT['ru'].get(rsp_object, '<Unknown>.')))
    # 4. handle exceptions:
    # - TimeoutError (no host for socket.create_connection())
    # TODO: verbosity (e.g. `print(frame.hex().upper())`), dry_run


if __name__ == '__main__':
    main()
