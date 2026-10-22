from interfaces import FitnessFunction
from cvrp_model import decode
from cvrp_feasibility import CVRPFeasibilityCheck


class CVRPFitness(FitnessFunction):

    def __init__(self, problem, overload_penalty=1000):
        self.problem = problem
        self.overload_penalty = overload_penalty
        # reuse cvrp_feasibility's calculation instead of rewriting it
        self.checker = CVRPFeasibilityCheck(problem)

    def total_distance(self, routes):
        # sum of all route distances 
        return sum(self.problem.route_distance(route) for route in routes)

    def evaluate(self, individual):
        routes = decode(individual.chromosome.genes, self.problem)
        distance = self.total_distance(routes)
        overload = self.checker.overload(routes)
        return distance + self.overload_penalty * overload