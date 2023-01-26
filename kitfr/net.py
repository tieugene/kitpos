"""Network things."""
# 1. std
import socket


def send(host: str, port: int, data_out: bytes, timeout=None) -> bytes:
    """Communicate with net host."""
    with socket.create_connection((host, port), timeout=timeout or socket.getdefaulttimeout()) as sock:
        sock.sendall(data_out)  # or .send()
        return sock.recv(2048, socket.MSG_WAITALL)
