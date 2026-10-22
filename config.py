from interfaces import (FitnessFunction, FeasibilityCheck,
                        SelectionMethod, CrossoverMethod,
                        MutationMethod, ReplacementMethod)


class GAConfig:

    def __init__(self):

        # ── Population & Evolution ──────────────────
        self.population_size   = 50       # N
        self.max_generations   = 1000     # how many generations to run
        self.crossover_rate    = 0.7      # Pc
        self.mutation_rate     = 0.05     # Pm

        # ── Pluggable Methods ───────────────────────
        self.fitness_function    = None   # FitnessFunction   — must be set
        self.feasibility_check   = None   # FeasibilityCheck  — must be set
        self.selection_method    = None   # SelectionMethod   — must be set
        self.crossover_method    = None   # CrossoverMethod   — must be set
        self.mutation_method     = None   # MutationMethod    — must be set
        self.replacement_method  = None   # ReplacementMethod — must be set

        # ── Objective ───────────────────────────────
        self.objective = "maximize"       # "maximize" or "minimize" a feasible solution's fitness. If "minimize", the fitness function is negated before selection.

        # ── Infeasibility Handling ──────────────────
        self.infeasibility_strategy = "penalty"   # "penalty" or "reject"
        self.penalty_weight         = 1000        # used if strategy = "penalty"

    def validate(self):
        """Check that all required fields are set before running the GA"""
        errors = []

        if self.fitness_function is None:
            errors.append("fitness_function is not set")
        if self.feasibility_check is None:
            errors.append("feasibility_check is not set")
        if self.objective not in ("maximize", "minimize"):
            errors.append("objective must be 'maximize' or 'minimize'")
        if self.selection_method is None:
            errors.append("selection_method is not set")
        if self.crossover_method is None:
            errors.append("crossover_method is not set")
        if self.mutation_method is None:
            errors.append("mutation_method is not set")
        if self.replacement_method is None:
            errors.append("replacement_method is not set")


        if errors:
            raise ValueError("GAConfig is missing:\n" + "\n".join(errors))

    def __str__(self):
        return (f"GAConfig(\n"
                f"  population_size={self.population_size},\n"
                f"  max_generations={self.max_generations},\n"
                f"  objective={self.objective},\n"
                f"  crossover_rate={self.crossover_rate},\n"
                f"  mutation_rate={self.mutation_rate},\n"
                f"  infeasibility_strategy={self.infeasibility_strategy},\n"
                f"  penalty_weight={self.penalty_weight}\n"
                f")")