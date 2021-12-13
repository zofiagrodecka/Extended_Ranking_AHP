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
    def calculate_evm_priority(matrix):
        matrix /= matrix.sum(axis=0)
        print("Po normalizacji:\n", matrix)
        priority = matrix.mean(axis=1)
        print("Priority:", priority)
        return priority

    def calculate_evm_criteria_priorities(self):
        self.criteria_priorities = self.calculate_evm_priority(self.criteria_comparison)

    def calculate_evm_alternatives_priorities(self):
        for matrix in self.alternative_matrixes:
            priority = self.calculate_evm_priority(matrix)
            self.alternatives_priorities.append(priority)
        print(self.alternatives_priorities)

    def synthesize_result(self):
        result = np.array([[None] * self.alternatives_number for _ in range(self.criteria_number)])
        for i in range(self.criteria_number):
            for j in range(self.alternatives_number):
                result[i][j] = self.alternatives_priorities[i][j] * self.criteria_priorities[i]
        return result

    def run_EVM_method(self):
        self.calculate_evm_alternatives_priorities()
        self.calculate_evm_criteria_priorities()
        result = self.synthesize_result()
        for i in range(self.criteria_number):
            print(result[i])
        total = result.sum(axis=0)
        return total

    @staticmethod
    def calculate_gmm_priority(matrix):
        priority = np.prod(matrix, axis=1)
        priority = np.power(priority, 1/len(matrix))
        s = np.sum(priority)
        priority /= s  # normalization
        print("Priority:", priority)
        return priority

    def calculate_gmm_criteria_priorities(self):
        self.criteria_priorities = self.calculate_gmm_priority(self.criteria_comparison)
        print(self.criteria_comparison)

    def calculate_gmm_alternatives_priorities(self):
        for matrix in self.alternative_matrixes:
            priority = self.calculate_gmm_priority(matrix)
            self.alternatives_priorities.append(priority)
        print(self.alternatives_priorities)

    def run_GMM_method(self):
        self.calculate_gmm_alternatives_priorities()
        self.calculate_gmm_criteria_priorities()
        result = self.synthesize_result()
        for i in range(self.criteria_number):
            print(result[i])
        total = result.sum(axis=0)
        return total
