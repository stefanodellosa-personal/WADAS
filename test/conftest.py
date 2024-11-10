import getpass
import pathlib
import sys

# Add the wadas directory to the sys.path in order to be able to import the modules.
__this_dir = pathlib.Path(__file__).absolute().parent
sys.path.append(str(__this_dir.parent))

if getpass.getuser() == "Cesare":  # Hack to mock PySide6 when running tests on Cesare's PC.

    class QObject:
        pass

    class Signal:
        def __init__(self, *args, **kwargs):
            pass

    pyside6 = type(sys)("PySide6")
    sys.modules["PySide6"] = pyside6
    pyside6.qtcore = qtcore = type(sys)("QtCore")
    sys.modules["PySide6.QtCore"] = qtcore
    qtcore.QObject = QObject
    qtcore.Signal = Signal
