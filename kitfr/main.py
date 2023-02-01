#!/usr/bin/env python3
"""Main CLI module."""
# 1. std
import sys
import os
from typing import Optional

# 3. local
from kitfr import cli, net, rsp, util, errs
# x. consts
CONN_TIMEOUT = 3  # Too fast; can be 20+


def __do_it(host: str, port: int, cmd_name: str, arg: Optional[str]):
    """Main command dispatcher."""
    if (cmd_object := cli.COMMANDS[cmd_name](arg)) is None:
        return
    bytes_o = cmd_object.to_bytes()  # 1. make command...
    frame_o = util.bytes2frame(bytes_o)  # ..., frame it
    print(frame_o.hex().upper())
    return
    # 2. txrx
    frame_i = net.txrx(host, port, frame_o, conn_timeout=CONN_TIMEOUT, txrx_timeout=0.1)
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


def main():
    """CLI."""
    if not (4 <= len(sys.argv) <= 5):
        print(f"Usage: python3 {os.path.basename(__file__)} <host> <port> <command> [arg]")
    elif sys.argv[3] not in cli.COMMANDS:
        print(f"Commands:\n\t" + "\n\t".join([f"{k}: {v.__doc__}" for k, v in cli.COMMANDS.items()]))
    else:
        __do_it(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) == 5 else None)


if __name__ == '__main__':
    main()
