import os
import logging


class Router:
    def __init__(self, sounds_dir: str, sound_pack: str):
        self.sounds_dir = sounds_dir
        self.sound_pack = sound_pack

    def resolve(self, event: dict) -> str | None:
        event_type = event.get('event')
        if event_type not in ('success', 'failure'):
            return None
        filename = f"{event_type}.mp3"
        path = os.path.join(self.sounds_dir, self.sound_pack, filename)
        if os.path.isfile(path):
            return path
        # fallback to default pack
        fallback = os.path.join(self.sounds_dir, 'default', filename)
        if os.path.isfile(fallback):
            logging.warning(f"laff: sound pack '{self.sound_pack}' missing {filename}, using default")
            return fallback
        logging.warning(f"laff: no sound file found for event '{event_type}'")
        return None
