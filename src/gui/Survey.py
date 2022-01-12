from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, \
    QFileDialog, QLineEdit, QSlider, QGridLayout, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import csv
import numpy
from src.app.AHPCalculator import AHPCalculator
from copy import deepcopy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure

class Survey(QWidget):
    def __init__(self):
        super(Survey, self).__init__()
        self.criteria_number = 0
        self.alternative_number = 0
        self.criteria = []
        self.subcriteria = []
        self.allcriteria = []
        self.alternatives = []
        self.initWindow()

    def initWindow(self):
        self.setGeometry(200, 200, 500, 230)
        self.setWindowTitle("AHP-Survey")
        self.setWindowIcon(QIcon('pathology.png'))
        self.setStyleSheet("background-color:#b8b8b8")
        self.title = QLabel(self)
        self.title.setText("Prosta aplikacja licząca ranking AHP")
        self.show()