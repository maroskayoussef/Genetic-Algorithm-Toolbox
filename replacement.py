from interfaces import ReplacementMethod
from population import Population
import random

class GenerationalReplacement(ReplacementMethod):
    def replace(self, old_pop, new_pop):
        next_gen = Population()

        # the entire set of parents is replaced by the offspring
        for ind in new_pop.get_all():
            if next_gen.size() < old_pop.size():    # stop when the group is full
                next_gen.add(ind)  
        return next_gen                                

 

class SteadyStateReplacement(ReplacementMethod):
    def __init__(self,k=2,elitism=True):
        self.k = k # number of individuals replaced each time
        self.elitism = elitism #  True for default to keep best solutions discovered so far
    def replace(self, old_pop, new_pop):
        old_list = list(old_pop.get_all())
        new_list = list(new_pop.get_all())
        

        k = min(self.k, len(old_list))      # K can't be bigger than the group

        if self.elitism:
            # Sort best old first
            old_list.sort(key=lambda x: x.fitness, reverse=True) 
        else:
            # Random order
            random.shuffle(old_list)                              

        # Selected without k inds
        selected = old_list[:len(old_list) - k]     
        children = new_list[:k]     

        next_gen = Population()
        for ind in selected:
            next_gen.add(ind)
        for ind in children:
            next_gen.add(ind)
        return next_gen
    
  