import random

from interfaces import SelectionMethod


class _ParentSelection(SelectionMethod):
    # Shared logic for selection methods.

    def select(self, population):
        individuals = population.get_all()
        if len(individuals) == 0:
            raise ValueError("Cannot select from an empty population")
        if any(ind.fitness is None for ind in individuals):
            raise ValueError("All individuals must be evaluated before selection")

        parent1 = self._pick_one(individuals)
        others = [ind for ind in individuals if ind is not parent1]
        parent2 = self._pick_one(others if others else individuals)
        return parent1, parent2

    def _pick_one(self, individuals):
        raise NotImplementedError


class TournamentSelection(_ParentSelection):

    def __init__(self, tournament_size=3):
        if tournament_size < 1:
            raise ValueError("tournament_size must be >= 1")
        self.tournament_size = tournament_size

    def _pick_one(self, individuals):
        k = min(self.tournament_size, len(individuals))
        contestants = random.sample(individuals, k)
        best = contestants[0]
        for ind in contestants:
            if ind.fitness > best.fitness:
                best = ind
        return best

class RouletteWheelSelection(_ParentSelection):

    def _pick_one(self, individuals):
        fitnesses = [ind.fitness for ind in individuals]
        lowest = min(fitnesses)
        weights = [f - lowest + 1e-6 for f in fitnesses]   # all weights > 0
        return random.choices(individuals, weights=weights, k=1)[0]