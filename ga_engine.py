from population import Population
from individual import Individual
from config import GAConfig


class GeneticAlgorithm:

    def __init__(self, config: GAConfig, chromosome_factory):
        """
        config             — GAConfig object with all settings
        chromosome_factory — a function that creates a new Chromosome
                             e.g: lambda: IntegerChromosome(10, 0, 100)
        """
        self.config = config
        self.chromosome_factory = chromosome_factory
        self.population = Population()
        self.best_individual = None

    # ─────────────────────────────────────────
    # Step 1 — Initialize
    # ─────────────────────────────────────────
    def _initialize_population(self):
        self.population.clear()
        for _ in range(self.config.population_size):
            chromosome = self.chromosome_factory()
            chromosome.initialize()
            individual = Individual(chromosome)
            self.population.add(individual)

    # ─────────────────────────────────────────
    # Step 2 — Evaluate
    # ─────────────────────────────────────────
    def _evaluate_population(self):
        for individual in self.population.get_all():
            # check feasibility
            individual.is_feasible = self.config.feasibility_check.is_feasible(individual)

            # calculate fitness
            raw_fitness = self.config.fitness_function.evaluate(individual)
            if self.config.objective == "minimize":
                raw_fitness = -raw_fitness

            # handle infeasible solutions
            if not individual.is_feasible:
                if self.config.infeasibility_strategy == "penalty":
                    individual.fitness = raw_fitness - self.config.penalty_weight
                elif self.config.infeasibility_strategy == "reject":
                    # replace with a new random individual
                    new_chromosome = self.chromosome_factory()
                    new_chromosome.initialize()
                    individual.chromosome = new_chromosome
                    individual.fitness = self.config.fitness_function.evaluate(individual)
                    if self.config.objective == "minimize":
                        individual.fitness = -individual.fitness
            else:
                individual.fitness = raw_fitness

    # ─────────────────────────────────────────
    # Step 3 — Track Best
    # ─────────────────────────────────────────
    def _update_best(self):
        current_best = self.population.get_best()
        if (self.best_individual is None or
                current_best.fitness > self.best_individual.fitness):
            self.best_individual = current_best

    def _display(self, fitness):
        # undo the flip so printed values are in the problem's real units
        return -fitness if self.config.objective == "minimize" else fitness

    # ─────────────────────────────────────────
    # Main Run Loop
    # ─────────────────────────────────────────
    def run(self):
        # validate config before starting
        self.config.validate()

        print("Initializing population...")
        self._initialize_population()

        print("Evaluating initial population...")
        self._evaluate_population()
        self._update_best()

        for generation in range(1, self.config.max_generations + 1):

            new_population = Population()

            # fill new population
            while new_population.size() < self.config.population_size:

                # 1 — select parents
                parent1, parent2 = self.config.selection_method.select(self.population)

                # 2 — crossover
                child1, child2 = self.config.crossover_method.crossover(parent1, parent2)

                # 3 — mutate
                child1 = self.config.mutation_method.mutate(child1)
                child2 = self.config.mutation_method.mutate(child2)

                new_population.add(child1)
                new_population.add(child2)

            # 4 — replace
            self.population = self.config.replacement_method.replace(
                self.population, new_population
            )

            # 5 — evaluate new generation
            self._evaluate_population()

            # 6 — track best
            self._update_best()

            # print progress every 100 generations
            if generation % 100 == 0:
                print(f"Generation {generation} | Best Fitness: "
                  f"{self._display(self.best_individual.fitness)}")

        print(f"\nDone! Best solution found:")
        print(f"  Genes:   {self.best_individual.chromosome}")
        print(f"  Fitness: {self._display(self.best_individual.fitness)}")

        return self.best_individual