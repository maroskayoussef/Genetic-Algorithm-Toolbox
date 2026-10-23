import random

from chromosome import IntegerChromosome


class CVRPProblem:
    # Holds the problem data: distances, demands and vehicles.

    def __init__(self, distance_matrix, demands, vehicle_capacities, depot=0):
        self.distance_matrix = distance_matrix
        self.demands = demands
        self.vehicle_capacities = vehicle_capacities
        self.num_vehicles = len(vehicle_capacities)
        self.depot = depot
        self.num_nodes = len(distance_matrix)

        # every node except the depot is a customer
        self.customers = [i for i in range(self.num_nodes) if i != depot]

    def route_load(self, route):
        # total demand picked up on one route
        return sum(self.demands[c] for c in route)

    def route_distance(self, route):
        # depot -> customers -> depot
        if not route:
            return 0
        path = [self.depot] + route + [self.depot]
        return sum(self.distance_matrix[a][b] for a, b in zip(path, path[1:]))


class CVRPChromosome(IntegerChromosome):
    # Permutation of customers + separators.
    # Customers keep their node number (1..n).
    # Separators are numbers >= num_nodes; each one means "start the next vehicle".
    # With V vehicles we need V-1 separators.
    # Example (8 customers, 3 vehicles): [3, 1, 9, 5, 2, 7, 10, 4, 6, 8]
    #   -> vehicle 1: [3, 1]   vehicle 2: [5, 2, 7]   vehicle 3: [4, 6, 8]

    def __init__(self, problem):
        self.problem = problem
        separators = list(range(problem.num_nodes,
                                problem.num_nodes + problem.num_vehicles - 1))
        self.values = problem.customers + separators
        super().__init__(len(self.values), min(self.values), max(self.values))

    def initialize(self):
        # random order of all values (each appears once)
        self.genes = self.values[:]
        random.shuffle(self.genes)

    def __deepcopy__(self, memo):
        # Called by copy.deepcopy (used in crossover and mutation).
        # Copy only the genes; share the problem and values, which never
        # change. This avoids copying the whole distance matrix every time.
        new = self.__class__.__new__(self.__class__)
        new.__dict__.update(self.__dict__)
        new.genes = list(self.genes)
        return new


def decode(genes, problem):
    # Turn the gene list into a list of routes (one list per vehicle).
    routes = [[]]
    for gene in genes:
        if gene >= problem.num_nodes:   # separator -> next vehicle
            routes.append([])
        else:
            routes[-1].append(gene)
    return routes


def example_problem():
    # The example instance from the Google OR-Tools CVRP page (best known: 6208).
    distance_matrix = [
        [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
        [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
        [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
        [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
        [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
        [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
        [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
        [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
        [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
        [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
        [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
        [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
        [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
        [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
        [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
        [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
        [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
    ]
    demands = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    vehicle_capacities = [15, 15, 15, 15]
    return CVRPProblem(distance_matrix, demands, vehicle_capacities, depot=0)
