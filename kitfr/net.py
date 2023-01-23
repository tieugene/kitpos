"""Network things."""
# 1. std
import socket
import time
# 3. local
from kitfr import exc


def send(host: str, port: int, data_out: bytes, timeout=None) -> bytes:
    """Communicate with net host."""
    with socket.create_connection((host, port), timeout=timeout if timeout else socket.getdefaulttimeout()) as sock:
        sock.sendall(data_out)  # or .send()
        time.sleep(0.05)  # TODO: ?
        data_in = sock.recv(1031)
        if (l_rsp := len(data_in)) > 1030:
            raise exc.KitFRNetError(f"Too big data received: {l_rsp} bytes.")
        # sock.close()  # not need
        return data_in
