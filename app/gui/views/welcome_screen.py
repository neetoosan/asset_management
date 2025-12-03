from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
from app.gui.ui.welcome_screen_ui import Ui_WelcomeScreen
from pathlib import Path
from PySide6.QtCore import QEvent, QTimer


class WelcomeScreen(QWidget):
    """Simple welcome screen with an image and a Login button.

    Emits:
        loginRequested: emitted when the user clicks the Login button.
    """
    loginRequested = Signal()

    def __init__(self, parent=None, image_path: str = None):
        super().__init__(parent)
        self.ui = Ui_WelcomeScreen()
        self.ui.setupUi(self)

        # Prepare for pixmap handling and resizing.
        self._pix = None

        # Load image if path provided or fallback to bundled static path
        if image_path is None:
            project_root = Path(__file__).parent.parent.parent
            default_img = project_root / 'static' / 'images' / 'welcome_screen_img.jpg'
            image_path = str(default_img)

        try:
            pix = QPixmap(image_path)
            if not pix.isNull():
                # keep original pixmap and scale when we know the label size
                self._pix = pix
                # update after the widget has been laid out
                QTimer.singleShot(0, self._update_pixmap)
        except Exception:
            # If loading fails, leave the label empty silently
            self._pix = None

        # Install an event filter on the label so we can rescale the image when it resizes
        try:
            self.ui.imageLabel.installEventFilter(self)
        except Exception:
            pass

        # Forward button clicks as a simple signal so callers can show the login screen
        self.ui.loginBtn.clicked.connect(self._on_login_clicked)

    def _on_login_clicked(self):
        try:
            self.loginRequested.emit()
        except Exception:
            pass

    def eventFilter(self, obj, event):
        # Watch for resize events on the image label so we can rescale the pixmap
        try:
            if obj is self.ui.imageLabel and event.type() == QEvent.Resize:
                # update scaled pixmap to fill the label
                self._update_pixmap()
        except Exception:
            pass
        return super().eventFilter(obj, event)

    def _update_pixmap(self):
        """Scale the loaded pixmap so it fills the imageLabel area.

        Uses KeepAspectRatioByExpanding so the image covers the whole label and
        centers the resulting pixmap (cropping may occur to fill).
        """
        if not self._pix:
            return
        try:
            lbl = self.ui.imageLabel
            w = max(1, lbl.width())
            h = max(1, lbl.height())
            scaled = self._pix.scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            lbl.setPixmap(scaled)
            lbl.setAlignment(Qt.AlignCenter)
        except Exception:
            # If something goes wrong, silently ignore to avoid breaking startup
            pass
