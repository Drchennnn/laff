import socket
import threading
import json
import queue
import logging


class Listener:
    def __init__(self, port: int, event_queue: queue.Queue):
        self.port = port
        self.event_queue = event_queue
        self._stop = threading.Event()

    def start(self):
        t = threading.Thread(target=self._serve, daemon=True)
        t.start()

    def stop(self):
        self._stop.set()

    def _serve(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
                srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                srv.bind(('127.0.0.1', self.port))
                srv.listen(5)
                srv.settimeout(1.0)
                logging.info(f"laff: listening on 127.0.0.1:{self.port}")
                while not self._stop.is_set():
                    try:
                        conn, _ = srv.accept()
                    except socket.timeout:
                        continue
                    threading.Thread(target=self._handle, args=(conn,), daemon=True).start()
        except OSError as e:
            logging.error(f"laff: could not bind to port {self.port}: {e}")

    def _handle(self, conn):
        with conn:
            try:
                data = conn.makefile().readline()
                if not data.strip():
                    return
                event = json.loads(data.strip())
                self.event_queue.put(event)
            except (json.JSONDecodeError, OSError) as e:
                logging.warning(f"laff: bad message: {e}")
