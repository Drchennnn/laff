import time
import logging

try:
    import pygame
    _pygame_available = True
except ImportError:
    _pygame_available = False
    logging.error("laff: pygame not installed — audio disabled")


class SoundEngine:
    def __init__(self, volume: float, cooldown: float):
        self.volume = volume
        self.cooldown = cooldown
        self._last_played: dict[str, float] = {}
        self._ready = False
        if _pygame_available:
            try:
                pygame.mixer.init()
                self._ready = True
            except Exception as e:
                logging.error(f"laff: pygame mixer init failed: {e}")

    def play(self, event_type: str, path: str):
        if not self._ready:
            return
        now = time.monotonic()
        if now - self._last_played.get(event_type, 0.0) < self.cooldown:
            return
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.volume)
            sound.play()
            self._last_played[event_type] = now
            logging.info(f"laff: playing {path}")
        except Exception as e:
            logging.warning(f"laff: could not play {path}: {e}")

    def shutdown(self):
        if self._ready:
            pygame.mixer.quit()
