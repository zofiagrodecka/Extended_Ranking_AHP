class ExpertCalculations:
    def __init__(self, criteria, alternatives, criteria_tables, alternatives_tables, criteria_priorities, alternatives_priorities, subcriteria, subcriteria_priorities):
        self.criteria_names = criteria
        self.alternatives_names = alternatives
        self.criteria_comparison = criteria_tables
        self.alternatives_comparisons = alternatives_tables
        self.criteria_priorities = criteria_priorities
        self.alternatives_priorities = alternatives_priorities
        self.subcriteria = subcriteria
        self.subcriteria_priorities = subcriteria_priorities
        self.cr_cryteria_indexes = []
        self.cr_alternatives_indexes = []
        self.gwi_criteria_indexes = []
        self.gwi_alternatives_indexes = []
