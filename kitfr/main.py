#!/usr/bin/env python3
"""Main CLI module.

:todo: Call commands w/ separate functions.
"""
# 1. std
import sys
import os
# 3. local
from kitfr import cli, net, rsp, util, errs

# x. consts
CONN_TIMEOUT = 3  # Too fast; can be 20+


def main():
    """CLI."""
    if len(sys.argv) < 4 or sys.argv[3] not in cli.COMMANDS:
        print(
            f"Usage: python3 {os.path.basename(__file__)} <host> <port> <command> [arg]\n"
            "Commands:\n\t" + "\n\t".join([f"{k}: {v.__doc__}" for k, v in cli.COMMANDS.items()])
        )
        return
    if (cmd_object := cli.COMMANDS[sys.argv[3]](sys.argv[4:])) is None:
        return
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
        cmd_class = type(cmd_object)
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
