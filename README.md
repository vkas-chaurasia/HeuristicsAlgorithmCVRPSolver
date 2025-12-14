# Santa Challenge - Heuristic Algorithms Course

This repository contains a solution for the Santa Challenge, developed as part of the **Heuristic Algorithms** course (3 ECTS credits). It demonstrates the application of constructive heuristics and spatial data structures to solve a large-scale Vehicle Routing Problem (VRP).

## Project Structure

The project is organized to separate the algorithmic core from utility functions:

- `src/santa_challenge/`: Main package.
    - `algorithms/`: Contains the heuristic implementation.
        - `greedy_kd_tree.py`: The core Greedy Nearest Neighbor solver using KD-Tree.
    - `utils/`: Helper modules for data handling and metrics.
        - `data_loader.py`: Loads the `gifts.csv` dataset.
        - `metrics.py`: Calculates Weighted Reindeer Weariness (WRW).
        - `config.py`: Problem constraints (North Pole coordinates, weight limits).
- `data/`: Directory for input data (place `gifts.csv` here or in parent directory).
- `results/`: Directory where the `submission.csv` is generated.
- `main.py`: The entry point script to run the experiment.

## Algorithm Description

The problem is modeled as a Capacitated Vehicle Routing Problem (CVRP) on a sphere. We implemented a **Constructive Greedy Heuristic** to generate a feasible solution efficiently.

### 1. Heuristic Strategy: Greedy Nearest Neighbor
The algorithm builds routes (trips) sequentially. For each step:
-   **State**: The sleigh is at a `current_location` (starts at North Pole, then updates to the location of the most recently delivered gift).
-   **Decision**: Select the *nearest* unvisited gift that fits in the sleigh (Weight Limit: 1000kg).
-   **Constraint**: If no gift fits or the sleigh is full, the trip ends. A new trip starts, continuing the search from the *last visited location*. (Note: While cost is calculated assuming a return to North Pole, the greedy search heuristically continues from the last point to cluster deliveries).

This is a "greedy" approach because it makes the locally optimal choice at every step without looking ahead. While it doesn't guarantee a global optimum, it produces a valid solution very quickly.

### 2. Optimization: KD-Tree (k-Dimensional Tree)
Searching for the "nearest neighbor" among 100,000 gifts linearly would be slow ($O(N)$ per step, total $O(N^2)$).
To optimize this, we use a **KD-Tree**:
-   **Preprocessing**: All gift coordinates are indexed in a KD-Tree ($O(N \log N)$).
-   **Querying**: We query the tree for the $k$ nearest neighbors to the current location ($O(\log N)$).
-   **Dynamic Search Radius**: If valid neighbors are not found in the initial $k$, the search radius is dynamically expanded.

## Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Solver**:
    ```bash
    python main.py
    ```

3.  **Output**:
    The solution file `submission.csv` will be saved in the `results/` folder. The total Weighted Reindeer Weariness score will be printed to the console.

## Visualization

An interactive map visualization of the computed routes is available in `map.html`.

[**Click here to open the Interactive Map**](map.html)

*(Note: The map requires JavaScript and cannot be embedded directly in this README on GitHub. If viewing on GitHub, you may need to download the file or view it via a specialized HTML preview service.)*
