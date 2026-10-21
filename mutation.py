from interfaces import MutationMethod
import copy
import random

class BitFlipMutation(MutationMethod):
    # Bit flip process takes a binary chromosome and randomly flips some genes
    
    # chance that each single gene is flipped with default of 5%
    def __init__(self,rate=0.05):
        self.rate = rate
        
    # Implements mutate from MutationMethod
    def mutate(self, individual):
        # Work on a copy so the original individual stays unchange 
        copied = copy.deepcopy(individual)
        genes =  copied.chromosome.genes
        
        # Randomize through a loop
        for i in range(len(genes)):
            # Flip genes only with given probability rate
            if random.random() < self.rate:
                if genes[i] == 0:
                    genes[i] = 1
                else:
                    genes[i] = 0
        return copied 
                        
class SwapMutation(MutationMethod):
    
    # mutation for permutations where every value appears once
    # Define a default chance rate of 5 %
    def __init__(self,rate=0.05):
        self.rate = rate
            
    def mutate(self, individual):
        copied = copy.deepcopy(individual)
        genes =  copied.chromosome.genes
        # Safe guard: need at least two genes to swap
        if len(genes) < 2:
            return copied
            
        # Roll the dice once for the whole individual
        if random.random() < self.rate:
            # pick two random positions and swap genes
            pos1, pos2 = random.sample(range(len(genes)), 2)
            genes[pos1], genes[pos2] = genes[pos2], genes[pos1]

        return copied
    
                        
class UniformMutation(MutationMethod):
    
    # Move a random step either left or right in boundaries range for float chromosomes 
    # Define a default chance rate of 5 %
    def __init__(self,rate=0.05):
        self.rate = rate
            
    def mutate(self, individual):
        copied = copy.deepcopy(individual)   
        genes =  copied.chromosome.genes
        # Get lower and upper bounds
        low = copied.chromosome.min_val
        high = copied.chromosome.max_val
        for i in range(len(genes)):
            # Roll the dice for each gene
            if random.random() < self.rate:
                num =  genes[i]
                # flip a coin to go left or right
                if random.random() <= 0.5:
                    # going left
                    # calculate maximum room space allowed to step to 
                    room = num - low
                    # random step 
                    step =  random.uniform(0,room)
                    genes[i] = num - step

                else:
                    # going right
                    room = high - num
                    step =  random.uniform(0,room)
                    genes[i] = num + step

        return copied
        
        
 