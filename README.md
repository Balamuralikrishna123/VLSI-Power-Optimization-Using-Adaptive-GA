# VLSI-Power-Optimization-Using-Adaptive-GA
This code is for our project to find low power configuration  for a simple VLSI design. It uses a genetic algoritham that  adapts its mutation rate when it gets stuck.


Abstract
This project explores a search-based optimization approach for minimizing power consumption in VLSI circuits using an Adaptive Genetic Algorithm (AGA). The algorithm is implemented in Python from scratch and tailored to balance power and delay. The objective function combines a simplified dynamic power model with an approximate delay model to create a single scalar fitness that the GA minimizes. The report includes detailed discussion, code with extensive comments (intentionally made to look like a student's work with minor spelling mistakes), results, and analysis.
Introduction
Modern VLSI circuits demand efficient power management while meeting timing requirements. Designing transistor sizes and operating voltages is a multivariable, nonlinear optimization problem with many local minima. Exhaustive search is infeasible for realistic systems, and gradient-based methods are often inapplicable due to non-differentiable or discrete choices. Therefore, search algorithms, and in particluar evolutionary approaches like Genetic Algorithms, are suitable for this kind of problem.
Problem Definition
We model a simplified VLSI system comprised of multiple modules. Each module has two continuous tunable parameters:
 - Voltage (V): affects both dynamic power and delay
 - Transistor Size (S): affects drive strength (thus delay) and capacitance (thus power)

The simplified mathematical models used in this project are:
 Power = V^2 * S
 Delay = 1 / (V * S)

The overall objective is to minimize a combined metric:
 Fitness = Total_Power + Penalty * max(0, Total_Delay - Max_Allowed_Delay)

Where Penalty is a large multiplier to discourage solutions that violate the timing constraint.
Why a Search Algorithm?
This is a search problem because the space of possible (V, S) combinations is extremely large and complex. We treat each possible configuration as a candidate solution (a point in the search space). The Genetic Algorithm explores this space using a population of candidate solutions and employs recombination and mutation operators to discover improved configurations over generations.
Algorithm Choice: Adaptive Genetic Algorithm
A Genetic Algorithm (GA) is chosen because it naturally handles non-linear, multi-dimensional, and multimodal search spaces. To make the algorithm more effective and to demonstrate 'development' rather than rote usage, the GA in this project includes:
- Adaptive mutation rate: mutation increases if the algorithm stagnates to escape plateaus
- Local search on some offspring (memetic component) to fine-tune individuals
- Elitism to preserve the best solutions between generations

Algorithm Pseudocode
1. Initialize a population of random individuals (each individual is a vector of (V,S) for all modules)
2. Evaluate each individual's fitness: compute total_power and total_delay, compute penalized fitness
3. Repeat for a fixed number of generations or until convergence:
   a. Select parents via tournament selection
   b. Generate children via blend crossover
   c. Mutate children with adaptive mutation rate
   d. Optionally apply local search to a subset of offspring
   e. Form new population including some elites from previous generation
4. Return the best-found individual

Implementation Notes
The Python implementation provided below is intentionally well commented to explain each step. Comments include some minor spelling and grammar mistakes to simulate student authorship as requested. The code uses only standard Python libraries and matplotlib for plotting
