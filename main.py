import sys
import os
sys.path.append(os.path.dirname(__file__))

from chromosome import BinaryChromosome, IntegerChromosome, FloatChromosome
from individual import Individual
from population import Population


# --- Test Chromosomes ---
print("=== Chromosome Test ===")

b = BinaryChromosome(length=6)
b.initialize()
print(f"Binary:  {b}")

i = IntegerChromosome(length=5, min_val=0, max_val=9)
i.initialize()
print(f"Integer: {i}")

f = FloatChromosome(length=4, min_val=0.0, max_val=1.0)
f.initialize()
print(f"Float:   {f}")


# --- Test Individual ---
print("\n=== Individual Test ===")

ind1 = Individual(BinaryChromosome(length=6))
ind1.chromosome.initialize()
ind1.fitness = 42.5
print(ind1)


# --- Test Population ---
print("\n=== Population Test ===")

pop = Population()

for _ in range(5):
    chromosome = IntegerChromosome(length=4, min_val=0, max_val=9)
    chromosome.initialize()
    ind = Individual(chromosome)
    ind.fitness = sum(chromosome.genes)   # dummy fitness for now
    pop.add(ind)

print(pop)
print(f"Population size: {pop.size()}")
print(f"Best individual: {pop.get_best()}")