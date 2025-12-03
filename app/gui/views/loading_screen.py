from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
import os
import time

from ..ui.loading_screen_ui import Ui_LoadingScreen


class LoadingScreen(QDialog):
    """Simple slideshow loading screen.

    Looks for images in `app/static/splash` and displays them in order.
    Call `play(duration_ms=3000)` to run the slideshow (each image for duration_ms)
    and block until complete.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoadingScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setModal(True)

        self._images = []
        self._index = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._next_image)
        # Find splash images directory relative to this file
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        # Use images in app/static/images/splash as requested
        splash_dir = os.path.join(base_dir, 'static', 'images', 'splash')
        if os.path.isdir(splash_dir):
            for fname in sorted(os.listdir(splash_dir)):
                if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    self._images.append(os.path.join(splash_dir, fname))

        if not self._images:
            # No images found, show placeholder text
            self.ui.splashLabel.setText('Welcome')
            self.ui.statusLabel.setText('Starting...')
        else:
            self._index = 0
            self._set_pixmap(self._images[0])
        # Timing for min display
        self._started_at = None
        self._min_total_ms = 0

    def _set_pixmap(self, path: str):
        try:
            pix = QPixmap(path)
            if not pix.isNull():
                # scale to label while keeping aspect ratio
                lbl = self.ui.splashLabel
                w = lbl.width() or 400
                h = lbl.height() or 250
                scaled = pix.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                lbl.setPixmap(scaled)
                # Force a repaint to ensure UI updates immediately
                try:
                    lbl.repaint()
                except Exception:
                    pass
        except Exception:
            self.ui.splashLabel.setText('Image load error')

    def _next_image(self):
        if not self._images:
            self._timer.stop()
            self.accept()
            return

        # Advance index and loop indefinitely until stop() is called
        self._index = (self._index + 1) % len(self._images)
        self._set_pixmap(self._images[self._index])
        # Debug: show which image index is set
        try:
            print(f"LoadingScreen: showing image {self._index} -> {self._images[self._index]}")
        except Exception:
            pass

    def play(self, duration_ms: int = 2000):
        """Show the slideshow modally. Each image is shown for duration_ms.

        Returns when the slideshow completes (dialog closed).
        """
        if not self._images:
            # Nothing to show, close immediately
            self.accept()
            return

        # Start timer and exec modal (blocking)
        # default minimum total display is one full cycle
        if self._images:
            self._min_total_ms = duration_ms * max(1, len(self._images))
        else:
            self._min_total_ms = 0
        self._started_at = int(time.time() * 1000)
        print(f"LoadingScreen.play: starting slideshow, duration_ms={duration_ms}, min_total_ms={self._min_total_ms}")
        # For play (blocking) we still loop images but will close when the dialog is accepted/stopped
        self._timer.start(duration_ms)
        self.exec()

    def start(self, duration_ms: int = 2000):
        """Start the slideshow non-blocking.

        Use `stop()` to end the slideshow and close the dialog programmatically.
        """
        if not self._images:
            # Nothing to show
            self.show()
            return

        # Non-blocking show and start timer; loop images until stop() is called
        if self._images:
            self._min_total_ms = duration_ms * max(1, len(self._images))
        else:
            self._min_total_ms = 0
        self._started_at = int(time.time() * 1000)
        print(f"LoadingScreen.start: starting slideshow, duration_ms={duration_ms}, min_total_ms={self._min_total_ms}")
        self.setModal(False)
        # Show the dialog first so label sizes are available for scaling
        self.show()
        # If an initial image was set prior to show(), re-scale it now that geometry is available
        if self._images:
            self._set_pixmap(self._images[self._index])
        self._timer.start(duration_ms)

    def stop(self):
        """Stop the slideshow and close the dialog."""
        try:
            # enforce minimum display time
            if self._min_total_ms and self._started_at is not None:
                elapsed = int(time.time() * 1000) - self._started_at
                if elapsed < self._min_total_ms:
                    remaining = self._min_total_ms - elapsed
                    print(f"LoadingScreen.stop: minimum not reached, waiting {remaining}ms")
                    QTimer.singleShot(remaining, self.stop)
                    return
            if self._timer.isActive():
                self._timer.stop()
        except Exception:
            pass
        print("LoadingScreen.stop: closing dialog")
        self.close()
