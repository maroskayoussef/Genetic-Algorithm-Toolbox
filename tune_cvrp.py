import contextlib
import csv
import io
import itertools
import time
from multiprocessing import Pool

from cvrp_model import example_problem
from run_cvrp import solve

# the grid of settings to test, stage 1: mutation rate and elitism size
MUTATION_RATES = [0.1, 0.3, 0.5, 0.6, 0.7, 0.9]
ELITISM_SIZES = [0, 1, 2, 5, 10]     # plain generational (no elitism)
CROSSOVER_RATES = [0.6, 0.7, 0.8, 0.9, 1.0]   # stage 2
BASE_CROSSOVER = 0.9                 # crossover rate used in stage 1 (run_cvrp default)
SEEDS = list(range(10))              # same seeds for every setting
KNOWN_OPTIMUM = 6208                 # from the OR-Tools example
GOOD_GAP = 0.05                      #  within 5% of the optimum
WORKERS = 7                          # parallel processes (1 = no parallelism)


def run_one(job):
    """Run the GA once for one (mutation, elitism, seed) job."""
    mutation, elitism, seed = job
    problem = example_problem()
    with contextlib.redirect_stdout(io.StringIO()):   # hide engine progress output
        routes, best = solve(problem, seed=seed,
                             mutation_rate=mutation, elitism=elitism)
    distance = sum(problem.route_distance(r) for r in routes)
    return mutation, elitism, seed, best.is_feasible, distance


def run_crossover(job):
    """Stage 2: run the GA once for one (crossover, mutation, elitism, seed) job."""
    crossover, mutation, elitism, seed = job
    problem = example_problem()
    with contextlib.redirect_stdout(io.StringIO()):
        routes, best = solve(problem, seed=seed, crossover_rate=crossover,
                             mutation_rate=mutation, elitism=elitism)
    distance = sum(problem.route_distance(r) for r in routes)
    return crossover, seed, best.is_feasible, distance


def print_crossover_table(results):
    """Stage 2 table: one row per crossover rate."""
    n = len(SEEDS)
    good_limit = KNOWN_OPTIMUM * (1 + GOOD_GAP)
    print(f"{'crossover':>9} {'good':>6} {'feasible':>9} {'optimum':>8} {'avg':>6}")
    best_rate, best_key = None, None
    for rate in CROSSOVER_RATES:
        feasible = [r[3] for r in results if r[0] == rate and r[2]]
        good = sum(1 for d in feasible if d <= good_limit)
        avg = round(sum(feasible) / len(feasible)) if feasible else None
        print(f"{rate:>9} {str(good) + '/' + str(n):>6} "
              f"{str(len(feasible)) + '/' + str(n):>9} "
              f"{str(feasible.count(KNOWN_OPTIMUM)) + '/' + str(n):>8} "
              f"{'-' if avg is None else avg:>6}")
        
        # same ranking rule as stage 1; if still tied, prefer BASE_CROSSOVER
        key = (-good, -len(feasible), avg if avg is not None else float("inf"),
               rate != BASE_CROSSOVER)
        if best_key is None or key < best_key:
            best_rate, best_key = rate, key
    return best_rate


def summarize(results):
    """Group the runs by setting and compute the statistics."""
    rows = []
    for mutation, elitism in itertools.product(MUTATION_RATES, ELITISM_SIZES):
        runs = [r for r in results if r[0] == mutation and r[1] == elitism]
        feasible = [r[4] for r in runs if r[3]]
        good_limit = KNOWN_OPTIMUM * (1 + GOOD_GAP)
        rows.append({
            "mutation": mutation,
            "elitism": elitism,
            "good": sum(1 for d in feasible if d <= good_limit),
            "feasible": len(feasible),
            "optimum": feasible.count(KNOWN_OPTIMUM),
            "best": min(feasible) if feasible else None,
            "avg": round(sum(feasible) / len(feasible)) if feasible else None,
            "worst": max(feasible) if feasible else None,
        })
    # ranking rule: most good runs, then most feasible, then lowest average
    rows.sort(key=lambda r: (-r["good"], -r["feasible"],
                             r["avg"] if r["avg"] is not None else float("inf")))
    return rows


def save_runs(results, path="tune_runs.csv"):
    """Save every single run so the table can be checked or re-ranked."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mutation", "elitism", "seed", "feasible", "distance"])
        writer.writerows(results)


def print_table(rows):
    n = len(SEEDS)
    print(f"{'rank':>4} {'mutation':>8} {'elitism':>7} {'good':>6} {'feasible':>9} "
          f"{'optimum':>8} {'best':>6} {'avg':>6} {'worst':>6}")
    for i, r in enumerate(rows, 1):
        fmt = lambda v: "-" if v is None else v
        print(f"{i:>4} {r['mutation']:>8} {r['elitism']:>7} "
              f"{str(r['good']) + '/' + str(n):>6} "
              f"{str(r['feasible']) + '/' + str(n):>9} "
              f"{str(r['optimum']) + '/' + str(n):>8} "
              f"{fmt(r['best']):>6} {fmt(r['avg']):>6} {fmt(r['worst']):>6}")


if __name__ == "__main__":
    jobs = list(itertools.product(MUTATION_RATES, ELITISM_SIZES, SEEDS))
    print(f"Running {len(jobs)} GA runs "
          f"({len(MUTATION_RATES)} mutation rates x {len(ELITISM_SIZES)} "
          f"elitism sizes x {len(SEEDS)} seeds)...")
    start = time.time()
    with Pool(WORKERS) as pool:
        results = pool.map(run_one, jobs)
    print(f"Done in {time.time() - start:.0f}s\n")

    save_runs(results)
    rows = summarize(results)
    print_table(rows)
    top = rows[0]
    print(f"\nBest setting: mutation_rate={top['mutation']}, elitism={top['elitism']}")

    #  Stage 2: crossover rate, with the best mutation and elitism fixed 
    jobs2 = [(c, top["mutation"], top["elitism"], s)
             for c in CROSSOVER_RATES for s in SEEDS]
    print(f"\nStage 2: testing {len(CROSSOVER_RATES)} crossover rates x "
          f"{len(SEEDS)} seeds (mutation={top['mutation']}, "
          f"elitism={top['elitism']})...")
    start = time.time()
    with Pool(WORKERS) as pool:
        results2 = pool.map(run_crossover, jobs2)
    print(f"Done in {time.time() - start:.0f}s\n")

    best_crossover = print_crossover_table(results2)
    print(f"\nBest crossover rate: {best_crossover}")
    print(f"\nFinal settings: mutation_rate={top['mutation']}, "
          f"elitism={top['elitism']}, crossover_rate={best_crossover}")