#!/usr/bin/env python3
"""Stress-test of POS networking.
Try to txrx random commands and get responses."""
import os.path
import sys
import time
import random
import socket
import crcmod

HELP = f"Usage: {os.path.basename(__file__)} <host> <port> <tickets> <retries>"
FRAME_HEADER = b'\xB6\x29'
__SIMPLES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 0x50, 0x73, 0x75, 0x77)  # simple commands
SAMPLES = []

crc = crcmod.predefined.mkCrcFun('crc-ccitt-false')  # CRC16-CCITT, LE, polynom = 0x1021, initValue=0xFFFF.


def _send(host: str, port: int, data_out: bytes, timeout=None) -> bytes:
    """Send command and get response."""
    with socket.create_connection((host, port), timeout=timeout or socket.getdefaulttimeout()) as sock:
        sock.sendall(data_out)
        return sock.recv(2048, socket.MSG_WAITALL)


def __gen_commands(tickets: int):
    """Generate command samples."""
    def __wrap(data: bytes) -> bytes:
        """Wrap command into frame (hdr+len+body+crc)"""
        return FRAME_HEADER + (inner := (len(data)).to_bytes(2, 'big') + data) + crc(inner).to_bytes(2, 'little')
    for i in __SIMPLES:
        SAMPLES.append(__wrap(i.to_bytes(1, 'little')))
    for i in range(tickets):
        SAMPLES.append(__wrap(b'\x30' + (i + 1).to_bytes(4, 'little')))
    # for b in SAMPLES:
    #    print(b.hex())


def main():
    """Entry point."""
    if len(sys.argv) != 5:
        print(HELP)
        return
    __gen_commands(int(sys.argv[3]))
    retries = int(sys.argv[4])
    max_i = len(SAMPLES) - 1
    random.seed()
    for i in range(retries):
        r = _send(sys.argv[1], int(sys.argv[2]), SAMPLES[random.randint(0, max_i)])
        l_r = len(r)
        if l_r > 1030:
            print(f"#{i}: Data too big: {l_r} bytes.")
        elif l_r < 7:
            print(f"#{i}: Data too short: {l_r} bytes ({r.hex().upper()}).")


if __name__ == '__main__':
    main()
