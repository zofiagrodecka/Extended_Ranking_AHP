from copy import deepcopy

from IPython.external.qt_for_kernel import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QToolButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtWidgets
import numpy as np


class ResultsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabele porównań")
        self.display_width = 300
        self.display_height = 500
        self.height = int(self.display_height * 1.3)
        self.width = self.display_width * 2
        self.desktop = QApplication.desktop()
        self.x = (self.desktop.screenGeometry().width() - self.width) // 2
        self.y = (self.desktop.screenGeometry().height() - self.height) // 2
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.title = QLabel()
        self.title.setText("Ekspert 1")
        self.title.setFont(QFont('Times', 12))
        self.table_header = QLabel()
        self.table_header.setText("Kryteria")
        self.table_header.setFont(QFont('Times', 12))
        self.results_header = QLabel()
        self.results_header.setText("Wyniki")
        self.results_header.setFont(QFont('Times', 12))
        self.left_button = QToolButton()
        self.right_button = QToolButton()
        self.left_button.setToolTip('Previous table')
        self.left_button.setArrowType(Qt.LeftArrow)
        self.left_button.clicked.connect(self.left_on_click)
        self.left_button.setDisabled(True)
        self.right_button.setToolTip('Next table')
        self.right_button.setArrowType(Qt.RightArrow)
        self.right_button.clicked.connect(self.right_on_click)
        self.cr_index = QLabel()
        self.cr_index.setText("CR= ")
        self.cr_index.setFont(QFont('Times', 12))
        self.gwi_index = QLabel()
        self.gwi_index.setText("GWI= ")
        self.gwi_index.setFont(QFont('Times', 12))
        self.table_widget = QTableWidget()
        self.buttons = QWidget(self)
        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.layout_widget = None
        self.experts = []
        self.tables = []
        self.table_index = 0
        self.experts_index = 0
        self.subcriteria_index = 0
        self.right_subcriteria = False
        self.left_subcriteria = False
        self.show_subcriteria = False
        self.right_counter = 0
        self.left_counter = 0
        self.main_criteria_names = []

    def add_expert(self, expert):
        self.experts.append(expert)

    def show_experts(self):
        print(len(self.experts[0].criteria_comparison))
        self.create_table(0, self.experts[0])
        self.prepare_layout()

    def setTableSize(self):
        # self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        w = self.table_widget.contentsMargins().left() + self.table_widget.contentsMargins().right() + self.table_widget.verticalHeader().width()
        h = self.table_widget.contentsMargins().top() + self.table_widget.contentsMargins().bottom() + self.table_widget.horizontalHeader().height()
        for i in range(self.table_widget.rowCount()+1):
            h += self.table_widget.rowHeight(i)
        for i in range(self.table_widget.columnCount()+1):
            w += self.table_widget.columnWidth(i)
        self.table_widget.setFixedSize(w, h)

    def create_table(self, index, expert):
        if expert.subcriteria is None:
            if index == 0:  # Porownania kryteriow
                self.table_widget.setRowCount(len(expert.criteria_names))
                self.table_widget.setColumnCount(len(expert.criteria_names)+1)
                self.table_widget.setHorizontalHeaderLabels(expert.criteria_names + ['priorytet'])
                self.table_widget.setVerticalHeaderLabels(expert.criteria_names)
                for w in range(len(expert.criteria_names)):
                    for k in range(len(expert.criteria_names)):
                        self.table_widget.setItem(w, k, QTableWidgetItem(str(round(expert.criteria_comparison[w][k], 2))))
                for w in range(len(expert.criteria_names)):
                    for k in range(len(expert.criteria_names), len(expert.criteria_names)+1):
                        self.table_widget.setItem(w, k, QTableWidgetItem(str(round(expert.criteria_priorities[w], 3))))
            else:  # Porownania alternatyw
                self.table_widget.setRowCount(len(expert.alternatives_names))
                self.table_widget.setColumnCount(len(expert.alternatives_names)+1)
                alternatives_with_priority = expert.alternatives_names.tolist()
                alternatives_with_priority.append('Priorytet')
                self.table_widget.setHorizontalHeaderLabels(alternatives_with_priority)
                self.table_widget.setVerticalHeaderLabels(expert.alternatives_names)
                for w in range(len(expert.alternatives_names)):
                    for k in range(len(expert.alternatives_names)):
                        self.table_widget.setItem(w, k, QTableWidgetItem(str(round(expert.alternatives_comparisons[index-1][w][k], 2))))
                print(expert.alternatives_priorities)
                for w in range(len(expert.alternatives_names)):
                    for k in range(len(expert.alternatives_names), len(expert.alternatives_names)+1):
                        self.table_widget.setItem(w, k, QTableWidgetItem(str(round(expert.alternatives_priorities[self.table_index-1][w], 3))))
        else:
            if self.show_subcriteria:  # Wyswietlam podkryteria
                self.table_widget.setRowCount(len(expert.subcriteria[self.subcriteria_index]))
                self.table_widget.setColumnCount(len(expert.subcriteria[self.subcriteria_index]) + 1)
                labels = expert.criteria_names[self.subcriteria_index:self.subcriteria_index + len(expert.subcriteria[self.subcriteria_index])] + ['priorytet']
                self.table_widget.setHorizontalHeaderLabels(labels)
                self.table_widget.setVerticalHeaderLabels(labels)
                for w in range(len(expert.subcriteria[self.subcriteria_index])):
                    for k in range(len(expert.subcriteria[self.subcriteria_index])):
                        self.table_widget.setItem(w, k,
                                                  QTableWidgetItem(str(round(expert.subcriteria[self.subcriteria_index][w][k], 2))))
                for w in range(len(expert.subcriteria[self.subcriteria_index])):
                    for k in range(len(expert.subcriteria[self.subcriteria_index]), len(expert.subcriteria[self.subcriteria_index]) + 1):
                        self.table_widget.setItem(w, k, QTableWidgetItem(str(round(expert.subcriteria_priorities[self.subcriteria_index][w], 3))))
            elif index == 0:  # Porownania kryteriow
                self.table_widget.setRowCount(len(expert.subcriteria))
                self.table_widget.setColumnCount(len(expert.subcriteria) + 1)
                counter = 0
                self.main_criteria_names = []
                print(expert.subcriteria)
                for i in range(len(expert.subcriteria)):
                    if expert.subcriteria[i] is None:
                        self.main_criteria_names.append(expert.criteria_names[counter])
                        counter += 1
                    else:
                        matrix = expert.subcriteria[i]
                        merged_str = deepcopy(expert.criteria_names[counter])
                        for j in range(counter+1, counter+len(matrix)):
                            merged_str += "\n" + expert.criteria_names[j]
                        self.main_criteria_names.append(deepcopy(merged_str))
                        counter += len(matrix)
                self.table_widget.setHorizontalHeaderLabels(self.main_criteria_names + ['priorytet'])
                self.table_widget.setVerticalHeaderLabels(self.main_criteria_names)
                for w in range(len(self.main_criteria_names)):
                    for k in range(len(self.main_criteria_names)):
                        self.table_widget.setItem(w, k,
                                                  QTableWidgetItem(str(round(expert.criteria_comparison[w][k], 2))))
                for w in range(len(self.main_criteria_names)):
                    for k in range(len(self.main_criteria_names), len(self.main_criteria_names) + 1):
                        self.table_widget.setItem(w, k, QTableWidgetItem(str(round(expert.criteria_priorities[w], 3))))
                self.show_subcriteria = True
                self.subcriteria_index = 0
            else:
                self.table_widget.setRowCount(len(expert.alternatives_names))
                self.table_widget.setColumnCount(len(expert.alternatives_names) + 1)
                alternatives_with_priority = expert.alternatives_names.tolist()
                alternatives_with_priority.append('Priorytet')
                self.table_widget.setHorizontalHeaderLabels(alternatives_with_priority)
                self.table_widget.setVerticalHeaderLabels(expert.alternatives_names)
                for w in range(len(expert.alternatives_names)):
                    for k in range(len(expert.alternatives_names)):
                        self.table_widget.setItem(w, k, QTableWidgetItem(
                            str(round(expert.alternatives_comparisons[index - 1][w][k], 2))))
                print(expert.alternatives_priorities)
                for w in range(len(expert.alternatives_names)):
                    for k in range(len(expert.alternatives_names), len(expert.alternatives_names) + 1):
                        self.table_widget.setItem(w, k, QTableWidgetItem(
                            str(round(expert.alternatives_priorities[self.table_index - 1][w], 3))))
        self.setTableSize()
        #self.layout.addWidget(self.table_widget, 2, 0, 4, 2, Qt.AlignCenter)
        #self.setLayout(self.layout)

    def prepare_layout(self):
        # self.layout.addWidget(self.title, 0, 0, 1, 4, Qt.AlignCenter)
        # self.layout.addWidget(self.table_header, 1, 0, 1, 4, Qt.AlignCenter)
        # self.layout.addWidget(self.table_widget, 2, 0, 1, 4, Qt.AlignCenter)
        # self.layout.addWidget(self.left_button, 3, 0, 1, 2, Qt.AlignRight)
        # self.layout.addWidget(self.right_button, 3, 2, 1, 2, Qt.AlignLeft)
        self.buttons_layout.addWidget(self.left_button)
        self.buttons_layout.addWidget(self.right_button)
        self.buttons.setLayout(self.buttons_layout)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.table_header)
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.buttons)
        self.layout.addWidget(self.cr_index)
        self.layout.addWidget(self.gwi_index)
        self.setLayout(self.layout)

    def left_on_click(self):
        if self.experts[self.experts_index].subcriteria is not None and self.left_counter == 0 and self.table_index == 1:
            self.show_subcriteria = True
            self.subcriteria_index = len(self.experts[self.experts_index].subcriteria)
            self.left_counter += 1
        if not self.show_subcriteria:
            self.table_index -= 1
            if self.table_index < 0 and self.experts_index - 1 >= 0:
                self.experts_index -= 1
                self.table_index = len(self.experts[self.experts_index].alternatives_comparisons)
                self.left_button.setDisabled(False)
                self.right_counter = 0
                self.title.setText("Ekspert " + str(self.experts_index + 1))
                if self.table_index == 0:
                    self.table_header.setText("Kryteria")
                else:
                    self.table_header.setText(self.experts[self.experts_index].criteria_names[self.table_index-1])
            elif self.table_index < 0 and self.experts_index - 1 < 0:
                self.table_index += 1
            else:
                self.left_button.setDisabled(False)
                if self.table_index == 0:
                    self.table_header.setText("Kryteria")
                else:
                    self.table_header.setText(self.experts[self.experts_index].criteria_names[self.table_index - 1])

            if self.table_index == 0 and self.experts_index == 0:
                self.left_button.setDisabled(True)

            if self.table_index <= len(self.experts[self.experts_index].alternatives_names):
                self.right_button.setDisabled(False)
        else:
            self.subcriteria_index -= 1
            while self.subcriteria_index >= 0 and self.experts[self.experts_index].subcriteria[self.subcriteria_index] is None:
                self.subcriteria_index -= 1
            if self.subcriteria_index < 0:
                self.show_subcriteria = False
                self.left_on_click()
                return
            else:
                self.table_header.setText(self.main_criteria_names[self.subcriteria_index])
        self.create_table(self.table_index, self.experts[self.experts_index])

    def right_on_click(self):
        if self.experts[self.experts_index].subcriteria is not None and self.table_index == 0 and self.right_counter == 0:
            self.show_subcriteria = True
            self.right_counter += 1
        if not self.show_subcriteria:
            self.table_index += 1
            print(self.table_index)
            if self.table_index > len(self.experts[self.experts_index].alternatives_comparisons) and self.experts_index + 1 < len(self.experts):
                self.experts_index += 1
                self.table_index = 0
                self.right_button.setDisabled(False)
                self.title.setText("Ekspert " + str(self.experts_index + 1))
                self.table_header.setText("Kryteria")
                self.left_counter = 0
            elif self.table_index > len(self.experts[self.experts_index].alternatives_comparisons) and self.experts_index + 1 >= len(self.experts):
                self.table_index -= 1
            else:
                self.table_header.setText(self.experts[self.experts_index].criteria_names[self.table_index - 1])
                self.right_button.setDisabled(False)

            if self.table_index == 1:
                self.left_counter = 0

            if self.table_index == len(self.experts[self.experts_index].alternatives_comparisons) and self.experts_index == len(self.experts) - 1:
                self.right_button.setDisabled(True)

            if self.table_index > 0:
                self.left_button.setDisabled(False)
        else:
            self.subcriteria_index += 1
            while self.subcriteria_index < len(self.experts[self.experts_index].subcriteria) and self.experts[self.experts_index].subcriteria[self.subcriteria_index] is None:
                self.subcriteria_index += 1

            if self.subcriteria_index >= len(self.experts[self.experts_index].subcriteria):
                self.show_subcriteria = False
                self.right_on_click()
                return
            else:
                self.table_header.setText(self.main_criteria_names[self.subcriteria_index])
            self.left_button.setDisabled(False)
        self.create_table(self.table_index, self.experts[self.experts_index])
        return
