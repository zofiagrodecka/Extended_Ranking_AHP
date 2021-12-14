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
        self.ri = [0, 0, 0, 0.52, 0.89, 1.11, 1.25, 1.35, 1.40, 1.45, 1.49, 1.51, 1.54, 1.56, 1.57, 1.58]

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
