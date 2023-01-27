#!/usr/bin/env python3
"""Dump POS response."""
import os.path
import sys
import socket


def _send(host: str, port: int, data_out: bytes, timeout=None) -> bytes:
    """Send command and get response."""
    with socket.create_connection((host, port), timeout=timeout or socket.getdefaulttimeout()) as sock:
        sock.sendall(data_out)
        return sock.recv(2048, socket.MSG_WAITALL)


def main():
    """Entry point."""
    if len(sys.argv) != 4:
        print(f"Usage: {os.path.basename(__file__)} <host> <port> <cmd_hex_dump>")
        return
    cmd = bytes.fromhex(sys.argv[3])
    if r := _send(sys.argv[1], int(sys.argv[2]), cmd):
        print(f"{r.hex().upper()} ({len(r)}).")
    else:
        print("No data.", file=sys.stderr)


if __name__ == '__main__':
    main()
