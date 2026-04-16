import threading
import logging

try:
    import pystray
    from PIL import Image, ImageDraw
    _tray_available = True
except ImportError:
    _tray_available = False
    logging.error("laff: pystray/Pillow not installed — tray disabled")


def _make_icon(enabled: bool) -> "Image.Image":
    img = Image.new('RGB', (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    color = (0, 200, 100) if enabled else (150, 150, 150)
    draw.ellipse([8, 8, 56, 56], fill=color)
    return img


class TrayApp:
    def __init__(self, config: dict, on_quit):
        self._config = config
        self._on_quit = on_quit
        self._icon = None

    def start(self):
        if not _tray_available:
            return
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        def toggle(icon, item):
            self._config['enabled'] = not self._config['enabled']
            icon.icon = _make_icon(self._config['enabled'])

        def quit_app(icon, item):
            icon.stop()
            self._on_quit()

        menu = pystray.Menu(
            pystray.MenuItem(
                lambda item: 'Enabled' if self._config['enabled'] else 'Disabled',
                toggle,
                checked=lambda item: self._config['enabled'],
            ),
            pystray.MenuItem('Quit', quit_app),
        )
        self._icon = pystray.Icon(
            'laff',
            _make_icon(self._config['enabled']),
            'laff',
            menu=menu,
        )
        self._icon.run()
