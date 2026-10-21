from individual import Individual


class Population:

    def __init__(self):
        self.individuals = []   # list of Individual objects

    def add(self, individual: Individual):
        """Add one individual to the population"""
        self.individuals.append(individual)

    def size(self):
        """Return how many individuals are in the population"""
        return len(self.individuals)

    def get(self, index):
        """Return individual at position index"""
        return self.individuals[index]

    def get_best(self):
        """Return the individual with the highest fitness"""
        return max(self.individuals, key=lambda ind: ind.fitness)

    def get_all(self):
        """Return all individuals"""
        return self.individuals

    def clear(self):
        """Empty the population"""
        self.individuals = []

    def __str__(self):
        result = ""
        for i, ind in enumerate(self.individuals):
            result += f"Individual {i+1}: {ind}\n"
        return result