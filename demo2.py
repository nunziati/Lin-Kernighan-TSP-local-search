from linkernighan import *



if __name__=='__main__':
    instance=read_tsplib("./datasets/dj38.tsp")
    tour = random_tour(instance, False, 2154)
    tour.plot()
    tour=lk_based_metaheuristic(instance, nearest_neighbor_algorithm, cycles=50, loop_initial_city=False, p=15)
    cls()
    print("Multiple local search completed.")
    print(f"Cost of the best found tour: {tour.length()}")
    tour.plot()
