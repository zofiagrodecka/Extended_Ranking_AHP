from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, \
    QFileDialog, QLineEdit, QSlider, QGridLayout, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import csv
import numpy
import random
from src.app.AHPCalculator import AHPCalculator
from copy import deepcopy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure

from src.gui.MainWindow import GUIWindow


class Survey(QWidget):
    def __init__(self):
        super(Survey, self).__init__()
        self.criteria_number = 0
        self.alternative_number = 0
        self.criteria = []
        self.subcriteria = []
        self.all_criteria = []
        self.alternatives = []
        self.comparison_matrix = []
        self.have_subcriteria = False
        self.criteria_done = 0
        self.questions_todo = 0
        self.questions_done = 0
        self.question_list = None
        self.subcriteria_number = 0
        self.initWindow()

    def initWindow(self):
        self.setGeometry(200, 200, 500, 90)
        self.setWindowTitle("AHP-Survey")
        self.setWindowIcon(QIcon('pathology.png'))
        self.setStyleSheet("background-color:#b8b8b8")
        self.title = QLabel(self)
        self.title.setText("Prosta aplikacja licząca ranking AHP")
        self.title.setStyleSheet("color:black; font-size:20px;text-transform:uppercase; text-align:center;")
        self.title.setGeometry(0, 10, 500, 50)
        self.title.setAlignment(Qt.AlignCenter)
        self.create = QPushButton("Otwórz nową ankietę", self)
        self.create.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
        self.create.setGeometry(170, 250, 150, 30)
        self.create.clicked.connect(self.create_file)
        self.calculate = QPushButton("Oblicz ranking", self)
        self.calculate.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
        self.calculate.setGeometry(170, 250, 150, 30)
        self.calculate.clicked.connect(self.calculate_AHP)
        self.layout = QVBoxLayout()
        #self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.create)
        self.layout.addWidget(self.calculate)
        self.setLayout(self.layout)
        self.show()

    def create_file(self):
        self.layout.itemAt(2).widget().deleteLater()
        self.layout.itemAt(1).widget().deleteLater()
        self.load = QPushButton("załaduj plik z ankietą", self)
        self.load.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
        self.load.setGeometry(170, 270, 150, 30)
        self.load.move(0, 40)
        self.load.clicked.connect(self.load_file)
        self.layout.addWidget(self.load)

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, 'Open File', "")
        if file_name[0] and file_name[0] != '':
            self.read_file(file_name[0])

    def read_file(self, file_name):
        reader = csv.reader(open(file_name, "rt"), delimiter=";")
        x = list(reader)
        result = numpy.array(x)
        self.result = result
        filtered_criteria = list(filter(None, result[0]))
        self.criteria_number = len(filtered_criteria)
        c = self.criteria_number
        self.criteria = result[0][0:c]
        print("Criteria:", self.criteria)
        subcriteria_number = 0
        for i in range(1, c + 1):
            row = list(filter(None, result[i]))
            print(row)
            if (len(row) == 0):
                row = None
                subcriteria_number = subcriteria_number + 1
                self.all_criteria.append(self.criteria[i - 1])
            else:
                subcriteria_number = subcriteria_number + len(row)
                self.have_subcriteria = True
                for j in range(len(row)):
                    self.all_criteria.append(row[j])
            self.subcriteria.append(row)
        print("Subriteria:", self.subcriteria)
        print("All criteria", self.all_criteria)
        filtered_alternatives = list(filter(None, result[c + 1]))
        self.alternative_number = len(filtered_alternatives)
        a = self.alternative_number
        l = len(result)
        self.alternatives = result[c + 1][0:a]
        print("Alternatives:", self.alternatives)
        self.questions_todo = self.alternative_number * (self.alternative_number - 1) / 2
        self.subcriteria_number = len(self.all_criteria)
        for i in range(self.subcriteria_number):
            m = [['' for i in range(self.alternative_number)] for j in range(self.alternative_number)]
            for x in range(self.alternative_number):
                m[x][x] = 1
            self.comparison_matrix.append(m)
        print(self.comparison_matrix)
        self.layout.itemAt(1).widget().deleteLater()
        self.start = QPushButton("rozpocznij ankietę", self)
        self.start.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
        self.start.setGeometry(170, 250, 150, 30)
        self.start.clicked.connect(self.next)
        self.layout.addWidget(self.start)

    def next(self):
        if (self.criteria_done == self.subcriteria_number):
            print(self.line_which.text())
            print(self.line_num.text())
            if (self.line_which.text() == self.alternatives[self.x]):
                num = int(self.line_num.text())
                print(num)
                self.comparison_matrix[self.criteria_done - 1][self.x][self.y] = num
                self.comparison_matrix[self.criteria_done - 1][self.y][self.x] = 1 / num
                print(self.comparison_matrix[self.criteria_done - 1][self.x][self.y])
            elif (self.line_which.text() == self.alternatives[self.y]):
                num = int(self.line_num.text())
                print(num)
                self.comparison_matrix[self.criteria_done - 1][self.y][self.x] = num
                self.comparison_matrix[self.criteria_done - 1][self.x][self.y] = 1 / num
                print(self.comparison_matrix[self.criteria_done - 1][self.x][self.y])
            else:
                print("NayNay")
            self.layout.itemAt(1).widget().deleteLater()
            self.layout.itemAt(2).widget().deleteLater()
            self.layout.itemAt(3).widget().deleteLater()
            self.layout.itemAt(4).widget().deleteLater()
            self.layout.itemAt(5).widget().deleteLater()
            self.layout.itemAt(6).widget().deleteLater()
            self.layout.itemAt(7).widget().deleteLater()
            self.end_message = QLabel(self)
            self.end_message.setText("Koniec ankiety")
            self.end_message.setStyleSheet("color:black; font-size:15px;text-transform:uppercase; text-align:center;")
            self.end_message.setGeometry(0, 50, 500, 50)
            self.end_message.setAlignment(Qt.AlignCenter)
            self.name_file = QLabel("wprowadź ścieżkę i nazwę dla pliku:")
            self.new_file = QLineEdit()
            self.save_button = QPushButton("zapisz plik", self)
            self.save_button.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
            self.save_button.setGeometry(170, 250, 150, 30)
            self.save_button.clicked.connect(self.save_file)
            self.layout.addWidget(self.end_message)
            self.layout.addWidget(self.name_file)
            self.layout.addWidget(self.new_file)
            self.layout.addWidget(self.save_button)
            print(self.comparison_matrix)
        elif (self.criteria_done == 0 and self.questions_done == 0):
            self.layout.itemAt(1).widget().deleteLater()
            self.questions_list = self.comparison_list()
            self.crit_label = QLabel(self)
            self.crit_label.setText("Kryterium " + self.all_criteria[self.criteria_done])
            self.crit_label.setStyleSheet("color:black; font-size:15px;text-transform:uppercase; text-align:center;")
            self.crit_label.setGeometry(0, 50, 500, 50)
            self.crit_label.setAlignment(Qt.AlignCenter)
            self.ques_label = QLabel(self)
            self.x = self.questions_list[self.questions_done][0]
            self.y = self.questions_list[self.questions_done][1]
            self.ques_label.setText(
                "W skali od 1-9 którą opcję Pan/Pani preferuje: " + self.alternatives[self.x] + " czy " +
                self.alternatives[self.y] + "?")
            self.ques_label.setStyleSheet("color:black; font-size:15px;text-align:center;")
            self.ques_label.setGeometry(0, 50, 500, 50)
            self.ques_label.setAlignment(Qt.AlignCenter)
            self.next_button = QPushButton("dalej", self)
            self.next_button.setStyleSheet("background:#3f3f3f; color:#d1d1d1; text-transform:uppercase;")
            self.next_button.setGeometry(170, 250, 150, 30)
            self.next_button.clicked.connect(self.next)
            self.line_which = QLineEdit()
            self.line_num = QLineEdit()
            self.option = QLabel("opcja", self)
            self.score = QLabel("ocena", self)
            self.layout.addWidget(self.crit_label)
            self.layout.addWidget(self.ques_label)
            #self.layout.addWidget(self.next_button)
            self.layout.addWidget(self.option)
            self.layout.addWidget(self.line_which)
            self.layout.addWidget(self.score)
            self.layout.addWidget(self.line_num)
            self.layout.addWidget(self.next_button)
            self.questions_done = self.questions_done + 1
            if (self.questions_done == self.questions_todo):
                self.questions_done = 0
                self.criteria_done = self.criteria_done + 1
        elif (self.questions_done == 0):
            print(self.line_which.text())
            print(self.line_num.text())
            if (self.line_which.text() == self.alternatives[self.x]):
                num = int(self.line_num.text())
                print(num)
                self.comparison_matrix[self.criteria_done - 1][self.x][self.y] = num
                self.comparison_matrix[self.criteria_done - 1][self.y][self.x] = 1 / num
                print(self.comparison_matrix[self.criteria_done - 1][self.x][self.y])
            elif (self.line_which.text() == self.alternatives[self.y]):
                num = int(self.line_num.text())
                print(num)
                self.comparison_matrix[self.criteria_done - 1][self.y][self.x] = num
                self.comparison_matrix[self.criteria_done - 1][self.x][self.y] = 1 / num
                print(self.comparison_matrix[self.criteria_done - 1][self.x][self.y])
            else:
                print("NayNay")
            self.line_which.setText("")
            self.line_num.setText("")
            self.questions_list = self.comparison_list()
            self.crit_label.setText("Kryterium " + self.all_criteria[self.criteria_done])
            self.x = self.questions_list[self.questions_done][0]
            self.y = self.questions_list[self.questions_done][1]
            self.ques_label.setText(
                "W skali od 1-9 którą opcję Pan/Pani preferuje: " + self.alternatives[self.x] + " czy " +
                self.alternatives[self.y] + "?")
            self.questions_done = self.questions_done + 1
            if (self.questions_done == self.questions_todo):
                self.questions_done = 0
                self.criteria_done = self.criteria_done + 1
        else:
            print(self.line_which.text())
            print(self.line_num.text())
            if (self.line_which.text() == self.alternatives[self.x]):
                num = int(self.line_num.text())
                print(num)
                self.comparison_matrix[self.criteria_done][self.x][self.y] = num
                self.comparison_matrix[self.criteria_done][self.y][self.x] = 1 / num
                print(self.comparison_matrix[self.criteria_done][self.x][self.y])
            elif (self.line_which.text() == self.alternatives[self.y]):
                num = int(self.line_num.text())
                print(num)
                self.comparison_matrix[self.criteria_done][self.y][self.x] = num
                self.comparison_matrix[self.criteria_done][self.x][self.y] = 1 / num
                print(self.comparison_matrix[self.criteria_done][self.x][self.y])
            else:
                print("NayNay")
            self.line_which.setText("")
            self.line_num.setText("")
            self.x = self.questions_list[self.questions_done][0]
            self.y = self.questions_list[self.questions_done][1]
            self.ques_label.setText(
                "W skali od 1-9 którą opcję Pan/Pani preferuje: " + self.alternatives[self.x] + " czy " +
                self.alternatives[
                    self.y] + "?")
            self.questions_done = self.questions_done + 1
            if (self.questions_done == self.questions_todo):
                self.questions_done = 0
                self.criteria_done = self.criteria_done + 1

    def save_file(self):
        print("save")
        f = open(self.new_file.text() + ".csv", 'w', encoding='UTF8', newline='')
        writer = csv.writer(f, delimiter=';')
        l = len(self.result)
        for i in range(self.criteria_number + 2):
            writer.writerow(self.result[i])
        for i in range(self.subcriteria_number):
            matrix = self.comparison_matrix[i]
            writer.writerows(matrix)
        for i in range(self.criteria_number + 2, l):
            writer.writerow(self.result[i])
        f.close()
        self.layout.itemAt(1).widget().deleteLater()
        self.layout.itemAt(2).widget().deleteLater()
        self.layout.itemAt(3).widget().deleteLater()
        self.layout.itemAt(4).widget().deleteLater()
        self.message = QLabel(self)
        self.message.setText("Plik został zapisany")
        self.message.setGeometry(0, 50, 500, 50)
        self.message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.message)

    def comparison_list(self):
        alt_comp = [[0 for i in range(self.alternative_number)] for j in range(self.alternative_number)]
        for i in range(self.alternative_number):
            for j in range(self.alternative_number):
                if (i >= j):
                    alt_comp[i][j] = 1
        max_p = self.alternative_number * (self.alternative_number - 1) / 2
        p = 0
        list = []
        while p < max_p:
            x = random.randint(0, self.alternative_number - 1)
            y = random.randint(0, self.alternative_number - 1)
            # print(x)
            # print(y)
            if (alt_comp[x][y] != 1):
                new = [x, y]
                list.append(new)
                p = p + 1
                alt_comp[x][y] = 1
        print(list)
        return list

    def calculate_AHP(self):
        self.gui = GUIWindow()
