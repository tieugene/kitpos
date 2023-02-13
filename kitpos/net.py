"""Network things.

Copyright 2023 TI_Eugene <ti.eugene@gmail.com>
This file is part of the kitpos project.
You may use this file under the terms of the GPLv3 license.
"""
# 1. std
from typing import Optional
import socket
import time
# 3. local
from kitpos import const, exc


def txrx(
        host: str,
        port: int,
        data_out: bytes,
        conn_timeout: Optional[float] = None,
        txrx_timeout: Optional[float] = None) -> bytes:
    """Communicate with net device - send output data and get response data (sample)."""
    def __rx(__sock):
        return sock.recv(2048, socket.MSG_WAITALL)
    try:
        sock = socket.create_connection((host, port), timeout=conn_timeout or socket.getdefaulttimeout())
        sock.sendall(data_out)  # or .send()
        retvalue = __rx(sock)
        if retvalue == const.FRAME_HEADER and txrx_timeout:  # hack: wait for slow response after single header
            time.sleep(txrx_timeout)
            retvalue += __rx(sock)
        return retvalue
    except (socket.gaierror, socket.timeout, socket.error) as __e:
        raise exc.KpeNet(__e) from __e
