

import random
import matplotlib.pyplot as plt

# ---------- Problem Setup -----------
NUM_MODULES = 8   # number of VLSI modules we are optimizing
V_MIN, V_MAX = 0.7, 1.3   # Voltage limits
S_MIN, S_MAX = 0.5, 2.5   # Transistor size limits
MAX_DELAY = 25.0           # Max allowed delay (soft constraint)
PENALTY = 40.0             # penalty for delay violation

# ---------- GA Settings -------------
POP_SIZE = 50
GENERATIONS = 60
ELITE = 3
TOUR_SIZE = 3
MUTATION_RATE = 0.12
MAX_MUTATION = 0.35
MIN_MUTATION = 0.02
STAGNATION_LIMIT = 8

# ---------- Helper Functions ----------

def power(v, s):
    """Power eqn (simple model): P = V^2 * S"""
    return (v ** 2) * s

def delay(v, s):
    """Delay eqn (simple model): D = 1 / (V * S)"""
    return 1.0 / (max(0.00001, v * s))

def evaluate(individual):
    """Calc total power, delay and fitness (lower is better)"""
    total_p = 0
    total_d = 0
    for (v, s) in individual:
        total_p += power(v, s)
        total_d += delay(v, s)
    penalty = max(0, total_d - MAX_DELAY)
    fit = total_p + PENALTY * penalty
    return fit, total_p, total_d

def random_individual():
    """make random (v,s) pairs for one design"""
    return [(random.uniform(V_MIN, V_MAX), random.uniform(S_MIN, S_MAX))
            for _ in range(NUM_MODULES)]

def init_population():
    """make first generation with random guys"""
    return [random_individual() for _ in range(POP_SIZE)]

def tournament_selection(pop, fits):
    """select best from few random"""
    sample = random.sample(range(len(pop)), TOUR_SIZE)
    best_idx = min(sample, key=lambda i: fits[i])
    return pop[best_idx]

def crossover(p1, p2):
    """mix two parents to make baby"""
    child = []
    for (v1, s1), (v2, s2) in zip(p1, p2):
        a = random.random()
        vc = a * v1 + (1 - a) * v2
        sc = a * s1 + (1 - a) * s2
        vc = max(V_MIN, min(V_MAX, vc))
        sc = max(S_MIN, min(S_MAX, sc))
        child.append((vc, sc))
    return child

def mutate(ind, rate):
    """randomly change some genes"""
    new = []
    for v, s in ind:
        if random.random() < rate:
            v += random.uniform(-0.05, 0.05)
            s += random.uniform(-0.1, 0.1)
        v = max(V_MIN, min(V_MAX, v))
        s = max(S_MIN, min(S_MAX, s))
        new.append((v, s))
    return new

def run_genetic_algo(seed=42):
    random.seed(seed)
    pop = init_population()
    best_fit = float("inf")
    best_ind = None
    stagnation = 0
    mutation_rate = MUTATION_RATE

    best_hist = []
    pow_hist = []
    del_hist = []

    for gen in range(1, GENERATIONS + 1):
        fits = [evaluate(ind)[0] for ind in pop]
        sorted_idx = sorted(range(len(fits)), key=lambda i: fits[i])
        elites = [pop[i] for i in sorted_idx[:ELITE]]

        cur_best_fit = fits[sorted_idx[0]]
        cur_best = pop[sorted_idx[0]]
        f, p, d = evaluate(cur_best)

        if cur_best_fit < best_fit:
            best_fit = cur_best_fit
            best_ind = cur_best
            stagnation = 0
        else:
            stagnation += 1

        # adapt mutation if stuck
        if stagnation > STAGNATION_LIMIT:
            mutation_rate = min(MAX_MUTATION, mutation_rate * 1.3)
        else:
            mutation_rate = max(MIN_MUTATION, mutation_rate * 0.98)

        new_pop = elites.copy()

        while len(new_pop) < POP_SIZE:
            p1 = tournament_selection(pop, fits)
            p2 = tournament_selection(pop, fits)
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            new_pop.append(child)

        pop = new_pop

        best_hist.append(best_fit)
        pow_hist.append(p)
        del_hist.append(d)

        if gen % 5 == 0 or gen == 1 or gen == GENERATIONS:
            print(f"Gen {gen}: best fit={f:.3f}, power={p:.3f}, delay={d:.3f}, mut={mutation_rate:.3f}")

    print("\nFinal best solution:")
    for i, (v, s) in enumerate(best_ind):
        print(f" Module {i+1}: V={v:.3f}, S={s:.3f}")
    f, p, d = evaluate(best_ind)
    print(f"Total Power={p:.3f}, Delay={d:.3f}, Fitness={f:.3f}")

    # plotting result graphs
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.plot(best_hist, '-o')
    plt.title("Best Fitness")
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(pow_hist, '-o')
    plt.title("Power per Gen")
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(del_hist, '-o')
    plt.axhline(MAX_DELAY, color='r', linestyle='--')
    plt.title("Delay per Gen")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Run the algorithm
if __name__ == "__main__":
    run_genetic_algo(seed=123)
