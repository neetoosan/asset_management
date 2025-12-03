from PySide6.QtWidgets import QDialog
from ..ui.asset_delete_reason_ui import Ui_AssetDeleteReason

class AssetDeleteReasonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AssetDeleteReason()
        self.ui.setupUi(self)
        self.ui.okBtn.clicked.connect(self.accept)
        self.ui.cancelBtn.clicked.connect(self.reject)

    def get_reason(self) -> str:
        return self.ui.reasonEdit.toPlainText().strip()
