import numpy as np


class AHPCalculator:
    def __init__(self, criteria_number, alternative_number, criteria, alternatives):
        self.criteria_number = criteria_number
        self.alternatives_number = alternative_number
        self.criteria_names = criteria
        self.alternatives_names = alternatives
        self.alternative_matrixes = []
        self.criteria_comparison = None
        self.criteria_priorities = []
        self.alternatives_priorities = []

    def append_alternative(self, matrix):
        self.alternative_matrixes.append(np.array(matrix))

    @staticmethod
    def calculate_priority(matrix):
        matrix /= matrix.sum(axis=0)
        print("Po normalizacji:\n", matrix)
        priority = matrix.mean(axis=1)
        print("Priority:", priority)
        return priority

    def calculate_criteria_priorities(self):
        self.criteria_priorities = self.calculate_priority(self.criteria_comparison)

    def calculate_alternatives_priorities(self):
        for matrix in self.alternative_matrixes:
            priority = self.calculate_priority(matrix)
            self.alternatives_priorities.append(priority)
        print(self.alternatives_priorities)

    def synthesize_result(self):
        result = np.array([[None] * self.alternatives_number for _ in range(self.criteria_number)])
        for i in range(self.criteria_number):
            for j in range(self.alternatives_number):
                result[i][j] = self.alternatives_priorities[i][j] * self.criteria_priorities[i]
        return result
