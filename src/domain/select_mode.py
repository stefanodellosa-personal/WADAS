from ui.ui_select_mode import Ui_DialogSelectMode
from PySide6.QtWidgets import QDialog

"""Dialog to select WADAS operating mode."""
class DialogSelectMode(QDialog, Ui_DialogSelectMode):
    def __init__(self):
        super(DialogSelectMode, self).__init__()
        self.ui = Ui_DialogSelectMode()
        self.ui.setupUi(self)
        self.selected_mode = ""
        self.ui.buttonBox.accepted.connect(self.accept_and_close)

    """When Ok is clicked, save radio button selection before closing."""
    def accept_and_close(self):
        if self.ui.radioButton_test_model_mode.isChecked:
            self.selected_mode = "test_model_mode"
        elif self.ui.radioButton_tunnel_mode.isChecked:
            self.selected_mode = "tunnel_mode"
        elif self.ui.radioButton_bear_det_mode.isChecked:
            self.selected_mode = "bear_det_mode"
        self.accept()