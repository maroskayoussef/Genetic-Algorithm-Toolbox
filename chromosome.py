from abc import ABC, abstractmethod
import random


class Chromosome(ABC):

    def __init__(self, length):
        self.length = length  # number of genes
        self.genes = []       # the actual values

    @abstractmethod
    def initialize(self):
        """Randomly initialize the genes"""
        pass

    @abstractmethod
    def get_gene(self, index):
        """Return gene at position index"""
        pass

    @abstractmethod
    def set_gene(self, index, value):
        """Set gene at position index"""
        pass

    def __str__(self):
        return str(self.genes)


class BinaryChromosome(Chromosome):

    def __init__(self, length):
        super().__init__(length)

    def initialize(self):
        self.genes = [random.randint(0, 1) for _ in range(self.length)]

    def get_gene(self, index):
        return self.genes[index]

    def set_gene(self, index, value):
        if value not in (0, 1):
            raise ValueError("Binary gene must be 0 or 1")
        self.genes[index] = value


class IntegerChromosome(Chromosome):

    def __init__(self, length, min_val, max_val):
        super().__init__(length)
        self.min_val = min_val
        self.max_val = max_val

    def initialize(self):
        self.genes = [random.randint(self.min_val, self.max_val)
                      for _ in range(self.length)]

    def get_gene(self, index):
        return self.genes[index]

    def set_gene(self, index, value):
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"Gene must be between {self.min_val} and {self.max_val}")
        self.genes[index] = value


class FloatChromosome(Chromosome):

    def __init__(self, length, min_val, max_val):
        super().__init__(length)
        self.min_val = min_val
        self.max_val = max_val

    def initialize(self):
        self.genes = [random.uniform(self.min_val, self.max_val)
                      for _ in range(self.length)]

    def get_gene(self, index):
        return self.genes[index]

    def set_gene(self, index, value):
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"Gene must be between {self.min_val} and {self.max_val}")
        self.genes[index] = value