# Local search for TSP with Lin-Kernighan neighborhood

Simple python implementation of a local-search-based heuristic for the symmetric travelling salesman problem (TSP) using the Lin-Kernighan neighborhood.

## Usage

```python
from linkernighan import *

instance = generate_random_instance(10)
tour = random_tour(instance)

# returns the locally optimal tour
tour = lin_kernighan(instance, tour)

# Repeat the heuristic for different initial tours and returns the best found solution
tour = lk_based_metaheuristic(instance, random_tour, cycles=100)
```

