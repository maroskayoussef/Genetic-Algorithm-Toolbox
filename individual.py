from chromosome import Chromosome


class Individual:

    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome  # the genes
        self.fitness = None           # score — set later after evaluation
        self.is_feasible = True       # will be checked later

    def __str__(self):
        return f"Genes: {self.chromosome} | Fitness: {self.fitness} | Feasible: {self.is_feasible}"