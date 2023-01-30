"""Network things."""
# 1. std
from typing import Optional
import socket
import time


def txrx(
        host: str,
        port: int,
        data_out: bytes,
        conn_timeout: Optional[float] = None,
        txrx_timeout: Optional[float] = None) -> bytes:
    """Communicate with net device - send output data and get response data (sample)."""
    def __rx(__sock):
        return sock.recv(2048, socket.MSG_WAITALL)
    with socket.create_connection((host, port), timeout=conn_timeout or socket.getdefaulttimeout()) as sock:
        sock.sendall(data_out)  # or .send()
        retvalue = __rx(sock)
        if retvalue == b'\xb6\x29' and txrx_timeout:  # hack: wait for slow device
            time.sleep(txrx_timeout)
            retvalue += __rx(sock)
        return retvalue
