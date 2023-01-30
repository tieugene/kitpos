"""Network things."""
# 1. std
import socket
import time


def txrx(host: str, port: int, data_out: bytes, conn_timeout=None, txrx_timeout=None) -> bytes:
    """Communicate with net device - send output data and get response data (sample)."""
    with socket.create_connection((host, port), timeout=conn_timeout or socket.getdefaulttimeout()) as sock:
        sock.sendall(data_out)  # or .send()
        if txrx:
            time.sleep(txrx_timeout)
        return sock.recv(2048, socket.MSG_WAITALL)
