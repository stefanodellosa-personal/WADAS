import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog

from wadas.ai.models import txt_animalclasses
from wadas.ui.qt.ui_select_animal_species import Ui_DialogSelectAnimalSpecies

module_dir_path = os.path.dirname(os.path.abspath(__file__))

class DialogSelectAnimalSpecies(QDialog,Ui_DialogSelectAnimalSpecies):
    """Class to create a UI dialog to select animal species to run classification on."""
    def __init__(self, parent=None):
        super(DialogSelectAnimalSpecies, self).__init__()
        self.selected_species = None
        self.ui = Ui_DialogSelectAnimalSpecies()

        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))

    def populate_species_dropdown(self):
        """Populate the dropdown with the list of available actuators."""
        self.ui.comboBox_select_species.clear()
        for species in txt_animalclasses["en"]:
            self.ui.comboBox_select_species.addItem(species)

    def accept_and_close(self):
        """When Ok is clicked, save Ai model config info before closing."""
        self.selected_species = self.ui.comboBox_select_species.currentText()