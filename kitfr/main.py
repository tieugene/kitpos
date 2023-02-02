#!/usr/bin/env python3
"""Main CLI module."""
# 1. std
from typing import Optional
import sys
import os
import argparse
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


def __mk_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kitpos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Tool to control Termanal-FA POS",
        epilog=f"Commands:\n\t" + "\n\t".join([f"{k}: {v.__doc__}" for k, v in cli.COMMANDS.items()]))
    parser.add_argument('-p', '--port', type=int, default=7777, help="POS TCP/IP port (default 7777)")
    parser.add_argument('--dry-run', action='store_true', help="Print cmd dump")
    parser.add_argument('-f', '--file', action='store_true', help="Get json from file (default from arg)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Extended logging")
    parser.add_argument('host', type=str, help="POS to connect")
    parser.add_argument('cmd', metavar='cmd', choices=cli.COMMANDS.keys(), help="Command to execute")
    parser.add_argument('arg', nargs='?', help="Argument of some commands")
    return parser


def main():
    """CLI."""
    parser = __mk_args_parser()
    # print(parser.print_help())
    print(parser.parse_args(sys.argv[1:]))
    return
    if not (4 <= len(sys.argv) <= 5):
        print(f"Usage: python3 {os.path.basename(__file__)} <host> <port> <command> [arg]")
    elif sys.argv[3] not in cli.COMMANDS:
        print(f"Commands:\n\t" + "\n\t".join([f"{k}: {v.__doc__}" for k, v in cli.COMMANDS.items()]))
    else:
        # TODO: process argv[4] B4 by arg type required (int, str, dict)
        # TODO: json from cli/stdin/file
        __do_it(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) == 5 else None)


if __name__ == '__main__':
    main()
