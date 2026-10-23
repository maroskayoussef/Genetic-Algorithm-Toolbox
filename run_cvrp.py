import random

from config import GAConfig
from ga_engine import GeneticAlgorithm
from selection import TournamentSelection
from crossover import OrderCrossover
from mutation import SwapMutation
from replacement import SteadyStateReplacement

from cvrp_model import CVRPChromosome, decode, example_problem
from cvrp_feasibility import CVRPFeasibilityCheck
from cvrp_fitness import CVRPFitness
from cvrp_solution import print_solution


def build_config(problem, population_size=100, max_generations=1000,
                 crossover_rate=0.9, mutation_rate=0.7, tournament_size=3,
                 elitism=10, replacement=None, overload_penalty=1000):
    config = GAConfig()

    # hyperparameters
    config.population_size = population_size
    config.max_generations = max_generations
    config.crossover_rate = crossover_rate
    config.mutation_rate = mutation_rate

    # problem-specific functions
    config.objective = "minimize"                    # lower distance = better
    config.fitness_function = CVRPFitness(problem, overload_penalty)
    config.feasibility_check = CVRPFeasibilityCheck(problem)
    config.infeasibility_strategy = "penalty"

    # GA operators (permutation-safe ones only)
    config.selection_method = TournamentSelection(tournament_size)
    config.crossover_method = OrderCrossover(crossover_rate=crossover_rate)
    config.mutation_method = SwapMutation(rate=mutation_rate)
    # keep the best `elitism` parents, children fill the rest
    # (= generational replacement with elitism)
    config.replacement_method = replacement or SteadyStateReplacement(
        k=population_size - elitism, elitism=True)

    return config


def solve(problem, seed=None, **settings):
    #Run the GA once and return (routes, best_individual)
    if seed is not None:
        random.seed(seed)                            # same seed = same result
    config = build_config(problem, **settings)
    ga = GeneticAlgorithm(config, lambda: CVRPChromosome(problem))
    best = ga.run()
    routes = decode(best.chromosome.genes, problem)
    return routes, best


if __name__ == "__main__":
    problem = example_problem()
    routes, best = solve(problem, seed=0)
    print()
    print_solution(problem, routes, best.is_feasible)