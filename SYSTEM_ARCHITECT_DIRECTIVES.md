# SYSTEM ARCHITECT DIRECTIVES: ATTENTION-GUIDED NSGA-II vs. BRKGA
**PROJECT PHASE:** Preliminary 10-Task Toy Factory Demonstration
**DOMAIN:** Operations Research / Deep Learning for Combinatorial Optimization

## I. CRITICAL ARCHITECTURAL DIRECTIVE: PREVENTING SEMANTIC TENSOR ERRORS
As an advanced reasoning model, you will easily handle standard PyTorch syntax. However, you must actively prevent **Semantic Tensor Errors**. In a physically grounded Graph Neural Network, tensor dimensions can mathematically align while physically cross-contaminating constraints (e.g., multiplying `Empty_Energy` data using linear weights reserved for `Travel_Time`). PyTorch will not crash, but the structural attention heuristic will collapse into noise.

**YOUR MANDATE FOR ALL GNN CODE:**
1. **Strict Semantic Assertions:** You MUST write hardcoded `assert` statements verifying the exact shape and semantic index mapping of `x_i`, `x_j`, and `edge_attr` before any `torch.cat` or linear projection.
2. **Violent Failsafe:** The code must crash with a descriptive stack trace if the input edge tensor does not explicitly match the physical parameters (Time, Empty Energy, Loaded Energy) of the SA-AGV routing.

---

## II. MODULE 1: THE ENVIRONMENT & ORACLE (`environment.py`)
**Objective:** Construct a strict, deterministic dual-cycling container terminal environment and calculate the absolute true Pareto front.

**Physical Constants & Constraints:**
* **Layout Topology:** 10 containers (mixed loading/unloading), 3 Quay Cranes (QCs), 2 Speed-Adjustable AGVs (SA-AGVs). 
* [cite_start]**QC Handling Time ($\tau_j$):** Generate deterministically using a uniform distribution $U(30, 80)$ seconds[cite: 505].
* **SA-AGV Physics (3 Speed Levels $V$):**
  * [cite_start]*Nominal:* Empty $6\text{ m/s}$ (10 kW), Loaded $3\text{ m/s}$ (15 kW)[cite: 374, 375].
  * [cite_start]*Higher (+20%):* Empty $7.2\text{ m/s}$ (13.2 kW), Loaded $3.6\text{ m/s}$ (19.8 kW)[cite: 513, 514, 515].
  * *Lower (-20%):* Empty $4.8\text{ m/s}$ (7.8 kW), Loaded $2.4\text{ m/s}$ (11.7 kW)[cite: 513, 514, 515].
* **Travel Distance:** Generate a static distance matrix mimicking the quayside-to-storage layout.
* **The Oracle Solver:** Write a brute-force exact solver using `itertools.permutations` to evaluate all physically valid topological sequence permutations of this 10-task graph. Output the absolute optimal Pareto front coordinates for $C_{max}$ (Makespan) and $\mathcal{E}$ (Total Energy) to a JSON file.

---

## III. MODULE 2: THE DISCRETE BASELINE (`baseline_brkga.py`)
**Objective:** Implement a simplified, single-population Biased Random-Key Genetic Algorithm (BRKGA) as the exact comparative baseline.

**Implementation Rules:**
* [cite_start]**Chromosome Encoding:** The random-key vector must have a length of $4N$ (where $N=10$)[cite: 1087]. The array is strictly partitioned:
  1. [cite_start]*Genes 1 to $N$:* Task sequence[cite: 1089].
  2. [cite_start]*Genes $N+1$ to $2N$:* SA-AGV assignment[cite: 1089].
  3. [cite_start]*Genes $2N+1$ to $3N$:* Empty travel speed[cite: 1089].
  4. [cite_start]*Genes $3N+1$ to $4N$:* Loaded travel speed[cite: 1089].
* **Decoder Logic (Strict Mathematical Mapping):**
  * [cite_start]*Sequence:* Use the smallest position value rule[cite: 1161].
  * *SA-AGV Assignment:* Values in $[0, \frac{1}{|A|}]$ decode to SA-AGV 1, values in $(\frac{1}{|A|}, \frac{2}{|A|}]$ decode to SA-AGV 2[cite: 1164, 1165, 1166].
  * [cite_start]*Speed Assignment:* Values in $[0, \frac{1}{|V|}]$ decode to Speed 1 (Lower), up to $|V|$ (Higher)[cite: 1167, 1168, 1169].
* [cite_start]**Constraint Propagation:** The decoder must mathematically enforce QC precedence constraints: $c_j \ge c_{j-1} + \tau_j$ for tasks on the same crane[cite: 997]. Calculate the decoded $C_{max}$ and $\mathcal{E}$.

---

## IV. MODULE 3: THE SELF-EXPLAINING SURROGATE (`surrogate_gnn.py`)
[cite_start]**Objective:** Engineer a Max-Plus Graph Neural Network to extract structural attribution heuristics[cite: 1680].

**Implementation Rules:**
* **Architecture:** PyTorch Geometric Homogeneous `GATv2Conv`.
* **Node Features ($\mathbf{h}_i$):** `[Handling_Time, Is_Load, Is_Unload, QC_ID]`.
* **Edge Features ($\mathbf{e}_{ij}$):** `[Travel_Time, Empty_Energy, Loaded_Energy]`.
* **Max-Plus Algebra:** In the custom `MessagePassing` class, the `aggr` parameter MUST be set to `'max'`. The `forward` function must simulate the propagation of maximum temporal delays through the Directed Acyclic Graph.
* **Heuristic Extraction:** Implement a forward hook or direct return statement that detaches the attention coefficient matrix ($\alpha$) from the GPU computation graph.
* **Offline Training Loop:** Generate 1,000 synthetic permutations using `environment.py`. Train the GNN for 50 epochs using MSE loss to predict ground-truth $C_{max}$ and $\mathcal{E}$.

---

## V. MODULE 4: THE INTEGRATION (`attention_nsgaii.py`)
[cite_start]**Objective:** Replace stochastic evolution with Explainable AI-guided structural search[cite: 1682, 1686].

**Implementation Rules:**
* **Evolutionary Framework:** Implement standard NSGA-II non-dominated sorting and crowding distance[cite: 1071].
* **The Targeted Mutation Operator:**
  1. Translate the current schedule into a PyG `Data` object.
  2. [cite_start]Execute a forward pass through `surrogate_gnn.py` and read the extracted $\alpha$ matrix[cite: 1683, 1684].
  3. Identify the disjunctive routing edge $(i, j)$ possessing the maximum $\alpha$ coefficient (the predicted physical bottleneck).
  4. Perform targeted mutation exclusively on this edge (e.g., swap the assigned SA-AGV or adjust the speed level).
  5. Apply Kahn's Algorithm for topological sorting to instantaneously verify the mutated graph contains no cyclic deadlocks.

---

## VI. MODULE 5: EMPIRICAL BENCHMARKING (`benchmark.py`)
**Objective:** Generate the definitive visual proof of convergence velocity for the thesis committee.

**Execution:**
* Initialize the exact static 10-task environment.
* Run `baseline_brkga.py` ($P=50$) and `attention_nsgaii.py` ($P=50$) concurrently for exactly 50 generations.

**Output Generation:**
Output two high-resolution Matplotlib charts:
1. **Convergence Velocity:** Plot Hypervolume vs. Generations. The line for Attention-Guided NSGA-II must demonstrate exponential superiority over the BRKGA stochastic baseline.
2. **Pareto Trade-off:** A 2D scatter plot mapping Makespan ($C_{max}$) against Total Energy ($\mathcal{E}$). Overlay the BRKGA final population (Red markers), the Attention-Guided NSGA-II final population (Green markers), and the exact mathematical Oracle front (Solid Black Line) derived from Module 1.
