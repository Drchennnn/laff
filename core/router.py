import os
import glob
import random
import logging


class Router:
    def __init__(self, sounds_dir: str, sound_pack: str):
        self.sounds_dir = sounds_dir
        self.sound_pack = sound_pack

    def resolve(self, event: dict) -> str | None:
        event_type = event.get('event')
        if event_type not in ('success', 'failure'):
            return None
        files = self._scan(self.sound_pack, event_type)
        if not files and self.sound_pack != 'default':
            logging.warning(f"laff: sound pack '{self.sound_pack}' 没有 {event_type} 音效，回退到 default")
            files = self._scan('default', event_type)
        if not files:
            logging.warning(f"laff: 找不到 {event_type} 的音效文件")
            return None
        return random.choice(files)

    def _scan(self, pack: str, event_type: str) -> list[str]:
        pattern = os.path.join(self.sounds_dir, pack, event_type, '*.mp3')
        return glob.glob(pattern)
