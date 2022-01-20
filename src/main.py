import sys
from PyQt5.QtWidgets import QApplication
from src.gui.MainWindow import GUIWindow
from src.gui.Survey import Survey


def main(arg):
    app = QApplication(arg)
    #gui = GUIWindow()
    quest = Survey()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
