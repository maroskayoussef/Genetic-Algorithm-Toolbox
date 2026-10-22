# Quick tests for the CVRP model, decoder and feasibility check.
from individual import Individual
from cvrp_model import CVRPChromosome, decode, example_problem
from cvrp_feasibility import CVRPFeasibilityCheck

problem = example_problem()
check = CVRPFeasibilityCheck(problem)

# 1. random chromosome
chrom = CVRPChromosome(problem)
chrom.initialize()
ind = Individual(chrom)
routes = decode(chrom.genes, problem)
print("Random genes :", chrom.genes)
print("Routes       :", routes)
print("Loads        :", [problem.route_load(r) for r in routes])
print("Feasible     :", check.is_feasible(ind), "| overload:", check.overload(routes))

# 2. the known optimal solution from OR-Tools (17, 18, 19 are separators)
chrom.genes = [4, 3, 1, 7, 17, 14, 16, 10, 9, 18, 12, 11, 15, 13, 19, 8, 2, 6, 5]
routes = decode(chrom.genes, problem)
total = sum(problem.route_distance(r) for r in routes)
print("\nOptimal routes:", routes)
print("Feasible     :", check.is_feasible(ind), "| distance:", total)   # True, 6208

# 3. overloaded vehicle: customers 7, 8, 15 (8+8+8 = 24 > 15)
chrom.genes = [7, 8, 15, 17, 14, 16, 10, 9, 18, 12, 11, 4, 13, 19, 3, 2, 6, 5, 1]
print("\nOverloaded   :", check.is_feasible(ind))   # False
