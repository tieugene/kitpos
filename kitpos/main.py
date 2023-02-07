#!/usr/bin/env python3
"""Main CLI module."""
# 1. std
from typing import Optional
from types import FunctionType
import sys
import json
import argparse
# 3. local
from kitpos import cli, net, rsp, util, errs
# x. consts
CONN_TIMEOUT = 3  # TODO: too fast; can be 20+


def __mk_args_parser() -> argparse.ArgumentParser:
    """TODO: [RTFM](https://habr.com/ru/post/466999/)."""
    def __mk_subhelp() -> str:
        retvalue = 'command:'
        for k, v in cli.COMMANDS.items():
            if isinstance(v, tuple):
                retvalue += f"\n  {k} {v[1]}: {v[0].__doc__}"
            else:
                retvalue += f"\n  {k}: {v.__doc__}"
        return retvalue
    parser = argparse.ArgumentParser(
        prog="kitpos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Tool to control Termanal-FA POS",
        epilog=__mk_subhelp())
    parser.add_argument('-p', '--port', type=int, default=7777, help="POS TCP/IP port (default 7777)")
    parser.add_argument('--dry-run', action='store_true', help="Print cmd dump")
    parser.add_argument('-f', '--file', action='store_true', help="Get json from file (default from arg)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Extended logging")
    parser.add_argument('host', type=str, help="POS to connect")
    parser.add_argument('cmd', metavar='cmd', choices=cli.COMMANDS.keys(), help="Command to execute")
    parser.add_argument('arg', nargs='?', help="Argument of some commands")
    return parser


def __do_it(host: str, port: int, cmd_name: str, arg: Optional[str], dry_run: bool, from_file: bool, verbose: bool):
    __cmd_XX = cli.COMMANDS[cmd_name]
    if isinstance(__cmd_XX, FunctionType):
        cmd_object = __cmd_XX()
    else:  # isinstance(__cmd_XX, tuple)
        if __cmd_XX[1] == cli.JSON_ARG:
            if arg is None:
                print("JSON data required")
                return
            if from_file:
                with open(arg, 'rt') as fp:
                    arg = json.load(fp)
            else:
                arg = json.loads(arg)
        cmd_object = __cmd_XX[0](arg)
    if cmd_object is None:
        return
    bytes_o = cmd_object.to_bytes()  # 1. make command...
    frame_o = util.bytes2frame(bytes_o)  # ..., frame it
    if dry_run:
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


def main():
    """CLI entry point."""
    args = __mk_args_parser().parse_args(sys.argv[1:])
    __do_it(args.host, args.port, args.cmd, args.arg, args.dry_run, args.file, args.verbose)


if __name__ == '__main__':
    main()
