import copy
import numpy as np


class AHPCalculator:
    def __init__(self, experts_number):
        self.criteria_number = None
        self.alternatives_number = None
        self.criteria_names = None
        self.alternatives_names = None
        self.alternative_matrixes = []
        self.criteria_comparison = None
        self.criteria_priorities = []
        self.alternatives_priorities = []
        self.ri = [0, 0, 0, 0.52, 0.89, 1.11, 1.25, 1.35, 1.40, 1.45, 1.49, 1.51, 1.54, 1.56, 1.57, 1.58]
        self.experts_number = experts_number
        self.multiple_experts_criteria = []
        self.multiple_experts_alternatives = [[] for _ in range(self.experts_number)]
        self.multiple_experts_subcriteria = []
        self.multiple_experts_results = []
        self.subcriteria_comparison = None
        self.subcriteria_priorities = []

    def initialize_alternatives(self, alternatives_number, alternatives):
        self.alternatives_names = alternatives
        self.alternatives_number = alternatives_number

    def initialize_criteria(self, criteria_number, criteria):
        self.criteria_number = criteria_number
        self.criteria_names = criteria

    def append_alternative(self, matrix):
        self.alternative_matrixes.append(np.array(matrix))

    def append_experts_alternative(self, matrix, index):
        self.multiple_experts_alternatives[index].append(np.array(matrix))

    def append_experts_criteria(self, matrix):
        self.multiple_experts_criteria.append(np.array(matrix))

    def append_experts_subcriteria(self, matrix):
        self.multiple_experts_subcriteria.append(matrix)

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
        print('Syntesis result:', result)
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
        print(matrix)
        priority = np.prod(matrix, axis=1)
        priority = np.power(priority, 1/len(matrix))
        s = np.sum(priority)
        priority /= s  # normalization
        print("Priority:", priority)
        return priority

    def calculate_gmm_criteria_priorities(self):
        self.criteria_priorities = self.calculate_gmm_priority(self.criteria_comparison)
        print('criteria priorities' , self.criteria_priorities)

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

    def calculate_inc_gmm_criteria_priorities(self):
        l = len(self.criteria_comparison)
        G = np.zeros((l,l))
        r = np.zeros(l)
        for i in range(l):
            s = 0
            for x in range(l):
                if self.criteria_comparison[i][x] == 0:
                    s = s + 1
            lnc = 0
            for j in range(l):
                if self.criteria_comparison[i][j] == 0 and i != j:
                    G[i][j] = 1
                elif self.criteria_comparison[i][j] != 0 and i != j:
                    G[i][j] = 0
                    lnc = lnc + np.log(self.criteria_comparison[i][j])
                elif i == j:
                    G[i][j] = l - s
            r[i] = lnc
        W = np.linalg.inv(G).dot(r)
        w = np.zeros(len(W))
        sum_w = 0
        for e in range(len(W)):
            w[e] = np.exp(W[e])
            sum_w = sum_w + w[e]
        for e in range(len(w)):
            w[e] = w[e] / sum_w
        self.criteria_priorities = w

    def calculate_inc_gmm_alternatives_priorities(self):
        for matrix in self.alternative_matrixes:
            l = len(matrix)
            #print(l)
            G = np.zeros((l, l))
            # print(G)
            r = np.zeros(l)
            # print(r)
            for i in range(l):
                s = 0
                for x in range(l):
                    if matrix[i][x] == 0:
                        s = s +1
                #print(s)
                lnc = 0
                for j in range(l):
                    if matrix[i][j] == 0 and i != j:
                        G[i][j] = 1
                    elif matrix[i][j] != 0  and i!=j:
                        G[i][j] = 0
                        lnc = lnc + np.log(matrix[i][j])
                    elif i == j:
                        G[i][j] = l - s
                r[i] = lnc
            #print(G)
            #print(r)
            W = np.linalg.inv(G).dot(r)
            #print(W)
            w = np.zeros(len(W))
            sum_w = 0
            for e in range(len(W)):
                w[e] = np.exp(W[e])
                sum_w = sum_w + w[e]
            for e in range(len(w)):
                w[e] = w[e]/sum_w
            #print(w)
            self.alternatives_priorities.append(w)
        print(self.alternatives_priorities)

    def run_incomplete_GMM_method(self):
        self.calculate_inc_gmm_alternatives_priorities()
        self.calculate_inc_gmm_criteria_priorities()
        result = self.synthesize_result()
        for i in range(self.criteria_number):
            print(result[i])
        total = result.sum(axis=0)
        return total

    def count_CR(self, matrix):
        n = len(matrix)
        eigvals, eigvecs = np.linalg.eig(matrix)
        eigvals = eigvals.real
        max_eig = np.max(eigvals)
        CI = (max_eig - n)/n-1
        RI = self.ri[n]
        CR = CI/RI
        return CR

    def count_GWI(self, matrix, priority):
        res = 0
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                res += abs(matrix[i][j] - priority[i])
        return res

    def run_multiple_experts_EVM_method(self, i):  # metoda AIP
        self.criteria_number = len(self.multiple_experts_criteria[i])
        self.alternative_matrixes = self.multiple_experts_alternatives[i]
        self.criteria_comparison = self.multiple_experts_criteria[i]
        return self.run_EVM_method()

    def run_multiple_experts_GMM_method(self, i):
        self.criteria_number = len(self.multiple_experts_criteria[i])
        self.alternative_matrixes = self.multiple_experts_alternatives[i]
        self.criteria_comparison = self.multiple_experts_criteria[i]
        return self.run_GMM_method()

    def run_multiple_experts_incomplete_GMM_method(self, i):
        self.criteria_number = len(self.multiple_experts_criteria[i])
        self.alternative_matrixes = self.multiple_experts_alternatives[i]
        self.criteria_comparison = self.multiple_experts_criteria[i]
        return self.run_incomplete_GMM_method()

    def run_multiple_experts_subcriteria_EVM_method(self, i):
        self.alternative_matrixes = self.multiple_experts_alternatives[i]
        self.criteria_comparison = self.multiple_experts_criteria[i]
        if self.multiple_experts_subcriteria[i] is not None:
            self.subcriteria_comparison = self.multiple_experts_subcriteria[i]
        self.criteria_number = 0
        for list in self.subcriteria_comparison:
            if list is not None:
                self.criteria_number += len(list)
            else:
                self.criteria_number += 1
        return self.run_subcriteria_evm_method()

    def run_multiple_experts_subcriteria_GMM_method(self, i):
        self.alternative_matrixes = self.multiple_experts_alternatives[i]
        self.criteria_comparison = self.multiple_experts_criteria[i]
        self.subcriteria_comparison = self.multiple_experts_subcriteria[i]
        self.criteria_number = 0
        for list in self.subcriteria_comparison:
            if list is not None:
                self.criteria_number += len(list)
            else:
                self.criteria_number += 1
        return self.run_subcriteria_gmm_method()

    def synthesize_multiple_experts_result(self):
        print('ALL RESULTS', self.multiple_experts_results)
        result = np.prod(self.multiple_experts_results, axis=0)
        result = np.power(result, 1 / self.experts_number)
        return result

    def calculate_global_priorities(self):
        criteria_priorities = copy.deepcopy(self.criteria_priorities)
        res = []
        i = 0
        for priority in self.subcriteria_priorities:
            if priority is not None:
                res.append(priority*criteria_priorities[i])
            else:
                res.append(np.array([criteria_priorities[i]]))
            i += 1
        self.criteria_priorities = []
        for array in res:
            for element in array:
                self.criteria_priorities.append(element)

    def calculate_subcriteria_evm_priorities(self):
        subcriteria_numbers = []
        for comparison in self.subcriteria_comparison:
            if comparison is not None:
                self.subcriteria_priorities.append(self.calculate_evm_priority(np.array(comparison)))
                subcriteria_numbers.append(len(comparison))
            else:
                self.subcriteria_priorities.append(None)
                subcriteria_numbers.append(0)
        self.calculate_global_priorities()
        print('Res priority:', self.criteria_priorities)

    def run_subcriteria_evm_method(self):
        self.calculate_evm_alternatives_priorities()
        self.calculate_evm_criteria_priorities()
        self.calculate_subcriteria_evm_priorities()
        result = self.synthesize_result()
        for i in range(self.criteria_number):
            print(result[i])
        total = result.sum(axis=0)
        return total

    def calculate_subcriteria_gmm_priorities(self):
        subcriteria_numbers = []
        for comparison in self.subcriteria_comparison:
            if comparison is not None:
                self.subcriteria_priorities.append(self.calculate_gmm_priority(comparison))
                subcriteria_numbers.append(len(comparison))
            else:
                self.subcriteria_priorities.append(None)
                subcriteria_numbers.append(0)
        self.calculate_global_priorities()
        print('Res priority:', self.criteria_priorities)

    def run_subcriteria_gmm_method(self):
        self.calculate_gmm_alternatives_priorities()
        self.calculate_gmm_criteria_priorities()
        self.calculate_subcriteria_gmm_priorities()
        result = self.synthesize_result()
        for i in range(self.criteria_number):
            print(result[i])
        total = result.sum(axis=0)
        return total
