import random
from math import sqrt
import matplotlib.pyplot as plt
from time import sleep

class City():
    def __init__(self, coord_x, coord_y, city_name=None):
        self.x = coord_x
        self.y = coord_y
        self.name = city_name

    def __repr__(self):
        if self.name == None:
            return(f"X{self.x} Y{self.y}")
        else:
            return(f"{self.name}: X{self.x} Y{self.y}")

    def distance(self, other_city):
        return sqrt((self.x-other_city.x)**2 + (self.y-other_city.y)**2)

def distance(c1, c2):
    return c1.distance(c2)

def generate_random_instance(num_city, max_x, max_y, seed=None):
    # manage seed
    if seed != None:
        random.seed(seed)
    else:
        random.seed()
    # loop to fill the set
    instance = set()
    for c in range(num_city):
        instance.add( City( random.randint(0, max_x), random.randint(0, max_y), f"C{c}" ) )
    return instance

class Tour():
    def __init__(self):
        self.list = []

    def __repr__(self):
        return(f"Tour:{self.list}")
    
    def __len__(self):
        return len(self.list)

    def append(self, new_city):
        if isinstance(new_city, City):
            self.list.append(new_city)
        else:
            print("ERROR")

    def pred(self, city, index=False):
        idx=self.list.index(city)
        city=self.list[idx-1]
        if index: return idx, city
        return city

    def succ(self, city, index=False):
        idx=self.list.index(city)+1
        city=self.list[0] if idx>=len(self.list) else self.list[idx]
        if index: return idx, city
        return city

    def between(self, a, b, c): # c in [a, ~,  b] in forward sense
        idx_a=self.index(a)
        idx_b=self.index(b)-idx_a
        idx_c=self.index(c)-idx_a
        if idx_b<0: idx_b+=len(self)
        if idx_c<0: idx_c+=len(self)
        return 0<=idx_c and idx_c<=idx_b


    def length(self):
        l = 0.0
        prev_city = self.list[0]
        for c in self.list[1:]:
            l += prev_city.distance(c)
            prev_city = c
        # add the last arc back to the starting city
        l += prev_city.distance(self.list[0])
        return l

    def is_valid(self, instance):
        if (len(self.list) == len(instance)) and (set(self.list) == instance):
            return True
        return False

    def plot(self, style='bo-'):
        tour_list = self.list.copy()
        tour_list.append(self.list[0])
        plt.plot( [c.x for c in tour_list], [c.y for c in tour_list], style)
        plt.axis('scaled')
        plt.axis('off')
        plt.show()

    def shift(self, index):
        if index>=len(self.list): raise Exception(f"ERROR: Out of range")
        self.list=self.list[index:]+self.list[:index]

    def position(self, position_number):
        """Return the city in the requested position"""
        if position_number < 0 or position_number >= len(self.list):
            raise Exception(f"ERROR: Accessing outside the tour ({position_number})")
        return self.list[position_number]

    def index(self, city):
        return self.list.index(city)

    def remove(self, position_number):
        """Remove a city from the tour based on the position"""
        del self.list[position_number]

    def compare(self, tour):
        return self.list==tour.list

    def copy(self):
        copy_tour=Tour()
        copy_tour.list=self.list.copy()
        return copy_tour


def compare_tours(tour1, tour2): return tour1.compare(tour2)


def random_tour(instance, verbose=False, seed=None):
    # manage seed
    if seed != None:
        random.seed(seed)
    else:
        random.seed()
  
    # BUG: list(instance) produces a different list every time
    list_instance = sorted(list(instance), key=lambda x: x.name)
    if verbose:
        print(f"Before the shuffle {list_instance}")
    random.shuffle(list_instance)
    if verbose:
        print(f"After the shuffle {list_instance}")
    t = Tour()
    for c in list_instance:
        t.append(c)
    return t

def nearest_city(instance, current_city):
  best_d = None
  best_city = None
  for c in sorted(list(instance), key=lambda x: x.name):
    d = current_city.distance(c)
    if best_d == None:
      best_d = d
      best_city = c
    elif d < best_d:
      best_d = d
      best_city = c
  return best_city

def nearest_neighbor_algorithm( original_instance, initial_city = None , initial_city_index=-1):
    tour = Tour()
    # we select an initial city and remove it from the instance
    instance = original_instance.copy()
    if initial_city == None:
        current_city = random.choice(list(instance))
    elif initial_city_index>=0 and initial_city_index<len(instance):
        current_city=sorted(list(instance), key=lambda x: x.name)[initial_city_index]
    else:
        current_city = initial_city
    
    instance.remove(current_city)
    tour.append(current_city)

    # main loop to empty the set
    while instance:
        current_city = nearest_city(instance, current_city)
        # move best city from the instance to the tour
        tour.append(current_city)
        instance.remove(current_city)
  
    # check if it is valid
    if tour.is_valid(original_instance):
        return tour
    else:
        print("ERROR NOT VALID TOUR IN NEAREST NEIGHBOR")
        return None
