from interfaces import FeasibilityCheck
from cvrp_model import decode


class CVRPFeasibilityCheck(FeasibilityCheck):
    # A solution is feasible when:
    #   1. every customer is visited exactly once
    #   2. it uses at most the available vehicles
    #   3. no vehicle carries more than its capacity

    def __init__(self, problem):
        self.problem = problem

    def is_feasible(self, individual):
        routes = decode(individual.chromosome.genes, self.problem)

        # 1. each customer exactly once
        visited = [c for route in routes for c in route]
        if sorted(visited) != sorted(self.problem.customers):
            return False

        # 2. not more routes than vehicles
        if len(routes) > self.problem.num_vehicles:
            return False

        # 3. capacity of each vehicle
        return self.overload(routes) == 0

    def overload(self, routes):
        # Total load above capacity over all vehicles (0 means no violation).
        # Useful for the fitness function to give a penalty based on how bad it is.
        total = 0
        for route, capacity in zip(routes, self.problem.vehicle_capacities):
            total += max(0, self.problem.route_load(route) - capacity)
        return total
