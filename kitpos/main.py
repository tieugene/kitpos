#!/usr/bin/env python3
"""Main CLI module."""
# 1. std
from typing import Optional
from types import FunctionType
import sys
import json
import argparse
import logging
# 3. local
from kitpos import cli, net, rsp, util, exc
# x. consts
CONN_TIMEOUT = 3  # TODO: too fast; can be 20+


def __mk_args_parser() -> argparse.ArgumentParser:
    """TODO: [RTFM](https://habr.com/ru/post/466999/)."""
    def __mk_subhelp() -> str:
        retvalue = 'command:'
        for k, val in cli.COMMANDS.items():
            if isinstance(val, tuple):
                retvalue += f"\n  {k} {val[1]}: {val[0].__doc__}"
            else:
                retvalue += f"\n  {k}: {val.__doc__}"
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


def __do_it(host: str, port: int, cmd_name: str, arg: Optional[str], dry_run: bool, from_file: bool) -> Optional[str]:
    """Execute CLI.

    :param host: POS IP
    :param port: POS TCP/IP port
    :param cmd_name: Command to execute
    :param arg: Command argument (optional)
    :param dry_run: If True: dump bytes to send and exit
    :param from_file: Whether read json data from file instead of argv
    """
    __cmd_xx = cli.COMMANDS[cmd_name]
    if isinstance(__cmd_xx, FunctionType):
        cmd_object = __cmd_xx()
    else:  # isinstance(__cmd_XX, tuple)
        if __cmd_xx[1] == cli.JSON_ARG:
            if arg is None:
                exc.KpeCLI("JSON data required")
            if from_file:
                with open(arg, 'rt', encoding='utf-8') as infile:  # TODO: handle opening error
                    arg = json.load(infile)  # TODO: handle json.load() exceptions
            else:
                arg = json.loads(arg)  # TODO: handle json.loads() exceptions
        cmd_object = __cmd_xx[0](arg)
    bytes_o = cmd_object.to_bytes()  # 1. make command...
    logging.debug(f"Cmd bytes: {util.b2hex(bytes_o)}")
    frame_o = util.frame_pack(bytes_o)  # ..., frame it
    logging.debug(f"Cmd frame: {util.b2hex(frame_o)}")
    if dry_run:
        return
    # 2. txrx
    frame_i = net.txrx(host, port, frame_o, conn_timeout=CONN_TIMEOUT, txrx_timeout=1)
    logging.debug(f"Rsp frame: {util.b2hex(frame_i)}")
    # 3. dispatch response
    # - unwrap frame
    payload_i = util.frame_unpack(frame_i)
    logging.debug(f"Rsp payload: {util.b2hex(payload_i)}")
    # - ok/err
    decoded_ok, bytes_i = util.frame_payload_dispatch(payload_i)
    # - dispatch last
    if decoded_ok:
        logging.debug(f"Rsp bytes: {util.b2hex(bytes_i)}")
        cmd_class = type(cmd_object)
        rsp_object = rsp.bytes2rsp(cmd_class.cmd_id, bytes_i)
        return rsp_object.str('\n')
    else:
        raise exc.KpePOS(bytes_i)


def main():
    """CLI entry point."""
    args = __mk_args_parser().parse_args(sys.argv[1:])
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
    # logger = logging.getLogger(__name__)
    try:
        result = __do_it(args.host, args.port, args.cmd, args.arg, args.dry_run, args.file)
    except exc.KpePOS as e:
        err_text = cli.ERR_TEXT['ru'].get(e.code, '<Unknown>.')
        logging.error(f"POS error: {e.code:02x} '{err_text}'")
    except exc.Kpe as e:
        msg = f"Exception occurs ({e})"
        logging.exception(msg) if args.verbose else logging.error(msg)
    else:
        if result:
            print(result)


if __name__ == '__main__':
    main()
