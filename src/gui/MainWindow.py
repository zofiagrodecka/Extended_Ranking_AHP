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


class GUIWindow(QWidget):
    def __init__(self):
        super(GUIWindow, self).__init__()
        self.criteria_number = 0
        self.alternative_number = 0
        self.criteria = []
        self.alternatives = []
        self.subcriteria = []
        self.all_criteria = []
        self.AHPCalculator = None
        self.choose_method = 0
        self.choose_methods = []
        self.multiple_experts = False
        self.have_subcriteria = False
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
        self.subtitle_p = QLabel(self)
        self.subtitle_p.setText("Wybierz metodę")
        self.subtitle_p.setStyleSheet("color:black; font-size:15px;text-transform:uppercase; text-align:center;")
        self.subtitle_p.setGeometry(0, 50, 500, 50)
        self.subtitle_p.setAlignment(Qt.AlignCenter)
        self.method = QWidget(self)
        self.method_layout = QHBoxLayout()
        self.choose1 = QRadioButton("EVM")
        self.choose1.toggled.connect(lambda:self.state(self.choose1))
        self.choose2 = QRadioButton("GMM")
        self.choose2.toggled.connect(lambda:self.state(self.choose2))
        self.method_layout.addWidget(self.choose1)
        self.method_layout.addWidget(self.choose2)
        self.method.setLayout(self.method_layout)
        # self.subtitle = QLabel(self)
        # self.subtitle.setText("Wprowadź parametry:")
        # self.subtitle.setStyleSheet("color:black; font-size:15px;text-transform:uppercase; text-align:center;")
        # self.subtitle.setGeometry(0, 50, 500, 50)
        # self.subtitle.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        # self.param = QWidget(self)
        # self.param.setGeometry(0, 100, 500, 150)
        # self.param_layout = QGridLayout()
        # self.param_layout.setColumnStretch(0, 0)
        # self.param_title_1 = QLabel()
        # self.param_title_1.setText("Liczba kryteriów:")
        # self.param_title_1.setGeometry(10, 0, 200, 50)
        # # self.param_title_1.setAlignment(Qt.AlignCenter)
        # self.param_title_2 = QLabel(self.param)
        # self.param_title_2.setText("Liczba alternatyw:")
        # self.param_title_2.setGeometry(10, 20, 200, 50)
        # # self.param_title_2.setAlignment(Qt.AlignCenter)
        # self.param_edit_1 = QLineEdit(self.param)
        # self.param_edit_1.setGeometry(0, 0, 100, 50)
        # self.param_edit_2 = QLineEdit(self.param)
        # self.param_edit_2.setGeometry(0, 0, 100, 50)
        # self.param_layout.addWidget(self.param_title_1, 0, 0)
        # self.param_layout.addWidget(self.param_edit_1, 0, 1)
        # self.param_layout.addWidget(self.param_title_2, 1, 0)
        # self.param_layout.addWidget(self.param_edit_2, 1, 1)
        # self.param.setLayout(self.param_layout)
        self.load = QPushButton("Załaduj plik z danymi", self)
        self.load.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
        self.load.setGeometry(170, 250, 150, 30)
        self.load.clicked.connect(self.load_files)
        self.forward = QPushButton("Dalej", self)
        self.forward.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
        self.forward.setGeometry(170, 270, 150, 30)
        self.forward.clicked.connect(self.processing)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle_p)
        self.layout.addWidget(self.method)
        #self.layout.addWidget(self.subtitle)
        #self.layout.addWidget(self.param)
        self.layout.addWidget(self.load)
        self.layout.addWidget(self.forward)
        self.setLayout(self.layout)
        self.show()

    def load_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        files, types = file_name.getOpenFileNames(self, "Open files", "")
        print(files)
        self.AHPCalculator = AHPCalculator(len(files))
        if len(files) == 1: # not multiple experts
            self.read_file(files[0], 0)
        else:
            self.multiple_experts = True
            for i in range(len(files)):
                self.choose_methods.append(self.choose_method)
                self.read_file(files[i], i)

    def read_file(self, file_name, index):
        """self.criteria_number = int(self.param_edit_1.text())
        self.alternative_number = int(self.param_edit_2.text())
        print("liczba kryterów: ", self.criteria_number)
        print("liczba alternatyw: ", self.alternative_number)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, 'Open File', "")
        if file_name:
            print(file_name)"""
        reader = csv.reader(open(file_name, "rt"), delimiter=";")
        x = list(reader)
        print("X: ", x)
        result = numpy.array(x)
        filtered_criteria = list(filter(None, result[0]))
        self.criteria_number = len(filtered_criteria)
        c = self.criteria_number
        self.criteria = result[0][0:c]
        print("Criteria:", self.criteria)
        subcriteria_number = 0
        self.have_subcriteria = False
        for i in range(1,c+1):
            row = list(filter(None, result[i]))
            if(len(row) == 0):
                row = None
                subcriteria_number = subcriteria_number + 1
                self.all_criteria.append(self.criteria[i-1])
            else:
                subcriteria_number = subcriteria_number + len(row)
                self.have_subcriteria = True
                for j in range(len(row)):
                    self.all_criteria.append(row[j])
            self.subcriteria.append(row)
        print("Subriteria:", self.subcriteria)
        print("All criteria", self.all_criteria)
        filtered_alternatives = list(filter(None, result[c+1]))
        #self.criteria_number = len(filtered_criteria)
        self.alternative_number = len(filtered_alternatives)
        #c = self.criteria_number
        a = self.alternative_number
        l = len(result)
        #self.criteria = result[0][0:c]
        #print("Criteria:", self.criteria)
        self.alternatives = result[c+1][0:a]
        print("Alternatives:", self.alternatives)
        self.AHPCalculator.initialize_alternatives(self.alternative_number, deepcopy(self.alternatives))
        if not self.multiple_experts:
            if self.have_subcriteria:
                self.AHPCalculator.initialize_criteria(len(self.all_criteria), deepcopy(self.all_criteria))
            else:
                self.AHPCalculator.initialize_criteria(len(self.all_criteria), deepcopy(self.all_criteria))
        matrixes = [[]] * subcriteria_number
        beg = c+2
        for i in range(subcriteria_number):
            matrixes[i] = []
            for j in range(a):
                r = result[beg+j][0:a]
                empty_nr = 0
                for x in range(len(r)):
                    if r[x] == '':
                        r[x] = 0
                        empty_nr = empty_nr+1
                        if (self.choose_method == 1):
                            if not self.multiple_experts:
                                self.choose_method = 3
                            else:
                                self.choose_methods[index] = 3
                        elif (self.choose_method == 2):
                            if not self.multiple_experts:
                                self.choose_method = 4
                            else:
                                self.choose_methods[index] = 4
                if(self.choose_method == 1 or self.choose_method == 3):
                    r[j] = empty_nr+1
                matrixes[i].append(r.astype("float"))
            beg = beg + a
            matrixes[i] = numpy.matrix(matrixes[i])
            print("Comparison matrix - criterium ", self.all_criteria[i])
            print(matrixes[i])
            if not self.multiple_experts:
                self.AHPCalculator.append_alternative(deepcopy(matrixes[i]))
            else:
                self.AHPCalculator.append_experts_alternative(deepcopy(matrixes[i]), index)

        if (self.choose_method == 1) and (self.have_subcriteria):
            if not self.multiple_experts:
                self.choose_method = 5
            else:
                self.choose_methods[index] = 5
        elif (self.choose_method == 2) and (self.have_subcriteria):
            if not self.multiple_experts:
                self.choose_method = 6
            else:
                self.choose_methods[index] = 6
        c_beg = beg
        c_end = beg + c
        criteria_comparison = [[]]*c
        for i in range(c):
            r =  result[beg][0:c]
            for x in range(len(r)):
                if r[x] == '':
                    r[x] = 0
            criteria_comparison[i] = r.astype("float")
            beg+=1
        criteria_comparison = numpy.array(criteria_comparison)
        print("Criteria comarison matrix - main")
        print(criteria_comparison)
        if(self.have_subcriteria):
            subcriteria_comparison = [None for _ in range(c)]
            for i in range(c):
                sub_nr = 0
                if self.subcriteria[i] is not None:
                    subcriteria_comparison[i] = []
                    sub_nr = len(self.subcriteria[i])
                    for j in range(sub_nr):
                        r = result[beg][0:sub_nr]
                        for x in range(len(r)):
                            if r[x] == '':
                                r[x] = 0
                        subcriteria_comparison[i].append(r.astype("float"))
                        beg = beg + 1
                #subcriteria_comparison[i] = numpy.matrix(subcriteria_comparison[i])
                print("Subcriteria comparison - criteria: ", self.criteria[i])
                print(subcriteria_comparison[i])
        if not self.multiple_experts:
            self.AHPCalculator.criteria_comparison = deepcopy(criteria_comparison)
        else:
            self.AHPCalculator.append_experts_criteria(deepcopy(criteria_comparison))
        if self.have_subcriteria:
            if not self.multiple_experts:
                self.AHPCalculator.subcriteria_comparison = deepcopy(subcriteria_comparison)
            else:
                self.AHPCalculator.append_experts_subcriteria(deepcopy(subcriteria_comparison))
        print("Criteria comparison:", criteria_comparison)

    def processing(self):
        print("processing")
        total = None
        if not self.multiple_experts:
            print('METOD:', self.choose_method)
            if (self.choose_method == 1) or (self.choose_method == 3):
                total = self.AHPCalculator.run_EVM_method()
            elif (self.choose_method == 2):
                total = self.AHPCalculator.run_GMM_method()
            elif (self.choose_method == 4):
                total = self.AHPCalculator.run_incomplete_GMM_method()
            elif self.choose_method == 5:
                total = self.AHPCalculator.run_subcriteria_evm_method()
            elif self.choose_method == 6:
                total = self.AHPCalculator.run_subcriteria_gmm_method()
        else:
            print("CHOOSE METHODS: ", self.choose_methods)
            for i in range(len(self.choose_methods)):
                method = self.choose_methods[i]
                print(method)
                if method == 1 or method == 3:
                    self.AHPCalculator.multiple_experts_results.append(self.AHPCalculator.run_multiple_experts_EVM_method(i))
                elif method == 2:
                    self.AHPCalculator.multiple_experts_results.append(self.AHPCalculator.run_multiple_experts_GMM_method(i))
                elif method == 4:
                    self.AHPCalculator.multiple_experts_results.append(self.AHPCalculator.run_multiple_experts_incomplete_GMM_method(i))
                elif method == 5:
                    self.AHPCalculator.multiple_experts_results.append(self.AHPCalculator.run_multiple_experts_subcriteria_EVM_method(i))
                elif method == 6:
                    self.AHPCalculator.multiple_experts_results.append(self.AHPCalculator.run_multiple_experts_subcriteria_GMM_method(i))
            total = self.AHPCalculator.synthesize_multiple_experts_result()
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
        #self.layout.itemAt(5).widget().deleteLater()
        #self.layout.itemAt(6).widget().deleteLater()
        sub_message = "Najlepszą opcją jest " + best_choice
        self.subtitle_p.setText(sub_message)

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

    def state(self, b):
        if b.text() == "EVM":
            if b.isChecked() == True:
                self.choose_method = 1
                print(self.choose_method)

        if b.text() == "GMM":
            if b.isChecked() == True:
                self.choose_method = 2
                print(self.choose_method)





