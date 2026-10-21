from abc import ABC, abstractmethod


# ─────────────────────────────────────────
# Fitness Function — Member 5 implements this for CVRP
# ─────────────────────────────────────────
class FitnessFunction(ABC):

    @abstractmethod
    def evaluate(self, individual):
        # Takes an Individual, returns a float score.
        # Higher score = better solution.
        pass


# ─────────────────────────────────────────
# Feasibility Check — Member 4 implements this for CVRP
# ─────────────────────────────────────────
class FeasibilityCheck(ABC):

    @abstractmethod
    def is_feasible(self, individual):
        # Takes an Individual, returns True if solution is valid.
        pass

class SelectionMethod(ABC):

    @abstractmethod
    def select(self, population):
        # Takes a Population, returns two Individual parents.
        pass

class CrossoverMethod(ABC):

    @abstractmethod
    def crossover(self, parent1, parent2):
        # Takes two Individuals, returns two new child Individuals.
        pass


class MutationMethod(ABC):

    @abstractmethod
    def mutate(self, individual):
        # Takes an Individual, returns a mutated Individual.
        pass

class ReplacementMethod(ABC):

    @abstractmethod
    def replace(self, old_population, new_population):
        # Takes old and new Population, returns the next generation Population.
        pass