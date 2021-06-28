from linkernighan import *
import cProfile

if __name__=='__main__':
    instance=read_tsplib("./datasets/it16862.tsp")
    tour = random_tour(instance, False, 1535)
    tour.plot()
    tour=lin_kernighan(instance, tour, p=150, verbose=True, animation=True, s_time=0.5)
    tour.plot()
