import copy
import random

from interfaces import CrossoverMethod
from individual import Individual


class _BaseCrossover(CrossoverMethod):

    def __init__(self, crossover_rate=0.7):
        if not 0.0 <= crossover_rate <= 1.0:
            raise ValueError("crossover_rate must be between 0 and 1")
        self.crossover_rate = crossover_rate

    def crossover(self, parent1, parent2):
        genes1 = list(parent1.chromosome.genes)
        genes2 = list(parent2.chromosome.genes)
        if len(genes1) != len(genes2):
            raise ValueError("Parents must have the same number of genes")

        if random.random() < self.crossover_rate:
            genes1, genes2 = self._cross(genes1, genes2)

        return self._make_child(parent1, genes1), self._make_child(parent2, genes2)

    @staticmethod
    def _make_child(template_parent, genes):
        chromosome = copy.deepcopy(template_parent.chromosome)
        chromosome.genes = list(genes)
        return Individual(chromosome)

    def _cross(self, genes1, genes2):
        raise NotImplementedError


class MultiPointCrossover(_BaseCrossover):

    def __init__(self, num_points=2, crossover_rate=0.7):
        super().__init__(crossover_rate)
        if num_points < 1:
            raise ValueError("num_points must be >= 1")
        self.num_points = num_points

    def _cross(self, genes1, genes2):
        n = len(genes1)
        if n < 2:
            return genes1, genes2

        k = min(self.num_points, n - 1)
        cuts = sorted(random.sample(range(1, n), k))
        boundaries = [0] + cuts + [n]

        child1, child2 = [], []
        swap = False
        for start, end in zip(boundaries, boundaries[1:]):
            seg1, seg2 = genes1[start:end], genes2[start:end]
            if swap:
                seg1, seg2 = seg2, seg1
            child1 += seg1
            child2 += seg2
            swap = not swap
        return child1, child2


class OrderCrossover(_BaseCrossover):

    def _cross(self, genes1, genes2):
        n = len(genes1)
        if sorted(genes1) != sorted(genes2) or len(set(genes1)) != n:
            raise ValueError("OrderCrossover needs permutations (no repeated genes, "
                             "both parents with the same genes)")
        if n < 2:
            return genes1, genes2

        a, b = sorted(random.sample(range(n), 2))
        return self._make_order_child(genes1, genes2, a, b), \
            self._make_order_child(genes2, genes1, a, b)

    @staticmethod
    def _make_order_child(donor, filler, a, b):
        n = len(donor)
        child = [None] * n
        child[a:b + 1] = donor[a:b + 1]

        filler_order = filler[b + 1:] + filler[:b + 1]

        missing = [gene for gene in filler_order if gene not in child]

        empty_positions = list(range(b + 1, n)) + list(range(0, a))

        for position, gene in zip(empty_positions, missing):
            child[position] = gene
        return child