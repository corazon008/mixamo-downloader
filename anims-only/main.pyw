# Third-party modules
import os
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"

from PySide2 import QtWidgets

# Local modules
from ui import MixamoDownloaderUI


if __name__ == "__main__":

    app = QtWidgets.QApplication([])

    md = MixamoDownloaderUI()
    md.show()

    app.exec_()
