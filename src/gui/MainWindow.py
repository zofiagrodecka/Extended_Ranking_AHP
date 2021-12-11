from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, \
    QFileDialog, QLineEdit, QSlider, QGridLayout
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


class GUIWindow(QWidget):
    def __init__(self):
        super(GUIWindow, self).__init__()
        self.criteria_number = 0
        self.alternative_number = 0
        self.criteria = []
        self.alternatives = []
        self.AHPCalculator = None
        self.initGUI()

    def initGUI(self):
        self.setGeometry(200, 200, 500, 230)
        self.setWindowTitle("AHP-Ranking")
        self.setWindowIcon(QIcon('pathology.png'))
        self.setStyleSheet("background-color:#b8b8b8")
        self.title = QLabel(self)
        self.title.setText("Prosta aplikacja licząca ranking AHP")
        self.title.setStyleSheet("color:black; font-size:20px;text-transform:uppercase; text-align:center;")
        self.title.setGeometry(0, 10, 500, 50)
        self.title.setAlignment(Qt.AlignCenter)
        self.subtitle = QLabel(self)
        self.subtitle.setText("Wprowadź parametry:")
        self.subtitle.setStyleSheet("color:black; font-size:15px;text-transform:uppercase; text-align:center;")
        self.subtitle.setGeometry(0, 50, 500, 50)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.param = QWidget(self)
        self.param.setGeometry(0, 100, 500, 150)
        self.param_layout = QGridLayout()
        self.param_layout.setColumnStretch(0, 0)
        self.param_title_1 = QLabel()
        self.param_title_1.setText("Liczba kryteriów:")
        self.param_title_1.setGeometry(10, 0, 200, 50)
        # self.param_title_1.setAlignment(Qt.AlignCenter)
        self.param_title_2 = QLabel(self.param)
        self.param_title_2.setText("Liczba alternatyw:")
        self.param_title_2.setGeometry(10, 20, 200, 50)
        # self.param_title_2.setAlignment(Qt.AlignCenter)
        self.param_edit_1 = QLineEdit(self.param)
        self.param_edit_1.setGeometry(0, 0, 100, 50)
        self.param_edit_2 = QLineEdit(self.param)
        self.param_edit_2.setGeometry(0, 0, 100, 50)
        self.param_layout.addWidget(self.param_title_1, 0, 0)
        self.param_layout.addWidget(self.param_edit_1, 0, 1)
        self.param_layout.addWidget(self.param_title_2, 1, 0)
        self.param_layout.addWidget(self.param_edit_2, 1, 1)
        self.param.setLayout(self.param_layout)
        self.load = QPushButton("Załaduj plik z danymi", self)
        self.load.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
        self.load.setGeometry(170, 250, 150, 30)
        self.load.clicked.connect(self.read_file)
        self.forward = QPushButton("Dalej", self)
        self.forward.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
        self.forward.setGeometry(170, 270, 150, 30)
        self.forward.clicked.connect(self.processing)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.param)
        self.layout.addWidget(self.load)
        self.layout.addWidget(self.forward)
        self.setLayout(self.layout)
        self.show()

    def read_file(self):
        self.criteria_number = int(self.param_edit_1.text())
        self.alternative_number = int(self.param_edit_2.text())
        print("liczba kryterów: ", self.criteria_number)
        print("liczba alternatyw: ", self.alternative_number)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, 'Open File', "")
        if file_name:
            print(file_name)
        reader = csv.reader(open(file_name[0], "rt"), delimiter=";")
        x = list(reader)
        result = numpy.array(x)
        print(result)
        c = self.criteria_number
        a = self.alternative_number
        l = len(result)
        self.criteria = result[0][0:c]
        print("Criteria:", self.criteria)
        self.alternatives = result[1][0:a]
        print("Alternatives:", self.alternatives)
        self.AHPCalculator = AHPCalculator(self.criteria_number, self.alternative_number, deepcopy(self.criteria), deepcopy(self.alternatives))
        matrixes = [[]] * c
        beg = 2
        for i in range(c):
            #matrixes[i] = result[beg:beg + a].astype("float")
            matrixes[i] = []
            for j in range(a):
                matrixes[i].append(result[beg+j][0:a].astype("float"))
            beg = beg + a
            print(matrixes[i])
            self.AHPCalculator.append_alternative(deepcopy(matrixes[i]))
        c_beg = l - c
        c_end = l
        criteria_comparison = [[]]*c
        for i in range(c):
            criteria_comparison[i] = result[c_beg][0:c].astype("float")
            c_beg+=1
        criteria_comparison = numpy.array(criteria_comparison)
        self.AHPCalculator.criteria_comparison = deepcopy(criteria_comparison)
        print("Criteria comparison:", criteria_comparison)

    def processing(self):
        print("processing")
        # print(self.AHPCalculator.alternative_matrixes)
        self.AHPCalculator.calculate_alternatives_priorities()
        self.AHPCalculator.calculate_criteria_priorities()
        result = self.AHPCalculator.synthesize_result()
        for i in range(self.criteria_number):
            print(result[i])
        total = result.sum(axis=0)
        print("Total:", total)
        best_choice = self.AHPCalculator.alternatives_names[numpy.argmax(total)]
        print("The best choice is:", best_choice)

        # Plot
        ax_x = []
        for i in range(self.alternative_number):
            ax_x.append(i)
        self.figure = plt.figure()
        objects = self.AHPCalculator.alternatives_names
        y_pos = numpy.arange(self.alternative_number)
        self.plot = self.figure.add_subplot(111)
        self.plot.bar(y_pos, total)
        self.plot.set_xticks(ax_x)
        self.plot.set_xticklabels(self.alternatives)
        self.plot.set_ylabel('Priorytet')
        self.plot.set_title('Ranking AHP domów w okolicy Krakowa')
        #self.plot.show()

        self.setGeometry(200, 200, 800, 500)
        self.layout.itemAt(2).widget().deleteLater()
        self.layout.itemAt(3).widget().deleteLater()
        self.layout.itemAt(4).widget().deleteLater()
        sub_message = "Najlepszą opcją jest " + best_choice
        self.subtitle.setText(sub_message)

        sorted_alternatives = []
        result_copy = deepcopy(total)

        for i in range(self.alternative_number):
            index = numpy.argmax(result_copy)
            sorted_alternatives.append(self.alternatives[index])
            result_copy[index] = -1

        print(sorted_alternatives)

        self.bottom = QWidget(self)
        self.b_layout = QHBoxLayout(self.bottom)
        self.rank_widget = QWidget(self.bottom)
        self.rank_layout = QVBoxLayout(self.rank_widget)
        title_label = QLabel(self.rank_widget)
        title_label.setText("Ranking alternatyw: ")
        self.rank_layout.addWidget(title_label)
        for i in range(self.alternative_number):
            label = QLabel(self.rank_widget)
            mes = str(i+1) + ". " + sorted_alternatives[i]
            label.setText(mes)
            self.rank_layout.addWidget(label)
        self.rank_layout.setAlignment(Qt.AlignTop)
        self.rank_widget.setLayout(self.rank_layout)
        self.b_layout.addWidget(self.rank_widget)

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.b_layout.addWidget(self.canvas)
        self.bottom.setLayout(self.b_layout)
        self.layout.addWidget(self.bottom)






