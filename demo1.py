from linkernighan import *

if __name__=='__main__':
	countries={'djibouti': 'dj38', 'qatar': 'qa194', 'uruguay': 'uy734', 'italy': 'it16862'}
	selected_country='djibouti'
	instance=read_tsplib("./datasets/"+countries[selected_country]+".tsp")
	tour = random_tour(instance, False, 35)
	tour.plot()
	tour=lin_kernighan(instance, tour, p=15, verbose=True, animation=True, s_time=0.2)
	tour.plot()
