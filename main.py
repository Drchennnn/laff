import queue
import os
import sys
import logging
import yaml

from core.listener import Listener
from core.router import Router
from core.sound_engine import SoundEngine
from tray.tray_app import TrayApp

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))


def load_config() -> dict:
    path = os.path.join(BASE_DIR, 'config.yaml')
    try:
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"laff: config.yaml not found at {path}", file=sys.stderr)
        sys.exit(1)


def main():
    config = load_config()
    event_queue: queue.Queue = queue.Queue()

    sounds_dir = os.path.join(BASE_DIR, 'sounds')
    router = Router(sounds_dir, config['sound_pack'])
    engine = SoundEngine(config['volume'], config['cooldown'])
    listener = Listener(config['port'], event_queue)

    stop = False

    def on_quit():
        nonlocal stop
        stop = True

    tray = TrayApp(config, on_quit)
    tray.start()
    listener.start()

    try:
        while not stop:
            try:
                event = event_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if not config.get('enabled', True):
                continue

            path = router.resolve(event)
            if path:
                engine.play(event['event'], path)
    finally:
        listener.stop()
        engine.shutdown()
        logging.info("laff stopped")


if __name__ == '__main__':
    main()
