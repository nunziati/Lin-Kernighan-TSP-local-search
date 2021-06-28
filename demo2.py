from linkernighan import *

if __name__=='__main__':
	countries={'djibouti': 'dj38', 'qatar': 'qa194', 'uruguay': 'uy734', 'italy': 'it16862'}
	selected_country='djibouti'
	instance=read_tsplib("./datasets/"+countries[selected_country]+".tsp")
	tour = random_tour(instance, False, 2154)
	tour.plot()
	tour=lk_based_metaheuristic(instance, random_tour, cycles=100, loop_initial_city=False, p=5, seed=1244)
	cls()
	print("Multiple local search completed.")
	print(f"Cost of the best found tour: {tour.length()}")
	tour.plot()
