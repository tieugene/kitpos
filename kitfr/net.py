"""Network things."""
# 1. std
import socket


def txrx(host: str, port: int, data_out: bytes, timeout=None) -> bytes:
    """Communicate with net device - send output data and get response data (sample)."""
    with socket.create_connection((host, port), timeout=timeout or socket.getdefaulttimeout()) as sock:
        sock.sendall(data_out)  # or .send()
        return sock.recv(2048, socket.MSG_WAITALL)
