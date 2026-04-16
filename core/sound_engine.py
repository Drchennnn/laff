import time
import threading
import logging

try:
    from playsound import playsound
    _playsound_available = True
except ImportError:
    _playsound_available = False
    logging.error("laff: playsound not installed — audio disabled")


class SoundEngine:
    def __init__(self, cooldown: float):
        self.cooldown = cooldown
        self._last_played: dict[str, float] = {}
        if not _playsound_available:
            logging.error("laff: audio disabled")

    def play(self, event_type: str, path: str):
        if not _playsound_available:
            return
        now = time.monotonic()
        if now - self._last_played.get(event_type, 0.0) < self.cooldown:
            return
        self._last_played[event_type] = now
        logging.info(f"laff: playing {path}")
        # playsound 是阻塞的，放到线程里避免卡主循环
        threading.Thread(target=playsound, args=(path,), daemon=True).start()

    def shutdown(self):
        pass
